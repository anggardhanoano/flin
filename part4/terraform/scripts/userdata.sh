#!/bin/bash
set -e

yum update -y

yum install -y amazon-linux-extras docker
amazon-linux-extras enable docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

curl -L "https://github.com/docker/compose/releases/download/v2.17.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

yum install -y unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

mkdir -p /home/ec2-user/wordpress

cat > /home/ec2-user/wordpress/docker-compose.yml << 'EOF'
version: '3'

services:
  wordpress:
    image: wordpress:latest
    container_name: wordpress
    restart: always
    ports:
      - 80:80
    environment:
      WORDPRESS_DB_HOST: ${db_host}
      WORDPRESS_DB_NAME: ${db_name}
      WORDPRESS_DB_USER: ${db_user}
      WORDPRESS_DB_PASSWORD: ${db_password}
      WORDPRESS_CONFIG_EXTRA: |
        define('WP_MEMORY_LIMIT', '256M');
        define('AS3CF_SETTINGS', serialize(array(
          'provider' => 'aws',
          'access-key-id' => '',
          'secret-access-key' => '',
          'use-server-roles' => true,
          'bucket' => '${s3_bucket}',
          'region' => '${region}',
          'copy-to-s3' => true,
          'serve-from-s3' => true,
          'domain' => 'cloudfront',
          'cloudfront' => '${domain_name}'
        )));
    volumes:
      - wordpress_data:/var/www/html

  webserver:
    image: nginx:latest
    container_name: nginx
    restart: always
    ports:
      - 443:443
    depends_on:
      - wordpress
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/ssl:/etc/nginx/ssl
      - wordpress_data:/var/www/html:ro
    
volumes:
  wordpress_data:
EOF

# Nginx configuration
mkdir -p /home/ec2-user/wordpress/nginx/conf.d

cat > /home/ec2-user/wordpress/nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://wordpress:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF


# Set proper permissions
chown -R ec2-user:ec2-user /home/ec2-user/wordpress

# Start Docker Compose
cd /home/ec2-user/wordpress
docker-compose up -d

# Install plugin for S3 integration
sleep 60
docker exec wordpress curl -O https://downloads.wordpress.org/plugin/amazon-s3-and-cloudfront.zip
docker exec wordpress unzip amazon-s3-and-cloudfront.zip -d /var/www/html/wp-content/plugins/
docker exec wordpress chown -R www-data:www-data /var/www/html/wp-content/plugins/

echo "WordPress setup complete!"
