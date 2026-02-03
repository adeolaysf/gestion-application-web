import unittest
# On importe la fonction de calcul depuis ton fichier app.py
from app import calculer_top_produit

class TestCourses(unittest.TestCase):
    def test_logique_top_produit(self):
        # Scénario de test : Pomme apparaît 2 fois, Poire 1 fois
        donnees_test = ["Pomme", "Poire", "Pomme"]
        resultat = calculer_top_produit(donnees_test)
        
        # Le test vérifie si le résultat est bien "Pomme"
        self.assertEqual(resultat, "Pomme")

    def test_liste_vide(self):
        # Vérifie que si la liste est vide, on obtient None
        self.assertIsNone(calculer_top_produit([]))

if __name__ == '__main__':
    unittest.main()