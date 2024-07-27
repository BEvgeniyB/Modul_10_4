from queue import Queue
from threading import Thread
from time import sleep


class Table:
    guest: str

    def __init__(self, num):
        self.num = num
        self.is_busy = True
        self.time = 0
        self.guest = ''

    def condition(self, args):
        if args[0]:
            self.guest = ""
            self.time = 0
            self.is_busy = True
        else:
            self.guest = args[1]
            self.time = 1
            self.is_busy = False


class Customer:
    count = 0

    def __init__(self,current_time):
        type(self).count += 1
        self.names = 'Посетитель № ' + str(self.count)
        print(f'Текущее время : {current_time} / {self.names} прибыл')


class Cafe:
    def __init__(self, tables_):
        self.tables = tables_

    def customer_arrival(self):
        guest_num = 20
        current_time = 1
        while True:
            self.serve_customer(current_time)
            if guest_num != 0:
                guest_new = Customer(current_time)
                queue.put(guest_new)
                guest_num -= 1
                found = False
                for table in self.tables:
                    if table.is_busy:
                        guest_queue = queue.get()
                        if guest_new != guest_queue:
                            print(f'Текущее время : {current_time} / {guest_new.names} ожидает свободный стол')
                        table.condition((False, guest_queue.names))
                        print(f"Текущее время : {current_time} / {guest_queue.names} сел за стол № {table.num}. (начало обслуживания)")
                        found = True
                        break
                if not found:
                    queue.put(guest_new)
                    print(f'Текущее время : {current_time} / {guest_new.names} ожидает свободный стол')

            elif not queue.empty():
                guest_queue = queue.get()
                for table in self.tables:
                    if table.is_busy:
                        table.condition((False, guest_queue.names))
                        print(f"Текущее время : {current_time} / {guest_queue.names} сел за стол № {table.num}. (начало обслуживания)")
                        break
            else:
                all_tables_empty = True
                for table in self.tables:
                    if not table.is_busy:
                        all_tables_empty = False
                if all_tables_empty:
                    break
            sleep(1)
            current_time += 1
    def serve_customer(self,current_time):
        for table in self.tables:
            if not table.is_busy:
                table.time += 1
                if table.time == 5:
                    print(f'Текущее время : {current_time}  /{table.guest} покушал и ушёл.')
                    table.condition((True,))


queue = Queue()
# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
