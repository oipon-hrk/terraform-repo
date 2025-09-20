import json
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # 1. 入力パラメータのチェック
    if "id" not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('id does not exist')
        }
    
    # 2. 入力パラメータの取得
    item_id = event["id"] 
    
    # 3. タイムスタンプの取得
    timestamp = datetime.now(timezone.utc).isoformat()  # 例：2024-07-17T23:11:11.541085
    
    # 4. AWSクライアントの初期化
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('InquiryTable')
    br_agent = boto3.client("bedrock-agent-runtime")

    # 2) DynamoDB から reviewText を取得
    try:
        res = table.get_item(Key={"id": item_id})
        item = res.get("Item")
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps({"message": "DynamoDB get_item error", "error": str(e)})}

    if not item or "reviewText" not in item:
        return {"statusCode": 404, "body": json.dumps({"message": "reviewText not found for given id", "id": item_id})}

    review_text = item["reviewText"]

    # 3) Bedrock ナレッジベースに問い合わせ
    try:
        resp = br_agent.retrieve_and_generate(
            input={"text": review_text},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": "kb-xxxxxxxxxxxx",
                    "modelArn": "arn:aws:bedrock:ap-northeast-1:123456789012:inference-profile/my-profile"
                }
            }
        )
        answer = resp["output"]["text"]
    except ClientError as e:
        return {"statusCode": 502, "body": json.dumps({"message": f"Bedrock error: {e}"})}
    
    # 4) 更新する内容を定義
    update_expression = "SET reviewAnswer = :a, updatedAt = :t"
    expression_attribute_values = {
        ":a": answer,
        ":t": timestamp
    }

    # 5) DynamoDB に保存
    try:
        table.update_item(
            Key={"id": item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error updating item in DynamoDB: {str(e)}")
        }
    
    # 6) 正常レスポンス
    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": item_id,
            "question": review_text,
            "answer": answer,
            "updatedAt": timestamp
        }, ensure_ascii=False)
    }