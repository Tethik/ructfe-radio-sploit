import requests
import jwt


def list_users():    
    url = "http://10.61.119.2:4553/frontend-api/our-users/"
    resp = requests.get(url)
    print(resp)

list_users()

secret = "2a1b317063259394a61c326277d2a01c82c5b38a4e4ae692074a7e2de5b178d9"
token = "eyJhbGciOiI0MiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiNjJiMSJ9.NlXuqr3Jn1/1jMQmBcx98GFiVqVeP2efWiDWrGmgrSSshNEso/DSeF8vubptVHDF/iEr/1CiT+KmKM9Ufg36crN+54Ib+W4pPe8SBTkHCjAQ9pw3oke7S8E0TTSRuJhEUlUZ3zDYmknSU3kFswz6fzpu5UMk6xwoCvWnR/O6qsU="


def create_jwt(user, secret):
    encoded_jwt = jwt.encode({'user': user}, 'secret', algorithm='HS256')

res = jwt.decode(token, secret, algorithms=['HS256'])
print(res)