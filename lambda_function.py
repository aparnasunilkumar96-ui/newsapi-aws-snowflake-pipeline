import json
import os
import urllib.request
import boto3
from datetime import datetime

s3 = boto3.client("s3")

def lambda_handler(event, context):

    # NewsAPI details
    api_key = os.environ["NEWS_API_KEY"]

    url = (
        "https://newsapi.org/v2/everything?"
        "q=technology&"
        "language=en&"
        "sortBy=publishedAt&"
        "pageSize=20&"
        f"apiKey={api_key}"
    )

    # Call NewsAPI
    with urllib.request.urlopen(url) as response:
        news_data = json.loads(response.read().decode("utf-8"))

    # S3 bucket
    bucket_name = "news-data-aparna-2026"

    # Create a unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_name = f"news/news_{timestamp}.json"

    # Save NewsAPI response to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(news_data),
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "News data successfully saved to S3",
            "file": file_name,
            "articles": len(news_data.get("articles", []))
        })
    }
