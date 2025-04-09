output "wordpress_public_ip" {
  description = "Public IP of the WordPress EC2 instance"
  value       = aws_eip.wordpress.public_ip
}

output "rds_endpoint" {
  description = "Endpoint of the RDS instance"
  value       = aws_db_instance.wordpress.endpoint
}

output "s3_bucket" {
  description = "Name of the S3 bucket for WordPress media"
  value       = aws_s3_bucket.wordpress.bucket
}

output "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.wordpress_media.domain_name
}

output "cloudfront_distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = aws_cloudfront_distribution.wordpress_media.id
}
