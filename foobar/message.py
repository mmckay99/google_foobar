import base64
encrypted = b"Fk4YEA4ADhIKFRIKE0oOGQAMF0xNWRVRX18BDAoCGAZMQUMSFVVAGQwOCAgHTE1ZFVdWVQIbHxZK Q1FBXltcU0EIDQIHAQZMTVkVU1NbBAwdAAAGBRVeEggQFBgHBwoOCA4FXh4SF0EMCwkMGRBMQUMS FUNSCwxMSU1EDQ4WFRIKE0oeAgtMRBY="
username = b"mikemckay2203"

# FRIKE appears twice... what does this mean
bde = base64.b64decode(encrypted)
print(bde)
username_repeated = int.from_bytes(username * 30, byteorder='little')

message_int = int.from_bytes(bde, byteorder='little')

xored = message_int ^ username_repeated

n = xored
print(n.to_bytes((n.bit_length() + 7) // 8, 'little').decode())
