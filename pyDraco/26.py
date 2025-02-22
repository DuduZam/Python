print("EJERCICIO 26\n")
# Determinar el monto de dinero a retirar y mostrar en cuántos de cada billete de 200, 100, 50, 20, 
# 10 se necesita para retirar el monto solicitado.

# Ejemplo: 
# monto = 380 Bs 
# Mostrar:  
# 1 billete(s) de 200 Bs 
# 1 billete(s) de 100 Bs 
# 1 billete(s) de 50 Bs 
# 1 billete(s) de 20 Bs  
# 1 billete(s) de 10 Bs

monto_real = int(input("Ingrese el monto [multiplos de 10]: "))
monto = monto_real

while monto != 0:
	b200 = int(monto / 200)
	monto -= (b200 * 200)
	b100 = int(monto / 100)
	monto -= (b100 * 100)
	b50 = int(monto / 50)
	monto -= (b50 * 50)
	b20 = int(monto / 20)
	monto -= (b20 * 20)
	b10 = int(monto / 10)
	monto -= (b10 * 10)

print(f"Monto = {monto_real}Bs.\n{b200} billete(s) de 200Bs.\n{b100} billete(s) de 100Bs.\n{b50} billete(s) de 50Bs.\n{b20} billete(s) de 20Bs.\n{b10} billete(s) de 10Bs.")