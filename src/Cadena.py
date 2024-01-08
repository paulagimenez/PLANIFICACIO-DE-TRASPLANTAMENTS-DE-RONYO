class Cadena:
    numCadenes = 0

    def __init__(self):
        """
        Inicialitza una instància de Cadena amb una llista buida de donacions i un identificador únic.

        """
        self.donacions = []
        Cadena.incre_num_cadenes()
        self.ident = Cadena.numCadenes

    def __str__(self):
        """
        Retorna una representació en format de cadena de text de l'objecte Cadena.

        :return str: Una cadena que mostra la cadena de donacions amb els detalls de cada pas.

        """
        cadena_str = "Cadena de donació:\n"
        for i, (donant, receptor) in enumerate(self.donacions):
            cadena_str += f"Pas {i + 1}: Donant {donant.id_don} dona al receptor {receptor.id_rec}\n"
        return cadena_str

    @classmethod
    def incre_num_cadenes(cls):
        """
        Incrementa el nombre de cadenes cada vegada que es crea una nova cadena.

        """
        cls.numCadenes += 1

    def afegir_donacio(self, donant, receptor):
        """
        Afegeix una donació a la cadena amb un donant i un receptor.

        :param donant: El donant que participa en la donació.
        :param receptor: El receptor que rep la donació.

        """
        self.donacions.append((donant, receptor))
