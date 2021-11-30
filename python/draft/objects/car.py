class Car:
    def __init__(self, objem_motoru, pocet_kol):
        self.pocet_kol = pocet_kol
        self.objem_motoru = objem_motoru

    def info(self):
        print("Objem motoru={}, pocet kol={}".format(self.objem_motoru, self.pocet_kol))

    def lepsi_motor(self, zvysit):
        self.objem_motoru += zvysit


car = Car(2.5, 3)
car.info()
car.lepsi_motor(3)
car.info()

