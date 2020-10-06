from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from validate_email import validate_email
import datetime
#from flask_pymongo import PyMongo
app = Flask(__name__)

############################### PyMongo database  ############################
#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/abdou"
#mongo = PyMongo(app)
####################################################################################

############################### SQlAlchemy database  ############################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///steManar.db'
app.config['SECRET_KEY'] = '619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIOS'] = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Installation_Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adresse = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    tel = db.Column(db.Integer, nullable=False)
    modele = db.Column(db.Integer, nullable=False)
    date_ = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    confirmation = db.Column(db.String(20), nullable=False)

    
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Produits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomProduit = db.Column(db.String(30), nullable=False)
    prixProduit = db.Column(db.Integer, nullable=False)
    imgProduit = db.Column(db.String(30), nullable=False)
    descriptionProduit = db.Column(db.Text, nullable=False)


#####################################################################################


def email_isValid(mail):
    user_email = validate_email(mail, verify=True)
    if user_email == True :
        return True
    else:
        return False



@app.route('/')
def hello_world():
    titre = "Acceil"
    return render_template('home.html', titre = titre)

@app.route('/erreur')
def erreur():
    return render_template('err.html')


@app.route('/about')
def aboutUs():
    id = "about-body"
    titre = "About Us"
    return render_template('about.html',  titre = titre, id = id)

@app.route('/changePWD_Admin', methods = ['POST', 'GET'])
def changePWD_Admin() :
    admin = Admin.query.filter_by(id = 1).first()
    if request.method == "POST":
        PWD =  request.form.get('passwordActuel')
        if PWD == admin.password :
            newPWD = request.form.get('NVpassword')
            CnfnewPWD = request.form.get('CnfNVpassword')
            if newPWD == CnfnewPWD :
                admin.password = newPWD
                db.session.commit()
                return redirect('/login')
            else:
                return redirect('/erreur')
        else:
            return redirect('/erreur')


#############################################-------------- Administration systéme---------------###################


@login_manager.user_loader
def get(id):
    return Admin.query.get(id)


@app.route('/suprimerClient/<int:id>')
def suprClient(id) :
    ClientSuprimer = Installation_Clients.query.filter_by(id = id).first()
    db.session.delete(ClientSuprimer)
    db.session.commit()
    return redirect('/admin-installation_admin')
    
@app.route('/suprimerTousClients')
def suprTsClients() :
    ClientsSuprimer = Installation_Clients.query.all()
    for e in range(1, len(ClientsSuprimer) + 1) :
        Client__Suprimer = Installation_Clients.query.filter_by(id = e).first()
        db.session.delete(Client__Suprimer)
        db.session.commit()
    return redirect('/admin-installation_admin')



@app.route('/estConfermer/<int:id>')
def est_confermer(id):
    client_confermer = Installation_Clients.query.filter_by(id = id).first()
    client_confermer.confirmation = "Client deja Conferme"
    db.session.commit()
    return redirect('/admin-installation_admin')

@app.route('/admin-installation_admin')
def installation_admin():
    Clients = Installation_Clients.query.all()
    installation_Clients = []
    for client in Clients:
        installation_Clients.insert(0,client)
    return render_template('installation_admin.html', installation_Clients = installation_Clients)

@app.route('/login', methods = ['GET'] )
def loginAdminGet():
    #logout_user()
    return render_template('loginAdmin.html')

@app.route('/login', methods = ['POst'] )
def loginAdminPost():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    adminEmail = Admin.query.filter_by(email = email).first() # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    adminUsername = Admin.query.filter_by(username = username).first()
    adminPassword = Admin.query.filter_by(password = password).first()
    login_user(adminEmail)
    if adminEmail is None or adminUsername is None or adminPassword is None : 
        return redirect('/')
    else :
        return redirect('/admin')

@app.route('/admin')#######################################
@login_required
def admin():
    return render_template('admin.html')############

@app.route('/singOut', methods = ['GET'])
def singOut() :
    logout_user()# ------------------------->  khasni nrje3ha fash nsali !!!
    return redirect('/')
##########################################################################################


@app.route('/services-installation', methods=['POST'])
def installationPost() :
    if request.method=="POST":
        adresse=request.form.get("adresse")
        email=request.form.get("email")
        tel=request.form.get("tel")
        date_=request.form.get("date_")
        modele=request.form.get("modele")
        confirmation = "Confermer ?"

        TEST = email_isValid(email)
        if TEST == True:
            camClient = Installation_Clients(adresse = adresse, email = email, tel = tel, date_ = date_, modele = modele, confirmation = confirmation)
            db.session.add(camClient)
            db.session.commit()
            return redirect('/services-installation')
        if TEST == False:
            return redirect('/erreur')


@app.route('/services-installation', methods=['GET'])
def installationgGet() :
    if request.method=="GET":
        Clients = Installation_Clients.query.all()
        return render_template('installation.html', Clients = Clients)



################################### achat ###########################
@app.route('/achat')
def achat():
    titre = "Achat"
    produits = Produits.query.all()
    return render_template('achat.html',  titre = titre, produits = produits)



@app.route('/supProduit/<int:id>')
def delProd(id) :
    produit_suprimer = Produits.query.filter_by(id = id).first()
    db.session.delete(produit_suprimer)
    db.session.commit()
    return redirect('/achat_admin')




@app.route('/modifProduit/<int:id>', methods = ['POST', 'GET'])
def modifProdForm(id) :
    produit_modifie = Produits.query.filter_by(id = id).first()
    if request.method == "POST":
        produit_modifie.nomProduit = request.form.get('NVnomProduit')
        produit_modifie.prixProduit = request.form.get('NVprixProduit')
        produit_modifie.imgProduit = request.form.get('NVimgProduit')
        produit_modifie.descriptionProduit = request.form.get('NVdescriptionProduit')
        db.session.commit()
        return redirect('/achat_admin')


@app.route('/achat_admin', methods = ['GET', 'POST'])
def achat_admin() :
    if request.method =="POST":
        nomProduit = request.form.get("nomProduit")
        prixProduit = request.form.get("prixProduit")
        imgProduit = request.form.get("imgProduit")
        descriptionProduit = request.form.get("descriptionProduit")
        Produit = Produits(nomProduit = nomProduit, prixProduit = prixProduit, imgProduit = imgProduit, descriptionProduit = descriptionProduit)
        db.session.add(Produit)
        db.session.commit()
    produits = Produits.query.all()
    return render_template('achat_admin.html', produits = produits)




################################################
if __name__ == "__main__" :
    app.run(debug=True)