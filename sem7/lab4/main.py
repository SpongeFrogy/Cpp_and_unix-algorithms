import time
import random
import threading
import asyncio
import subprocess

# Действие 1: Регистрация на портале
def action1():
    time.sleep(2)  # Время обработки T1
    cpu_load = 25
    print(f"Регистрация завершена. Нагрузка на процессор: {cpu_load}%")

# Действие 2: Получение главной страницы
def action2():
    time.sleep(1)  # Время обработки T2
    cpu_load = 15
    print(f"Главная страница получена. Нагрузка на процессор: {cpu_load}%")

# Действие 3: Просмотр перечня зарегистрированных пользователей
def action3():
    time.sleep(0.1)  # Время обработки T3
    cpu_load = 1
    print(f"Просмотр перечня пользователей завершен. Нагрузка на процессор: {cpu_load}%")

# Последовательное решение (1)
def sequential_processing():
    action1()
    action2()
    action3()

# Параллельное решение с использованием subprocess (2)
def parallel_processing_subprocess():
    processes = []
    for action in [action1, action2, action3]:
        process = subprocess.Popen(["python", "parallel_request.py"])
        processes.append(process)
    
    for process, action in zip(processes, [1, 2, 3]):
        process.wait()
        print(f"Действие {action} завершено")

# Параллельное решение с использованием threads (3)
def parallel_processing_threads():
    threads = []
    for action in [action1, action2, action3]:
        thread = threading.Thread(target=action)
        threads.append(thread)
    
    for thread, action in zip(threads, [1, 2, 3]):
        thread.start()
        print(f"Действие {action} начато")
    
    for thread, action in zip(threads, [1, 2, 3]):
        thread.join()
        print(f"Действие {action} завершено")

# Параллельное решение с использованием asyncio (4)
async def async_action(action, action_number):
    await asyncio.sleep(random.uniform(0.5, 2.0))  # Рандомное время обработки
    print(f"Действие {action_number} завершено")

async def parallel_processing_asyncio():
    tasks = [async_action(action, i) for i, action in enumerate([action1, action2, action3], start=1)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("Последовательное решение (1):")
    sequential_processing()

    print("\nПараллельное решение с использованием subprocess (2):")
    parallel_processing_subprocess()

    print("\nПараллельное решение с использованием threads (3):")
    parallel_processing_threads()

    print("\nПараллельное решение с использованием asyncio (4):")
    asyncio.run(parallel_processing_asyncio())