module "vpc" {
  source = "../../modules/vpc"
  env    = var.env
}

module "dynamodb" {
  source = "../../modules/dynamodb"
  env    = var.env
}

module "lambda" {
  source = "../../modules/lambda"
  env    = var.env
}

# 既存リソースをインポート
# 1. importブロックを記載する
# 2. terraform plan --generate-config-out=generated.tf　を実行（この時はルートモジュールで事項するのでmoduleパスを書かないこと）
#    generated.tfが生成される（リソースの設定が出力される）
# 3. generated.tfを修正した後、必要項目のみをmain.tfに書き写す（generated.tfは削除）
# 4. terraform init
# 5. terraform pran > applyを実行する
# 6. importが完了したら、importブロックは削除してoK

import {
  id = "UploadInquiry"                     # リソース名を入力
  to = module.lambda.aws_lambda_function.imported_lambda #  <モジュールパス>.<awsリソースタイプ>.<リソース名>
}