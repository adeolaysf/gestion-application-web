from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# ==========================================
# LOGIQUE MÉTIER (Le "Cerveau" de l'app)
# ==========================================
def calculer_top_produit(liste):
    """Calcule le produit le plus fréquent (exigé par le sujet)."""
    if not liste:
        return None
    return max(set(liste), key=liste.count)

# ==========================================
# GESTION DATABASE (SQLite)
# ==========================================
def initialiser_db():
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS produits (
                        id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS achats (
                        id_achat INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_produit INTEGER,
                        prix REAL,
                        date TEXT,
                        FOREIGN KEY(id_produit) REFERENCES produits(id_produit))''')
    conn.commit()
    conn.close()

def db_query(query, args=(), one=False):
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# ==========================================
# INTERFACE FRONT-END (Responsive Bootstrap)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>T.H.O.T - Gestion des Courses</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .header-card { background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%); color: white; border: none; }
        .stats-badge { font-size: 1.2rem; padding: 10px 20px; border-radius: 50px; }
        .card { border-radius: 15px; border: none; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        .btn-primary { border-radius: 10px; padding: 10px 20px; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                
                <div class="card header-card p-5 mb-4 text-center shadow-lg">
                    <h1 class="display-4 fw-bold">🛒 T.H.O.T</h1>
                    <p class="lead">Votre assistant de gestion de courses intelligent</p>
                    <div class="mt-4">
                        <span class="stats-badge bg-white text-dark shadow-sm">
                            ⭐ Produit Phare : <strong>{{ top if top else 'En attente...' }}</strong>
                        </span>
                    </div>
                </div>

                <div class="card p-4 mb-4 shadow-sm">
                    <h5 class="mb-3 text-secondary">Enregistrer un nouvel achat</h5>
                    <form action="/add" method="post" class="row g-3">
                        <div class="col-md-7">
                            <input type="text" name="nom" class="form-control form-control-lg" placeholder="Nom du produit" required>
                        </div>
                        <div class="col-md-3">
                            <div class="input-group input-group-lg">
                                <input type="number" step="0.01" name="prix" class="form-control" placeholder="Prix" required>
                                <span class="input-group-text">€</span>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <button type="submit" class="btn btn-primary btn-lg w-100">Ajouter</button>
                        </div>
                    </form>
                </div>

                <div class="card p-4 shadow-sm">
                    <h5 class="mb-3 text-secondary">Historique des dépenses</h5>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>Produit</th>
                                    <th>Prix</th>
                                    <th>Date d'achat</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for a in achats %}
                                <tr>
                                    <td><span class="fw-bold text-dark">{{ a[0] }}</span></td>
                                    <td><span class="badge bg-light text-success fs-6">{{ a[1] }} €</span></td>
                                    <td><small class="text-muted">{{ a[2] }}</small></td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                        {% if not achats %}
                        <div class="text-center py-4 text-muted small">Aucun achat enregistré pour le moment.</div>
                        {% endif %}
                    </div>
                </div>

            </div>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# ROUTES FLASK
# ==========================================
@app.route('/')
def index():
    # Récupération des données
    achats = db_query("""
        SELECT p.nom, a.prix, a.date 
        FROM achats a 
        JOIN produits p ON a.id_produit = p.id_produit
        ORDER BY a.id_achat DESC
    """)
    
    # Calcul du Top Produit
    noms_achats = [row[0] for row in achats]
    top = calculer_top_produit(noms_achats)
    
    return render_template_string(HTML_TEMPLATE, achats=achats, top=top)

@app.route('/add', methods=['POST'])
def add():
    nom = request.form['nom'].strip()
    prix = request.form['prix']
    
    if nom and prix:
        db_query("INSERT OR IGNORE INTO produits (nom) VALUES (?)", (nom,))
        id_p = db_query("SELECT id_produit FROM produits WHERE nom = ?", (nom,), one=True)[0]
        db_query("INSERT INTO achats (id_produit, prix, date) VALUES (?, ?, '2026-02-03')", (id_p, prix))
    
    return redirect('/')

if __name__ == '__main__':
    initialiser_db()
    app.run(debug=True, port=5000)