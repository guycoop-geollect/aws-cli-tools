from auth_only import update_mfa
from assume_role_only import assume_role


def main():
    update_mfa()
    assume_role()


if __name__ == "__main__":
    main()
