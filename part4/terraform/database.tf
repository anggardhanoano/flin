# DB Subnet Group
resource "aws_db_subnet_group" "wordpress" {
  name       = "flin-wordpress-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "flin-wordpress-db-subnet-group"
  }
}

# RDS MySQL Instance
resource "aws_db_instance" "wordpress" {
  allocated_storage       = 20
  storage_type            = "gp2"
  engine                  = "mysql"
  engine_version          = "8.0"
  instance_class          = var.db_instance_class
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  parameter_group_name    = "default.mysql8.0"
  db_subnet_group_name    = aws_db_subnet_group.wordpress.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  skip_final_snapshot     = true
  multi_az                = true
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"
  storage_encrypted       = true
  max_allocated_storage   = 100 # Enables storage autoscaling up to 100GB

  tags = {
    Name = "flin-wordpress-db"
  }
}
