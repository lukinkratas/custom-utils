from io import BytesIO

import boto3
import pandas as pd
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')


def s3_put_object(bytes: bytes, bucket: str, key: str):
    try:
        response = s3_client.put_object(Body=bytes, Bucket=bucket, Key=key)

    except ClientError as e:
        print(e)
        return False

    return response


def s3_put_df(df: pd.DataFrame, bucket: str, key: str, **kwargs):
    bytes = BytesIO()
    df.to_csv(bytes, **kwargs)
    bytes.seek(0)
    return s3_put_object(bytes.getvalue(), bucket=bucket, key=key)


def s3_list_objects(bucket: str, key_prefix: str):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=key_prefix)

    except ClientError as e:
        print(e)
        return False

    return [content.get('Key') for content in response.get('Contents')]


def s3_get_object(bucket: str, key: str) -> dict:
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)

    except ClientError as e:
        print(e)
        return False

    return response


def s3_read_df(bucket: str, key: str, **kwargs) -> pd.DataFrame:
    response = s3_get_object(bucket, key)
    bytes = BytesIO(response['Body'].read())
    bytes.seek(0)
    return pd.read_csv(bytes, **kwargs)
