output "vpc_id" {
  value = aws_vpc.tf-test_vpc.id
}

# web Subnet
output "web_subnet_id" {
  description = "Public Subnet IDs"
  value = aws_subnet.web_subnet-01.id
}

output "api_subnet01_id" {
  description = "Private subnets"
  value = [
    aws_subnet.api_subnet01_id,
    aws_subnet.api_subnet02_id,
  ]
}

output "alb_subnet01_id" {
  description = "ALB subnets in multiple AZs"
  value = [
    aws_subnet.alb_subnet-01.id,
    aws_subnet.alb_subnet-02.id,
  ]
}