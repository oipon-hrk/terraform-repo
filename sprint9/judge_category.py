import json
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

# ---- 必要に応じてハードコード / 環境変数に置き換え ----
TABLE_NAME = "InquiryTable"
KB_ID = "your-kb-id"  # 例: "A1B2C3D4E5"（英数字のみ・最大10文字）
INFERENCE_PROFILE_ARN = "arn:aws:bedrock:ap-northeast-1:123456789012:inference-profile/your-profile"

# 保存するカテゴリは固定リスト
CATEGORIES_LIST = {"質問", "改善要望", "ポジティブな感想", "ネガティブな感想", "その他"}

def lambda_handler(event, context):
    # 1) 入力チェック
    if "id" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps("id does not exist")
        }
    item_id = event["id"]

    # 2) クライアント
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(TABLE_NAME)
    br_agent = boto3.client("bedrock-agent-runtime")

    # 3) reviewText を取得
    try:
        res = table.get_item(Key={"id": item_id})
        item = res.get("Item")
    except ClientError as e:
        print(f"[ERROR] DynamoDB get_item error: {e}")
        return {"statusCode": 500, "body": json.dumps(f"DynamoDB get_item error: {str(e)}")}

    if not item or "reviewText" not in item:
        print(f"[WARN] reviewText not found for id={item_id}")
        return {"statusCode": 404, "body": json.dumps(f"reviewText not found for id: {item_id}")}

    review_text = item["reviewText"]

    # 4) Bedrock（ナレッジベース）に分類依頼
    prompt = (
        "次のテキストを、以下のカテゴリから最も当てはまる1つだけで回答してください。\n"
        "候補: 質問 / 改善要望 / ポジティブな感想 / ネガティブな感想 / その他\n"
        "出力は候補の文字列のみ（余計な説明なし）。\n\n"
        f"テキスト: {review_text}"
    )

    try:
        resp = br_agent.retrieve_and_generate(
            input={"text": prompt},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KB_ID,
                    "modelArn": INFERENCE_PROFILE_ARN
                }
            }
        )
        raw = resp["output"]["text"].strip()
    except ClientError as e:
        print(f"[ERROR] Bedrock RetrieveAndGenerate error: {e}")
        return {"statusCode": 502, "body": json.dumps(f"Bedrock error: {str(e)}")}

    # 5) 最小の正規化（許可外は「その他」に丸める）
    category = raw.splitlines()[0].strip("：: 　")
    if category not in CATEGORIES_LIST:
        category = "その他"

    # CloudWatch Logs に分類結果を出す（見やすいように要点のみ）
    print(f"[CLASSIFY] id={item_id} category={category}")
    # 必要なら元テキストも確認（長文の場合は控えめ推奨）
    # print(f"[TEXT] {review_text}")

    # 6) DynamoDB に保存
    timestamp = datetime.now(timezone.utc).isoformat()
    update_expression = "SET Category = :c, updatedAt = :t"
    expression_attribute_values = {
        ":c": category,
        ":t": timestamp
    }

    try:
        table.update_item(
            Key={"id": item_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        print(f"[UPDATE] id={item_id} saved Category={category} at {timestamp}")
    except Exception as e:
        print(f"[ERROR] DynamoDB update_item error: {e}")
        return {"statusCode": 500, "body": json.dumps(f"Error updating item in DynamoDB: {str(e)}")}

    # 7) レスポンス（テスト実行の結果欄に表示される）
    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": item_id,
            "reviewText": review_text,
            "Category": category,
            "updatedAt": timestamp
        }, ensure_ascii=False)
    }