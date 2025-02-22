print("EJERCICIO 12\n")
# Calcular el descuento en una compra. Si la compra es mayor a 100 $us, aplicar un descuento del 
# 10%. Si la compra en menor a 100 $us, aplicar un descuento del 5%. Mostrar el total a pagar 
# aplicando el descuento correspondiente. 

num1 = int(input("Ingrese el valor de la compra: "))

if num1 > 100:
	descuento = num1-(num1*0.1)
	print(f"Valor de la compra: {num1}\nPrecio a pagar: {descuento}\n10% de decuento.")
else:
	descuento = num1-(num1*0.05)
	print(f"Valor de la compra: {num1}\nPrecio a pagar: {descuento}\n5% de decuento.")