from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate, upgrade
from random import randint
from forms import PersonEditForm, PersonNewForm, UserRegistrationForm, TransaktionForm, TransferForm
from model import User, user_manager, UserRegistration
from flask_user import login_required, roles_required, roles_accepted

from model import db, Customer, Transaction, Account, seedData

 
app = Flask(__name__)
app.config.from_object('config.ConfigDebug')
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

user_manager.app = app
user_manager.init_app(app,db,User)
 

@app.route("/")
def startPage():
    activePage = "startPage"
    Kunder = Customer.query.count()
    konton = Account.query.count()
    total = Account.query.with_entities(func.sum(Account.Balance).label("mySum"))
    totSaldo = total.scalar()
    print(totSaldo)
    return render_template('startPage.html', AntalKunder=Kunder, AllaKonto=konton, AntalSaldo=totSaldo)

@app.route("/personer")
#@login_required
@roles_accepted("Cashier", 'Admin') # AND # OR
def personerPage():
    
    sortColumn = request.args.get('sortColumn', 'namn')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))
    searchWord = request.args.get('q','')
    activePage = "personerPage"

    allaPersoner = Customer.query.filter(
        Customer.GivenName.like('%' + searchWord + '%') | 
        Customer.Surname.like('%' + searchWord + '%') | 
        Customer.City.like('%' + searchWord + '%')  | 
        Customer.Id.like(searchWord)          )

    if sortColumn == "Kund.Id":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Id.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Id.asc())
    
    if sortColumn == "namn":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Surname.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Surname.asc())

    if sortColumn == "city":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.City.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.City.asc())

    if sortColumn == "prsnnmr":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.NationalId.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.NationalId.asc())

    paginationObject = allaPersoner.paginate(page,20,False)

    return render_template('Kunder.html', 
            allaPersoner=paginationObject.items, 
            page=page,
            sortColumn=sortColumn,
            sortOrder=sortOrder,
            q=searchWord,
            has_next=paginationObject.has_next,
            has_prev=paginationObject.has_prev, 
            pages=paginationObject.pages, 
            activePage=activePage)

@app.route("/userconfirmation")
def userConfirmationPage():
    namnet = request.args.get('namn',"")
    return render_template('userconfirmation.html',namn=namnet)

@app.route("/newuser",methods=["GET", "POST"]) 
def userRegistrationPage():
    form = UserRegistrationForm(request.form) 
    if request.method == "GET":
        return render_template('userregistration.html',form=form)
    if form.validate_on_submit():
        userReg = UserRegistration()
        userReg.email = form.email.data
        userReg.firstname = form.firstname.data
        userReg.lastname = form.lastname.data
        userReg.password = form.pwd.data
        userReg.updates = form.updates.data
        db.session.add(userReg)
        db.session.commit()
        return redirect(url_for('userConfirmationPage', namn=form.firstname.data ))

    return render_template('userregistration.html',form=form)



@app.route("/personnew",methods=["GET", "POST"]) 
@roles_accepted("Admin","Cashier")
def personNewPage():
    form = PersonNewForm(request.form) 

    if request.method == "GET":
        return render_template('personnew.html',form=form)

    if form.validate_on_submit():
        NewCustomer = Customer()
        NewCustomer.GivenName = form.Gname.data
        NewCustomer.Surname = form.Sname.data
        NewCustomer.City = form.city.data 
        NewCustomer.Zipcode = str(form.zipcode.data)
        NewCustomer.Streetaddress = form.Streetaddress.data  
        NewCustomer.Country = form.Country.data
        NewCustomer.CountryCode = form.CountryCode.data
        NewCustomer.Birthday = form.Birthday.data
        NewCustomer.NationalId = form.NationalId.data
        NewCustomer.TelephoneCountryCode = form.TelephoneCountryCode.data
        NewCustomer.Telephone = form.Telephone.data
        NewCustomer.EmailAddress = form.EmailAddress.data

        db.session.add(NewCustomer)
        db.session.commit()
        return redirect(url_for('personerPage'))

    return render_template('personnew.html',form=form)

@app.route("/edit/<id>",methods=["GET", "POST"])  # EDIT   3
@roles_accepted("Admin","Cashier")
def editPerson(id):
    form = PersonEditForm(request.form) 
    personFromDb = Customer.query.filter(Customer.Id == id).first()

    if request.method == "GET":
        form.Gname.data = personFromDb.GivenName
        form.Sname.data = personFromDb.Surname
        form.city.data = personFromDb.City
        form.zipcode.data = int(personFromDb.Zipcode)
        form.NationalId.data = personFromDb.NationalId
        form.Telephone.data = personFromDb.Telephone
        form.EmailAddress.data = personFromDb.EmailAddress
        form.Birthday.data = personFromDb.Birthday

        return render_template('EditPerson.html',person=personFromDb, form=form, id=personFromDb.Id)
    if form.validate_on_submit():
        personFromDb.GivenName = form.Gname.data
        personFromDb.Surname =  form.Sname.data
        personFromDb.City = form.city.data 
        personFromDb.NationalId = form.Telephone.data
        personFromDb.Telephone = form.Telephone.data
        personFromDb.EmailAddress = form.EmailAddress.data
        personFromDb.Birthday = form.Birthday.data
        
        db.session.commit()
        return redirect(url_for('personerPage'))
    return render_template('EditPerson.html',person=personFromDb, form=form)

