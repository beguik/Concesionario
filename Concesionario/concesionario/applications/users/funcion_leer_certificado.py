import base64,re
from operator import le
def certificado_en_base64(cert):
    message_bytes = base64.b64decode(cert)
    message = message_bytes.decode('ascii',errors="ignore")
    return message


def recordar(lista):
    recordar=[]
    for i in range(len(lista)):
        if "-" in lista[i]:
            recordar.append(i)
    return recordar
def validoDNI(dni): 
	"""
	Comprueba que el dni es correcto
	"""
	tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
	dig_ext = "XYZ"
	reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
	numeros = "1234567890"
	dni = dni.upper()
	if len(dni) == 9:
		dig_control = dni[8]
		dni = dni[:8]
		if dni[0] in dig_ext:
			dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
		return len(dni) == len([n for n in dni if n in numeros]) \
			and tabla[int(dni)%23] == dig_control
	return False

def resultado(certificado=""):
	certificado_lista=certificado.split()
	lista_apoyo=[]
	lista_resultado=[]
	numero_del_nombre=int()
	for i in recordar(certificado_lista):
		if validoDNI(certificado_lista[i+1][:9]):
			for a in range(1,7):
				lista_apoyo.append(certificado_lista[i-a])
			print(lista_apoyo)
			try:
				if lista_apoyo[3]==lista_apoyo[5][lista_apoyo[5].index(lista_apoyo[3][0]):]:
					lista_apoyo[3]=lista_apoyo[3]
					numero_del_nombre=4
					for e in range(numero_del_nombre):
						lista_resultado.append(lista_apoyo[e])
					lista_resultado.append(certificado_lista[i+1][:9])
					return lista_resultado
			except:
				if lista_apoyo[3][1:]== lista_apoyo[5][lista_apoyo[5].index(lista_apoyo[3][1]):]:
					lista_apoyo[3]=lista_apoyo[3][1:]
					numero_del_nombre=4
					for e in range(numero_del_nombre):
						lista_resultado.append(lista_apoyo[e])
					lista_resultado.append(certificado_lista[i+1][:9])
					return lista_resultado
			finally:
				
				if numero_del_nombre!=4:
					try:
						print(lista_apoyo[4][lista_apoyo[4].index(lista_apoyo[2][1]):])
						if lista_apoyo[2][1:]== lista_apoyo[4][lista_apoyo[4].index(lista_apoyo[2][1]):]:
							lista_apoyo[2]=lista_apoyo[2][1:]
							numero_del_nombre=3
							for e in range(numero_del_nombre):
								lista_resultado.append(lista_apoyo[e])
							lista_resultado.append(certificado_lista[i+1][:9])
							return lista_resultado
					except:
						if lista_apoyo[2]==lista_apoyo[4][lista_apoyo[4].index(lista_apoyo[2][0]):]:
							lista_apoyo[2]=lista_apoyo[2]
							numero_del_nombre=3
							for e in range(numero_del_nombre):
								lista_resultado.append(lista_apoyo[e])
							lista_resultado.append(certificado_lista[i+1][:9])
						return lista_resultado
			
			
			
			
			
def bien_ordenado_diccionario(lista):
    dic={}
    print(lista)
    if len(lista)==5:
        dic["Nombre"]=lista[1]+" "+lista[0]
        dic["Apellido"]=lista[3]+" "+lista[2]
        
    else:
        dic["Nombre"]=lista[0]
        dic["Apellido"]=lista[2]+" "+lista[1]
    dic["DNI"]=lista[-1]
    return dic
        
        



