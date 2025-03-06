#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licenciado bajo la Licencia Apache, Versión 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Clase de Python de Google
# http://code.google.com/edu/languages/google-python-class/

# Ejercicios básicos de cadenas de caracteres
# Completa el código de las funciones a continuación. main() ya está configurado
# para llamar a las funciones con algunas entradas diferentes,
# imprimiendo 'OK' cuando cada función sea correcta.
# El código inicial para cada función incluye un 'return'
# que es solo un marcador de posición para tu código.
# No importa si no completas todas las funciones, y hay
# algunas funciones adicionales para probar en string2.py.


# A. donuts
# Dado un número entero count de donuts, devuelve una cadena
# de la forma 'Número de donuts: <count>', donde <count> es el número
# pasado. Sin embargo, si el recuento es 10 o más, usa la palabra 'muchos'
# en lugar del recuento real.
# Entonces, donuts(5) devuelve 'Número de donuts: 5'
# y donuts(23) devuelve 'Número de donuts: muchos'
def donuts(count):
  # +++tu código aquí+++  
  if count<10:
    return f"Número de donuts: {count}"
  else:
    return f"Número de donuts: many"
  


# B. both_ends
# Dada una cadena s, devuelve una cadena formada por los primeros 2
# y los últimos 2 caracteres de la cadena original,
# así 'spring' produce 'spng'. Sin embargo, si la longitud de la cadena
# es menos de 2, devuelve en su lugar la cadena vacía.
def both_ends(s):
  # +++tu código aquí+++
  if len(s) < 2:
    return ""
  else:
    return s[:2]+s[-2:]
  


# C. fix_start
# Dada una cadena s, devuelve una cadena
# donde todas las ocurrencias de su primer carácter se hayan
# cambiado por '*', excepto que no se debe cambiar
# el primer carácter en sí mismo.
# Por ejemplo, 'babble' produce 'ba**le'
# Supón que la longitud de la cadena es 1 o más.
# Sugerencia: s.replace(stra, strb) devuelve una versión de la cadena s
# donde todas las instancias de stra han sido reemplazadas por strb.
def fix_start(s):
  # +++tu código aquí+++  
  return s[0] + s[1:].replace(s[0], '*')


# D. MixUp
# Dadas las cadenas a y b, devuelve una única cadena con a y b separadas
# por un espacio '<a> <b>', excepto intercambia los primeros 2 caracteres de cada cadena.
# Por ejemplo:
#   'mix', 'pod' -> 'pox mid'
#   'dog', 'dinner' -> 'dig donner'
# Supón que a y b tienen una longitud de 2 o más.
def mix_up(a, b):
  # +++tu código aquí+++
  a,b = b[:2]+a[2:], a[:2]+b[2:]  
  return a+" "+b


# Función simple de prueba proporcionada utilizada en main() para imprimir
# lo que cada función devuelve frente a lo que se supone que debe devolver.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# main() proporcionado llama a las funciones anteriores con entradas interesantes,
# utilizando test() para verificar si cada resultado es correcto o no.
def main():
  print('donuts')
  # Cada línea llama a donuts, compara su resultado con el esperado para esa llamada.
  test(donuts(4), 'Número de donuts: 4')
  test(donuts(9), 'Número de donuts: 9')
  test(donuts(10), 'Número de donuts: many')
  test(donuts(99), 'Número de donuts: many')

  print()
  print('both_ends')
  test(both_ends('spring'), 'spng')
  test(both_ends('Hello'), 'Helo')
  test(both_ends('a'), '')
  test(both_ends('xyz'), 'xyyz')


  print()
  print('fix_start')
  test(fix_start('babble'), 'ba**le')
  test(fix_start('aardvark'), 'a*rdv*rk')
  test(fix_start('google'), 'goo*le')
  test(fix_start('donut'), 'donut')

  print()
  print('mix_up')
  test(mix_up('mix', 'pod'), 'pox mid')
  test(mix_up('dog', 'dinner'), 'dig donner')
  test(mix_up('gnash', 'sport'), 'spash gnort')
  test(mix_up('pezzy', 'firm'), 'fizzy perm')


# Código estándar para llamar a la función main().
if __name__ == '__main__':
  main()