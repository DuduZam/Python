# Funcion calcular_base
def calcular_base(activaciones):
    base = 1000
    if activaciones > 699:
        base += 500        
        if activaciones > 1049:
            base += 500            
            if activaciones > 1099:
                base += 500
    return base

# Funcion calcular_bono
def calcular_bono(activaciones):
    bono = 2
    remuneracion = 0
    if activaciones > -1 :
        if activaciones < 1101:
            remuneracion = activaciones * bono
        elif activaciones < 1401:            
            bono = 2.25  # Ajustamos el bono para este rango
            activaciones_restantes = activaciones - 1100
            remuneracion += (activaciones_restantes * bono) + (1100 * 2)
        elif activaciones > 1401:
            bono = 2.50  # Ajustamos el bono para este rango
            activaciones_restantes = activaciones - 1400
            remuneracion += (activaciones_restantes * bono) + (1100 * 2) + (300 * 2.25)
    return remuneracion

def calcular_sueldo(base , bono):
    sueldo = base + bono    
    return sueldo

print("CONTROLAR MI SUELDO YAPE.")
activaciones = int(input("Numero de activaciones: "))  

if activaciones < 0:
    print("¿Hermano que haces con tu vida?\nPonte a Chambear") 
else:
    Pago_Base = calcular_base(activaciones)
    Pago_Bono = calcular_bono(activaciones)
    Total = calcular_sueldo(Pago_Base , Pago_Bono)
    print(F"Activaciones: {activaciones}\nBase: {Pago_Base} Bs.\nRemuneracion por activacion: {Pago_Bono} Bs.\nSueldo: {Total} Bs.")
    
