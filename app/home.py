# Importer les modules Flask
from flask import Flask, render_template

# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir une route pour l'URL racine '/'
@app.route('/')
def home():
    # Rendre le template index.html
    return render_template('index.html')

# Point d'entrée de l'application
if __name__ == '__main__':
    # Lancer l'application Flask
    app.run()

