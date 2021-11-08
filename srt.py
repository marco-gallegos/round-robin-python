"""
pip install pendulum keyboard tabulate

mostrar procesos nuevos
procesos en listos
procesos en ejecucion
"""
import random
import pendulum, time, keyboard
from tabulate import tabulate

class CustomProcess(object):
    def __init__(self):
        pass

class Supervisor(object):
    """Class to manage the process execution"""
    def __init__(self, numero_procesos:int, funciones_lote:list = []):
        self.numero_procesos = numero_procesos
        self.function_catalog = funciones_lote
        self.new_proces = []
        self.ready_process = []


    def build_process_queue(self):
        """
        :return:
        """
        for process_number in range(0, self.numero_procesos):
            self.new_proces.append({
                "process": process_number,
                "function": self.function_catalog[random.randint(0, len(self.function_catalog)-1)],
            })

    def execute_process(self, process:dict = {} ):
        #print("=" * 100)
        inicio = pendulum.now()

        print(f"proceso en ejecucion {process['process']}")
        resultado = process["function"]["funcion"]()
        print(f"resultado {resultado}")

        fin = pendulum.now()
        #print(f"se ejecuto : {inicio.diff(fin).microseconds} micro segundos")

    def is_shorter_than(self,first_process:dict):
        print(first_process)
        return first_process["function"]["tiempo"]

    def move_newprocess_toready(self):
        while len(self.ready_process) < 5:
            if len(self.new_proces) == 0:
                break
            else:
                proces_to_execute = self.new_proces.pop(0)
                self.ready_process.append(proces_to_execute)
                self.ready_process.sort(key=self.is_shorter_than)

    def print_queues_info(self, to_execute):
        resume = [
            ["nuevos", [ element['process'] for element in self.new_proces ]],
            ["listos", [element['process'] for element in self.ready_process ]],
            ["ejecucion", to_execute],
        ]
        print(tabulate(resume, headers=["concepto", "valores"], tablefmt="fancy_grid"))


    def execute_process_queue(self):
        self.build_process_queue()
        execution_queue_size = len(self.new_proces)
        aborted = 0
        aborted_processes = []
        executed_correctly = 0
        while len(self.new_proces) > 0 or len(self.ready_process) > 0:
            self.move_newprocess_toready()
            element = self.ready_process.pop(0)
            self.print_queues_info(element)
            if keyboard.is_pressed('e'):
                aborted += 1
                aborted_processes.append(element["process"])
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('t'):
                aborted = (execution_queue_size - (aborted + executed_correctly))
                aborted_processes.append(element["process"])
                aborted_processes += [str(x["process"]) for x in self.ready_process]
                break
            self.execute_process(element)
            executed_correctly += 1
        resume = [
            ["total procesos", f"{execution_queue_size}"],
            ["ejecutados correctamente", f"{executed_correctly}"],
            ["abortados", f"{aborted}"],
            ["abortados numero proceso", ",".join([str(x) for x in aborted_processes])],
        ]
        print(tabulate(resume, headers=["concepto", "valor"], tablefmt="fancy_grid"))


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

lista_funciones = [
    {
        "funcion": suma,
        "tiempo": 1
    },
    {
        "funcion": division,
        "tiempo": 3
    },
    {
        "funcion": multiplicacion,
        "tiempo": 2
    },
]


if __name__ == "__main__":
    numero_procesos = random.randint(0, 30)
    print(f"se ejecutaran : {numero_procesos} procesos")
    maquina = Supervisor(numero_procesos=numero_procesos,funciones_lote=lista_funciones)
    maquina.execute_process_queue()
