

class Deneme:
    deger = 111
    def __init__(self) -> None:
        pass


    def fnc(self):
        self.deger = 123
        pass
        


    def fnc2(self):
        self.fnc()
        print(self.deger)




deneme = Deneme()

deneme.fnc2()