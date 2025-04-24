from abc import ABC, abstractmethod    # Este es la importacion para una clase abstracta
import random

# Clase abstracta para definir la interfaz de procesadores de pago
class PaymentProcessor(ABC):
    @abstractmethod
    def authenticate_user(self):
        """Autentica al usuario (este método debe ser implementado)."""
        pass

    @abstractmethod
    def process_payment(self, amount):
        """Procesa el pago (este método debe ser implementado)."""
        pass

# Clase concreta: Procesador para Tarjetas de Crédito
class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number, cvv, expiration_date):
        self.card_number = card_number
        self.cvv = cvv
        self.expiration_date = expiration_date
        self.is_authenticated = False

    def authenticate_user(self):
        # Simula la verificación de los datos de la tarjeta
        print(f"Verificando tarjeta {self.card_number}...")
        if len(self.card_number) == 16 and self.cvv.isdigit() and len(self.cvv) == 3:
            self.is_authenticated = True
            print("Autenticación exitosa.")
            return True
        else:
            print("Error: Tarjeta inválida.")
            return False

    def process_payment(self, amount):
        # Verifica la autenticación y simula el cobro
        if not self.is_authenticated:
            print("Autenticación necesaria antes de procesar el pago.")
            return False
        
        if amount > 0:
            print(f"Procesando pago de ${amount:.2f} con la tarjeta {self.card_number[-4:]}...")
            print("Pago aprobado.")
            return True
        else:
            print("Error: Monto inválido.")
            return False

# Clase concreta: Procesador para PayPal
class PayPalProcessor(PaymentProcessor):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.is_authenticated = False

    def authenticate_user(self):
        # Simula la autenticación del usuario
        print(f"Iniciando sesión en PayPal con el correo: {self.email}...")
        if "@" in self.email and len(self.password) >= 6:
            self.is_authenticated = True
            print("Cuenta autenticada correctamente.")
            return True
        else:
            print("Error: Credenciales de PayPal inválidas.")
            return False

    def process_payment(self, amount):
        # Verifica la autenticación y simula el cobro
        if not self.is_authenticated:
            print("Autenticación requerida antes de procesar el pago.")
            return False

        if amount > 0:
            print(f"Procesando pago de ${amount:.2f} a través de PayPal...")
            print("Pago exitoso.")
            return True
        else:
            print("Error: Monto inválido.")
            return False

# Clase concreta: Procesador para Criptomonedas
class CryptoProcessor(PaymentProcessor):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
        self.is_authenticated = False

    def authenticate_user(self):
        # Simula la autenticación de la billetera
        print(f"Verificando billetera: {self.wallet_address}...")
        if len(self.wallet_address) == 42 and self.wallet_address.startswith("0x"):
            self.is_authenticated = True
            print("Billetera validada correctamente.")
            return True
        else:
            print("Error: Dirección de billetera inválida.")
            return False

    def process_payment(self, amount):
        # Verifica la autenticación y simula el pago
        if not self.is_authenticated:
            print("Autenticación requerida antes de procesar el pago.")
            return False

        if amount > 0:
            print(f"Procesando pago de {amount} BTC desde {self.wallet_address}...")
            print("Pago confirmado en blockchain.")
            return True
        else:
            print("Error: Monto inválido.")
            return False

# Clase para gestionar pagos
class PaymentManager:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def make_payment(self, amount):
        print("Iniciando proceso de pago...")
        if self.processor.authenticate_user():
            if self.processor.process_payment(amount):
                print("Pago realizado con éxito.")
            else:
                print("Error al realizar el pago.")
        else:
            print("Autenticación fallida. El pago no se procesó.")

# Simulación de pagos
credit_card = CreditCardProcessor("1234567890123456", "123", "12/25")
paypal = PayPalProcessor("usuario@ejemplo.com", "contraseña_segura")
crypto = CryptoProcessor("0x123abc456def789ghi012jkl345mno678pqr9stu")

print("\nPago con tarjeta:")
manager = PaymentManager(credit_card)
manager.make_payment(150.50)

print("\nPago con PayPal:")
manager = PaymentManager(paypal)
manager.make_payment(299.99)

print("\nPago con criptomonedas:")
manager = PaymentManager(crypto)
manager.make_payment(0.0123)
