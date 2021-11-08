"""
this file contains the function handler to randomize
"""
import random, time

def suma():
    print("sumando")
    a = random.randint(0, 1000)
    b = random.randint(0, 1000)
    print(f" operadores a : {a} b: {b} ")
    return a + b


def division():
    print("division")
    a = random.randint(0, 1000)
    b = random.randint(1, 1000)
    print(f" operadores a : {a} b: {b} ")
    time.sleep(1)
    return a / b


def multiplicacion():
    print("multiplicaciones")
    a = random.randint(0, 1000)
    b = random.randint(0, 1000)
    print(f" operadores a : {a} b: {b} ")
    return a * b

def mockTimedFunction():
    time.sleep(1)
    return random.randint(0, 100000)

functions = [
    {
        "funcion": mockTimedFunction,
        "tiempo_ejecucion": 1
    },
    {
        "funcion": mockTimedFunction,
        "tiempo_ejecucion": 3
    },
    {
        "funcion": mockTimedFunction,
        "tiempo_ejecucion": 2
    },
    {
        "funcion": mockTimedFunction,
        "tiempo_ejecucion": 6
    },
    {
        "funcion": mockTimedFunction,
        "tiempo_ejecucion": 10
    },
    {
        "funcion": mockTimedFunction,
        "tiempo_ejecucion": 4
    },
]



def getRandomFunction():
    return functions[random.randint(0, len(functions)-1)]