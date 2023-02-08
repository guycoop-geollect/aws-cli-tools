import boto3
import select
import config as cfg
import sys
import time


def _assume_role(role_arn, role_name):
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn, RoleSessionName=role_name
    )
    credentials = assumed_role_object["Credentials"]
    return credentials


def write_credentials_to_file(credentials, file_name):
    # open the file and modify the [default] profile in the file with the new credentials
    with open(file_name, "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if line.startswith("[default]"):
                f.write(line)
                f.write(f"aws_access_key_id = {credentials['AccessKeyId']}" + "\n")
                f.write(
                    f"aws_secret_access_key = {credentials['SecretAccessKey']}" + "\n"
                )
                f.write(f"aws_session_token = {credentials['SessionToken']}" + "\n")
                break
            else:
                f.write(line)

        else:
            print("did not find default profile")
            f.write(f"[default]")
            f.write(f"aws_access_key_id = {credentials['AccessKeyId']}")
            f.write(f"aws_secret_access_key = {credentials['SecretAccessKey']}")
            f.write(f"aws_session_token = {credentials['SessionToken']}")


def assume_role():
    print(f"Enter the role name {list(cfg.ROLES.keys())}: ")
    print("skipping in 10 s...")
    i, o, e = select.select([sys.stdin], [], [], 10)
    if i:
        assumed_role_name = sys.stdin.readline().strip()
        role_arn = cfg.ROLES[assumed_role_name]
        credentials = _assume_role(role_arn, assumed_role_name)
        write_credentials_to_file(credentials, cfg.CREDENTIALS_FILE)
        print(
            f"Assumed role {assumed_role_name} and wrote credentials to {cfg.CREDENTIALS_FILE}"
        )
    else:
        print("skipped")
    time.sleep(3)
    return
