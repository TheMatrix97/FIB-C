
# 9756 equivale a 'a'
print("hello")
f = open("test.Cifrado","r")
output = ""
for line in f:
    for c in line:
        distancia_a = ord(c) - 9756
        res = c
        if abs(distancia_a) < 28:
            res = chr(ord('a') + distancia_a)
        output += res
print(output)
f.close()


