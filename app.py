from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de données
class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

# Template HTML intégré (Bootstrap 5)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>T.H.O.T - Gestion de Courses</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <h1 class="text-center mb-4">🛒 T.H.O.T - Gestionnaire de Courses</h1>
        
        <div class="card p-4 shadow-sm mb-4">
            <form action="/add" method="POST" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="nom" class="form-control" placeholder="Nom du produit" required>
                </div>
                <div class="col-md-4">
                    <input type="number" step="0.01" name="prix" class="form-control" placeholder="Prix (€)" required>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Ajouter</button>
                </div>
            </form>
        </div>

        <div class="card p-4 shadow-sm">
            <h3>Liste des courses</h3>
            <table class="table table-hover mt-3">
                <thead class="table-dark">
                    <tr>
                        <th>Produit</th>
                        <th>Prix</th>
                        <th class="text-end">Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in produits %}
                    <tr>
                        <td>{{ p.nom }}</td>
                        <td>{{ p.prix }} €</td>
                        <td class="text-end">
                            <a href="/delete/{{ p.id }}" class="btn btn-sm btn-danger">Supprimer</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="mt-4 p-3 bg-white border rounded d-flex justify-content-between align-items-center">
                <p class="mb-0"><strong>🌟 Analyse Statistique (Top Produit) :</strong> <span class="badge bg-success fs-6">{{ top_produit }}</span></p>
                <a href="/clear" class="btn btn-outline-secondary btn-sm" onclick="return confirm('Vider toute la liste ?')">Réinitialiser</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    produits = Produit.query.all()
    top_produit = "Aucun"
    if produits:
        noms = [p.nom for p in produits]
        top_produit = max(set(noms), key=noms.count)
    return render_template_string(HTML_TEMPLATE, produits=produits, top_produit=top_produit)

@app.route('/add', methods=['POST'])
def add():
    nom = request.form.get('nom')
    prix = request.form.get('prix')
    if nom and prix:
        nouveau_produit = Produit(nom=nom, prix=float(prix))
        db.session.add(nouveau_produit)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    produit = Produit.query.get_or_404(id)
    db.session.delete(produit)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    Produit.query.delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)