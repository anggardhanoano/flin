variable "aws_region" {
  type    = string
  default = "ap-southeast-3"
}


variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "availability_zones" {
  type    = list(string)
  default = ["ap-southeast-3a", "ap-southeast-3b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

# EC2 Variables
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.small"
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
  default     = null
}

variable "ssh_allowed_ips" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

# RDS Variables
variable "db_name" {
  type    = string
  default = "flin_wordpress_db"
}

variable "db_username" {
  description = "Username for the database"
  type        = string
  default     = "flin"
  sensitive   = true
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  type    = string
  default = "db.t3.small"
}

# S3 Variables
variable "s3_bucket_name" {
  type    = string
  default = "flin-wordpress-assets"
}

# Domain Variables
variable "domain_name" {
  type    = string
  default = ""
}

variable "enable_https" {
  description = "Whether to enable HTTPS"
  type        = bool
  default     = true
}
