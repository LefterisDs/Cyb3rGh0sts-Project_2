from hashlib import sha256

for i in range(1,7):
    for j in range(1,32):
        passphrase = "2020-0" + str(i) + "-"
        if j < 10:
            passphrase = passphrase + "0" + str(j)
        else:
            passphrase = passphrase + str(j)
        passphrase = passphrase + " raccoon"
        key = sha256(passphrase.encode('utf8').rstrip()).hexdigest()

        if "d1689c23e86421529297" in key:
            print(passphrase)
            print(key)

key = sha256(b"cybergh0sts").hexdigest()
# x = float.fromhex( "0." + str(key[:16])   )
# y = float.fromhex( "0." + str(key[16:32]) )

x = "0." + str(key[:16])
y = "0." + str(key[16:32])

mult  = 1/16
dec_x = 0.0
for i in range(2,18):
    dec_x = dec_x + int(x[i],16) * mult
    mult = mult / 16

print(key)
print(x)
print("%.30lf"%dec_x)
print(y)
print(mult)
# 47.47298416481722560089
#  0.47298416481722560523
# 4.7991375472458345437

(0*16**0) + (7*16**(-1)) + (9*16**(-2)) + (1*16**(-3)) + (5*16**(-4)) + (7*16**(-5)) + (13*16**(-6)) + (7*16**(-7)) + (15*16**(-8)) + (6*16**(-9)) + (10*16**(-10)) + (7*16**(-11)) + (5*16**(-12)) + (10*16**(-13)) + (7*16**(-14)) + (11*16**(-15)) + (0*16**(-16))