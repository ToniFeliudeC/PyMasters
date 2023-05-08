### Función de tests.
totalTests = 1005
correct = 0
cases = []




### Tests definidos por el creador del kata gracias a la función assertEquals()
tests = '''import random

print('Example Test Cases')
assertEquals(suma(2,3), 5)
assertEquals(suma(2,10), 12)
assertEquals(suma(2,2), 4)
assertEquals(suma(2,90), 92)
assertEquals(suma(2,-3), -1)

print("Random Test Cases")
for i in range(1000):
    a = random.randint(-100, 100)
    b = random.randint(-100, 100)
    
    result = a + b
    
    assertEquals(suma(a,b), result)'''


solucion = '''def suma(a,b):
    return a + b'''

script = solucion + "\n\n" + tests

result = exec(script)

if correct == totalTests:
    print('Reto superado!')


import random

def paresAdmin(lista):
	result = []
	for numero in lista:
        if not numero % 2:
        	lista.append(numero)
    return result

assertEquals(pares([1,2,3,4,5,6]), paresAdmin([1,2,3,4,5,6]))
assertEquals(pares([1,2]), paresAdmin([1,2]))
assertEquals(pares([21,22,10,54]), paresAdmin([21,22,10,54]))
assertEquals(pares([123,321,222,111,200]), paresAdmin([123,321,222,111,200]))

for i in range(100):
	lista = []
	for i in range(5):
    	lista.append(random.int(-100,100))
    
    assertEquals(pares(lista), paresAdmin(lista))
	
assertEquals(suma(2,3), 5)
assertEquals(suma(2,3), 5)
assertEquals(suma(2,3), 5)
assertEquals(suma(2,3), 5)
assertEquals(suma(2,3), 5)

