
def GF_sum(a, b):
	return a ^ b

def GF_product_p(a, b):
    res = 0
    contador = 0
    for val in reversed(bin(b)):
        if(val == 'b'):
            break
        if(val == '1'):
            res = GF_sum(res, a << contador)
        contador += 1
    #print("pre red " + hex(res))
    if (res > 255):
        res = reduccion(res)
    return res

def GF_product_t(a, b): #si a = g^i y b = g^j el producte de a i b es: g^(i+j)
	global dic_exp_log
	if not dic_exp_log: #check si ja he calculat les tables, sino les calculem
		dic_exp_log = GF_tables()
	i = dic_exp_log['log'][a]
	j = dic_exp_log['log'][b]
	return dic_exp_log['exp'][(i+j)%255]
	
def GF_invers(a): #a^-1 -> (g^i)^-1 = g^-i = g^255-i
	if a == 0x00:
		return 0
	global dic_exp_log
	if not dic_exp_log: #check si ja he calculat les tables, sino les calculem
		dic_exp_log = GF_tables()
	i = dic_exp_log['log'][a]
	return dic_exp_log['exp'][255-i]
	

def GF_tables(): #esto se deberia ejecutar solo una vez
	#load exp table
	res = {'exp': {}, 'log': {}}
	g = 0x02
	last = 0x01
	for i in range(0,256): #g^i on i [1,254]
		res['exp'][i] = last
		last = GF_product_p(last,g)
	res['log'] = {v: k for k, v in res['exp'].items()} #invertim el diccionari
	return res

def GF_es_generador(a): # a es generador si mcd(log(a),255) == 1
	global dic_exp_log
	if not dic_exp_log: #check si ja he calculat les tables, sino les calculem
		dic_exp_log = GF_tables()
	return a in dic_exp_log['log'] and mcd_euclides(dic_exp_log['log'][a],255) == 1 #suposem que a inclos a gf(256)
	

def reduccion(a): #https://en.wikipedia.org/wiki/Finite_field_arithmetic -> Multiplication
    rij_pol = 0x11d
    aux = a
    contador = 0
    while(int(aux) > 255):
        #print("it " + str(contador))
        #print(bin(aux))
        aux_rij_pol = rij_pol << (int(aux).bit_length()-int(rij_pol.bit_length()))
        aux = GF_sum(aux, aux_rij_pol)
        #print("post")
        #print(bin(aux))
        contador += 1
    #print("fin")
    return aux


def mcd_euclides(a,b):
    while b != 0:
        a, b = b, a % b
    return a == 1

#tabla exponencial en la posicion i pones g^i y en la logaritmica haces la tabla inversa, en g^i pones i
def main():
	#print("res -> " + str(GF_product_p(0x57,0x83)))
	print("generador 0x04 " + str(GF_es_generador(0x04)))
	print("sense tables: " + hex(GF_product_p(0x57,0x83)))
	print("amb tables:" + hex(GF_product_t(0x57,0x83)))
	print("invers 0x02 " + hex(GF_invers(0x02)))

dic_exp_log = GF_tables()
print(dic_exp_log)
main()

