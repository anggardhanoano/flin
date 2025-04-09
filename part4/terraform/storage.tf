# S3 Bucket for WordPress Assets
resource "aws_s3_bucket" "wordpress" {
  bucket = var.s3_bucket_name

  tags = {
    Name = "flin-wordpress-assets"
  }
}

resource "aws_s3_bucket_acl" "wordpress" {
  bucket = aws_s3_bucket.wordpress.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "wordpress" {
  bucket = aws_s3_bucket.wordpress.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
