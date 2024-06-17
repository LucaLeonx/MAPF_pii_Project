class Prova:

    def __init__(self, integer):
        self._integer = integer

    @property
    def integer(self):
        return self._integer


def main():
    prova = Prova(11)
    funzione = Prova.integer
    if isinstance(funzione, property):
        funzione = funzione.fget

    print(funzione(prova))


if __name__ == '__main__':
    main()
