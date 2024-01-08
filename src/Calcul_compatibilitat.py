def compatibilitat_grup_sanguini(donant, receptor):
    """
    Verifica la compatibilitat de grup sanguini entre el donant i el receptor.

    :param donant: Objecte Donant amb informació sobre el donant.
    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :return: Retorna True si els grups sanguinis són compatibles, False si no ho són.
    """
    ABO_COMPATIBLE = {
        '0': ['A', 'B', 'AB', '0'],
        'A': ['A', 'AB'],
        'B': ['B', 'AB'],
        'AB': ['AB']
    }

    gs_donant = donant.grup_sanguini
    gs_receptor = receptor.grup_sanguini

    if gs_donant not in ABO_COMPATIBLE or gs_receptor not in ABO_COMPATIBLE:
        raise ValueError("Grups sanguinis no vàlids. Els grups vàlids són: A, B, AB, 0")

    if gs_receptor in ABO_COMPATIBLE[gs_donant]:
        return True
    else:
        return False


def compatibilitat_HLA_anti_prohibits(donant, receptor):
    """
    Verifica la compatibilitat HLA entre el donant i el receptor, seran compatibles quan el donant no contingui els anticossos prohibits del receptor.

    :param donant: Objecte Donant amb informació sobre el donant.
    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :return: Retorna True si són compatibles, False si no ho són.
    """
    # Valors del donant
    valors_a = [donant.hla1, donant.hla2]
    valors_b = [donant.hlb1, donant.hlb2]
    valors_cw = [donant.hlcw1, donant.hlcw2]
    valors_dq = [donant.hldq1, donant.hldq2]
    valors_dr = [donant.hldr1, donant.hldr2]

    # Valors del receptor
    anticossos_receptor = receptor.anticossos_prohibits

    if not anticossos_receptor:
        return True
    else:
        valors_numerics = anticossos_receptor[0][0]
        tipus = anticossos_receptor[1][0]

        valors_per_tipus = {}
        for tipus, valor in zip(tipus, valors_numerics):
            if tipus not in valors_per_tipus:
                valors_per_tipus[tipus] = []
            valors_per_tipus[tipus].append(valor)

        # Comprovar compatibilitat per a cada tipus
        compatible = True
        compatible &= check_compatibilitat_HLA_prohibits(valors_a, valors_per_tipus.get('A', []))
        compatible &= check_compatibilitat_HLA_prohibits(valors_b, valors_per_tipus.get('B', []))
        compatible &= check_compatibilitat_HLA_prohibits(valors_cw, valors_per_tipus.get('CW', []))
        compatible &= check_compatibilitat_HLA_prohibits(valors_dq, valors_per_tipus.get('DQ', []))
        compatible &= check_compatibilitat_HLA_prohibits(valors_dr, valors_per_tipus.get('DR', []))

        return compatible


def check_compatibilitat_HLA_prohibits(valors_donant, valors_receptor):
    """
    Verifica la compatibilitat entre valors HLA d'un donant i un receptor.

    :param valors_donant: Llista dels valors HLA del donant.
    :param valors_receptor: Llista dels valors HLA del receptor.
    :return: Retorna True si són compatibles, False si no ho són.
    """
    for valor_receptor in valors_receptor:
        for valor_donant in valors_donant:
            if valor_donant.endswith('00'):  # Terminació 00 correspon a la representació general del antigen.
                donant_2_digits = valor_donant[:2]
                if valor_receptor.startswith(donant_2_digits):
                    return False
            elif valor_donant == valor_receptor:
                return False
    return True


def compatibilidad_HLA_similitud(donant, receptor):
    """
    Verifica la compatibilitat global HLA entre el donant i el receptor. Es considera compatible si almenys el 30% dels
    antígens HLA són similars.

    :param donant: Objecte Donant amb informació sobre el donant.
    :param receptor: Objecte Receptor amb informació sobre el receptor.
    :return: Retorna True si són compatibles, False si no ho són.
    """
    valors_donant = [
        donant.hla1, donant.hla2, donant.hlb1, donant.hlb2,
        donant.hlcw1, donant.hlcw2, donant.hldq1, donant.hldq2,
        donant.hldr1, donant.hldr2
    ]

    valors_receptor = [
        receptor.hla1, receptor.hla2, receptor.hlb1, receptor.hlb2,
        receptor.hlcw1, receptor.hlcw2, receptor.hldq1, receptor.hldq2,
        receptor.hldr1, receptor.hldr2
    ]

    # Comptador de similitud
    similituds = sum(check_similitud_HLA_similitud(valor_donant, valor_receptor) for valor_donant, valor_receptor in
                     zip(valors_donant, valors_receptor))

    # Calcular el percentatge de similitud
    percentatge_similitud = (similituds / len(valors_donant)) * 100

    # Verificar si el percentatge de similitud és almenys del 30%
    if percentatge_similitud >= 30:
        return True
    else:
        return False


def check_similitud_HLA_similitud(valor_donant, valor_receptor):
    """
    Verifica la similitud de dos valors d'antígens HLA.

    :param valor_donant: Valor HLA del donant.
    :param valor_receptor: Valor HLA del receptor.
    :return: Retorna True si són similars, False si no ho són.
    """
    if valor_donant.endswith('00'):
        donant_2_digits = valor_donant[:2]
        return valor_receptor.startswith(donant_2_digits)
    else:
        return valor_donant == valor_receptor


def es_compatible(donant, receptor):
    """
    Comprova si la donació és compatible tenint en compte el grup sanguini i la compatibilitat HLA segons els anticossos prohibits i la similitud d'anticossos.

    :param donant: Objecte Donant amb informació sobre el donant.
    :param receptor: Objecte Receptor amb informació sobre el receptor.
    """
    if compatibilitat_grup_sanguini(donant, receptor) and compatibilitat_HLA_anti_prohibits(donant, receptor) and compatibilidad_HLA_similitud(donant, receptor):
        return True
    else:
        return False
