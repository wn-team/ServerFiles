from flask import Flask, render_template, request, flash
import csv
import os

app = Flask(__name__)
path ='/var/www/FlaskGitApp/FlaskGitApp'

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/newactivation.html', methods=['POST','GET'])

def form_example1():
    error = None
    CustomerAccountNo=""
    SIMNo=""
    ELID=""
    if request.method=='POST':
        CustomerAccountNoAcq = request.form.get('CustomerAccountNo')
        SIMNoAcq = request.form.get('SIMNo')
        ELIDAcq = request.form.get('ELID')
        ProductOfferID = request.form.get('ProductOfferID')
        CustomerAccountNo = CustomerAccountNoAcq.replace(" ","")
        SIMNo = SIMNoAcq.replace(" ","")
        ELID = ELIDAcq.replace(" ","")


        if CustomerAccountNo == "":
            error = 'Invalid input'
            flash('-Please fill this data- ', category='CustomerAccountNosms')
        if SIMNo == "":
            error = 'Invalid input'
            flash('-Please fill this data- ', category='SIMNosms')
        if ELID == "":
            error = 'Invalid input'
            flash('-Please fill this data- ', category='ELIDsms')
        if ProductOfferID == "":
            error = 'Invalid input'
            flash('-Please select an option-', category='ProductOfferIDsms')

        if len(CustomerAccountNo) != sum(c.isdigit() for c in CustomerAccountNo) and CustomerAccountNo != "":
            error = 'Invalid input'
            if len(CustomerAccountNo)-sum(c.isdigit() for c in CustomerAccountNo) != 0:
                flash('-Error: {} characters that are not digits-'\
                      .format(len(CustomerAccountNo)-sum(c.isdigit() for c in CustomerAccountNo)), category='CustomerAccountNosms')

        if [len(SIMNo),sum(c.isdigit() for c in SIMNo)] != [17,17]  and SIMNo != "":
            error = 'Invalid input'
            if (len(SIMNo)-sum(c.isdigit() for c in SIMNo)) != 0:
                flash('-Error: {} characters that are not digits-'\
                      .format(len(SIMNo)-sum(c.isdigit() for c in SIMNo)), category='SIMNosms')
            if sum(c.isdigit() for c in SIMNo) != 17:
                flash('-Error: Inserted data has {} digits intead 17 digits-'
                      .format(sum(c.isdigit() for c in SIMNo)), category='SIMNosms')


        if [len(ELID),sum(c.isdigit() for c in ELID)] != [9,9] and ELID != "":
            error = 'Invalid input'
            if (len(ELID)-sum(c.isdigit() for c in ELID)) != 0:
                flash('-Error: {} characters that are not digits-'\
                      .format(len(ELID)-sum(c.isdigit() for c in ELID)), category='ELIDsms')
            if sum(c.isdigit() for c in ELID) != 9:
                flash('-Error: Inserted data has {} digits intead 9 digits-'\
                      .format(sum(c.isdigit() for c in ELID)), category='ELIDsms')

        if error != None:
            return render_template('newactivation.html', error=error)

        temp = ProductOfferID.split()
        ProductOfferID = temp[0]
        fileNameTemplate = 'WNNDDMMYY_Activate_EXAMPLE.csv'
        filePathTemplate=os.path.join(path,'CSVTemplate')
#        filePathTemplate=os.path.join(path,'CSVTemplate',fileNameTemplate)


        if os.path.exists(filePathTemplate):
            return '''path exist'''
#            try:
#                with open(filePathTemplate, 'rb') as f:
#                    csv_reader=csv.reader(f)
#                return '''file is open'''
#           except:
#                return '''not possible open file'''


        return '''Path {}......'''.format(filePathTemplate)

    return render_template('newactivation.html')










if __name__ == "__main__":
    app.run(debug=True)
