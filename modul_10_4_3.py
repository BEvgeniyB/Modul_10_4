from queue import Queue
from threading import Thread, Lock
from time import sleep


class Customer:
    count = 0

    def __init__(self):
        type(self).count += 1
        self.name = 'Посетитель № ' + str(self.count)


class Table():
    lock = Lock()

    def __init__(self, num):
        self.name = "Стол № " + str(num)
        self.is_busy = True
        self.guest = str()

    def condition(self, *args):
        print(f"Текущее время : {args[1]} /"
              f" {args[0]} сел за стол № {self.name}. (начало обслуживания) ")
        sleep(5)
        self.is_busy = True
        print(f'Текущее время : {args[1] + 5}  /{args[0]} покушал и ушёл.')
        print(f'{self.name} свободен')


class Cafe:
    def __init__(self, tables):
        self.tables = list(tables)

    def free_table(self):
        free = True
        for i in self.tables:
            if not i.is_busy:
                free = False
        return free

    def not_free_table(self):
        not_free = True
        for i in self.tables:
            if i.is_busy:
                not_free = False
        return not_free

    def customer_arrival(self):

        guest_num = 1
        current_time = 1
        while True:

            if guest_num != 20:
                guest_new = Customer()
                if self.not_free_table() or not queue.empty():
                    print(f'Текущее время : {current_time} / {guest_new.name} ожидает свободный стол')
                queue.put(guest_new)
                guest_num += 1
                print(f'Текущее время : {current_time} / {guest_new.name} прибыл')


            elif self.free_table() and queue.empty():
                print('Ресторан закрыт')
                break
            free = False
            for i in self.tables:
                if i.is_busy:
                    free = True
                    if queue.empty():
                        pass
                    else:
                        q = queue.get()
                        i.is_busy = False
                        lock = Lock()
                        with lock:
                            self.serve_customer(i, q.name, current_time)

            sleep(1)
            current_time += 1

    def serve_customer(self, table, guest, current_time):

        t1 = Thread(target=table.condition, args=(guest, current_time))
        t1.start()


queue = Queue()
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)

tables = [table1, table2, table3]
cafe = Cafe(tables=tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

customer_arrival_thread.join()
