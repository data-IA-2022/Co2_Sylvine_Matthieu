# Importer les modules Flask
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms import FloatField
# Créer une instance de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Clé secrète pour la protection CSRF

# Définir une classe de formulaire
class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    age = SelectField('Age', choices=[('18', '18'), ('19', '19'), ('20', '20')], validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Submit')

# Définir une route pour l'URL racine '/'
@app.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        age = form.age.data
        quantity = float(form.quantity.data)  

        return "Formulaire soumis avec succès !"

    return render_template('index.html', form=form)


# Point d'entrée de l'application
if __name__ == '__main__':
    # Lancer l'application Flask
    app.run(host='0.0.0.0')
