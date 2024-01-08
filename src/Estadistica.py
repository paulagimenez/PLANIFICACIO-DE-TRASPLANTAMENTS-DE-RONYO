class Estadistica:
    def __init__(self, mes=None):
        """
        Crea una instància de la classe Estadistica.

        :param mes: Mes associat a les estadístiques.
        """
        self.mes = mes
        self.num_trasplants_pool_viu = 0
        self.num_trasplants_pool_cadaver = 0
        self.num_trasplants_creuaments = 0
        self.num_trasplants_cadena = 0
        self.num_rebutjos_pool_viu = 0
        self.num_rebutjos_pool_cadaver = 0
        self.diccionari_cadenes = {}
        self.diccionari_trasplants = {}
        self.diccionari_rebutjos = {}
        self.contador_arribada_parelles = 0
        self.contador_arribada_receptor = 0
        self.contador_arribada_donant_cadaver = 0
        self.contador_mort_receptor = 0
        self.num_parelles_pool_viu = 0
        self.num_receptors_pool_cadaver = 0
        self.num_cicles_hill_climbing = 0
        self.num_cicles_mida_2 = 0
        self.num_cicles_mida_3 = 0
        self.ite_hill_climbing = 0
        self.maxim_rebuig = 0

    def imprimir_estadistiques_mes(self):
        """
        Imprimeix les estadístiques del mes actual.
        """
        resultado = f"\nNumero de total trasplantaments realitzats: {self.num_trasplants_pool_viu + self.num_trasplants_pool_cadaver}" \
                    f"\n - Numero de trasplantaments pool viu: {self.num_trasplants_pool_viu}" \
                    f"\n       - Numero de trasplantaments cadena: {self.num_trasplants_cadena} " \
                    f"\n - Numero de trasplantaments pool cadàver: {self.num_trasplants_pool_cadaver}" \
                    f"\nNumero de pacients difunts: {self.contador_mort_receptor} " \
                    f"\nNumero de rebutjos: {self.num_rebutjos_pool_viu + self.num_rebutjos_pool_cadaver} " \
                    f"\nNumero parelles pool viu: {self.num_parelles_pool_viu}  " \
                    f"\nNumero receptors pool cadàver: {self.num_receptors_pool_cadaver} " \
                    f"\nArribades: " \
                    f"\n - Numero arribades parelles pool viu: {self.contador_arribada_parelles} " \
                    f"\n - Numero arribades receptors pool cadàver: {self.contador_arribada_receptor} " \
                    f"\n - Numero arribades donant cadàver: {self.contador_arribada_donant_cadaver} "

        print(resultado)

    def imprimir_estadistiques_cicles(self):
        """
        Imprimeix les estadístiques dels cicles.
        """
        resultado = f"\nESTADISTIQUES CREUAMENTS" \
                    f"\nNumero de cicles solucio final: {self.num_cicles_hill_climbing} " \
                    f"\n - Numero de cicles de mida 2: {self.num_cicles_mida_2}" \
                    f"\n - Numero de cicles de mida 3: {self.num_cicles_mida_3}" \
                    f"\nNumero iteracions Hill Climbing: {self.ite_hill_climbing} " \
                    f"\nNumero de trasplantaments realitzats als cicles: {self.num_trasplants_creuaments}"
        print(resultado)

    def imprimir_estadistiques_finals(self):
        """
        Imprimeix les estadístiques finals.
        """
        mesos_dialisis = [valor[1] for valor in self.diccionari_trasplants.values() if valor]
        mitjana_mesos_dialisis = sum(mesos_dialisis) / len(mesos_dialisis)

        self.maxim_rebuig = max((valor[1] for valor in self.diccionari_rebutjos.values()), default=0)

        resultado = f"\nESTADISTIQUES FINALS" \
                    f"\nNumero de total trasplantaments realitzats: {self.num_trasplants_pool_viu + self.num_trasplants_pool_cadaver + self.num_trasplants_creuaments}" \
                    f"\n - Numero de trasplantaments pool viu: {self.num_trasplants_pool_viu + self.num_trasplants_creuaments}" \
                    f"\n       - Numero de trasplantaments creuament: {self.num_trasplants_creuaments} en un total de {self.num_cicles_hill_climbing} cicles" \
                    f"\n       - Numero de trasplantaments cadena: {self.num_trasplants_cadena}" \
                    f"\n - Numero de trasplantaments pool cadàver: {self.num_trasplants_pool_cadaver}" \
                    f"\nNumero de pacients difunts: {self.contador_mort_receptor} " \
                    f"\nNumero de rebutjos: {self.num_rebutjos_pool_viu + self.num_rebutjos_pool_cadaver} " \
                    f"\n       - Numero de rebutjos pool viu: {self.num_rebutjos_pool_viu}" \
                    f"\n       - Numero de rebutjos pool cadàver: {self.num_rebutjos_pool_cadaver}" \
                    f"\nMàxim rebutjos en un pacient: {self.maxim_rebuig} , mida diccion: {len(self.diccionari_rebutjos)}" \
                    f"\nMitjana mesos diàlisis dels pacients trasplantats: {mitjana_mesos_dialisis} , en anys: {mitjana_mesos_dialisis / 12}" \
                    f"\n" \
                    f"\nINFORMACIÓ EXTRA DE LES LLISTES D'ESPERA: " \
                    f"\nArribades: " \
                    f"\n - Numero arribades parelles pool viu: {self.contador_arribada_parelles} " \
                    f"\n - Numero arribades receptors pool cadàver: {self.contador_arribada_receptor} " \
                    f"\n - Numero arribades donant cadàver: {self.contador_arribada_donant_cadaver} " \
                    f"\nNumero parelles pool viu: {self.num_parelles_pool_viu}  " \
                    f"\nNumero receptors pool cadàver: {self.num_receptors_pool_cadaver} "

        print(resultado)

    def actualitzar_estadistiques(self, dic_trasplants_realitzats, dic_rebutjos, dic_cadenes,
                                  arribada_parelles, arribada_receptors, arribada_cadaver, morts, pool_cadaver,
                                  pool_viu):
        """
        Actualitza les estadístiques amb les dades proporcionades.

        :param dic_trasplants_realitzats: Diccionari amb els trasplants realitzats.
        :param dic_rebutjos: Diccionari amb els rebutjos.
        :param dic_cadenes: Diccionari amb les cadenes.
        :param arribada_parelles: Número d'arribades de parelles de pool viu.
        :param arribada_receptors: Número d'arribades de receptors de pool cadàver.
        :param arribada_cadaver: Número d'arribades de donants cadàver.
        :param morts: Número de receptors difunts.
        :param pool_cadaver: Pool de cadàver.
        :param pool_viu: Pool de viu.
        """
        self.num_trasplants_pool_viu = sum(1 for valor in dic_trasplants_realitzats.values() if valor[0] == 'v' or valor[0] == 'cadena')
        self.num_trasplants_pool_cadaver = sum(1 for valor in dic_trasplants_realitzats.values() if valor[0] == 'c')
        self.num_trasplants_cadena = sum(1 for valor in dic_trasplants_realitzats.values() if valor[0] == 'cadena')
        self.num_rebutjos_pool_viu = sum(1 for valor in dic_rebutjos.values() if valor[0] == 'v')
        self.num_rebutjos_pool_cadaver = sum(1 for valor in dic_rebutjos.values() if valor[0] == 'c')
        self.diccionari_cadenes = dic_cadenes
        self.contador_arribada_parelles = arribada_parelles
        self.contador_arribada_receptor = arribada_receptors
        self.contador_arribada_donant_cadaver = arribada_cadaver
        self.contador_mort_receptor = morts
        self.num_receptors_pool_cadaver = len(pool_cadaver.llista_receptors)
        self.num_parelles_pool_viu = len(pool_viu.parelles)
        self.diccionari_trasplants = dic_trasplants_realitzats
        self.diccionari_rebutjos = dic_rebutjos

    def actualitzar_estadistiques_cicles(self, solucio, dic_trasplants_realitzats, dic_rebutjos, pool_cadaver,
                                         pool_viu):
        """
        Actualitza les estadístiques dels cicles amb les dades proporcionades.

        :param solucio: Solució dels cicles.
        :param dic_trasplants_realitzats: Diccionari amb els trasplants realitzats.
        :param dic_rebutjos: Diccionari amb els rebutjos.
        :param pool_cadaver: Pool de cadàver.
        :param pool_viu: Pool de viu.
        """
        print("Disponible una solució final")
        self.num_cicles_hill_climbing = len(solucio.conjunt_cicles)
        self.num_cicles_mida_2 = solucio.cicles_2
        self.num_cicles_mida_3 = solucio.cicles_3
        self.ite_hill_climbing = solucio.iteracions
        self.num_trasplants_creuaments = sum(1 for valor in dic_trasplants_realitzats.values() if valor[0] == 'cicle')
        self.num_rebutjos_pool_viu = sum(1 for valor in dic_rebutjos.values() if valor[0] == 'v')
        self.num_receptors_pool_cadaver = len(pool_cadaver.llista_receptors)
        self.num_parelles_pool_viu = len(pool_viu.parelles)
        self.diccionari_trasplants = dic_trasplants_realitzats
        self.diccionari_rebutjos = dic_rebutjos

    def acumular_estadistiques(self, otra_estadistica):
        """
        Acumula les estadístiques amb les dades d'una altra instància d'Estadistica.

        :param otra_estadistica: Una altra instància d'Estadística.
        """
        self.num_trasplants_pool_viu += otra_estadistica.num_trasplants_pool_viu
        self.num_trasplants_pool_cadaver += otra_estadistica.num_trasplants_pool_cadaver
        self.num_trasplants_creuaments += otra_estadistica.num_trasplants_creuaments
        self.num_trasplants_cadena += otra_estadistica.num_trasplants_cadena
        self.num_rebutjos_pool_viu += otra_estadistica.num_rebutjos_pool_viu
        self.num_rebutjos_pool_cadaver += otra_estadistica.num_rebutjos_pool_cadaver
        self.contador_arribada_parelles += otra_estadistica.contador_arribada_parelles
        self.contador_arribada_receptor += otra_estadistica.contador_arribada_receptor
        self.contador_arribada_donant_cadaver += otra_estadistica.contador_arribada_donant_cadaver
        self.contador_mort_receptor += otra_estadistica.contador_mort_receptor
        self.num_parelles_pool_viu = otra_estadistica.num_parelles_pool_viu
        self.num_receptors_pool_cadaver = otra_estadistica.num_receptors_pool_cadaver
        self.diccionari_rebutjos.update(otra_estadistica.diccionari_rebutjos)
        self.diccionari_trasplants.update(otra_estadistica.diccionari_trasplants)
        self.num_cicles_hill_climbing += otra_estadistica.num_cicles_hill_climbing
