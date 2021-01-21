# doing necessary imports
from datetime import date,datetime

from flask import Flask, render_template, request,jsonify

app = Flask(__name__)  # initialising the flask app with the name 'app'


@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def ProcessPayment():
    if request.method == 'POST':
        result = ""
        details = {}
        #Get all post data
        details['CreditCardNumber'] = request.form['CreditCardNumber']
        details['CardHolder'] = request.form['CardHolder']
        details['ExpirationDate'] = request.form['ExpirationDate']
        details['SecurityCode'] = request.form['SecurityCode']
        details['Amount'] = request.form['Amount']

        if all([details['CreditCardNumber'],details['CardHolder'],details['ExpirationDate'],details['Amount']]):
            details['ExpirationDate'] = datetime.strptime(details['ExpirationDate'], '%Y-%m-%d').date()
            #Validate the fields
            valid = validation(details)
            if valid:
                details['Amount'] = int(details['Amount'])
                if details['Amount'] < 20:
                    result = CheapPaymentGateway(details)
                elif details['Amount'] <= 500 and details['Amount'] >= 21:
                    result = ExpensivePaymentGateway(details)
                elif details['Amount'] > 500:
                    result = PremiumPaymentGateway(details)
                return result
            else:
                result = "400 bad request"
                return result

        else:
            result= "500 internal server error"
            return result

    else:
        return render_template('ProcessPayment.html')


def validation(details):
    valid = False
    if details['Amount'].isdigit() and len(details['SecurityCode']) == 3 and details['ExpirationDate'] > date.today():
        valid = True

    return valid

def CheapPaymentGateway(details):
    return "Cheap Payment Gateway - 200 OK"

def ExpensivePaymentGateway(details):
    return "Expensive Payment Gateway- 200 OK"


def PremiumPaymentGateway(details):
    return "PremiumPaymentGateway - 200 OK"



if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000