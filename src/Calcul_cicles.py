import Calcul_compatibilitat
import networkx as nx
from Aresta import Aresta


def crear_nodes_edges(llista_espera, diccionari_arestes, punt_mesos):
    """
    Crea els nodes i les arestes del graf basat en la compatibilitat de les parelles.

    :param llista_espera: Llista d'espera amb les parelles.
    :param diccionari_arestes: Diccionari on es guardaran les arestes del graf.
    :param punt_mesos: Puntuació assignada als mesos de diàlisi.
    :return: Llista de cicles del graf.
    """
    G = nx.DiGraph()

    # Afegir nodes (parelles) al graf
    for parella in llista_espera.parelles.values():
        G.add_node(parella)

    # Afegir arestes (compatibilitats) al graf
    parelles_list = list(llista_espera.parelles.values())
    for i, parella1 in enumerate(parelles_list):
        for j in range(i + 1, len(parelles_list)):
            parella2 = parelles_list[j]
            if Calcul_compatibilitat.es_compatible(parella1.donant, parella2.receptor):
                G.add_edge(parella1, parella2)
                aresta = Aresta(parella1, parella2)
                diccionari_arestes[aresta.ident] = aresta

            if Calcul_compatibilitat.es_compatible(parella2.donant, parella1.receptor):
                G.add_edge(parella2, parella1)
                aresta = Aresta(parella2, parella1)
                aresta.calcular_puntuacio_aresta(punt_mesos)
                diccionari_arestes[aresta.ident] = aresta

    numero_de_nodos = G.number_of_nodes()
    print("Quantitat de nodes:", numero_de_nodos)
    numero_de_arestes = G.number_of_edges()
    print("Quantitat d'arestes:", numero_de_arestes)
    llista_cicles = list(nx.simple_cycles(G, length_bound=3))
    print("Quantitat de cicles: ", len(llista_cicles))

    len2, len3 = 0, 0
    for item in llista_cicles:
        if len(item) == 2:
            len2 += 1
        elif len(item) == 3:
            len3 += 1
    print("Quantitat de cicles mida 2: ", len2)
    print("Quantitat de cicles mida 3: ", len3)

    return llista_cicles
