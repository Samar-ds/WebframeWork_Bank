import unittest
from flask import Flask, request
from app import app
from model import  db, Customer
from datetime import datetime

# Det ska finnas Unit Tester där du skriver tester som testar att det 
# 1) inte går att ta ut eller
# 2) överföra mer pengar än det finns på kontot. Det ska inte heller
# 3) gå att sätta in eller
# 4) ta ut negativa belopp

class TransaaktionValidation(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        app.config["SERVER_NAME"] = "Samar.se"
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['WTF_CSRF_METHOD'] = []
        app.config['TESTING'] = True

    def test_when_negative_amount_is_given(self):
        test_client = app.test_client()
        url = "/addTransaktion/5"
        with test_client:
            response = test_client.post(url, data={ "Operation":"Salary",
                      "Type":"Debit", "Date":datetime.now(),"Amount":"-200" })
            assert url.endswith(request.path)

    def test_when_positive_amount_is_given(self):
        test_client = app.test_client()
        url = "/addTransaktion/5"
        with test_client:
            response = test_client.post(url, data={ "Operation":"Salary",
                      "Type":"Debit", "Date":datetime.now(),"Amount":"200" })
            assert response.status_code == 302

    def test_when_withdraw_is_larger_than_balance(self):
        test_client = app.test_client()
        url = "/addTransfer/1"
        with test_client:
            response = test_client.post(url, data={"Type":"Debit", "Date":datetime.now(),
                      "Amount":"500", "AccountId":"5"})
            assert url.endswith(request.path)

    def test_when_withdraw_is_smaller_than_balance(self):
        test_client = app.test_client()
        url = "/addTransfer/1"
        with test_client:
            response = test_client.post(url, data={"Type":"Debit", "Date":datetime.now(),
                      "Amount":"100", "AccountId":"5"})
            assert response.status_code == 302


if __name__ == "__main__":
    unittest.main()
        