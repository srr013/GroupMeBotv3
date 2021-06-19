import jwt

def verifyToken(token):
    with open('keys/public.pem') as key:
        publicKey = key.read()
    if publicKey:
        decoded = jwt.decode(token, publicKey, algorithms=['RS256'])
        print(decoded)