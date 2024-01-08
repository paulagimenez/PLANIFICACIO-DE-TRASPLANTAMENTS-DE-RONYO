import random
import Calcul_compatibilitat
import Calcul_puntuacions


class Pool_cadaver:

    def __init__(self):
        """
        Crea una instància de la classe Pool_cadaver.

        Atributs:
            llista_receptors (list): Llista de receptors disponibles.
        """
        self.llista_receptors = []

    def __str__(self):
        """
        Retorna una representació en forma de cadena de la llista de receptors.

        :return: Representació en forma de cadena de la llista de receptors.
        """
        if not self.llista_receptors:
            return "La llista de receptors està buida."

        receptor_str_list = [str(receptor) for receptor in self.llista_receptors]
        return "\n".join(receptor_str_list)

    def reiniciar_pool(self):
        """
        Reinicia el pool, buidant totes les parelles existents.
        """
        self.llista_receptors = []

    def afegir_receptor(self, receptor):
        """
        Afegeix un receptor a la llista de receptors.

        :param receptor: Receptor a afegir.
        """
        self.llista_receptors.append(receptor)

    def eliminar_receptor(self, receptor):
        """
        Elimina un receptor de la llista de receptors.

        :param receptor: Receptor a eliminar.
        """
        self.llista_receptors.remove(receptor)

    def buscar_receptor_mes_delicat(self):
        """
        Busca el receptor més delicat en la llista de receptors del pool cadàver.

        :return: Tuple que conté el receptor més delicat i la seva puntuació.
        """
        if not self.llista_receptors:
            print("La llista està buida.")
            return None

        receptor_mes_delicat = None
        max_puntuacio = -1

        for receptor in self.llista_receptors:
            # Establim una puntuació que serà la suma de temps en diàlisi + edat
            puntuacio = receptor.m_amb_dialisis + receptor.edat

            if puntuacio > max_puntuacio:
                receptor_mes_delicat = receptor
                max_puntuacio = puntuacio

        return receptor_mes_delicat, max_puntuacio

    def possible_donacio(self, donant, llista_rebutjos, punt_mesos):
        """
        Busca a la llista de receptors del pool cadàver el més compatible pel donant en qüestió.

        :param donant: Donant que vol realitzar la donació.
        :param llista_rebutjos: Llista de receptors ja rebutjats.
        :param punt_mesos: Puntuació en mesos.

        :return: Receptor més compatible amb el donant.
        """
        llista_rebutjats = []
        if not self.llista_receptors:
            print("No hi ha receptors disponibles. No es pot realitzar cap donació.")
            return None

        receptor_mes_compatible = self.buscar_receptor_mes_compatible(donant, llista_rebutjats, punt_mesos)

        while receptor_mes_compatible:  # Bucle per buscar un altre receptor en cas de rebuig
            num_aleatori = random.random()

            if num_aleatori >= receptor_mes_compatible.probabilitat_fallada:
                return receptor_mes_compatible
            else:
                receptor_mes_compatible.n_rebutjos += 1
                info_rebuig = ('c', receptor_mes_compatible.n_rebutjos)
                llista_rebutjos[receptor_mes_compatible.id_rec] = info_rebuig
                llista_rebutjats.append(receptor_mes_compatible)
                receptor_mes_compatible = self.buscar_receptor_mes_compatible(donant, llista_rebutjats, punt_mesos)

    def buscar_receptor_mes_compatible(self, donant, llista_rebutjats, punt_mesos):
        """
        Busca el receptor més compatible amb un donant en particular, evitant receptors ja rebutjats.

        :param donant: Donant pel qual buscar un receptor compatible.
        :param llista_rebutjats: Llista de receptors ja rebutjats.
        :param punt_mesos: Puntuació en mesos.

        :return: Receptor més compatible amb el donant.
        """
        receptor_mes_compatible = None
        puntuacio_mes_alta = 0

        for receptor in self.llista_receptors:
            for rebutjat in llista_rebutjats:
                if receptor.id_rec == rebutjat.id_rec:
                    continue

            if Calcul_compatibilitat.es_compatible(donant, receptor):
                puntuacio = Calcul_puntuacions.calc_puntuacio_total(donant, receptor, punt_mesos)
                if puntuacio > puntuacio_mes_alta:
                    puntuacio_mes_alta = puntuacio
                    receptor_mes_compatible = receptor

        return receptor_mes_compatible
