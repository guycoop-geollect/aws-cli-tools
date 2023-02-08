# Auth AWS and assume roles

## Setup
- create a `secrets_.py` file containing your mfa device serial from AWS i.e.:
```
MFA_DEVICE_SERIAL = "arn:aws:iam::123456789012:mfa/YourName"
```

- modify the paths in the `config.py` file.
- your main user profile should be created in `~/.aws/credentials` and should be named `auth`.

## Usage
run `main` to authenticate and optionally assume a role. (just follow the instructions)

---
alternatively it is possible to run `auth_only.py` or `assume_role_only.py` separately.