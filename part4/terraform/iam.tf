resource "aws_iam_role" "ec2_role" {
  name = "flin-wordpress-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "flin-wordpress-ec2-role"
  }
}

resource "aws_iam_policy" "s3_access" {
  name        = "flin-wordpress-s3-access"
  description = "Policy that allows EC2 to access S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Effect = "Allow"
        Resource = [
          aws_s3_bucket.wordpress.arn,
          "${aws_s3_bucket.wordpress.arn}/*"
        ]
      }
    ]
  })
}

# Attach S3 Access Policy to EC2 Role
resource "aws_iam_role_policy_attachment" "s3_access" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.s3_access.arn
}
