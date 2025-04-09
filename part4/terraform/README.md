# Flin WordPress Infrastructure

This Terraform configuration sets up an AWS infrastructure for hosting WordPress based on described Plan on the [PDF](../Flin%20Wordpress%20Infrastructure.pdf):

1. EC2 for the main server with Docker
2. RDS MySQL for the database
3. S3 for static asset storage
4. CloudFront for CDN

# Setup Explanation

- This terraform configuration makes us possible to easily maintain all AWS service programmatically and consistent.
- i decide to separate terraform script into few specific function based on its functionality such as
  - compute.tf --> managing ec2
  - database.tf --> managing rds
  - storage.tf --> managing s3
- also can see on userdata.sh, i tried to automatically setup everything needed for the Wordpress in production settings, and
- because of i'm using terraform, i can easily apply the configuration everytime we have any update and it will consistently and automatically update the Wordpress instance, basically its one of many ways to setup CI/CD for the this projects

# Benefits

1. Since i'm using terraform, any deployment activity, especialy if we have any update on Wordpress can be tracked via Github and also consistent as long as we don't make any changes on AWS console
2. automatic deployment of the Wordpress on EC2 everytime i run `terraform apply`
3. easy to scale and maintain, we can easily do vertical scaling by change the instance type for EC2, or we also can do horizontal scaling by adding more EC2 instance with same configuration. but of course if we will do horizontal scaling, we need to do some extra works which is configure load balancer between all EC2 instances
4. reliable and secure database since we are using RDS, which popular for its reliability
5. fast delivery of static assets because of utilizing Cloudfront CDN, since Wordpress usually used as CMS which contain a lot of static asset (image, video), usage of S3 and Cloudfront will be crucial, because it's almost imposible (hard) to maintain all those static asset manually in one instance without makes the server down due to low memory
