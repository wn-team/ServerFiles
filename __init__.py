from flask import Flask, render_template, request, flash
from ftplib import FTP
import csv
import os
import shutil

app = Flask(__name__)
path ='/var/www/FlaskGitApp/FlaskGitApp'

serverName='100.127.4.217'
username='wbbprov'
password='Nhderfnr433$zs'
FTPdirectoryIn='/Incoming'
FTPdirectoryOut='/Outgoing'


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
#        filePathTemplate=os.path.join(path,'CSVTemplate')
        basePath="/var/www/FirstGitApp/FirstGitApp/"

        with open(basePath+"CSVTemplate/WNNDDMMYY_Activate_EXAMPLE.csv", mode='r') as csv_file:
            csv_reader=csv.reader(csv_file)
            header=next(csv_reader)
            datalist=[row for row in csv_reader]
            data=datalist[0]

        data[3]='WNN'+str(CustomerAccountNo)
        data[8]=str(SIMNo)
        data[9]=str(ProductOfferID)
        data[30]=str(ELID)

        fileName = 'WNN'+str(CustomerAccountNo)+'.csv'
        filePathIn = basePath+"Incoming/"+fileName
        filePathWaiting =  basePath+"Waiting/"+fileName
        with open(filePathIn, mode='w') as csv_file:
            csv_writer=csv.writer(csv_file,lineterminator='\r')
            csv_writer.writerow(header)
            csv_writer.writerow(data)
        shutil.copy(filePathIn, filePathWaiting)


        ftp = FTP(serverName) 
        ftp.login(username,password)  
        ftp.set_pasv(False) 
        ftp.cwd(FTPdirectoryIn)
        with open(filePathIn, "rb") as f:
            ftp.storbinary('STOR ' + fileName, f,1024)




        return '''FTPdirectoryIn {}......'''.format(ftp.cwd(FTPdirectoryIn))

    return render_template('newactivation.html')










if __name__ == "__main__":
    app.run(debug=True)
