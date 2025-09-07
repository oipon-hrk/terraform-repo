provider "aws" {
  region = "ap-northeast-1"
}

locals{
    system_name = "sp8-test"
    name_prefix = "${local.system_name}"
}

# dynamodb
resource "aws_dynamodb_table" "imported_dynamodb" {
  billing_mode                = "PAY_PER_REQUEST"
  deletion_protection_enabled = false
  hash_key                    = "id"
  name                        = "InquiryTable"
  read_capacity               = 0
  region                      = "ap-northeast-1"
  stream_enabled              = false
  table_class                 = "STANDARD"
  write_capacity              = 0
  attribute {
    name = "id"
    type = "S"
  }
  # point_in_time_recovery {
  #   enabled                 = false
  #   recovery_period_in_days = 0
  # }
  ttl {
    attribute_name = null
    enabled        = false
  }
    tags = {
    Name = "InquiryTable"
  }
}