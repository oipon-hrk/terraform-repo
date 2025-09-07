provider "aws" {
  region = "ap-northeast-1"
}

locals{
    system_name = "tf-test"
    name_prefix = "${local.system_name}"
}

resource "aws_security_group" "web_sg" {
  vpc_id = var.vpc_id

  name        = "${local.name_prefix}-sg"
  description = "Allow HTTP access from my IP"

  ingress {
    description = "Allow HTTP traffic from my IP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["${var.myip}/32"] # var.myipからのHTTPアクセスを許可
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.name_prefix}-sg"
  }
}

# EC2
resource "aws_instance" "imported_ec2" {
  ami                                  = "ami-0bb2c57f7cfafb1cb"
  availability_zone                    = "ap-northeast-1a"
  iam_instance_profile                 = "s3-bucket-policy"
  instance_type                        = "t2.micro"
  key_name                             = "oikawa"
  subnet_id                            = var.web_subnet_id
  tags = {
    Name = "${local.name_prefix}-web-server-${var.env}-01"
  }

}