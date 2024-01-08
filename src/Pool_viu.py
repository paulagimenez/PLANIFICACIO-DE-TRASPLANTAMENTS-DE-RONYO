import random
from Cadena import Cadena
import Calcul_compatibilitat
import Calcul_puntuacions
from Parella import Parella


def possibilitat_pacient_dos_pools(pacient, llista_cadaver):
    """
    Assigna una probabilitat de 10% perquè el pacient s'assigni a les dues llistes d'espera (pool viu i pool cadàver)

    :param pacient: Pacient receptor.
    :param llista_cadaver: Llista de cadàvers amb la qual es podria fusionar.
    """
    num = random.random()
    if num < 0.1:
        pacient.probabilitat_dos_pools = True
        llista_cadaver.afegir_receptor(pacient)


class Pool_viu:
    def __init__(self):
        """
        Inicialitza un nou objecte Pool_viu.

        Atribut:
        - parelles: Un diccionari que emmagatzema les parelles en el pool, identificades pel seu identificador únic.
        """
        self.parelles = {}

    def __str__(self):
        """
        Retorna una representació en cadena de l'objecte Pool_viu.

        :return: Cadena que representa l'objecte Pool_viu.
        """
        return "\n".join(str(parella) for parella in self.parelles.values())

    def reiniciar_pool(self):
        """
        Reinicia el pool eliminant totes les parelles del diccionari.
        """
        self.parelles = {}

    def afegir_parella(self, donant, receptor, donants, receptors, llista_cadaver):
        """
        Afegeix una nova parella al pool viu i gestiona els canvis associats.

        :param donant: Donant de la parella.
        :param receptor: Receptor de la parella.
        :param donants: Llista de donants disponibles.
        :param receptors: Llista de receptors disponibles.
        :param llista_cadaver: Llista de cadàvers amb la qual es podria fusionar.
        """
        parella = Parella(donant, receptor)
        # Vincular donant i receptor de la parella
        donant.rec_asoc = receptor
        receptor.don_asoc = donant
        self.parelles[parella.ident] = parella
        donants.remove(donant)
        receptors.remove(receptor)
        possibilitat_pacient_dos_pools(receptor, llista_cadaver)

    def eliminar_parella(self, parella):
        """
        Elimina una parella del pool.

        :param parella: Parella a eliminar.
        """
        if parella.ident in self.parelles:
            del self.parelles[parella.ident]

    def afegir_parella_incompatible(self, donants, receptors, llista_cadaver):
        """
        Afegeix una nova parella al pool viu on el donant i el receptor no són compatibles.

        :param donants: Llista de donants disponibles.
        :param receptors: Llista de receptors disponibles.
        :param llista_cadaver: Llista de cadàvers amb la qual es podria fusionar.
        """
        donants_copia = donants.copy()
        random.shuffle(donants_copia)

        for donant in donants_copia:
            receptors_copia = receptors.copy()
            random.shuffle(receptors_copia)

            receptor_incompatible = next((receptor for receptor in receptors_copia if
                                          not Calcul_compatibilitat.es_compatible(donant, receptor)),
                                         None)

            if receptor_incompatible is not None:
                self.afegir_parella(donant, receptor_incompatible, donants, receptors, llista_cadaver)
                break  # Sortir del bucle després d'afegir una parella
        else:
            print("No s'ha trobat una parella prèviament incompatible")

    def afegir_incompatibles(self, donants, receptors, parelles_afegides, max_pacients, llista_cadaver):
        """
        Afegeix parelles incompatibles al pool viu fins arribar a la quantitat màxima de pacients.

        :param donants: Llista de donants disponibles.
        :param receptors: Llista de receptors disponibles.
        :param parelles_afegides: Nombre de parelles afegides fins ara.
        :param max_pacients: Quantitat màxima de pacients a assolir.
        :param llista_cadaver: Llista de cadàvers amb la qual es podria fusionar.
        """
        random.shuffle(receptors)
        receptors_copia = receptors.copy()

        for donant in donants:
            if parelles_afegides >= max_pacients:
                break

            receptor_incompatible = next((receptor for receptor in receptors_copia if
                                          not Calcul_compatibilitat.es_compatible(donant, receptor)),
                                         None)

            if receptor_incompatible is not None:
                self.afegir_parella(donant, receptor_incompatible, donants, receptors, llista_cadaver)
                receptors_copia.remove(receptor_incompatible)
                parelles_afegides += 1

    def crear_possible_cadena(self, donante_inicial, receptors_rebutjats, llista_cadaver, punt_mesos,
                              donant_complicat=None, receptor_complicat=None):
        """
        Crea una possible cadena de donació a partir del pool viu.

        :param donante_inicial: Donant inicial de la cadena.
        :param receptors_rebutjats: Diccionari amb receptors rebutjats.
        :param llista_cadaver: Llista de cadàvers amb la qual es podria fusionar.
        :param punt_mesos: Puntuació assignada als mesos de diàlisi.
        :param donant_complicat: Donant complicat a incloure a la cadena.
        :param receptor_complicat: Receptor complicat a incloure a la cadena.
        :return: La cadena de donació creada i el donant final.
        """
        if not self.parelles:
            print("No hi ha parelles disponibles. No es pot realitzar cap donació.")
            return None, None

        nueva_cadena = Cadena()
        donant_actual = donante_inicial
        donacions_realitzades = 0  # Comptador de donacions realitzades

        if donant_complicat and receptor_complicat:
            nueva_cadena.afegir_donacio(donant_complicat, receptor_complicat)
            donacions_realitzades += 1

        while donacions_realitzades < 5:
            llista_rebutjats = []
            receptor_mes_compatible = self.buscar_receptor_mes_compatible(donant_actual, llista_rebutjats, punt_mesos)
            while receptor_mes_compatible:  # Bucle per buscar un altre receptor en cas de rebuig
                num_aleatori = random.random()

                if num_aleatori >= receptor_mes_compatible.probabilitat_fallada:
                    # No hi ha rebuig, es realitza la donació
                    nueva_cadena.afegir_donacio(donant_actual, receptor_mes_compatible)

                    # Eliminar de la llista de parelles
                    parella_eliminar = self.buscar_pareja_per_donant_receptor(receptor_mes_compatible.don_asoc,
                                                                              receptor_mes_compatible)
                    self.eliminar_parella(parella_eliminar)
                    if parella_eliminar.receptor.probabilitat_dos_pools:
                        llista_cadaver.eliminar_receptor(parella_eliminar.receptor)
                    donant_actual = receptor_mes_compatible.don_asoc
                    donacions_realitzades += 1
                    break  # Sortir del bucle quan es produeixi una donació exitosa

                else:
                    receptor_mes_compatible.n_rebutjos += 1
                    info_rebuig = ('v', receptor_mes_compatible.n_rebutjos)
                    receptors_rebutjats[receptor_mes_compatible.id_rec] = info_rebuig
                    llista_rebutjats.append(receptor_mes_compatible)
                    # Buscar un altre receptor compatible pel donant
                    receptor_mes_compatible = self.buscar_receptor_mes_compatible(donant_actual,
                                                                                  llista_rebutjats, punt_mesos)

            else:
                if len(nueva_cadena.donacions) > 1:
                    return nueva_cadena, donant_actual
                else:
                    return None, donant_actual

        # El donant final serà l'últim donant de la cadena
        donant_final = donant_actual

        return nueva_cadena, donant_final

    def buscar_receptor_mes_compatible(self, nou_donant, llista_rebutjats, punt_mesos):
        """
        Busca el receptor més compatible amb el donant actual.

        :param nou_donant: Donant actual.
        :param llista_rebutjats: Llista de receptors rebutjats.
        :param punt_mesos: Puntuació assignada als mesos de diàlisi.
        :return: Receptor més compatible o None si no es troba cap receptor compatible.
        """
        receptor_mas_compatible = None
        puntuacio_mes_alta = 0

        for parella in self.parelles.values():
            for rebutjat in llista_rebutjats:
                if parella.receptor.id_rec == rebutjat.id_rec:
                    continue

            if Calcul_compatibilitat.es_compatible(nou_donant, parella.receptor):
                puntuacio = Calcul_puntuacions.calc_puntuacio_total(nou_donant, parella.receptor, punt_mesos)
                if puntuacio > puntuacio_mes_alta:
                    receptor_mas_compatible = parella.receptor
                    puntuacio_mes_alta = puntuacio

        return receptor_mas_compatible

    def buscar_pareja_per_donant_receptor(self, donant, receptor):
        """
        Busca la parella corresponent a un donant i un receptor específics.

        :param donant: Donant de la parella.
        :param receptor: Receptor de la parella.
        :return: Parella corresponent o None si no es troba.
        """
        for identificador, parella in self.parelles.items():
            if parella.donant.id_don == donant.id_don and parella.receptor.id_rec == receptor.id_rec:
                return parella
        return None

    def buscar_mes_delicat(self):
        """
        Busca la parella més delicada del pool segons la suma de temps en diàlisi i edat.

        :return: Parella més delicada i la seva puntuació o None si el pool està buit.
        """
        if not self.parelles:
            print("La llista está buida")
            return None

        parella_mes_delicada = None
        max_puntuacio = -1

        for parella in self.parelles.values():
            receptor = parella.receptor
            # Establim una puntuació que serà la suma de temps en diàlisi + edat
            puntuacio = receptor.m_amb_dialisis + receptor.edat

            if puntuacio > max_puntuacio:
                parella_mes_delicada = parella
                max_puntuacio = puntuacio

        return parella_mes_delicada, max_puntuacio

    def buscar_parelles_receptors_complicats(self):
        """
        Busca les parelles en què el receptor té un percentatge d'anticossos elevat i pertany al grup sanguini 0.

        :return: Una llista de parelles complicades.
        """
        parelles_complicades = []

        for parella in self.parelles.values():
            receptor = parella.receptor
            if 90 <= receptor.percentatge_anticossos <= 100 and receptor.grup_sanguini == '0':
                parelles_complicades.append(parella)

        return parelles_complicades

