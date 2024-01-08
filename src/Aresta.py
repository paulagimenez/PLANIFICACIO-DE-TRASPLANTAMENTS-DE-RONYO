import Calcul_puntuacions
import random


class Aresta:
    def __init__(self, p1, p2):
        """
        Inicialitza una instància d'Aresta amb dues parelles (donant-receptor).

        :param p1: La primera parella.
        :param p2: La segona parella.
        """
        self.parella1 = p1
        self.parella2 = p2
        self.puntuacio_aresta = 0
        self.ident = f"{self.parella1.ident}-{self.parella2.ident}"

    def __str__(self):
        """
        Retorna una representació en format de cadena de text de l'objecte Aresta.

        :return str: Una cadena que mostra l'identificador i la puntuació de l'aresta.
        """
        return f"{self.ident} - Puntuació: {self.puntuacio_aresta}"

    def calcular_puntuacio_aresta(self, punt_mesos):
        """
        Calcula la puntuació de l'aresta utilitzant una funció externa.

        :param punt_mesos: Puntuació per mesos en diàlisi.
        :return: La puntuació total de l'aresta.
        """
        punt_aresta = Calcul_puntuacions.calc_puntuacio_total(self.parella1.donant, self.parella2.receptor, punt_mesos)
        return punt_aresta

    def es_viable(self):
        """
        Avalua la viabilitat de l'aresta en funció de la probabilitat de fallada del receptor.

        :return: True si l'aresta és viable, False altrament.
        """
        num_aleatori = random.random()
        if num_aleatori >= self.parella2.receptor.probabilitat_fallada:
            return True
        else:
            return False

    def generar_identificador_contrari(self):
        """
        Genera un identificador intercanviant les parelles.

        :return: L'identificador contrari.
        """
        ident_contrari = f"{self.parella2.ident}-{self.parella1.ident}"
        return ident_contrari
