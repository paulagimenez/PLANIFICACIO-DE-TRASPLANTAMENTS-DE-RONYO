from Solucio import Solucio


def hill_climbing(solucio_actual, cicles_lliures):
    """
    Aplica l'algorisme Hill Climbing per buscar una solució òptima.

    :param solucio_actual: La solució inicial a partir de la qual començarà l'algorisme.
    :param cicles_lliures: Diccionari que conté els cicles lliures disponibles.
    :return: La solució millorada després de l'aplicació de l'algorisme Hill Climbing.
    """
    while True:
        millora = False
        sortint = None
        millor_opcio = Solucio()  # Millor combinació de cicles entrants (best_neighbor)

        for cicle in solucio_actual.conjunt_cicles:
            if len(cicle.llista_parelles) > 2:
                entrants = millor_canvi(cicle, solucio_actual, cicles_lliures)

                if entrants.puntuacio_total > millor_opcio.puntuacio_total:
                    millor_opcio = entrants
                    sortint = cicle

        if not millor_opcio.es_buida():
            millora = True
            solucio_actual.iteracions += 1
            solucio_actual.afegir_solucio(millor_opcio)
            solucio_actual.eliminar(sortint)
            solucio_actual.conjunt_cicles.sort(key=lambda c: c.puntuacio_cicle, reverse=True)
            eliminar_del_diccionari(cicles_lliures, millor_opcio)

        if not millora:
            return solucio_actual


def millor_canvi(sortint, solucio_actual, cicles_lliures):
    """
    Busca la millor combinació de cicles entrants donat un cicle de sortida.

    :param sortint: Cicle que es considera de sortida.
    :param solucio_actual: La solució actual en la qual es busca la millora.
    :param cicles_lliures: Diccionari que conté els cicles lliures disponibles.
    :return: La millor combinació de cicles entrants.
    """
    millor_combinacio = Solucio()
    llista_cicles_lliures = list(cicles_lliures.values())
    llista_cicles_lliures.sort(reverse=True, key=lambda x: x.puntuacio_cicle)
    # Crear una copia de la solució actual y eliminar sortint de la copia
    temp = Solucio()
    temp.conjunt_cicles = solucio_actual.conjunt_cicles.copy()
    temp.eliminar(sortint)  #

    for cicle_entrant in llista_cicles_lliures:
        if len(cicle_entrant.llista_parelles) <= len(sortint.llista_parelles):
            if cicle_entrant.parella_comu(cicle_entrant, sortint):
                if millor_combinacio.cicles_disjunts(cicle_entrant):
                    if temp.cicles_disjunts(cicle_entrant):
                        millor_combinacio.afegir_cicle(cicle_entrant)

    if millor_combinacio.puntuacio_total <= sortint.puntuacio_cicle:
        millor_combinacio.buidar()

    return millor_combinacio


def parella_comu(cicle1, cicle2):
    """
    Comprova si dos cicles tenen alguna parella en comú.

    :param cicle1: Primer cicle a comparar.
    :param cicle2: Segon cicle a comparar.
    :return: True si tenen alguna parella en comú, False si no en tenen.
    """
    return any(parella in cicle2.llista_parelles for parella in cicle1.llista_parelles)


def eliminar_del_diccionari(cicles_lliures, solucio):
    """
    Elimina els cicles d'una solució del diccionari de cicles lliures.

    :param cicles_lliures: Diccionari que conté els cicles lliures disponibles.
    :param solucio: Solució amb els cicles a eliminar del diccionari.
    """
    identificadors_conjunt = {cicle.ident for cicle in solucio.conjunt_cicles}
    for identificador in identificadors_conjunt:
        if identificador in cicles_lliures:
            del cicles_lliures[identificador]
