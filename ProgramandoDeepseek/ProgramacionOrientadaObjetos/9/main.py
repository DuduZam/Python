from youtube.auth import autenticar_usuario, cerrar_sesion_usuario
from youtube.api import obtener_estadisticas_youtube

# from youtube import autenticar_usuario, obtener_estadisticas_youtube # Con __init__

def main():
    creds = None  # Inicializamos la variable `creds` como None
    
    while True:
        print("Bienvenido:")
        print("1. Iniciar Sesion o Verificar Sesion Activa")
        print("2. Cerrar Sesion")
        print("3. Obtener Info de Youtube")
        print("4. Cerrar")
          
        op = int(input())
        # Salir del programa si el usuario elige la opción 4
        if op == 4:
            print("¡Gracias por usar el programa! ¡Hasta luego!")
            break  # Sale del bucle while
        if op == 1:
            print("Autenticando al usuario...")
            creds = autenticar_usuario()  # Autenticar y obtener credenciales        
        elif op == 2:
            print("Cerrando Sesion...")
            cerrar_sesion_usuario()
            creds = None  # Credenciales vacias
        elif op == 3:
            print("Obteniendo estadísticas del canal de YouTube...")
            if creds is None:
                print("No hay sesion activa, inicie sesion primero.")
            else:
                obtener_estadisticas_youtube(creds)  # Usar la API para obtener datos
        else:
            print("Opción no válida. Vuelve a intentarlo.")

if __name__ == "__main__":
    main()  # Solo ejecuta esto si es el archivo principal
