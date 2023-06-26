# Importer les modules Flask
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms import FloatField
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import pandas as pd
import csv

# Créer une instance de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Clé secrète pour la protection CSRF

# Définir une classe de formulaire
class MyForm(FlaskForm):
    utilisation = SelectField('utilisation', validators=[DataRequired()], choices=[])
    taille = FloatField('taille', validators=[DataRequired(), NumberRange(min=1, max=50000000)])
    utilise_gaz = SelectField('utilise_gaz', choices=[('Oui', 'Oui'), ('Non', 'Non')], validators=[DataRequired()])
    utilise_vapeur = SelectField('utilise_vapeur', choices=[('Oui', 'Oui'), ('Non', 'Non')], validators=[DataRequired()])
    nombre_batiments = FloatField('nombre_batiments', validators=[DataRequired(), NumberRange(min=1, max=200)])
    nombre_etages = FloatField('nombre_etages', validators=[DataRequired(), NumberRange(min=1, max=200)])
    submit = SubmitField('Submit')

# Définir une route pour l'URL racine '/'
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# Définir une route pour le formulaire
@app.route('/form', methods=['GET', 'POST'])
def form_page():
    form = MyForm()

    # Lire le fichier CSV et extraire les valeurs uniques de la colonne souhaitée
    with open('../dataset_prepared2.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        valeurs_colonne = set(row['primarypropertytype'] for row in reader)

    # Mettre à jour les choix de la select box avec les valeurs extraites
    form.utilisation.choices = [(val, val) for val in valeurs_colonne]

    if form.validate_on_submit():
        utilisation = form.utilisation.data
        taille = form.taille.data
        utilise_gaz = form.utilise_gaz.data
        utilise_vapeur = form.utilise_vapeur.data
        nombre_batiments = form.nombre_batiments.data
        nombre_etages = form.nombre_etages.data

        # Traitez les données du formulaire comme vous le souhaitez

        return "Formulaire soumis avec succès !"

    return render_template('form.html', form=form)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
class CSVForm(FlaskForm):
    csv_file = StringField('CSV File')
    submit = SubmitField('Charger')

# Route pour la page de chargement du CSV
@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    form = CSVForm()  # Créer une instance du formulaire
    if form.validate_on_submit():
        # Traiter le chargement du fichier CSV
        csv_file = form.csv_file.data
        
        # Lire le contenu du fichier CSV en tant que DataFrame
        df = pd.read_csv(csv_file)
        
        # Passer le DataFrame au modèle pour l'affichage
        return render_template('csv_display.html', csv_data=df.to_html(index=False))
    
    return render_template('csv.html', form=form)

# Point d'entrée de l'application
if __name__ == '__main__':
    # Lancer l'application Flask
    app.run(host='0.0.0.0')
