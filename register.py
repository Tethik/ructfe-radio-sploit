import requests
import uuid

username = "pizzaboi" # str(uuid.uuid4()).split("-")[0]
password = "da848dc1-7c06-47ea-9284-d80beb6dd024"

def register(service):
    resp = requests.post(f"{service}/frontend-api/register/", json={
        "username": username,
        "password": password,
        "repeated_password": password
    })    
    print(resp)
    print(resp.text)
    assert resp.status_code == 200

def create_token(service):
    s = requests.Session()
    resp = s.post(f"{service}/frontend-api/login/", json={
        "username": username,
        "password": password,
    })    
    print(resp)
    print(resp.text)
    assert resp.status_code == 200
    resp = s.get(f"{service}/api/v1/token/") 
    print(resp)
    print(resp.text)
    assert resp.status_code == 200
    return resp.json()['token']

with open("targets.txt") as fp:
    targets = fp.readlines()

successes = []
# targets = ["10.61.119.2"]
for target in targets:
    try:
        service = f"http://{target.strip()}:4553"
        register(service)        
        token = create_token(service)
        successes.append(service)
        with open("tokens.txt", "a") as myfile:
            myfile.write(",".join([service, token, username, password]) + "\n")
    except Exception as ex:
        print(ex)
        
print("#################")
print("#################")
print("#################")
print()
print()
print(f"{len(successes)} / {len(targets)} registered")
