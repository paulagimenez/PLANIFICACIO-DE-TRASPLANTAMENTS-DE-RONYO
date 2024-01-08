# Constants de puntuació
PUNTUACIO_GRUP_SANGUINI = 30
PUNTUACIO_COMUNITAT = 5
PUNTUACIO_PEDIATRIC = 30
PUNTUACIO_PRA_POC = 30
PUNTUACIO_PRA_MIG = 20
PUNTUACIO_PRA_ELEVAT = 10
PUNTUACIO_PRA_MOLT = 0
PUNTUACIO_EDAT_0_10 = 30


def calc_puntuacio_total(donant, receptor, puntuacio_mesos):
    """
    Calcula la puntuació total basada en les puntuacions individuals.

    :param donant: Objecte Donant amb informació sobre el donant.
    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :param puntuacio_mesos: Puntuació associada als mesos de diàlisi.
    :return: Retorna la puntuació total.
    """
    total_puntuacio = (
            puntuacio_grup_sanguini(donant, receptor) + puntuacio_comunitat_autonoma(donant, receptor) + puntuacio_pediatric(receptor)
            + puntuacio_pra(receptor) + puntuacio_edat(donant, receptor) + puntuacio_mesos_dialisi(receptor, puntuacio_mesos)
    )
    return total_puntuacio


# Puntuacions
def puntuacio_grup_sanguini(donant, receptor):
    """
    Calcula la puntuació basada en la coincidència del grup sanguini.

    :param donant: Objecte Donant amb informació sobre el donant.
    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :return: Retorna la puntuació pel grup sanguini.
    """
    if donant.grup_sanguini == receptor.grup_sanguini:
        return PUNTUACIO_GRUP_SANGUINI
    else:
        return 0


def puntuacio_comunitat_autonoma(donant, receptor):
    """
    Calcula la puntuació basada en la coincidència de la comunitat autònoma.

    :param donant: Objecte Donant amb informació sobre el donant.
    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :return: Retorna la puntuació per la coincidència de la comunitat autònoma.
    """
    if donant.id_ccaa == receptor.id_ccaa:
        return PUNTUACIO_COMUNITAT
    else:
        return 0


def puntuacio_pediatric(receptor):
    """
    Calcula la puntuació basada en si el receptor és un pacient pediàtric.

    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :return: Retorna la puntuació per ser pacient pediàtric.
    """
    if receptor.edat < 16:
        return PUNTUACIO_PEDIATRIC
    else:
        return 0


def puntuacio_pra(receptor):
    """
    Calcula la puntuació basada en el percentatge de PRA del receptor.

    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :return: Retorna la puntuació basada en el percentatge de PRA del receptor.
    """
    pra = receptor.percentatge_anticossos

    if 0 <= pra < 25:
        return PUNTUACIO_PRA_POC
    elif 25 <= pra < 50:
        return PUNTUACIO_PRA_MIG
    elif 50 <= pra < 75:
        return PUNTUACIO_PRA_ELEVAT
    elif 75 <= pra <= 100:
        return PUNTUACIO_PRA_MOLT


def puntuacio_edat(donant, receptor):
    """
    Calcula la puntuació basada en la diferència d'edat entre donant i receptor.

    :param donant: Objecte Donant amb informació sobre el donant.
    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :return: Retorna la puntuació basada en la diferència d'edat entre donant i receptor.
    """
    dif_edat = donant.edat - receptor.edat

    if 0 <= dif_edat <= 10:
        return PUNTUACIO_EDAT_0_10
    else:
        return 0


def puntuacio_mesos_dialisi(receptor, punt_mesos):
    """
    Calcula la puntuació segons el nombre de mesos que ha estat el receptor en diàlisi.

    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :param punt_mesos: Puntuació associada als mesos de diàlisi.
    :return: Retorna la puntuació basada en el nombre de mesos en diàlisi.
    """
    return receptor.m_amb_dialisis * punt_mesos
