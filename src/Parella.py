class Parella:
    numParelles = 0

    def __init__(self, donant, receptor):
        """
        Inicialitza una instància de Parella amb un donant, un receptor i un identificador únic.

        :param donant: Objecte Donant associat a la parella.
        :param receptor: Objecte Receptor associat a la parella.

        """
        self.donant = donant
        self.receptor = receptor
        Parella.incre_num_parelles()
        self.ident = Parella.numParelles  # Assigna el valor de numParelles com a identificador

    def __str__(self):
        """
        Retorna una representació en format de cadena de text de l'objecte Parella.

        :return str: Una cadena que mostra l'identificador de la parella, el donant i el receptor.

        """
        return f"Parella {self.ident} - ({self.donant}, {self.receptor})"

    @classmethod
    def incre_num_parelles(cls):
        """
        Incrementa el nombre de parelles. Mètode de classe.

        """
        cls.numParelles += 1

    def actualitzar_temps_edat(self):
        """
        Actualitza el temps en diàlisi i l'edat del donant i el receptor per cada mes de simulació.

        """
        self.donant.edat += (1 / 12)  # Incrementa l'edat una dotzena, que és equivalent a un mes
        self.receptor.edat += (1 / 12)
        self.receptor.m_amb_dialisis += 1
