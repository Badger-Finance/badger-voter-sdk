import json

import boto3
from moto import mock_secretsmanager
from moto import mock_sts

from badger_voter_sdk.aws import get_secret
from badger_voter_sdk.constants import REGION


@mock_secretsmanager
def test_get_secret_happy():
    secret_value = "private_key"
    conn = boto3.client("secretsmanager", region_name=REGION)
    conn.create_secret(
        Name="SecretId", SecretString=json.dumps({
            "SecretKey": secret_value
        })
    )
    assert get_secret(
        secret_id="SecretId",
        secret_key="SecretKey",
    ) == secret_value


@mock_secretsmanager
@mock_sts
def test_get_secret_assume_role_happy():
    secret_value = "private_key"
    conn = boto3.client("secretsmanager", region_name=REGION)
    conn.create_secret(
        Name="SecretId", SecretString=json.dumps({
            "SecretKey": secret_value
        })
    )
    get_secret(
        secret_id="SecretId",
        secret_key="SecretKey",
        assume_role_arn="Some_random_arm_with_len_of_twenty",
    )
    assert get_secret(
        secret_id="SecretId",
        secret_key="SecretKey",
    ) == secret_value


@mock_secretsmanager
def test_get_secret_binary_happy():
    secret_value = "private_key"
    conn = boto3.client("secretsmanager", region_name=REGION)
    conn.create_secret(
        Name="SecretId", SecretBinary=json.dumps({
            "SecretKey": secret_value
        }).encode()
    )
    assert get_secret(
        secret_id="SecretId",
        secret_key="SecretKey",
    ) == secret_value


@mock_secretsmanager
def test_get_secret_unhappy():
    assert get_secret(
        secret_id="SecretId",
        secret_key="SecretKey",
    ) is None
