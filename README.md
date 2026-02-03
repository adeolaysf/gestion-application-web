# 🛒 T.H.O.T - Gestionnaire de Courses Intelligent

Ce projet est une application web de gestion de courses développée dans le cadre du module de **Génie Logiciel**. Elle permet d'enregistrer des achats, de suivre les dépenses et d'identifier statistiquement le produit le plus acheté.

## 🚀 Fonctionnalités
- **Ajout d'achats** : Enregistrement du nom du produit et de son prix.
- **Base de données** : Stockage persistant avec SQLite.
- **Statistiques** : Calcul automatique du "Top Produit" via un algorithme dédié.
- **Interface Responsive** : Design moderne avec Bootstrap 5 (adapté mobile/PC).

## 🛠️ Stack Technique
- **Backend** : Python / Flask
- **Frontend** : HTML5 / CSS3 (Bootstrap 5)
- **Base de données** : SQLite3
- **Tests & Qualité** : Pytest & Pytest-Cov (Couverture de code)

## 🧪 Tests et Qualité
Pour vérifier la logique métier, nous utilisons `pytest`.
Lancer les tests avec mesure de couverture :
```bash
pytest --cov=app test_unitaire.py