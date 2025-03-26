import base64
import os
import time

import boto3
from openai import OpenAI


def handler(event, context):
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")  # API keyのセット
    response = client.images.generate(
        model="dall-e-3",  # モデル
        prompt="very very cute cats",  # プロンプト
        n=1,  # 生成数
        size="1024x1024",  # 解像度 dall-e-3では1024x1024、1792x1024、1024x1792
        response_format="b64_json",  # レスポンスフォーマット url or b64_json
        quality="hd",  # 品質 standard or hd
        style="vivid",  # スタイル vivid or natural
    )

    # S3クライアントの作成
    s3_client = boto3.client("s3")
    bucket_name = "image-generator-of-874wokiite-bucket"

    # 画像保存
    for d in response.data:
        file_name = f"{int(time.time())}.png"
        with open(f"/tmp/{file_name}", "wb") as f:
            f.write(base64.b64decode(d.b64_json))

    # S3にアップロード
    s3_client.upload_file(f"/tmp/{file_name}", bucket_name, file_name)

    # 署名付きURLを取得
    presigned_url = s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket_name, "Key": file_name}, ExpiresIn=3600
    )

    # 署名付きURLを返す
    return {"statusCode": 200, "body": {"presigned_url": presigned_url}}


if __name__ == "__main__":
    handler(None, None)
