from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen  # Para múltiples pantallas
from kivy.lang import Builder  # Cargar archivos .kv con el diseño
import requests  # Para hacer peticiones al backend

Builder.load_file('familymedia.kv')  # Carga la interfaz gráfica

class LoginScreen(Screen):
    def login(self):
        # Envía credenciales al backend
        response = requests.post('http://localhost:5000/login', json={
            'email': self.ids.email.text,  # Accede al TextInput de email
            'password': self.ids.password.text  # TextInput de contraseña
        })
        if response.status_code == 200:  # Si el login es exitoso
            self.manager.current = 'main'  # Navega a la pantalla principal

class MainScreen(Screen):
    def upload_media(self):
        file_chooser = self.ids.file_chooser  # Obtiene el FileChooser de la UI
        file_chooser.bind(on_selection=self.handle_selection)  # Cuando selecciona un archivo

    def handle_selection(self, instance, selection):
        if selection:
            file = open(selection[0], 'rb')  # Abre el archivo en modo lectura binaria
            files = {'file': file}  # Prepara para enviar como multipart/form-data
            # Envía el archivo al backend con el token de autenticación
            response = requests.post(
                'http://localhost:5000/upload',
                files=files,
                headers={'Authorization': f'Bearer {TOKEN}'}  # TOKEN se obtiene del login
            )
            if response.ok:
                print("¡Archivo subido!")  # Confirmación (mejorable con notificaciones)

class FamilyMediaApp(App):
    def build(self):
        sm = ScreenManager()  # Maneja las pantallas
        sm.add_widget(LoginScreen(name='login'))  # Pantalla de login
        sm.add_widget(MainScreen(name='main'))  # Pantalla principal
        return sm

if __name__ == '__main__':
    FamilyMediaApp().run()  # Inicia la aplicación