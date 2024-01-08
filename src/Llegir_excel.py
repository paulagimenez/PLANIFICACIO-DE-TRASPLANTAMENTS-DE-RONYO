import pandas as pd
from Donant import Donant
from Receptor import Receptor


def obtenir_anticossos_prohibits(id_rec, df_anticossos):
    """
    Obté una llista d'anticossos prohibits per a un receptor segons el fitxer proporcionat d'anticossos.

    :param id_rec: Identificació única del receptor.
    :param df_anticossos: DataFrame que conté les dades dels anticossos prohibits.

    :return: Llista amb els anticossos prohibits per al receptor donat.
    """
    dades_receptor = df_anticossos[df_anticossos["IDREC"] == id_rec]
    anticossos_prohibits = [dades_receptor["Valor"].tolist(), dades_receptor["Classe"].tolist()]
    return anticossos_prohibits


def crear_donats_receptors(ruta_arxiu_donants, ruta_arxiu_receptors, ruta_arxiu_anticossos):
    """
    Crea llistes de donants i receptors a partir d'arxius Excel específics.

    :param ruta_arxiu_donants: Ruta de l'arxiu Excel amb les dades dels donants.
    :param ruta_arxiu_receptors: Ruta de l'arxiu Excel amb les dades dels receptors.
    :param ruta_arxiu_anticossos: Ruta de l'arxiu Excel amb les dades dels anticossos.

    :return: Llistes de donants i receptors.
    """
    dtype_dict = {
        'HLA1': str, 'HLA2': str, 'HLB1': str, 'HLB2': str, 'HLCW1': str, 'HLCW2': str, 'HLDQ1': str,
        'HLDQ2': str, 'HLDR1': str, 'HLDR2': str, 'GS': str
    }

    df_donants = pd.read_excel(ruta_arxiu_donants, header=0, dtype=dtype_dict)
    df_receptors = pd.read_excel(ruta_arxiu_receptors, header=0, dtype=dtype_dict)
    df_anticossos = pd.read_excel(ruta_arxiu_anticossos)

    donants = []  # Creació llista donants
    receptors = []  # Creació llista receptors

    for _, row in df_donants.iterrows():
        donant = Donant(row['IDDON'], row['FECNAC'], row['GS'], row['SEXO'], row['IDHOS'], row['ID CCAA'], row['HLA1'],
                        row['HLA2'], row['HLB1'], row['HLB2'], row['HLCW1'], row['HLCW2'], row['HLDQ1'],
                        row['HLDQ2'], row['HLDR1'], row['HLDR2'])
        donants.append(donant)

    for _, row in df_receptors.iterrows():
        idrec = row['IDREC']
        anticossos_prohibits = obtenir_anticossos_prohibits(idrec, df_anticossos)

        receptor = Receptor(idrec, row['DON ASOC'], row['FECNAC'], row['GS'], row['%PRA'], row['FIDIALISIS'],
                            row['MSINDIALISIS'], row['SEXO'], row['IDHOS'], row['IDCCAA'], row['HLA1'], row['HLA2'],
                            row['HLB1'], row['HLB2'], row['HLCW1'], row['HLCW2'], row['HLDQ1'],
                            row['HLDQ2'], row['HLDR1'], row['HLDR2'], anticossos_prohibits)

        receptor.calcular_probabilitat_fallada()
        receptors.append(receptor)

    return donants, receptors


def vincular_receptor_a_donant(donants, receptors):
    """
    Vincula receptors amb els seus donants associats.

    :param donants: Llista de donants.
    :param receptors: Llista de receptors.
    """
    for donant in donants:
        for receptor in receptors:
            if receptor.don_asoc == donant.id_don:
                donant.rec_asoc = receptor
                receptor.don_asoc = donant
                break
