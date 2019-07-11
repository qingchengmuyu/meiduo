import base64
import json
import hmac, hashlib

header = {
    'typ': 'JWT',
    'alg': 'HS256'
}
header = json.dumps(header)
header = base64.b64encode(header.encode())
print('header:', header)
paylode = {
    'id': 1,
    'name': 'yang',
    'admin': True
}
paylode = json.dumps(paylode)
paylode = base64.b64encode(paylode.encode())
print('paylode:', paylode)
SECRET_KEY = b'-u2%v)w!s!e%tu=*n1kf80y6uj+49wzkp@y1k!z9o#@ohu%i4y'
msg = header + b'.' + paylode
signature = hmac.new(SECRET_KEY, msg=msg, digestmod=hashlib.sha256).hexdigest()
print('signature: ', signature)
JWT_token = header.decode() + '.' + paylode.decode() + '.' + signature
print('JWT_token:', JWT_token)

jwt_token_b = JWT_token
header_b = jwt_token_b.split('.')[0]
paylode_b = jwt_token_b.split('.')[1]
signature_b = jwt_token_b.split('.')[2]
print(header_b)
print(paylode_b)
print(signature_b)
new_signature = hmac.new(SECRET_KEY, msg=(header_b + '.' + paylode_b).encode(), digestmod=hashlib.sha256).hexdigest()
if new_signature == signature_b:
    print("数据完整")
    user_info = json.loads(base64.b64decode(paylode_b.encode()).decode())
    print(user_info)

else:
    print("数据被篡改了")
