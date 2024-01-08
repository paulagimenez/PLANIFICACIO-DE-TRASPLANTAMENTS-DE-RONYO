class Solucio:
    def __init__(self):
        """
        Inicialitza una nova instància de la classe Solucio.

        Attributes:
        - conjunt_cicles (list): Llista de cicles continguts en la solució.
        - puntuacio_total (int): Puntuació total de la solució.
        - iteracions (int): Nombre d'iteracions realitzades.
        - cicles_2 (int): Nombre de cicles amb 2 parelles.
        - cicles_3 (int): Nombre de cicles amb 3 parelles.
        """
        self.conjunt_cicles = []
        self.puntuacio_total = 0
        self.iteracions = 0
        self.cicles_2 = 0
        self.cicles_3 = 0

    def __str__(self):
        """
        Retorna una representació en cadena de la solució.

        :return: Cadena que representa la solució.
        """
        result = "Llista de cicles:\n"
        for cicle in self.conjunt_cicles:
            result += str(cicle)

        result += f"Puntuació total: {self.puntuacio_total}\n"
        return result

    def eliminar(self, cicle):
        """
        Elimina un cicle de la solució i recalcula la puntuació total.

        :param cicle: Cicle a ser eliminat de la solució.
        """
        self.conjunt_cicles.remove(cicle)
        self.calcular_punt_total()

    def es_buida(self):
        """
        Comprova si la solució està buida.

        :return: True si la solució està buida, False altrament.
        """
        return len(self.conjunt_cicles) == 0

    def buidar(self):
        """
        Buida la solució, eliminant tots els cicles i reinicialitzant la puntuació total.
        """
        self.conjunt_cicles.clear()
        self.puntuacio_total = 0

    def afegir_solucio(self, solucio):
        """
        Afegeix els cicles d'una altra solució a la solució actual, i recalcula la puntuació total.

        :param solucio: Solució que es vol afegir a la solució actual.
        """
        self.conjunt_cicles.extend(solucio.conjunt_cicles)
        self.calcular_punt_total()
        self.ordenar_por_puntuacio()

    def afegir_cicle(self, cicle):
        """
        Afegeix un cicle a la solució i recalcula la puntuació total.

        :param cicle: Cicle a ser afegit a la solució.
        """
        self.conjunt_cicles.append(cicle)
        self.calcular_punt_total()
        self.ordenar_por_puntuacio()

    def calcular_punt_total(self):
        """
        Calcula la puntuació total de la solució sumant les puntuacions de tots els cicles.
        """
        self.puntuacio_total = sum(c.puntuacio_cicle for c in self.conjunt_cicles)

    def cicles_disjunts(self, c):
        """
        Comprova si un cicle és disjunt amb tots els altres cicles de la solució. Serà disjunt quan no trobi cap parella repetida en tots els cicles que formen la solució.

        :param c: Cicle per comprovar la disjunció amb els altres cicles.
        :return: True si el cicle és disjunt amb tots els altres cicles, False altrament.
        """
        for cicle in self.conjunt_cicles:
            if cicle.parella_repetida(c):
                return False
        return True

    def ordenar_por_puntuacio(self):
        """
        Ordena els cicles de la solució segons la puntuació en ordre creixent.
        """
        self.conjunt_cicles.sort(key=lambda x: x.puntuacio_cicle, reverse=False)

    def calcular_quantitat_cicles(self):
        """
        Calcula la quantitat de cicles amb 2 i 3 parelles a la solució.
        """
        for cicle in self.conjunt_cicles:
            if len(cicle.llista_parelles) == 2:
                self.cicles_2 += 1
            if len(cicle.llista_parelles) == 3:
                self.cicles_3 += 1
