import threading
import time
import random

drinks = [
    "Chicory",
    "Fanta",
    "Sprite",
    "Juice",
    "Masala",
    "Coffee",
    "Milkshake"
]

names = [
    "Olya",
    "Masha",
    "Oleg",
    "Max",
    "Sveta",
    "Nikita",
    "Dima"
]

assigned = {}
lock = threading.Lock()

tables = [False, False, False]

table_lock = threading.Lock()


def find_table(name):
    with table_lock:
        for i in range(len(tables)):
            if not tables[i]:
                tables[i] = True
                print(f"[{name}] нашёл свободный столик №{i + 1}")
                return i
    return None


def free_table(i, name):
    with table_lock:
        tables[i] = False
        print(f"[{name}] освободил столик №{i + 1}")


def customer_process(name):
    print(f"  {name} подошёл к двери кафе")

    time.sleep(random.uniform(0.2, 0.5))
    print(f"  {name} вошёл в кафе")

    time.sleep(random.uniform(0.2, 0.6))
    print(f"  {name} ждёт в очереди...")

    time.sleep(0.5)
    print(f"  Бариста: «Здравствуйте, {name}! Что будете?»")

    with lock:
        if name in assigned:
            drink = assigned[name]
        else:
            available = [d for d in drinks if d not in assigned.values()]
            drink = random.choice(available)
            assigned[name] = drink

    print(f"  {name}: «Мне, пожалуйста, {drink}»")

    print(f" Бариста готовит {drink} для {name}...")
    time.sleep(random.uniform(0.8, 1.5))
    print(f"  {name} получил свой {drink}")

    mode = random.choice(["inside", "takeout"])

    if mode == "inside":
        print(f"  {name} хочет пить внутри")

        table_index = find_table(name)

        if table_index is None:
            print(f"  Все столики заняты. {name} берёт напиток с собой")
            mode = "takeout"

    if mode == "inside":
        print(f"  {name} сидит и пьёт {drink}...")
        time.sleep(random.uniform(1.5, 2.5))
        print(f"  {name} допил {drink}")

        free_table(table_index, name)

    else:
        print(f"  {name} взял {drink} с собой и выходит")

    time.sleep(0.3)
    print(f" {name} вышел из кафе\n")


print("===== Main start =====\n")

threads = []

for name in names:
    t = threading.Thread(target=customer_process, args=[name])
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("===== Main end =====")

