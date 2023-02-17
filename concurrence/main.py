from threading import Thread, Lock


class Cake:
    def __init__(self, quantity):
        self.quantity = quantity
    def biteMe(self):
        self.quantity -= 1
    def getQuantity(self):
        return self.quantity

class Person:
    def __init__(self, cake, name):
        self.cake = cake
        self.name = name

    def bite(self, lock):
        # acquire the lock
        #lock.acquire()
        with lock:
            while self.cake.getQuantity() > 0:
                print(f"==\n{self.name} muerde al pastel en {self.cake.getQuantity()}")
                self.cake.biteMe()
                print(f"{self.name} deja al pastel con {self.cake.getQuantity()}")
        #lock.release()

    def __str__(self):
        return self.name


c = Cake(30)

"""
p = Person(c, "Mario")
p.bite()
"""

people = [
    Person(c, "Mario"),
    Person(c, "Steph"),
    Person(c, "Anya"),
    Person(c, "Michaelt"),
    Person(c, "Marlon"),
]
#for p in people:
#    print(p)

# create a shared lock
lock = Lock()

threads = []
for p in people:
    #p.bite() # sequencial
    t = Thread(target=p.bite, args=(lock,))
    threads.append(t)
    #t.start()
    #t.join() # to wait

#print(threads)
for t in threads:
    t.start()


