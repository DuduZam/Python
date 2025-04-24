# Tipo de datos
class CuentaBancaria:
    """Tipo de datos:
    1. Publico: ejemplo(self.nombre)
    Se puede acceder y modificar en la clase, subclase(Herencia) e instanciacion.
    2. Protegido: ejemplo(self._correo)
    Se puede acceder y modificar en la clase y subclase(Herencia), tambien en instanciacion pero no es buena practica, no se recomienda.
    3. Privado: ejemplo(self.__contraseña)
    Se puede acceder y modificar solo en la clase, mientras subclase y instanciacion python lo "oculta" mediante el
    name mangling(cambio de nombre interno) para evitar conflictos de nombres en subclases.
    """
    def __init__(self, titular, numero_cuenta, saldo_inicial):
        self.titular = titular                     # Público
        self.numero_cuenta = numero_cuenta         # Público
        self._tipo_cuenta = "Ahorros"             # Protegido: solo para subclases
        self.__saldo = saldo_inicial               # Privado: acceso restringido
        
    def mostrar_saldo(self):
        print(f"Saldo actual de {self.titular}: ${self.__saldo}")

    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto
            print(f"Depositados ${monto}. Nuevo saldo: ${self.__saldo}")
        else:
            print("El monto debe ser mayor que 0.")

    def retirar(self, monto):
        if monto > 0 and monto <= self.__saldo:
            self.__saldo -= monto
            print(f"Retirados ${monto}. Nuevo saldo: ${self.__saldo}")
        else:
            print("Saldo insuficiente o monto inválido.")
        
    def _calcular_interes(self):  # Método protegido
        return self.__saldo * 0.03

class CuentaEmpresarial(CuentaBancaria):
    def __init__(self, titular, numero_cuenta, saldo_inicial, empresa):
        super().__init__(titular, numero_cuenta, saldo_inicial)
        self.empresa = empresa
        self._tipo_cuenta = "Empresarial"  # Modificamos el atributo protegido

    def mostrar_detalles_empresa(self):
        print(f"Cuenta empresarial de {self.empresa}, tipo: {self._tipo_cuenta}")

    def aplicar_interes(self):  # Método accesible para subclase
        interes = self._calcular_interes()  # Usamos el método protegido
        print(f"Interés aplicado: ${interes}")
        self.depositar(interes)  # Sumamos el interés al saldo
        
# Crear una cuenta de ahorros
cuenta1 = CuentaBancaria("Juan", "123456", 1000)
cuenta1.mostrar_saldo()
cuenta1.depositar(500)
cuenta1.retirar(200)

# Crear una cuenta empresarial
cuenta2 = CuentaEmpresarial("Lucía", "789101", 5000, "TechCorp")
cuenta2.mostrar_detalles_empresa()
cuenta2.aplicar_interes()
cuenta2.mostrar_saldo()

# Intentar acceder directamente a atributos protegidos y privados (mala práctica)
print(cuenta2._tipo_cuenta)     # Atributo protegido: accesible pero no recomendado
# print(cuenta2.__saldo)        # Esto dará error: AttributeError
print(cuenta2._CuentaBancaria__saldo)  # Acceso indirecto al atributo privado (¡mala práctica!)

"""
[IMPORTANTE]
Se puede acceder a tipos de datos __Privados con los metodos con en el ejemplo.
Pero con Subclase (Herencia) no podemos tener acceso.
"""