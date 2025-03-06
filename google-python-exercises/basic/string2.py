#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licenciado bajo la Licencia Apache, Versión 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Clase de Python de Google
# http://code.google.com/edu/languages/google-python-class/

# Ejercicios adicionales básicos de cadenas de caracteres

# D. verbing
# Dada una cadena, si su longitud es de al menos 3 caracteres,
# agrega 'ing' al final.
# A menos que ya termine en 'ing', en cuyo caso,
# agrega 'ly' en su lugar.
# Si la longitud de la cadena es menor a 3, déjala sin cambios.
# Devuelve la cadena resultante.
def verbing(s):
  # +++tu código aquí+++
  if(len(s) > 2):
    if(s[-3:] == "ing"):
      s += "ly"
      return s
    else:
      s += "ing"
      return s
  else:
    return s  


# E. not_bad
# Dada una cadena, encuentra la primera aparición de
# las subcadenas 'not' y 'bad'. Si 'bad' sigue a 'not',
# reemplaza toda la subcadena desde 'not' hasta 'bad'
# con 'good'.
# Devuelve la cadena resultante.
# Por ejemplo, 'This dinner is not that bad!' produce:
# 'This dinner is good!'
def not_bad(s):
  # +++tu código aquí+++
  word_not = s.find('not')
  word_bad = s.find('bad')
  if word_not != -1 and word_bad != -1 and word_not < word_bad:    
    s = s[:word_not] + 'good' + s[word_bad+3:]
    return s        
  else:
    return s
  return


# F. front_back
# Considera dividir una cadena en dos mitades.
# Si la longitud es par, las mitades delantera y trasera tienen la misma longitud.
# Si la longitud es impar, diremos que el carácter extra va en la mitad delantera.
# Por ejemplo, 'abcde', la mitad delantera es 'abc' y la mitad trasera es 'de'.
# Dadas dos cadenas, a y b, devuelve una cadena con la forma
# a-delantero + b-delantero + a-trasero + b-trasero
def front_back(a, b):
  # +++tu código aquí+++
  mitad_a = len(a) // 2
  mitad_b = len(b) // 2
    
  if len(a)  % 2 == 0:
    a_delantero = a[:mitad_a]
    a_trasero = a[mitad_a:]
  else:
    a_delantero = a[:mitad_a+1]
    a_trasero = a[mitad_a+1:]
        
  if len(b)  % 2 == 0:
    b_delantero = b[:mitad_b]
    b_trasero = b[mitad_b:]
  else:
    b_delantero = b[:mitad_b+1]
    b_trasero = b[mitad_b+1:]
        
  return a_delantero + b_delantero + a_trasero + b_trasero


# Función simple proporcionada utilizada en main() para imprimir
# lo que cada función devuelve frente a lo que se supone que debe devolver.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# main() proporciona llamadas a las funciones anteriores con entradas interesantes,
# utilizando test() para verificar si cada resultado es correcto o no.
def main():
  print('verbing')
  test(verbing('hail'), 'hailing')
  test(verbing('swiming'), 'swimingly')
  test(verbing('do'), 'do')

  print()
  print('not_bad')
  test(not_bad('This movie is not so bad'), 'This movie is good')
  test(not_bad('This dinner is not that bad!'), 'This dinner is good!')
  test(not_bad('This tea is not hot'), 'This tea is not hot')
  test(not_bad("It's bad yet not"), "It's bad yet not")

  print()
  print('front_back')
  test(front_back('abcd', 'xy'), 'abxcdy')
  test(front_back('abcde', 'xyz'), 'abcxydez')
  test(front_back('Kitten', 'Donut'), 'KitDontenut')

if __name__ == '__main__':
  main()
