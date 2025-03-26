import base64
import os
import time

from openai import OpenAI


def handler(event, context):
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")  # API keyのセット
    response = client.images.generate(
        model="dall-e-3",  # モデル
        prompt="28-year-old Japanese pretty woman with black bobbed hair",  # プロンプト
        n=1,  # 生成数
        size="1024x1024",  # 解像度 dall-e-3では1024x1024、1792x1024、1024x1792
        response_format="b64_json",  # レスポンスフォーマット url or b64_json
        quality="hd",  # 品質 standard or hd
        style="vivid",  # スタイル vivid or natural
    )

    # 画像保存
    # ファイル名にはタイムスタンプと通番を含めています
    for i, d in enumerate(response.data):
        with open(f"./dall-e-3_{int(time.time())}_{i}.png", "wb") as f:
            f.write(base64.b64decode(d.b64_json))

    return {"statusCode": 200, "body": "やっほー！Lambdaからの返事やで〜！"}


if __name__ == "__main__":
    handler(None, None)
