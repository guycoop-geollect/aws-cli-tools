# Auth AWS and assume roles

you will need a `secrets_.py` file containing your mfa device serial from AWS i.e.:
```
MFA_DEVICE_SERIAL = "arn:aws:iam::123456789012:mfa/YourName"
```

run `main` to reauth and optionally assume a role.

alternatively it is possible to run `auth_only` or `assume_role_only` separately.