def suma_numeros(num1, num2):
    resultado = num1 + num2
    return resultado

# Definir valores de num1 y num2
num1 = 5
num2 = 3
print(suma_numeros(num1, num2))

def saludo(nombre):
    print("Hola " + nombre)

saludo("Mundo")

edad = 25
print("Tu edad es: " + str(edad))  # Convertir edad a string para concatenar

def dividir(a, b):
    if b != 0:
        return a / b
    else:
        return "No se puede dividir entre cero"

print(dividir(10, 0))

lista = [1, 2, 3]
print("La longitud de la lista es: " + str(len(lista)))

if 5 > 3:  # Añadir ":"
    print("Cinco es mayor que tres")  # Remover "hay errores aqui?" de la línea
