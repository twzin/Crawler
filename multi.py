import threading # -> Biblioteca builtin para trabalhar com multithreading
import time

# Multithread serve para fazer varios serviços sem ter que esperar um terminar para passar para o proximo

def fazer_requisição():
    print("Fazendo requisição web!")
    time.sleep(2)
    print("Terminei a requisição")


thread_1 = threading.Thread(target=fazer_requisição)
thread_1.start()

thread_2 = threading.Thread(target=fazer_requisição)
thread_2.start()

thread_3 = threading.Thread(target=fazer_requisição)
thread_3.start()

thread_4 = threading.Thread(target=fazer_requisição)
thread_4.start()
