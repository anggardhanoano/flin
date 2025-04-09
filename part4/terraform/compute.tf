# Get latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# EC2 Instance Profile
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "flin-wordpress-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# EC2 Instance
resource "aws_instance" "wordpress" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.ec2.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 30
    delete_on_termination = true
  }

  user_data = templatefile("${path.module}/scripts/userdata.sh", {
    db_host     = aws_db_instance.wordpress.address
    db_name     = var.db_name
    db_user     = var.db_username
    db_password = var.db_password
    s3_bucket   = aws_s3_bucket.wordpress.bucket
    region      = var.aws_region
    domain_name = var.domain_name
  })

  depends_on = [
    aws_db_instance.wordpress,
    aws_s3_bucket.wordpress
  ]

  tags = {
    Name = "flin-wordpress-server"
  }
}

# Elastic IP for EC2
resource "aws_eip" "wordpress" {
  vpc      = true
  instance = aws_instance.wordpress.id

  tags = {
    Name = "flin-wordpress-eip"
  }

  depends_on = [aws_internet_gateway.igw]
}
