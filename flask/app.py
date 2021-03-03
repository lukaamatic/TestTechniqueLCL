# Fichier configurant l'application web
# Création et requêtes de la base de données

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import load_only

# Initialisation de l'application flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/decesFrance'
db = SQLAlchemy(app)

# Création de la base de données


class Data(db.Model):
    __tablename__ = "data"
    nom = db.Column(db.String(120))
    prenom = db.Column(db.String(120))
    datenaiss = db.Column(db.Date)
    sexe = db.Column(db.Integer)
    lieunaiss = db.Column(db.String(120))
    commnaiss = db.Column(db.String(120))
    paysnaiss = db.Column(db.String(120))
    datedeces = db.Column(db.Date)
    actedeces = db.Column(db.String(120))
    lieudeces = db.Column(db.String(120))
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, nom, prenom, datenaiss, sexe, lieunaiss, commnaiss, paysnaiss, datedeces, actedeces):
        self.nom = nom
        self.prenom = prenom
        self.datenaiss = datenaiss
        self.sexe = sexe
        self.lieunaiss = lieunaiss
        self.commnaiss = commnaiss
        self.paysnaiss = paysnaiss
        self.datedeces = datedeces
        self.actedeces = actedeces


# Definition des routes applicatives

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/response", methods=['POST'])
def response():
    if request.method == 'POST':
        # On cherche en base les données entrées dans l'interface
        # En faisant attention aux différents formats entrés
        date_naissance = datetime.fromisoformat(request.form["datenaiss"]).replace(hour=0, minute=0, second=0, microsecond=0)
        exists = db.session.query(Data).filter(func.upper(Data.nom) == request.form["nom"].upper(),
                                               func.upper(Data.prenom) == request.form["prenom"].upper(),
                                               Data.datenaiss == date_naissance).first()



        # Selon si la personne est présente en base ou non, on renvoie un message différent
        if exists is None:
            return render_template("index.html", text="Cette personne n'est pas décédée")
        else:
            # Query pour la date du décès
            date_deces = db.session.query(Data).filter(func.upper(Data.nom) == request.form["nom"].upper(),
                                                       func.upper(Data.prenom) == request.form["prenom"].upper(),
                                                       Data.datenaiss == date_naissance).first().datedeces
            return render_template("index.html",
                                   text=request.form["nom"] + " " + request.form["prenom"] +
                                   ", dont la date de naissance est le " +
                                   request.form["datenaiss"] + ", a pour date de décès le " + str(date_deces))


# run principal de l'application flask
if __name__ == '__main__':
    app.run()
