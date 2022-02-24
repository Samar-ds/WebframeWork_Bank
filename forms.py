from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators
from wtforms.validators import InputRequired
from wtforms.fields import IntegerField, SelectField, BooleanField, DecimalField
from datetime import date
from wtforms.fields import DateField
from wtforms.fields import DateTimeField

class PersonEditForm(FlaskForm):
    Gname = StringField("GivenName",[validators.Length(min=3, max=80, message="Skriv in mellan 2 och 80 tecken")])
    Sname = StringField("Surname",[validators.Length(min=3, max=80, message="Skriv in mellan 2 och 80 tecken")])
    city = StringField("city",[validators.Length(min=5, max=30)])
    zipcode = IntegerField("postalcode",[validators.NumberRange(10000,99999)])
    Streetaddress = StringField("Streetaddress", [validators.Length(min=5, max=40)])
    Country = StringField("country",[validators.Length(min=3, max=20)])
    CountryCode = IntegerField("countrycode",[validators.NumberRange(1,99)])
    Birthday = DateField("Birthday")    ###--- validator ????!!!!
    NationalId = StringField("nationalId",[validators.Length(min=10, max=15)])
    TelephoneCountryCode = IntegerField("Telephonecountrycode",[validators.NumberRange(1,99)])
    Telephone = StringField("Telephone",[validators.Length(min=6, max=14)])
    EmailAddress = StringField("Epost",[validators.Email()])

    # pwd = StringField("pwd",[validators.Length(min=5, max=30), validators.EqualTo('pwdagain') ])
    # pwdagain = StringField("pwdagain",[validators.Length(min=5, max=30)])


class PersonNewForm(FlaskForm):
    Gname = StringField("GivenName",[validators.Length(min=3, max=80, message="Skriv in mellan 2 och 80 tecken")])
    Sname = StringField("Surname",[validators.Length(min=3, max=80, message="Skriv in mellan 2 och 80 tecken")])
    city = StringField("city",[validators.Length(min=5, max=30)])
    zipcode = IntegerField("postalcode",[validators.NumberRange(10000,99999)])
    Streetaddress = StringField("Streetaddress", [validators.Length(min=5, max=40)])
    #position = SelectField("Streetaddress", choices=[('g', 'Goalie'), ('d', 'Defence'), ('f', 'Forward')])    
    Country = StringField("country",[validators.Length(min=3, max=20)])
    CountryCode = IntegerField("countrycode",[validators.NumberRange(1,99)])
    Birthday = DateField("Birthday")    ###--- validator ????!!!!
    NationalId = IntegerField("nationalId",[validators.NumberRange(10000,99999)])
    TelephoneCountryCode = IntegerField("Telephonecountrycode",[validators.NumberRange(1,99)])
    Telephone = IntegerField("Telephone",[validators.NumberRange(10000,99999)])
    EmailAddress = StringField("Epost",[validators.Email()])


class UserRegistrationForm(FlaskForm):
    email = StringField("Epost",[validators.Email()])
    firstname = StringField("Förnamn",[validators.Length(min=5, max=40)])
    lastname = StringField("Efternamn",[validators.Length(min=5, max=40)])
    
    val = []
    val.append(validators.Length(min=5, max=30))
    val.append(validators.EqualTo('pwdagain'))
    pwd = StringField("pwd",val)

    pwdagain = StringField("pwdagain",[validators.Length(min=5, max=30)])
    updates = BooleanField("Send me important updates")


class TransaktionForm(FlaskForm):
    Operation = SelectField("Operation Type", 
                choices=['Salary', 'Deposit cash', 'Payment', 'Bank withdrawal'])
    Type = SelectField("Transaktion Type", choices=['Credit', 'Debit'])
    Date = DateField("Date")
    Amount = DecimalField("Amount", [validators.NumberRange(min=1, max=10000)])

class TransferForm(FlaskForm):
    Type = SelectField("Transaktion Type", choices=['Credit', 'Debit'])
    Date = DateField("Date")
    Amount = DecimalField("Amount", [validators.NumberRange(min=1, max=10000)])
    AccountId = IntegerField("Transfer to Account Number",
             [validators.NumberRange(min=1, max=15000)])

    