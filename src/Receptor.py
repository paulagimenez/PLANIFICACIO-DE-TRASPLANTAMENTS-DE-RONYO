from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import pandas as pd

CONSTANT_A = 4
CONSTANT_B = 0.1


class Receptor:
    def __init__(self, id_rec, don_asoc, data_naixement, grup_sanguini, percentatge_anticossos, data_inici_dialisi,
                 m_sense_dialisi, sexe, id_hos, id_ccaa, hla1, hla2, hlb1, hlb2, hlcw1, hlcw2, hldq1, hldq2,
                 hldr1, hldr2, anticossos_prohibits):
        """
        Inicialitza un objecte Receptor amb els atributs proporcionats.

        :param id_rec: Identificació única del receptor.
        :param don_asoc: Donant associat al receptor.
        :param data_naixement: Data de naixement del receptor (format datetime.date).
        :param grup_sanguini: Grup sanguini del receptor.
        :param percentatge_anticossos: Percentatge d'anticossos del receptor.
        :param data_inici_dialisi: Data d'inici de la diàlisi (format datetime.datetime).
        :param m_sense_dialisi: Mesos sense diàlisi (pot ser NaN).
        :param sexe: Sexe del receptor.
        :param id_hos: Identificació de l'hospital associat al receptor.
        :param id_ccaa: Identificació de la comunitat autònoma associada al receptor.
        :param hla1, hla2, hlb1, hlb2, hlcw1, hlcw2, hldq1, hldq2, hldr1, hldr2: Informació genètica relacionada amb el sistema HLA del receptor.
        :param anticossos_prohibits: Anticossos prohibitius pel receptor.
        """
        self.data_naixement = data_naixement
        self.edat = self.calcular_edat()
        self.don_asoc = don_asoc
        self.id_rec = int(id_rec)
        self.grup_sanguini = str(grup_sanguini)
        self.percentatge_anticossos = percentatge_anticossos
        self.data_inici_dialisi = data_inici_dialisi
        self.m_sense_dialisi = m_sense_dialisi
        self.m_amb_dialisi = self.calcular_meses_con_dialisis()
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
        self.anticossos_prohibits = anticossos_prohibits
        self.probabilitat_fallada = 0
        self.n_rebutjos = 0
        self.probabilitat_dos_pools = False

    def __str__(self):
        """
        Retorna una representació en format de cadena de text de l'objecte Receptor.

        :return str: Una cadena que mostra l'ID del receptor.
        """
        return f"Receptor ID:{self.id_rec} - {self.n_rebutjos} rebutjos)"

    def calcular_meses_con_dialisis(self):
        """
        Calcula la quantitat de mesos en diàlisi pel receptor.

        :return int: El nombre de mesos que el receptor ha estat en diàlisi.
        """
        # Els valors buits de l'Excel els establim a 0
        if math.isnan(self.m_sense_dialisi):
            mesos_sense_dialisis = 0
        else:
            mesos_sense_dialisis = self.m_sense_dialisi

        if pd.isnull(self.data_inici_dialisi):
            mesos_amb_dialisi = 0
        else:
            # Definim la data actual com l'1 de gener de 2016.
            data_actual = datetime(2016, 1, 1).date()
            data_dialisi = self.data_inici_dialisi.date()
            # Calcular la diferència entre les dues dates en anys, mesos i dies
            diferencia = relativedelta(data_actual, data_dialisi)

            mesos_amb_dialisi = diferencia.years * 12 + diferencia.months - mesos_sense_dialisis
            if mesos_amb_dialisi < 0:  # Casos en què tingués molts mesos sense diàlisi per algun motiu llavors
                # mesos_amb_dialisi sería negatiu.
                mesos_amb_dialisi = 0

        return mesos_amb_dialisi

    def calcular_edat(self):
        """
        Calcula l'edat actual del receptor.

        :return int: L'edat del receptor en decimals.
        """
        # Definim la data actual com 1 de gener de 2016.
        data_actual = datetime(2016, 1, 1).date()

        diferencia = relativedelta(data_actual, self.data_naixement)

        # Calcular l'edat en decimals
        edat_decimal = diferencia.years + diferencia.months / 12.0 + diferencia.days / 365.0

        return edat_decimal

    def calcular_probabilitat_fallada(self):
        """
        Calcula la probabilitat de fallada del receptor segons el percentatge d'anticossos i les constants definides.
        """
        self.probabilitat_fallada = CONSTANT_B + (self.percentatge_anticossos / (100 * CONSTANT_A))

    def actualitzar_temps_edat(self):
        """
        Actualitza el temps en diàlisi i l'edat del receptor per cada mes de simulació.

        """
        self.edat += (1 / 12)  # Incrementa l'edat una dotzena, que és equivalent a un mes
        self.m_amb_dialisi += 1
