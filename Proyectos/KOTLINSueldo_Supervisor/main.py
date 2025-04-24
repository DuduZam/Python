from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

def calcular_base(activaciones):
    # (Tu función calcular_base aquí)
    base = 1000
    if activaciones > 699:
        base += 500
        if activaciones > 1049:
            base += 500
            if activaciones > 1099:
                base += 500
    return base

def calcular_bono(activaciones):
    # (Tu función calcular_bono aquí)
    bono = 2
    remuneracion = 0
    if activaciones > -1:
        if activaciones < 1101:
            remuneracion = activaciones * bono
        elif activaciones < 1401:
            bono = 2.25
            activaciones_restantes = activaciones - 1100
            remuneracion += (activaciones_restantes * bono) + (1100 * 2)
        elif activaciones > 1401:
            bono = 2.50
            activaciones_restantes = activaciones - 1400
            remuneracion += (activaciones_restantes * bono) + (1100 * 2) + (300 * 2.25)
    return remuneracion

def calcular_sueldo(base, bono):
    sueldo = base + bono
    return sueldo

class CalculadoraSueldoYapeApp(App):
    def build(self):
        pass

    def calcular(self):
        try:
            activaciones = int(self.root.ids.activaciones_input.text)
            if activaciones < 0:
                self.root.ids.resultado_label.text = "¿Hermano que haces con tu vida?\nPonte a Chambear"
            else:
                base = calcular_base(activaciones)
                bono = calcular_bono(activaciones)
                total = calcular_sueldo(base, bono)
                self.root.ids.resultado_label.text = f"Activaciones: {activaciones}\nBase: {base} Bs.\nRemuneracion por activacion: {bono} Bs.\nSueldo: {total} Bs."
                self.root.ids.activaciones_input.text = ''
        except ValueError:
            self.root.ids.resultado_label.text = "Por favor, ingresa un número válido."

if __name__ == '__main__':
    CalculadoraSueldoYapeApp().run()