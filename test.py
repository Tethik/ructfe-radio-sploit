import requests

def list_playlists(target, token):
    # print(token)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = f"{target}/api/v1/playlist/"
    resp = requests.get(url, headers=headers)    
    return resp.json()


target = "http://127.0.0.1:4553"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE0NDQ0Nzg0MDAsInVzZXIiOiJ0ZXN0In0.BqbppwKlJWJWnjEp-ITVU_pNbZXTILezrmPycMghiOs"

print(list_playlists(target, token))