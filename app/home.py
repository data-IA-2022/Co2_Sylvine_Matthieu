# Importer les modules Flask
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms import FloatField
from flask import Flask, render_template
import pandas as pd
import csv
from fonctions_app import makePredictionCsv, makePredictionIndiv


# Créer une instance de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Clé secrète pour la protection CSRF

# Définir une classe de formulaire
class MyForm(FlaskForm):
    utilisation = SelectField('Utilisation Principale de votre Building', validators=[DataRequired()], choices=[])
    taille = FloatField('Taille', validators=[DataRequired(), NumberRange(min=1, max=50000000)])
    utilise_gaz = SelectField('Utilisation du gaz ?', choices=[('Oui', 'Oui'), ('Non', 'Non')], validators=[DataRequired()])
    utilise_vapeur = SelectField('Utilisation de vapeur ?', choices=[('Oui', 'Oui'), ('Non', 'Non')], validators=[DataRequired()])
    nombre_batiments = FloatField('Combien de batiments au total ?', validators=[DataRequired(), NumberRange(min=1, max=200)])
    nombre_etages = FloatField("Combien avez-vous d'étages sur le batiment principal?", validators=[DataRequired(), NumberRange(min=1, max=200)])
    submit = SubmitField('Submit')

# Définir une route pour l'URL racine '/'
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/form_page', methods=['GET', 'POST'])
def form_page():
    form = MyForm()

    # Lire le fichier CSV et extraire les valeurs uniques de la colonne souhaitée
    with open('../dataset_prepared2.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        valeurs_colonne = set(row['primarypropertytype'] for row in reader)

    # Mettre à jour les choix de la select box avec les valeurs extraites
    form.utilisation.choices = [(val, val) for val in valeurs_colonne]

    if form.validate_on_submit():
        # Récupérer les valeurs du formulaire
        utilisation = form.utilisation.data
        taille = form.taille.data
        utilise_gaz = form.utilise_gaz.data
        utilise_vapeur = form.utilise_vapeur.data
        nombre_batiments = form.nombre_batiments.data
        nombre_etages = form.nombre_etages.data

        # Appeler la fonction makePredictionIndiv avec les données du formulaire
        predictions = makePredictionIndiv(nombre_batiments, nombre_etages, utilisation, utilise_gaz, utilise_vapeur, taille)

        data = [[ nombre_batiments, nombre_etages, utilisation, utilise_gaz, utilise_vapeur, taille, predictions[0], predictions[1]]]
        columns = [ "Nombre de batiments", "Nombre d'étages", "Utilité première", "Utilisation de gaz", "Utilisation de Vapeur", "Taille du batiment", "Emission de GES (T d'équivalent CO2)", "Consommation d'énergie (kBtu)"]
        prediction_df = pd.DataFrame(data, columns=columns)

        # Traitez les prédictions comme vous le souhaitez, par exemple, affichez-les ou enregistrez-les dans une base de données, etc.

        return render_template('prediction.html',  predictions=prediction_df.to_html(index=False))

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
        
        # Passer le DataFrame au modèle pour obtenir la prédiction
        prediction = makePredictionCsv(csv_file)  
        
        # Passer le DataFrame de prédiction au template pour l'affichage
        return render_template('csv_display.html', prediction=prediction.to_html(index=False))
    
    return render_template('csv.html', form=form)


# Point d'entrée de l'application
if __name__ == '__main__':
    # Lancer l'application Flask
    app.run(host='0.0.0.0')
