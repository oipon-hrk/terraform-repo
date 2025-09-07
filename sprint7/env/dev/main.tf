terraform {
  backend "s3" {
    bucket = "tf-test-hoikaw-20250823"
    key = "test/terraform.tfstate"
    region = "ap-northeast-1"
    use_lockfile = true
  }
}

module "vpc" {
    source = "../../modules/vpc"
    myip = var.myip
    env = var.env
}

module "ec2" {
    source = "../../modules/ec2"
    myip = var.myip
    env = var.env
    web_subnet_id = var.web_subnet_id
    vpc_id = module.vpc.vpc_id
}

# import {
#   id = "i-0174b092a089a3a0b"
#   to = aws_instance.imported_ec2
# }