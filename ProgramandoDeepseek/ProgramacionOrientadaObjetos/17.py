from typing import Callable, Any, TypedDict

# Decorador para verificar autenticación
def requiere_autenticacion(funcion_parametro: Callable[..., str]) -> Callable[..., str]:
    """
    Decorador que verifica si un usuario está autenticado antes de ejecutar la función.
    """
    def nueva_funcion(usuario: dict[str, Any], *args: Any, **kwargs: Any) -> str:
        if not usuario.get("autenticado", False):  # Verifica si el usuario tiene autenticado=True
            print(f"Usuario {usuario['nombre']} no está autenticado.")
            raise PermissionError("Error: No tienes acceso a esta función.")
        return funcion_parametro(usuario, *args, **kwargs)
    return nueva_funcion

# Función protegida por autenticación
@requiere_autenticacion
def ver_datos_confidenciales(usuario: dict[str, Any]) -> str:
    """
    Función accesible solo para usuarios autenticados.
    """
    return f"Datos confidenciales accesibles para {usuario['nombre']}."

@requiere_autenticacion
def ver_perfil(usuario: dict[str, Any]) -> str:
    """
    Función para ver el perfil del usuario autenticado.
    """
    return f"Perfil de {usuario['nombre']}: Información confidencial."  

# Definición de tipo para usuarios
class Usuario(TypedDict):
    nombre: str
    autenticado: bool

# Simulación de usuarios
usuario_autenticado: Usuario = {"nombre": "Jose", "autenticado": True}
usuario_no_autenticado: Usuario = {"nombre": "Maria", "autenticado": False}

# Ejemplo de uso
try:
    print(ver_datos_confidenciales(usuario_autenticado))  # Salida válida: Datos confidenciales accesibles para Jose
except PermissionError as e:
    print(f"Error: {e}")

try:
    print(ver_datos_confidenciales(usuario_no_autenticado))  # Salida inválida: Error de autenticación
except PermissionError as e:
    print(f"Error: {e}")
