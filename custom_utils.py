from functools import wraps
import os
import pwd
from datetime import datetime
from time import perf_counter
import boto3
from botocore.exceptions import ClientError
from io import BytesIO

def get_username():
    return pwd.getpwuid(os.getuid())[0]

def track_args(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        print(f"{datetime.now()} {get_username()} called {func.__name__} with {args=} and {kwargs=}.")

        result = func(*args, **kwargs)

        print(f"{func.__name__} finished successfully.")

        return result
    
    return wrapper

def track_time_performance(n=1):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            print(f"{func.__name__} running {n}time(s) started.")
            start_time = perf_counter()

            for _ in range(n):
                result = func(*args, **kwargs)

            elapsed_time = perf_counter() - start_time
            print(f"{func.__name__} finished, took: {elapsed_time:0.8f} seconds.")

            return result
        
        return wrapper
    
    return decorator

def s3_put_object(file_bytes, bucket:str, key:str):

    s3_client = boto3.client('s3')

    try:
        response = s3_client.put_object(
            Body=file_bytes,
            Bucket=bucket,
            Key=key
        )

    except ClientError as e:
        print(e)
        return False
    
    return response

def s3_put_df(df, bucket:str, key:str, **kwargs):

    # s3_filesystem = S3FileSystem()

    # with s3_filesystem.open(f's3://{bucket}/{key}', 'w') as s3_file:
    #     df.to_csv(s3_file, index=False)

    buffer = BytesIO()
    df.to_parquet(buffer, **kwargs)
    buffer.seek(0)
    return s3_put_object(buffer.getvalue(), bucket, key)