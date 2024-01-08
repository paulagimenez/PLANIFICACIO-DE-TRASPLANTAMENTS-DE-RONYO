class Cicle:

    def __init__(self):
        """
        Inicialitza una instància de Cicle amb una llista buida de parelles, arestes, cicles interns,
        puntuacions i un identificador nul d'inici.

        """
        self.llista_parelles = []
        self.llista_arestes = []
        self.puntuacio_cicle = 0
        self.puntuacio_interns = 0
        self.llista_cicles_interns = []
        self.llista_puntuacions = []
        self.ident = None

    def __str__(self):
        """
        Retorna una representació en format de cadena de text de l'objecte Cicle.

        :return str: Una cadena que mostra detalls del cicle, incloent parelles, arestes, cicles interns i puntuacions.

        """
        result = f"Cicle {self.ident} -- {self.puntuacio_cicle} -- {self.puntuacio_interns}:\n"
        result += "Parelles:\n"
        result += "\n".join([f"- {str(parella)}" for parella in self.llista_parelles])
        result += "\n"

        if self.llista_arestes:
            result += "Arestes:\n"
            result += "\n".join([f"- {str(aresta)}" for aresta in self.llista_arestes])
            result += "\n"

        if self.llista_cicles_interns:
            result += "Cicles interns:\n"
            for cicle_intern in self.llista_cicles_interns:
                result += str(cicle_intern) + "\n"

        return result

    def get_parelles(self):
        """
        Obté la llista de parelles contingudes en el cicle.

        :return list: La llista de parelles en el cicle.

        """
        return self.llista_parelles

    def parella_repetida(self, altre_cicle):
        """
        Comprova si hi ha parelles repetides entre dos cicles.

        :param altre_cicle: L'altre cicle amb el qual es comprova la repetició de parelles.
        :return bool: True si hi ha parelles repetides, False altrament.

        """
        for parella_actual in self.llista_parelles:
            for parella_otro in altre_cicle.llista_parelles:
                if parella_actual.donant.id_don == parella_otro.donant.id_don and \
                        parella_actual.receptor.id_rec == parella_otro.receptor.id_rec:
                    return True
        return False

    def identificar(self):
        """
        Identifica el cicle i retorna la tupla identificadora.

        :return tuple: La tupla que identifica el cicle.

        """
        ident = [parella.ident for parella in self.llista_parelles]
        min_ident = min(ident)
        min_index = ident.index(min_ident)
        ident = tuple(ident[min_index:] + ident[:min_index])
        self.ident = ident
        return ident

    def buscar_cicle_sentit_contrari(self):
        """
        Busca el cicle amb el sentit contrari.

        :return tuple: La identificació i la tupla del cicle amb el sentit contrari.

        """
        invers_tupla = tuple(reversed(self.ident))
        invers_ident = "-".join(map(str, invers_tupla))
        return invers_ident, invers_tupla

    def calcular_puntuacio_interns(self, puntuacio_intern_2, puntuacio_intern_3):
        """
        Calcula la puntuació dels cicles interns.

        :param puntuacio_intern_2: Puntuació assignada als cicles interns de mida 2.
        :param puntuacio_intern_3: Puntuació assignada als cicles interns de mida 3.

        """
        p_unit = self.puntuacio_cicle / len(self.llista_parelles)
        for intern in self.llista_cicles_interns:
            mida_intern = len(intern.split('-'))
            if mida_intern == 3:
                self.puntuacio_interns += p_unit / puntuacio_intern_3
            elif mida_intern == 2:
                self.puntuacio_interns += p_unit / puntuacio_intern_2
        self.puntuacio_cicle += self.puntuacio_interns
