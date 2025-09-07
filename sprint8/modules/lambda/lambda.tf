provider "aws" {
  region = "ap-northeast-1"
}

locals{
    system_name = "sp8-test"
    name_prefix = "${local.system_name}"
}

# __generated__ by Terraform
resource "aws_lambda_function" "imported_lambda" {
  architectures                      = ["x86_64"]
  # code_signing_config_arn            = null
  # description                        = null
  filename                           = "${path.module}/build/upload_inquiry.zip"
  source_code_hash                   = filebase64sha256("${path.module}/build/upload_inquiry.zip")
  function_name                      = "UploadInquiry"
  handler                            = "lambda_function.lambda_handler"
  # image_uri                          = null
  # kms_key_arn                        = null
  memory_size                        = 128
  package_type                       = "Zip"
  publish                            = null
  region                             = "ap-northeast-1"
  replace_security_groups_on_destroy = null
  replacement_security_group_ids     = null
  reserved_concurrent_executions     = -1
  role                               = "arn:aws:iam::816069136572:role/taskControlRole"
  runtime                            = "python3.13"
  s3_bucket                          = null
  s3_key                             = null
  s3_object_version                  = null
  skip_destroy                       = false
  tags = {
    Name = "InquiryTable"
  }
  timeout                            = 3
  ephemeral_storage {
    size = 512
  }
  logging_config {
    application_log_level = null
    log_format            = "Text"
    log_group             = "/aws/lambda/UploadInquiry"
    system_log_level      = null
  }
  tracing_config {
    mode = "PassThrough"
  }
}