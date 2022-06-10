import re

def email_slicer():
    valid_mail = False

    while not valid_mail:
        try:
            user_mail = input("Please enter your email: ")
            valid_mail = is_valid_mail(user_mail)
            if not valid_mail:
                raise Exception
        except Exception:
            print("Invalid email address, please enter a valid one!\n")

    username, domain = re.split('@', user_mail)
    print(f"Your username is {username} and your domain is {domain}")

def is_valid_mail(email):
    pattern = re.compile(r'([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(pattern, email) is None:
        return False
    return True

email_slicer()