"""
round robin simulation

logic:

* generate a number of functions

"""
import random
import keyboard
import time
import pendulum
from tabulate import tabulate
from functions import getRandomFunction


class Supervisor(object):
    def __init__(self, process_number: int, function_factory, quantum: int = 5):
        self.quamtum = quantum
        self.execution = None
        self.queue_new = list()
        self.queue_ready = list()
        self.queue_done = list()
        self.queue_bloqued = list()

        for process_id in range(0, process_number):
            process = {
                "id": process_id,
            }
            process.update(function_factory())
            process.update({
                "remainingtime": process["tiempo_ejecucion"],
                "executed": 0,
            })
            # print(process)
            self.queue_new.append(process)

    def is_shorter_than(self, first_process: dict):
        return first_process["remainingtime"]

    def move_newprocess_toready(self):
        # TODO : actualizar para considerar bloqueados y
        while len(self.queue_ready) < 3:
            if len(self.queue_new) == 0:
                break
            else:
                proces_to_execute = self.queue_new.pop(0)
                self.queue_ready.append(proces_to_execute)
                self.queue_ready.sort(key=self.is_shorter_than)

    def print_queues_info(self):
        resume = [
            ["nuevos", [element['id'] for element in self.queue_new]],
            ["listos", [element['id'] for element in self.queue_ready]],
            ["bloqued", [element['id'] for element in self.queue_bloqued]],
            ["ejecucion", self.execution],
        ]
        print(tabulate(resume, headers=["concepto", "valores"], tablefmt="fancy_grid"))

    def execute_process(self):
        """
        round robin logic
        si aun le falta ejecucion ejecutar
            * revisar si no ha sobrepasado el quantum
                * si lo paso devolver a listos
        si no mover a ejecutados
            * imprimir resultado de operacion

        :param process:
        :return:
        """

        print(f"proceso en ejecucion {self.execution['id']}")
        resultado = self.execution["funcion"]()

    def print_process_status(self):
        # print execution status
        pass

    def execute_process_queue(self):
        execution_queue_size = len(self.queue_new)
        aborted = 0
        aborted_processes = []
        executed_correctly = 0
        while len(self.queue_new) > 0 or len(self.queue_ready) > 0:
            self.move_newprocess_toready()
            current_process = self.queue_ready.pop(0)
            self.execution = current_process
            self.print_queues_info()

            # keyboard handler
            if keyboard.is_pressed('e'):
                aborted += 1
                aborted_processes.append(current_process["process"])
                time.sleep(0.1)
                continue
            if keyboard.is_pressed('t'):
                aborted = (execution_queue_size - (aborted + executed_correctly))
                aborted_processes.append(current_process["process"])
                aborted_processes += [str(x["process"]) for x in self.queue_ready]
                break
            if keyboard.is_pressed('b'):
                # implementar bloqueo de 3 a 4 secs
                continue
            # if dont have a kboard interrpt now we proced
            self.execute_process()
            #executed_correctly += 1

        # execution resume
        resume = [
            ["total procesos", f"{execution_queue_size}"],
            ["ejecutados correctamente", f"{executed_correctly}"],
            ["abortados", f"{aborted}"],
            ["abortados numero proceso", ",".join([str(x) for x in aborted_processes])],
        ]
        print(tabulate(resume, headers=["concepto", "valor"], tablefmt="fancy_grid"))


if __name__ == "__main__":
    numero_procesos = random.randint(10, 60)
    print(f"se ejecutaran : {numero_procesos} procesos")
    maquina = Supervisor(process_number=numero_procesos, function_factory=getRandomFunction)
    maquina.execute_process_queue()
