import numpy as np
import simpy
import Calcul_compatibilitat
import Calcul_puntuacions
import Calcul_solucio
from Aresta import Aresta
from Estadistica import Estadistica
import Llegir_excel
import Calcul_cicles
from Pool_viu import Pool_viu
from Pool_cadaver import Pool_cadaver
from Cicle import Cicle
from Solucio import Solucio
import random


def definir_taxes_poisson(mida_pool_viu, mida_pool_cadaver, temps_total_simulacio):
    """
    Defineix les taxes utilitzant distribucions de Poisson.

    :param mida_pool_viu: La mida del pool de vius.
    :param mida_pool_cadaver: La mida del pool de cadàvers.
    :param temps_total_simulacio: El temps total de simulació en hores.
    :return: Les taxes calculades per a donant cadàver, parelles, receptors, i morts.
    """
    total_receptors_pools = mida_pool_viu + mida_pool_cadaver

    taxa_arribada_donant_cadaver = list(np.random.poisson(lam=0.1, size=temps_total_simulacio))
    taxa_arribada_parelles = list(np.random.poisson(lam=mida_pool_viu / (365 * 24 * 2), size=temps_total_simulacio))
    taxa_arribada_receptor = list(
        np.random.poisson(lam=mida_pool_cadaver / (365 * 24 * 2), size=temps_total_simulacio))
    taxa_mort = list(np.random.poisson(lam=(total_receptors_pools * 0.08) / (365 * 24), size=temps_total_simulacio))

    return taxa_arribada_donant_cadaver, taxa_arribada_parelles, taxa_arribada_receptor, taxa_mort


