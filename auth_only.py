import json
import subprocess
import sys
import select
from os.path import exists
from datetime import datetime, timezone
import time
from secrets_ import MFA_DEVICE_SERIAL
import config as cfg


def run_subprocess(command):
    print(" ".join(command))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    decoded_err = bytes.decode(stderr)
    if decoded_err != "":
        print(f"error: {decoded_err}")
    return stdout, decoded_err


def update_mfa():
    if exists(cfg.EXPIRY_FILE):
        with open(cfg.EXPIRY_FILE, "r") as f:
            expiry_date = datetime.fromisoformat(f.readline().strip())
    else:
        expiry_date = None

    if expiry_date is not None and expiry_date >= datetime.now().replace(
        tzinfo=timezone.utc
    ):
        print("AWS credentials not expired, skipping in 3s...")
        print("type y to force update")
        i, o, e = select.select([sys.stdin], [], [], 3)
        if i:
            print("force updating credentials...")
            _ = sys.stdin.readline()
        else:
            print("skipping...")
            return

    print("AWS credentials expired, generating new credentials...")
    if len(sys.argv) >= 2:
        mfa_token = sys.argv[1]
    else:
        mfa_token = input("input mfa code: ")

    aws_set_command = ["aws", "configure", "set"]
    aws_sts_command = [
        "aws",
        "sts",
        "get-session-token",
        "--serial-number",
        MFA_DEVICE_SERIAL,
        "--token-code",
        str(mfa_token),
        "--profile",
        "auth",
    ]

    stdout, stderr = run_subprocess(aws_sts_command)

    if stderr == "":
        cred = json.loads(bytes.decode(stdout))

        print("Updating AWS credentials...")
        run_subprocess(
            [
                *aws_set_command,
                "aws_access_key_id",
                cred["Credentials"]["AccessKeyId"],
            ]
        )
        run_subprocess(
            [
                *aws_set_command,
                "aws_secret_access_key",
                cred["Credentials"]["SecretAccessKey"],
            ]
        )
        run_subprocess(
            [
                *aws_set_command,
                "aws_session_token",
                cred["Credentials"]["SessionToken"],
            ]
        )

        print("Updating expiration date...")
        with open(cfg.EXPIRY_FILE, "w") as f:
            f.write(cred["Credentials"]["Expiration"])

        print("Successfully updated AWS credentials")
    return


if __name__ == "__main__":
    update_mfa()
