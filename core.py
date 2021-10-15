"""
Vigenere Cipher Implementation
Author: Robert Guy
Date: 10/14/2021
"""

import sys
import string
args = sys.argv
keyword = args[1].split("=")[1].replace(" ", "")
msg = ' '.join([x for x in args[2:] if x != "\n"]).split("=")[1].replace(" ", "")

"""
SetupKeywordList(kw, m) returns a normalized length string equal to the length of
parameter m where m is the parsed command-line message. The content of m is derived
from kw where kw is the keyword command-line argument. For example, suppose m is
"diverttroopstoeastridge" and kw is "WHITE". We want to create a string that repeats
kw until it is the same length as m. This method would return a string s of length 23
where s = "WHITEWHITEWHITEWHITEWHI".
"""
def setupKeywordList(kw, m):
    j = len(kw)
    k = len(m)
    p = max(j, k) // min(j, k)
    kwl = ""
    for y in range(0, p):
        kwl += kw
    n = len(kwl)
    rem = k - n
    leftover = ""
    for z in range(0, rem):
        leftover += kw[z]
    return kwl + leftover

"""
ShiftListBy(a, b, c, d) returns a concentated string relative to the ordinal values of slice(s)
[a:b] and [c:d].
"""
def shiftListBy(a, b, c, d):
    if a == 'Z' and b == 'Z':
        return "Z" + string.ascii_uppercase[0:25]
    elif a == 'A' and b == 'Z':
        return string.ascii_uppercase[0:26]
    else:
        aPrime = getOrdinal(a)
        bPrime = getOrdinal(b)
        cPrime = getOrdinal(c)
        dPrime = getOrdinal(d)
        return string.ascii_uppercase[aPrime:bPrime + 1] + string.ascii_uppercase[cPrime:dPrime + 1]

"""
GetKeyLetterAbove(i, kps) returns the character located at index i of the string kps.
"""
def getKeyLetterAbove(i, kps):
    return kps[i]

"""
GetCipherRow(cs, tgt) returns the polyalphabetic cipher string within the 2D array cs that has a head
value of tgt. For example, "ABCDEFGHIJKLMNOPQRSTUVWXYZ" has a head value of "A". If tgt is equal
to "A", then this method would return "ABCDEFGHIJKLMNOPQRSTUVWXYZ".
"""
def getCipherRow(cs, tgt):
    for i in range(len(cs)):
        if(cs[i][0] == tgt):
            return cs[i]
    return None

"""
GetOrdinal(ch) returns the ordinal integer value of argument ch by computing an offset; this offset
is a difference of 65 from the upper-cased version of argument ch.
"""
def getOrdinal(ch):
    return ord(ch.upper()) - 65

"""
ConstructCiphers() constructs 26-polyalphabetic ciphers as shifted strings appended to a 2D array; per @see README.md
. It will return the 2D array (or list, per Python terminology).
"""
def constructCiphers():
    alpha = [x for x in string.ascii_uppercase[1:26]] + ['A']
    res = []
    for i in range(len(alpha)):
        x = alpha[i]
        temp = shiftListBy(x, 'Z', 'A', chr(ord(x) - 1))
        res.append(temp)
    return res

"""
Encode(res, m, ciphers) takes the normalized key phrase (res), the white-space cleaned message (m), and 
the 26-distinct ciphers (ciphers) as input. It returns a list of length 2, where the head is a list of 
length 2 tuples (x, y) where x denotes the character at index i within m and y denotes index i of the
normalized key-phrase. The second element of the list is the encoded message.
"""
def encode(res, m, ciphers):
    x = []
    y = []
    z = ""
    for i in range(len(res)):
        x.append(tuple([m[i], getKeyLetterAbove(i, res)]))
    for j in range(len(x)):
        row = getCipherRow(ciphers, x[j][1])
        y.append(row)
    for k in range(len(y)):
        temp = getOrdinal(x[k][0])
        z += y[k][temp]
    return [x, z]

"""
Decode(n, x) takes the length of the normalized key-phrase (n) and a list of length 2 tuples @see localized x from within
encode(...) method.
"""
def decode(n, x):
    res = ""
    for i in range(n):
        res += x[i][0]
    return res

print("Key Phrase: " + keyword)
print("Message: " + msg)
print("Encoding Message...")
res = setupKeywordList(keyword, msg)
ciphers = constructCiphers()
encoded_data = encode(res, msg, ciphers)
print("Encoded Message As: " + encoded_data[1])
print("Decoding Message...")
decoded_msg = decode(len(res), encoded_data[0])
print("Decoded Message As: " + decoded_msg)