class Simulador:
    contador_arribada_parelles = 0
    contador_arribada_receptor = 0
    contador_arribada_donant_cadaver = 0
    contador_mort_receptor = 0
    contador_cadenes = 0
    contador_trasplants_viu = 0

    MAX_PACIENTS_POOL_VIU = 200
    MAX_PACIENTS_POOL_CADAVER = 2000
    PUNTUACIO_CICLE_INTERN_2 = 0
    PUNTUACIO_CICLE_INTERN_3 = 0
    PUNTUACIO_MESOS_DIALISI = 0
    PUNTUACIO_REBUTJOS = 0

    WAIT_TIMES = []
    ruta_arxiu_donants = r'C:/Users/paula/OneDrive/Escritorio/GEB/TFG/Pràctica/Dades ' \
                         r'artificials/Dades_artificials_donants.xlsx'

    ruta_arxiu_receptors = r'C:/Users/paula/OneDrive/Escritorio/GEB/TFG/Pràctica/Dades ' \
                           r'artificials/Dades_artificials_receptors_1donant.xlsx'
    ruta_arxiu_anticossos = r'C:/Users/paula/OneDrive/Escritorio/GEB/TFG/Pràctica/Dades ' \
                            r'artificials/HOLA.xlsx'

    def __init__(self):
        """
        Inicialitza una instància del Simulador amb llistes buides i altres estructures necessàries.
        """
        self.donants = []
        self.receptors = []
        self.llista_espera_vius = Pool_viu()
        self.llista_espera_cadaver = Pool_cadaver()
        self.nous_cicles = {}
        self.arestes = {}
        self.cadenes = {}
        self.trasplantaments_realitzats = {}
        self.receptors_rebutjats = {}
        self.solucio_final = None

    # CARREGAR DADES I INICIALITZACIÓ LLISTES D'ESPERA
    def carregar_dades(self):
        """
        Carrega les dades dels arxius Excel especificat i vincula els donants amb els receptors corresponents.
        """
        self.donants, self.receptors = Llegir_excel.crear_donats_receptors(self.ruta_arxiu_donants,
                                                                           self.ruta_arxiu_receptors,
                                                                           self.ruta_arxiu_anticossos)
        Llegir_excel.vincular_receptor_a_donant(self.donants, self.receptors)

    def inicialitzar_pool_cadaver(self):
        """
        Inicialitza la llista d'espera de receptors cadàver, barrejant-los i afegint-los fins arribar al límit.
        """
        random.shuffle(self.receptors)
        max_receptors_a_afegir = self.MAX_PACIENTS_POOL_CADAVER - len(self.llista_espera_cadaver.llista_receptors)

        for receptor in self.receptors[:max_receptors_a_afegir]:
            self.llista_espera_cadaver.afegir_receptor(receptor)

        self.receptors = self.receptors[max_receptors_a_afegir:]

    def inicialitzar_pool_viu(self):
        """
        Inicialitza la llista d'espera de receptors vius, afegint parelles de donants-receptors associats i
        buscant possibles donants prèviament incompatibles per als receptors.
        """
        donants_copia = self.donants.copy()

        for donant in donants_copia:
            if donant.rec_asoc is not None:
                receptor_associat = donant.rec_asoc
                self.llista_espera_vius.afegir_parella(donant, receptor_associat, self.donants, self.receptors,
                                                       self.llista_espera_cadaver)

        parelles_afegides = len(self.llista_espera_vius.parelles)
        self.llista_espera_vius.afegir_incompatibles(self.donants, self.receptors, parelles_afegides,
                                                     self.MAX_PACIENTS_POOL_VIU, self.llista_espera_cadaver)

    def arribada_parella_pool_viu(self):
        """
        Simula l'arribada d'una nova parella a la llista d'espera de receptors vius.
        """
        self.llista_espera_vius.afegir_parella_incompatible(self.donants, self.receptors, self.llista_espera_cadaver)

    def arribada_receptor_pool_cadaver(self):
        """
        Simula l'arribada d'un nou receptor a la llista d'espera de receptors cadàver.
        """
        receptors_copia = self.receptors.copy()
        if not receptors_copia:
            print("La llista de receptors està buida.")
            return
        else:
            receptors_copia = self.receptors.copy()
            random.shuffle(receptors_copia)
            receptor_seleccionat = random.choice(receptors_copia)
            self.llista_espera_cadaver.afegir_receptor(receptor_seleccionat)
            self.receptors.remove(receptor_seleccionat)

    def arribada_ronyo_cadaver(self, opcio_simulacio, nou_donant):
        """
        Simula l'arribada d'un ronyó cadàver, prenent decisions basades en la simulació.

        :param opcio_simulacio: Indica si es permet l'arribada de donant cadàver al pool viu ('sí' o 'no').
        :param nou_donant: Donant associat al ronyó cadàver.
        """
        llista_rebutjats = []
        if opcio_simulacio == 'si':
            copia_donant = nou_donant
            if copia_donant.edat < 60:
                parelles_complicades = self.llista_espera_vius.buscar_parelles_receptors_complicats()
                receptor_mes_compatible = self.trobar_receptor_mes_compatible(nou_donant,
                                                                              parelles_complicades,
                                                                              llista_rebutjats)
                while receptor_mes_compatible:
                    num_aleatori = random.random()
                    if num_aleatori >= receptor_mes_compatible.probabilitat_fallada:
                        parella_eliminar = self.llista_espera_vius.buscar_pareja_per_donant_receptor(
                            receptor_mes_compatible.don_asoc,
                            receptor_mes_compatible)
                        self.llista_espera_vius.eliminar_parella(parella_eliminar)
                        if parella_eliminar.receptor.probabilitat_dos_pools:
                            self.llista_espera_cadaver.eliminar_receptor(parella_eliminar.receptor)
                        donant_inicial = receptor_mes_compatible.don_asoc
                        self.arribada_pool_viu(donant_inicial, copia_donant, receptor_mes_compatible)
                        break

                    else:
                        receptor_mes_compatible.n_rebutjos += 1
                        info_rebuig = ('v', receptor_mes_compatible.n_rebutjos)
                        self.receptors_rebutjats[receptor_mes_compatible.id_rec] = info_rebuig
                        llista_rebutjats.append(receptor_mes_compatible)
                        receptor_mes_compatible = self.trobar_receptor_mes_compatible(nou_donant,
                                                                                      parelles_complicades,
                                                                                      llista_rebutjats)
                if not receptor_mes_compatible:
                    self.arribada_pool_cadaver(copia_donant)

            else:
                self.arribada_pool_cadaver(nou_donant)

        elif opcio_simulacio == 'no':
            self.arribada_pool_cadaver(nou_donant)

        else:
            print("Opció no vàlida")

    def trobar_receptor_mes_compatible(self, donant, parelles_complicades, llista_rebutjats):
        """
        Troba el receptor més compatible per a un donant dins de les parelles complicades.

        :param donant: Donant per al qual es busca un receptor compatible.
        :param parelles_complicades: Llista de parelles complicades.
        :param llista_rebutjats: Llista de receptors ja rebutjats.
        :return: Receptor més compatible o None si no es troba cap.
        """
        receptor_mes_compatible = None
        puntuacio_mes_alta = -1

        for parella in parelles_complicades:
            receptor = parella.receptor
            for rebutjat in llista_rebutjats:
                if receptor.id_rec == rebutjat.id_rec:
                    continue

            if Calcul_compatibilitat.es_compatible(donant, receptor):
                puntuacio = Calcul_puntuacions.calc_puntuacio_total(donant, receptor, self.PUNTUACIO_MESOS_DIALISI)
                if puntuacio > puntuacio_mes_alta:
                    puntuacio_mes_alta = puntuacio
                    receptor_mes_compatible = receptor

        return receptor_mes_compatible

    def arribada_pool_viu(self, nou_donant, donant_complicat, receptor_complicat):
        """
        Simula l'arribada d'un donant al pool de receptors vius, intentant formar cadenes de trasplantament.

        :param nou_donant: Donant que arriba al pool viu.
        :param donant_complicat: Donant complicat associat a una cadena de trasplantament.
        :param receptor_complicat: Receptor complicat associat a una cadena de trasplantament.
        """
        donant_actual = nou_donant

        while True:
            cadena, donant_final = self.llista_espera_vius.crear_possible_cadena(donant_actual,
                                                                                 self.receptors_rebutjats,
                                                                                 self.llista_espera_cadaver,
                                                                                 self.PUNTUACIO_MESOS_DIALISI,
                                                                                 donant_complicat,
                                                                                 receptor_complicat,
                                                                                 )

            if cadena:
                donant_actual = donant_final
                if len(cadena.donaciones) == 5:
                    self.cadenes[cadena.ident] = cadena
                else:
                    self.cadenes[cadena.ident] = cadena
                    self.arribada_pool_cadaver(donant_actual)
                    break
            else:
                self.arribada_pool_cadaver(donant_actual)
                break

    def realitzar_donacions_cadena(self):
        """
        Realitza les donacions de la cadena (  quan aquesta cadena tingui mida 1 s'interpreta com una donació normal, sense la formació de cadenes de trasplantament )
        """
        for ident_cadena, cadena in self.cadenes.items():
            if len(cadena.donaciones) > 1:
                for donante, receptor in cadena.donaciones:
                    nova_donacio = (donante.id_don, receptor.id_rec)
                    info_donacio = ('cadena', receptor.m_amb_dialisis)
                    self.trasplantaments_realitzats[nova_donacio] = info_donacio
            elif len(cadena.donaciones) == 1:
                donante, receptor = cadena.donaciones[0]
                nova_donacio = (donante.id_don, receptor.id_rec)
                info_donacio = ('v', receptor.m_amb_dialisis)
                self.trasplantaments_realitzats[nova_donacio] = info_donacio

    def arribada_pool_cadaver(self, nou_donant):
        """
        Simula l'arribada d'un donant al pool de receptors cadàver i busca un possible receptor per realitzar una donació.

        :param nou_donant: Donant que arriba al pool cadàver.
        """
        receptor_compat = self.llista_espera_cadaver.possible_donacio(nou_donant, self.receptors_rebutjats,
                                                                      self.PUNTUACIO_MESOS_DIALISI)

        while receptor_compat:
            nova_donacio = (nou_donant.id_don, receptor_compat.id_rec)
            info_donacio = ('c', receptor_compat.m_amb_dialisis)
            self.trasplantaments_realitzats[nova_donacio] = info_donacio
            self.llista_espera_cadaver.eliminar_receptor(receptor_compat)

            if receptor_compat.probabilitat_dos_pools:
                parella = self.llista_espera_vius.buscar_pareja_per_donant_receptor(receptor_compat.don_asoc,
                                                                                    receptor_compat)
                self.llista_espera_vius.eliminar_parella(parella)

            return

    def mort_receptor(self):
        """
        Simula la mort d'un receptor i gestiona les possibles eliminacions de la llista d'espera. S'eliminarà el pacient que es trobi més delicat d'entre les dues llsites d'espera.
        """
        parella_mes_delicada, punt_parella = self.llista_espera_vius.buscar_mes_delicat()
        receptor_cadaver_delicat, punt_receptor = self.llista_espera_cadaver.buscar_receptor_mes_delicat()

        if punt_parella > punt_receptor:
            self.llista_espera_vius.eliminar_parella(parella_mes_delicada)

            if parella_mes_delicada.receptor.probabilitat_dos_pools:
                self.llista_espera_cadaver.eliminar_receptor(parella_mes_delicada.receptor)

        else:
            self.llista_espera_cadaver.eliminar_receptor(receptor_cadaver_delicat)

            if receptor_cadaver_delicat.probabilitat_dos_pools:
                parella = self.llista_espera_vius.buscar_pareja_per_donant_receptor(receptor_cadaver_delicat.don_asoc,
                                                                                    receptor_cadaver_delicat)
                self.llista_espera_vius.eliminar_parella(parella)

    def crear_cicles(self):
        """
        Crea cicles de donacions a partir de la llista d'espera de receptors vius i les arestes disponibles.
        """
        llista_cicles = Calcul_cicles.crear_nodes_edges(self.llista_espera_vius, self.arestes,
                                                        self.PUNTUACIO_MESOS_DIALISI)

        for cicle in llista_cicles:
            nou_cicle = Cicle()
            for parella in cicle:
                nou_cicle.llista_parelles.append(parella)
            nou_cicle.identificar()
            self.puntuacio_i_cicles_interns(nou_cicle)
            self.nous_cicles[nou_cicle.ident] = nou_cicle

        self.nous_cicles = {k: v for k, v in
                            sorted(self.nous_cicles.items(), key=lambda x: x[1].puntuacio_cicle, reverse=True)}

    def existeix_aresta(self, ident):
        """
        Verifica si una aresta existeix en el diccionari d'arestes.

        :param ident: Identificador de l'aresta a revisar.
        :return: True si l'aresta existeix, False en cas contrari.
        """
        return ident in self.arestes

    def puntuacio_i_cicles_interns(self, cicle):
        """
        Calcula la puntuació i identifica els cicles interns d'un cicle donat.

        :param cicle: Cicle sobre el qual es realitzen els càlculs.
        """
        for i in range(len(cicle.llista_parelles)):
            pareja1 = cicle.llista_parelles[i]
            pareja2 = cicle.llista_parelles[(i + 1) % len(cicle.llista_parelles)]

            ident = f"{pareja1.ident}-{pareja2.ident}"
            ident_invers = f"{pareja2.ident}-{pareja1.ident}"

            if self.existeix_aresta(ident):
                aresta = Aresta(pareja1, pareja2)
                aresta.calcular_puntuacio_aresta(self.PUNTUACIO_MESOS_DIALISI)
                cicle.llista_arestes.append(aresta)
                cicle.puntuacio_cicle += aresta.puntuacio_aresta

            if len(cicle.llista_parelles) > 2:
                if self.existeix_aresta(ident_invers):
                    cicle.llista_cicles_interns.append(ident_invers)

                if len(cicle.llista_cicles_interns) == len(cicle.llista_parelles):
                    ident_cicle_contrari, c_tupla = cicle.buscar_cicle_sentit_contrari()
                    cicle.llista_cicles_interns.append(ident_cicle_contrari)

        if cicle.llista_cicles_interns:
            cicle.calcular_puntuacio_interns(self.PUNTUACIO_CICLE_INTERN_2, self.PUNTUACIO_CICLE_INTERN_3)

    def crear_solucion_inicial(self):
        """
        Crea una solució inicial amb cicles disjunts a partir dels cicles generats.

        :return: Solució inicial amb cicles disjunts.
        """
        sol_ini = Solucio()
        cicles_items = list(self.nous_cicles.values())

        for cicle_actual in cicles_items:
            if sol_ini.cicles_disjunts(cicle_actual):
                sol_ini.conjunt_cicles.append(cicle_actual)
                del self.nous_cicles[cicle_actual.ident]

        sol_ini.calcular_punt_total()
        return sol_ini

    def realitzar_donacio_aresta(self, aresta):
        """
        Simula la donació d'òrgans entre les parelles d'una aresta.

        :param aresta: Aresta que representa la donació.
        """
        donant_aresta = aresta.parella1.donant
        receptor_aresta = aresta.parella2.receptor

        nova_donacio = (donant_aresta.id_don, receptor_aresta.id_rec)
        info_donacio = ('cicle', receptor_aresta.m_amb_dialisis)
        self.trasplantaments_realitzats[nova_donacio] = info_donacio

        parella = self.llista_espera_vius.buscar_pareja_per_donant_receptor(donant_aresta, donant_aresta.rec_asoc)
        self.llista_espera_vius.eliminar_parella(parella)

        if parella.receptor.probabilitat_dos_pools:
            self.llista_espera_cadaver.eliminar_receptor(parella.receptor)

    def convertir_identificador(self, identificador):
        """
        Converteix un identificador a l'objecte de cicle corresponent.

        :param identificador: Identificador del cicle.
        :return: Objecte Cicle corresponent a l'identificador.
        """
        indice_minimo = identificador.index(min(identificador))
        identificador_ordenado = identificador[indice_minimo:] + identificador[:indice_minimo]

        for ident, ciclo in self.nous_cicles.items():
            if tuple(map(int, ident)) == tuple(identificador_ordenado):
                return ciclo

        return None

    def realitzar_donacions_solucio(self, solucio):
        """
        Simula les possibles donacions per a cada cicle en la solució donada.

        :param solucio: Solució que conté els cicles per als quals es realitzaran les donacions.
        """
        for cicle in solucio.conjunt_cicles:
            self.intentar_possibles_donacions(cicle)

    def intentar_possibles_donacions(self, cicle):
        """
        Intenta realitzar donacions del cicle donat, considerant les arestes i cicles interns.

        :param cicle: Cicle en el qual es faran les donacions.
        """
        rebuig_cicle_actual = False
        rebuig_cicle_contrari = False
        llista_arestes_viables = []

        # Buscar arestes viables en el cicle actual
        for aresta in cicle.llista_arestes:
            if aresta.es_viable():
                llista_arestes_viables.append(aresta.ident)
            else:
                rebuig_cicle_actual = True

        # Buscar arestes viables en cicles interns
        for ident_intern in cicle.llista_cicles_interns:
            if len(ident_intern.split('-')) == 2:
                aresta_intern = self.arestes[ident_intern]
                if aresta_intern.es_viable():
                    llista_arestes_viables.append(aresta_intern.ident)
                else:
                    rebuig_cicle_contrari = True

        # Intentar donacions en el sentit original
        if not rebuig_cicle_actual:
            for aresta in cicle.llista_arestes:
                self.realitzar_donacio_aresta(aresta)

        # Intentar donacions en el sentit contrari si no hi ha rebuig i el cicle té quatre interns
        elif len(cicle.llista_cicles_interns) == 4 and not rebuig_cicle_contrari:
            ident_guio, ident_tupla = cicle.buscar_cicle_sentit_contrari()
            ciclo_buscado = self.convertir_identificador(ident_tupla)
            for aresta in ciclo_buscado.llista_arestes:
                self.realitzar_donacio_aresta(aresta)

        # Intentar alternatives als interns si no es poden realitzar les donacions anteriors
        else:
            self.buscar_alternatives_interns(cicle, llista_arestes_viables)

    def buscar_alternatives_interns(self, cicle, llista_viables):
        """
        Intenta trobar alternatives als cicles interns si no es poden realitzar les donacions previstes.

        :param cicle: Cicle en el qual es buscaran alternatives als interns.
        :param llista_viables: Llista d'identificadors d'arestes viables en el cicle actual.
        """
        millor_cicle_intern = None
        millor_puntuacio = float('-inf')  # Inicialitzar amb el valor més baix possible

        for ident_aresta in llista_viables:
            aresta = self.arestes[ident_aresta]
            ident_contrari = aresta.generar_identificador_contrario()

            if ident_contrari in llista_viables:
                aresta_contraria = self.arestes[ident_contrari]
                tupla_aresta = tuple(map(int, aresta.ident.split("-")))
                tupla_contraria = tuple(map(int, aresta_contraria.ident.split("-")))
                identificador_menor = min(tupla_aresta, tupla_contraria)

                cicle_intern = self.nous_cicles[identificador_menor]
                if cicle_intern.puntuacio_cicle > millor_puntuacio:
                    millor_cicle_intern = cicle_intern
                    millor_puntuacio = cicle_intern.puntuacio_cicle

        if millor_cicle_intern:
            receptors_arestes_donades = []
            for aresta in millor_cicle_intern.llista_arestes:
                receptors_arestes_donades.append(aresta.parella1.receptor)
                self.realitzar_donacio_aresta(aresta)

            for aresta in cicle.llista_arestes:
                receptor = aresta.parella1.receptor
                if receptor not in receptors_arestes_donades:
                    receptor.n_rebutjos += 1
                    info_rebuig = ('v', receptor.n_rebutjos)
                    self.receptors_rebutjats[receptor.id_rec] = info_rebuig

        else:
            for aresta in cicle.llista_arestes:
                receptor = aresta.parella1.receptor
                receptor.n_rebutjos += 1
                info_rebuig = ('v', receptor.n_rebutjos)
                self.receptors_rebutjats[receptor.id_rec] = info_rebuig

    # VISUALITZAR ATRIBUTS
    def imprimir_nous_cicles(self):
        """
        Imprimeix la informació sobre els nous cicles generats.
        """
        print("Diccionari de Nous Cicles:")
        for ident, cicle in self.nous_cicles.items():
            print(str(cicle))

    def imprimir_diccionari_arestes(self):
        """
        Imprimeix la informació sobre les arestes generades.
        """
        for ident, aresta in self.arestes.items():
            print(f"Aresta: {aresta}")

    def imprimir_diccionari_rebutjos(self):
        """
        Imprimeix la informació sobre els receptors rebutjats.
        """
        for ident_receptor, num_trasplants in self.receptors_rebutjats.items():
            print(f"Receptor: {ident_receptor}, Número de rebuigs: {num_trasplants}")

    def imprimir_diccionari_trasplants(self):
        """
        Imprimeix la informació sobre els trasplantaments realitzats.
        """
        for donant, receptor in self.trasplantaments_realitzats.values():
            print(f"Donant: {donant}, Receptor: {receptor}")

    def imprimir_diccionari_cadenes(self):
        """
        Imprimeix la informació sobre les cadenes generades.
        """
        print("Diccionari de Cadenes:")
        for ident_cadena, cadena in self.cadenes.items():
            print(f"Identificació de la cadena: {ident_cadena}")
            print(str(cadena))

    # DEFINIM TAXES
    """
    Companion code to https://realpython.com/simpy-simulating-with-python/

    'Simulating Real-World Processes With SimPy'

    """

    def taxa_arribada_parelles_pool_viu(self, env, taxa_arribada_parelles):
        """
        Genera la taxa d'arribada de parelles al pool de vius.

        :param env: Entorn de Simpy.
        :param taxa_arribada_parelles: Llista que conté la taxa d'arribada de parelles a cada hora.
        :return: Generador Simpy.
        """
        index = 0
        while True:
            yield env.timeout(1)  # Representa el pas d'una hora
            arribades_en_hora = taxa_arribada_parelles[index]
            if arribades_en_hora > 0:
                for _ in range(arribades_en_hora):
                    self.arribada_parella_pool_viu()
                    self.contador_arribada_parelles += 1
            index = (index + 1) % len(taxa_arribada_parelles)

    def taxa_arribada_receptor_pool_cadaver(self, env, taxa_arribada_receptors):
        """
        Genera la taxa d'arribada de receptors al pool de cadàvers.

        :param env: Entorn de Simpy.
        :param taxa_arribada_receptors: Llista que conté la taxa d'arribada de receptors a cada hora.
        :return: Generador Simpy.
        """
        index = 0
        while True:
            yield env.timeout(1)
            arribades_en_hora = taxa_arribada_receptors[index]
            if arribades_en_hora > 0:
                for _ in range(arribades_en_hora):
                    self.arribada_receptor_pool_cadaver()
                    self.contador_arribada_receptor += 1
            index = (index + 1) % len(taxa_arribada_receptors)

    def taxa_arribada_don_cadaver(self, env, opcio_simulacio, taxa_arribada_cadaver):
        """
        Genera la taxa d'arribada de donants cadàver.

        :param env: Entorn de Simpy.
        :param opcio_simulacio: Opció de simulació.
        :param taxa_arribada_cadaver: Llista que conté la taxa d'arribada de donants cadàver a cada hora.
        :return: Generador Simpy.
        """
        index = 0
        while True:
            yield env.timeout(1)
            arribades_en_hora = taxa_arribada_cadaver[index]
            if arribades_en_hora > 0:
                for _ in range(arribades_en_hora):
                    random.shuffle(self.donants)
                    nou_donant = random.choice(self.donants)
                    for _ in range(2):  # Cada donant cadàver tindrà 2 ronyons per donar
                        self.arribada_ronyo_cadaver(opcio_simulacio, nou_donant)
                        self.contador_arribada_donant_cadaver += 1
            index = (index + 1) % len(taxa_arribada_cadaver)

    def taxa_mort_receptor(self, env, taxa_mort):
        """
        Genera la taxa de mortalitat de receptors.

        :param env: Entorn de Simpy.
        :param taxa_mort: Llista que conté la taxa de mortalitat de receptors a cada hora.
        :return: Generador Simpy.
        """
        index = 0
        while True:
            yield env.timeout(1)
            arribades_en_hora = taxa_mort[index]
            if arribades_en_hora > 0:
                for _ in range(arribades_en_hora):
                    self.mort_receptor()
                    self.contador_mort_receptor += 1
            index = (index + 1) % len(taxa_mort)

    def crear_cicles_hill_climbing(self):
        """
        Crea cicles utilitzant l'algorisme Hill Climbing per millorar la solució inicial.
        """
        print("Es procedeix al càlcul de possibles trasplantaments creuats")
        self.crear_cicles()
        sol_inicial = self.crear_solucion_inicial()
        sol_final = Calcul_solucio.hill_climbing(sol_inicial, self.nous_cicles)  # Millora de la solució inicial
        self.solucio_final = sol_final
        self.solucio_final.calcular_quantitat_cicles()
        self.realitzar_donacions_solucio(self.solucio_final)

    def actualitzar_contadors(self):
        """
        Reinicialitza els comptadors per al següent període de simulació.
        """
        self.contador_arribada_parelles = 0
        self.contador_arribada_receptor = 0
        self.contador_arribada_donant_cadaver = 0
        self.contador_mort_receptor = 0
        self.nous_cicles = {}
        self.arestes = {}
        self.trasplantaments_realitzats = {}
        self.receptors_rebutjats = {}
        self.cadenes = {}
        self.actualitzar_temps_edat()

    def actualitzar_temps_edat(self):
        """
        Actualitza els temps d'edat per a les parelles i receptors en llista d'espera.
        """
        for parella in self.llista_espera_vius.parelles.values():
            parella.actualitzar_temps_edat()

        for receptor in self.llista_espera_cadaver.llista_receptors:
            receptor.actualitzar_temps_edat()

    def main(self):
        """
        Funció principal que executa la simulació. A més, demana els inputs a l'usuari, defineix les taxes i imprimeix les estadístiques.
        """
        # INPUTS DE L'USUARI
        mesos_simulacio = int(input("Temps de simulació (mesos): "))
        # Convertir mesos a hores (suposant que cada "tic" és una hora)
        TEMPS_TOTAL_SIMULACIO = mesos_simulacio * 30 * 24

        print("--VARIABLES QUE PODEM MODIFICAR--")
        opcio_simulacio = input("Arribada de donant cadaver al pool viu (si/no): ")
        self.PUNTUACIO_CICLE_INTERN_2 = int(input("Puntuació intern de 2: "))
        self.PUNTUACIO_CICLE_INTERN_3 = int(input("Puntuació intern de 3: "))
        self.PUNTUACIO_MESOS_DIALISI = float(input("Puntuació mesos diàlisi: "))

        # PRÈVIAMENT A LA SIMULACIÓ, CARREGAR DADES I INICIALITZAR LLISTES D'ESPERA.
        estadistica_acumulada = Estadistica()
        self.llista_espera_vius.reiniciar_pool()
        self.llista_espera_cadaver.reiniciar_pool()
        self.carregar_dades()
        self.inicialitzar_pool_viu()
        self.inicialitzar_pool_cadaver()

        # DEFINIR TAXES a través de distribucions de Poisson
        mida_pool_viu = len(self.llista_espera_vius.parelles)
        mida_pool_cadaver = len(self.llista_espera_cadaver.llista_receptors)

        TAXA_ARRIBADA_DONANT_CADAVER, TAXA_ARRIBADA_PARELLES, TAXA_ARRIBADA_RECEPTOR, TAXA_MORT = definir_taxes_poisson(
            mida_pool_viu, mida_pool_cadaver, TEMPS_TOTAL_SIMULACIO
        )

        # SIMULACIÓ amb instància de Simpy Environment
        env = simpy.Environment()
        env.process(self.taxa_arribada_don_cadaver(env, opcio_simulacio, TAXA_ARRIBADA_DONANT_CADAVER))
        env.process(self.taxa_arribada_parelles_pool_viu(env, TAXA_ARRIBADA_PARELLES))
        env.process(self.taxa_arribada_receptor_pool_cadaver(env, TAXA_ARRIBADA_RECEPTOR))
        env.process(self.taxa_mort_receptor(env, TAXA_MORT))

        # ESTADÍSTIQUES per cada mes
        for tic in range(TEMPS_TOTAL_SIMULACIO):
            env.run(until=tic + 1)

            if (tic + 1) % (30 * 24) == 0:
                mes = (tic + 1) // (30 * 24)

                self.realitzar_donacions_cadena()
                estadistica_mes = Estadistica(mes)
                estadistica_mes.actualitzar_estadistiques(
                    self.trasplantaments_realitzats,
                    self.receptors_rebutjats,
                    self.cadenes,
                    self.contador_arribada_parelles,
                    self.contador_arribada_receptor,
                    self.contador_arribada_donant_cadaver,
                    self.contador_mort_receptor,
                    self.llista_espera_cadaver,
                    self.llista_espera_vius,
                )
                print()  # Linea en blanc
                print("ESTADÍSTIQUES DEL MES ", mes)
                estadistica_mes.imprimir_estadistiques_mes()
                if mes % 3 == 0:
                    print(len(self.llista_espera_vius.parelles))
                    self.crear_cicles_hill_climbing()
                    estadistica_mes.actualitzar_estadistiques_cicles(self.solucio_final,
                                                                     self.trasplantaments_realitzats,
                                                                     self.receptors_rebutjats,
                                                                     self.llista_espera_cadaver,
                                                                     self.llista_espera_vius)
                    estadistica_mes.imprimir_estadistiques_cicles()

                estadistica_acumulada.acumular_estadistiques(estadistica_mes)
                if mes == mesos_simulacio:
                    break
                else:
                    self.actualitzar_contadors()

        print("Simulació completada.")
        estadistica_acumulada.imprimir_estadistiques_finals()
        self.imprimir_diccionari_rebutjos()


simulador = Simulador()
simulador.main()
