import time
import requests

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)

def main():
    response = fetch('http://example.com')
    if 200 <= response.status_code < 300:
        print('Success!')
    else:
        print('Error!')

def fetch(url):
    max_retries = 3
    retries = 0
    while True:
        try:
            print('Retrieving {0}...'.format(url))
            response = requests.get(url)
            print('Status: {0}'.format(response.status_code))
            if response.status_code not in TEMPORARY_ERROR_CODES:
                return response
        except requests.exceptions.RequestException as ex:
            print('Exception occured: {0}'.format(ex))
            retries += 1
            if retries >= max_retries:
                raise Exception('Too many retries.')
            wait = 2**(retries - 1)
            print('Waiting {0} seconds...'.format(wait))
            time.sleep(wait)

if __name__ == '__main__':
    main()