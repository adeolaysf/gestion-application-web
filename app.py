from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

# L'interface HTML complète avec les boutons visibles
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>T.H.O.T - Gestionnaire</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <h1 class="text-center mb-4">🛒 T.H.O.T - Liste de Courses</h1>
        
        <div class="card p-4 shadow-sm mb-4">
            <form action="/add" method="POST" class="row g-3">
                <div class="col-md-6"><input type="text" name="nom" class="form-control" placeholder="Produit" required></div>
                <div class="col-md-4"><input type="number" step="0.01" name="prix" class="form-control" placeholder="Prix (€)" required></div>
                <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Ajouter</button></div>
            </form>
        </div>

        <div class="card p-4 shadow-sm">
            <table class="table align-middle">
                <thead><tr><th>Produit</th><th>Prix</th><th class="text-end">Action</th></tr></thead>
                <tbody>
                    {% for p in produits %}
                    <tr>
                        <td>{{ p.nom }}</td>
                        <td>{{ p.prix }} €</td>
                        <td class="text-end">
                            <a href="/delete/{{ p.id }}" class="btn btn-danger btn-sm">Supprimer</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="mt-4 p-3 bg-white border rounded d-flex justify-content-between align-items-center">
                <span><strong>🌟 Top Produit :</strong> <span class="badge bg-success">{{ top_produit }}</span></span>
                <a href="/clear" class="btn btn-outline-secondary btn-sm" onclick="return confirm('Tout effacer ?')">Vider la liste</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    produits = Produit.query.all()
    noms = [p.nom for p in produits]
    top_produit = max(set(noms), key=noms.count) if noms else "Aucun"
    return render_template_string(HTML_TEMPLATE, produits=produits, top_produit=top_produit)

@app.route('/add', methods=['POST'])
def add():
    nom, prix = request.form.get('nom'), request.form.get('prix')
    if nom and prix:
        db.session.add(Produit(nom=nom, prix=float(prix)))
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    p = Produit.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    Produit.query.delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))