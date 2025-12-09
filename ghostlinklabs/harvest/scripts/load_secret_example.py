"""
Demonstrates loading secrets from (1) environment variables, (2) Docker secrets mounted at /run/secrets/, or (3) AWS Secrets Manager (optional).

This is a small helper — adapt to your application's config loading.
"""
import os


def load_secret(name: str) -> str | None:
    # 1. Environment variable
    val = os.getenv(name)
    if val:
        return val

    # 2. Docker secret (mounted file)
    secret_path = f"/run/secrets/{name.lower()}"
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            return f.read().strip()

    # 3. (Optional) AWS Secrets Manager: left as placeholder for production
    # from botocore.exceptions import BotoCoreError, ClientError
    # import boto3
    # try:
    #     client = boto3.client('secretsmanager')
    #     resp = client.get_secret_value(SecretId=name)
    #     return resp.get('SecretString')
    # except (BotoCoreError, ClientError):
    #     return None

    return None


if __name__ == "__main__":
    for key in ("GHOSTLINK_API_KEY", "DB_URL", "REDIS_URL"):
        print(key, "=", load_secret(key))
