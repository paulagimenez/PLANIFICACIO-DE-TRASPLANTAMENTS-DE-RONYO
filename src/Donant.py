from datetime import datetime
from dateutil.relativedelta import relativedelta


class Donant:
    def __init__(self, id_don, data_naixement, grup_sanguini, sexe, id_hos, id_ccaa, hla1, hla2, hlb1, hlb2, hlcw1,
                 hlcw2, hldq1, hldq2, hldr1, hldr2):
        """
        Inicialitza un objecte Donant amb els atributs proporcionats.

        :param id_don: Identificació única del donant.
        :param data_naixement: Data de naixement del donant (format datetime.date).
        :param grup_sanguini: Grup sanguini del donant.
        :param sexe: Sexe del donant.
        :param id_hos: Identificació de l'hospital associat al donant.
        :param id_ccaa: Identificació de la comunitat autònoma associada al donant.
        :param hla1, hla2, hlb1, hlb2, hlcw1, hlcw2, hldq1, hldq2, hldr1, hldr2: Informació genètica relacionada amb el sistema HLA del donant.
        """
        self.id_don = int(id_don)
        self.data_naixement = data_naixement
        self.grup_sanguini = str(grup_sanguini)
        self.sexe = sexe
        self.id_hos = id_hos
        self.id_ccaa = id_ccaa
        self.hla1 = str(hla1)
        self.hla2 = str(hla2)
        self.hlb1 = str(hlb1)
        self.hlb2 = str(hlb2)
        self.hlcw1 = str(hlcw1)
        self.hlcw2 = str(hlcw2)
        self.hldq1 = str(hldq1)
        self.hldq2 = str(hldq2)
        self.hldr1 = str(hldr1)
        self.hldr2 = str(hldr2)
        self.rec_asoc = None
        self.edat = self.calcular_edat()

    def __str__(self):
        """
        Retorna una representació en format de cadena de text de l'objecte Donant.

        :return str: Una cadena que mostra l'ID del donant.
        """
        return f"Donant ID:{self.id_don} "

    def calcular_edat(self):
        """
        Calcula l'edat actual del receptor.

        :return float: L'edat del receptor en anys.
        """
        # Definim la data actual com 1 de gener de 2016.
        data_actual = datetime(2016, 1, 1).date()

        diferencia = relativedelta(data_actual, self.data_naixement)

        # Calcular l'edat amb decimals
        edat_decimal = diferencia.years + diferencia.months / 12.0 + diferencia.days / 365.0

        return edat_decimal