@app.route("/person/<id>")  
@roles_accepted("Admin","Cashier")
def visaPerson(id):
    personToView = Customer.query.filter(Customer.Id == id).first()
    allaKonton = Account.query.filter(Account.CustomerId == id)
    AntalSaldo = Account.query.with_entities(func.sum(Account.Balance).label("mySum")).filter(Account.CustomerId == id)
    Saldo = AntalSaldo.scalar()
    return render_template('ViewPerson.html',person=personToView, accounts=allaKonton, Balance=Saldo)

@app.route("/konto/<id>")  
@roles_accepted("Admin","Cashier")
def visaKonton(id):
    kontoAttVisa = Account.query.filter(Account.Id == id).first()
    kontoTransaktion = Transaction.query.filter(Transaction.AccountId == id)
    TransaktionDesc = kontoTransaktion.order_by(Transaction.Id.asc())
    return render_template('VisaKonto.html',konto=kontoAttVisa, transaktions=TransaktionDesc)

@app.route("/addTransaktion/<id>",methods=["GET","POST"]) 
@roles_accepted("Admin","Cashier")
def addTransaktion(id):
    theAccount = Account.query.filter(Account.Id == id).first()
    Saldo = int(theAccount.Balance)
    form = TransaktionForm(request.form) 
    plusTag = ['Salary', 'Deposit cash']

    if request.method == "GET":
        return render_template('Transaktion.html',form=form)

    if form.validate_on_submit():
        ## tests
      if int(form.Amount.data) > theAccount.Balance and form.Operation.data not in plusTag:
        return render_template('valueError.html', idd=id)

      else:    
         
        NewTransaktion = Transaction()  
        NewTransaktion.Type = form.Type.data
        NewTransaktion.Operation = form.Operation.data
        NewTransaktion.Date = form.Date.data    
        NewTransaktion.Amount = int(form.Amount.data)
        NewTransaktion.AccountId = id
        
        if NewTransaktion.Operation in plusTag:
            NewTransaktion.NewBalance = Saldo + int(NewTransaktion.Amount)
        else:
            NewTransaktion.NewBalance = Saldo - int(NewTransaktion.Amount)
        theAccount.Balance = NewTransaktion.NewBalance
       
        db.session.add(NewTransaktion)
        db.session.commit()
        return redirect(url_for('visaKonton', id=NewTransaktion.AccountId))

    return render_template('Transaktion.html',form=form, idd=id)



@app.route("/addTransfer/<id>",methods=["GET","POST"]) 
@roles_accepted("Admin","Cashier")
def addTransfer(id):
    theAccount = Account.query.filter(Account.Id == id).first()
    Saldo = int(theAccount.Balance)
    form = TransferForm(request.form) 

    if request.method == "GET":
        return render_template('Transfer.html',form=form)

    if form.validate_on_submit():
        ToId = int(form.AccountId.data)
        ToAccount = Account.query.filter(Account.Id == ToId).first()

        try:
            ifIdExists = ToAccount.Id
        except:
            return render_template('IdError.html', idd=id)

        if int(form.Amount.data) > theAccount.Balance:
            return render_template('valueError.html', idd=id)
        else:
            TransferFrom = Transaction()  
            TransferFrom.Type = form.Type.data
            TransferFrom.Operation = 'Transfer'
            TransferFrom.Date = form.Date.data    
            TransferFrom.Amount = int(form.Amount.data)
            TransferFrom.AccountId = id
            TransferFrom.NewBalance = Saldo - int(TransferFrom.Amount)
            theAccount.Balance = TransferFrom.NewBalance

        
            ToSaldo = int(ToAccount.Balance)
            TransferTo = Transaction()  
            TransferTo.Type = form.Type.data
            TransferTo.Operation = 'Transfer'
            TransferTo.Date = form.Date.data    
            TransferTo.Amount = int(form.Amount.data)
            TransferTo.AccountId = ToId
            TransferTo.NewBalance = ToSaldo + int(TransferFrom.Amount)
            ToAccount.Balance = TransferTo.NewBalance

            db.session.add(TransferFrom)
            db.session.add(TransferTo)
            db.session.commit()
            return redirect(url_for('visaKonton', id=TransferFrom.AccountId))

    return render_template('Transfer.html',form=form, idd=id)

if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
    seedData(db)
    app.run()