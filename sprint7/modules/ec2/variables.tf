variable "env" {
    type = string
}

variable "myip" {
    type = string
}

variable "vpc_id" {
  description = "VPCID"
  type = string
}

variable "web_subnet_id" {
  description = "Webサーバを配置するサブネットID"
  type        = string
}