import time
import hmac
import hashlib
import codecs
# import pyotp
import base64
import struct
import argparse

# origin = base64.b32encode(b'0x74686f6d6173')
# print(origin)
# k = b'CI2FM6EQCI2FM6EQCI2FM6EQCI2FM6EQCI2FM6EQ'


def TOTP(k: bytes):
    t = int(time.time() / 30)
    myhmac = hmac.new(key=base64.b32decode(k), msg=struct.pack('>Q', t), digestmod=hashlib.sha1)
    return myhmac.digest()


def Truncate(hmac_result: bytes):
    offset = hmac_result[-1] & 0x0F
    truncated_hash = hmac_result[offset:offset+4]
    otp = struct.unpack('>I', truncated_hash)[0] & 0x7FFFFFFF
    otp %= 1000000
    return '{:06d}'.format(otp)


def g_args(file):
    f = open(file, "r")
    val = f.read()
    if len(val) == 64:
        # try:
        fbytes = int(val, 16)
        fbytes = codecs.decode(str(fbytes), 'hex_codec')
        fbytes = base64.b32encode(fbytes)
        r = open("ft_opt.key", "w")
        r.write(str(fbytes))
        # except Exception:
        #     print("Not an Hex value")
        #     exit(1)
    else:
        print("Key doesn't match the required lenght of 64")
        exit(1)


def main():
    parser = argparse.ArgumentParser(prog="ft_opt", description="Create and use TOTP")
    parser.add_argument('-k')
    parser.add_argument('-g')
    args = parser.parse_args()
    if args.k:
        print("On utilise K, argument : " + args.k)
    elif args.g:
        g_args(args.g)
    else:
        print("Aucun arguement. Affichage de la valeur par defaut")
        print(Truncate(TOTP(origin)))


main()

# pyotp test
# toto = pyotp.TOTP(k)
# print(toto.now())
