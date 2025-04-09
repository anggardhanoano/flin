# CloudFront Origin Access Identity
resource "aws_cloudfront_origin_access_identity" "wordpress" {
  comment = "OAI for flin WordPress Media"
}

# S3 Bucket Policy for CloudFront
resource "aws_s3_bucket_policy" "wordpress" {
  bucket = aws_s3_bucket.wordpress.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:GetObject"]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.wordpress.arn}/*"
        Principal = {
          AWS = "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity ${aws_cloudfront_origin_access_identity.wordpress.id}"
        }
      }
    ]
  })
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "wordpress_media" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "flin WordPress Media"
  default_root_object = "index.html"
  price_class         = "PriceClass_100" # Use only North America and Europe edge locations

  origin {
    domain_name = aws_s3_bucket.wordpress.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.wordpress.bucket}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.wordpress.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.wordpress.bucket}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
  }

  # Cache behavior for images
  ordered_cache_behavior {
    path_pattern     = "*.jpg"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.wordpress.bucket}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400    # 1 day
    max_ttl                = 31536000 # 1 year
    compress               = true
  }

  # Cache behavior for other static assets
  ordered_cache_behavior {
    path_pattern     = "*.png"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.wordpress.bucket}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400    # 1 day
    max_ttl                = 31536000 # 1 year
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = var.domain_name == "" ? true : false
    acm_certificate_arn            = var.domain_name == "" ? null : aws_acm_certificate.wordpress[0].arn
    ssl_support_method             = var.domain_name == "" ? null : "sni-only"
    minimum_protocol_version       = var.domain_name == "" ? "TLSv1" : "TLSv1.2_2021"
  }

  tags = {
    Name = "flin-wordpress-cdn"
  }
}

# ACM Certificate (only if domain_name is provided)
resource "aws_acm_certificate" "wordpress" {
  count             = var.domain_name == "" ? 0 : 1
  domain_name       = var.domain_name
  validation_method = "DNS"

  tags = {
    Name = "flin-wordpress-cert"
  }

  lifecycle {
    create_before_destroy = true
  }
}
