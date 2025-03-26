import json
import os
from base64 import b64decode
from uuid import uuid4

import boto3
from openai import OpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


def handler(event, context):
    request = json.loads(event["body"])

    # OpenAIのDALL・E 3を使用して画像を生成する
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.images.generate(
        model="dall-e-3",
        prompt=request["text"],
        n=1,
        size="1024x1024",
        response_format="b64_json",
        quality="standard",
        style="vivid",
    )

    # 画像をLambdaのエフェメラルストレージに保存
    file_name = f"{str(uuid4())}.png"
    with open(f"/tmp/{file_name}", "wb") as file:
        file.write(b64decode(str(response.data[0].b64_json)))

    s3_client = boto3.client("s3", region_name="ap-northeast-1")
    bucket_name = "image-generator-of-874wokiite-bucket"

    # S3に生成した画像をアップロード
    s3_client.upload_file(
        Filename=f"/tmp/{file_name}",
        Bucket=bucket_name,
        Key=file_name,
    )

    # アップロードした画像の署名付きURLを取得
    presigned_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket_name,
            "Key": file_name,
        },
        ExpiresIn=3600,
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
        },
        "body": json.dumps(
            {
                "presigned_url": presigned_url,
            }
        ),
    }
