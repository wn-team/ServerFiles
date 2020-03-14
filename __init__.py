
from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
from ftplib import FTP
from time import sleep
from datetime import datetime
from datetime import timedelta
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

app.secret_key='secretkey'
app.config.update(
        DEBUG=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USE_TLS=False,
        MAIL_USERNAME = 'projectsender20@gmail.com',
        MAIL_PASSWORD = '123abc!@#'
        )
mail = Mail(app)
def send_mail_good():
    try:
        msg = Message("RES2 received",
        sender="projectsender20@gmail.com",
        recipients=["projectsender20@gmail.com"])
        msg.body = "Hello!"
        mail.send(msg)
        return 'Mail sent!>good news'
    except Exception as e:
        return(str(e))

def check_reply(Account,basePath):
    fileNameMail = 'WNN'+Account+'_RES2.csv'
    filePathMail=basePath+"Outgoing/"+fileNameMail
    datalist=[]
    data=[]
    with open(filePathMail, mode='r') as csv_file:
        csv_reader=csv.reader(csv_file)
        header=next(csv_reader)
        datalist=[row for row in csv_reader]
        data=datalist[0]
    return (data)

def send_mail_good_activation(Account,basePath,filePathOut,fileNameOut,res2info):
    fileName = 'WNN'+Account+'.csv'
    filePathIn=basePath+"Incoming/"+fileName
    with open(filePathIn, mode='r') as csv_file:
        csv_reader=csv.reader(csv_file)
        header=next(csv_reader)
        datalist=[row for row in csv_reader]
        data=datalist[0]
        SIMNo=data[8]
        ProductOfferID=data[9]
        ReqType=data[0]
    try:
        msg = Message("Reply - Customer Account No: " + Account+" - Request type: "+ ReqType + " - Status: "+ res2info[7] ,
                      sender="projectsender20@gmail.com",
                      recipients=["projectsender20@gmail.com"])
        with app.open_resource(filePathOut) as fp:
            msg.attach(fileNameOut,'text/csv',fp.read())
        if str(res2info[7]) == 'Complete':
            msg.body = "\n\n\n            Replay form Spark, Customer Account No: {}\n\n\n\
            Mobile Number: {}\n            SIMNo: {}\n            External Batch Id: {}\n            Siebel Order Number: {}\n\n\n\
            Request type: {}\n            Spark Plan: {}\n\n\n\
            The Status is: {}\n\n\n\n"\
            .format(Account,res2info[6],SIMNo, res2info[3],res2info[2],ReqType, ProductOfferID, res2info[7])
        else:
            msg.body = "\n\n\n            Replay form Spark, Customer Account No: {}\n\n\n\
            Mobile Number: {}\n            SIMNo: {}\n            External Batch Id: {}\n            Siebel Order Number: {}\n\n\n\
            Request type: {}\n            Spark Plan: {}\n\n\n\
            The Status is: {}\n\n\n\n            Error Description is: {}\n\n\n\n"\
            .format(Account,res2info[6],SIMNo, res2info[3],res2info[2],ReqType, ProductOfferID, res2info[7], res2info[8])
        mail.send(msg)

    except Exception as e:
        return('The Reply File is created, you can find it in Outgoing folder. Mail are NOT created, some issues arise.')

def send_mail_bad(Account):
    try:
        msg = Message("Reply")
        msg = Message("Warning: Request for Customer Account No " + Account+" have wrong format. Reply IS NOT CREATED",
        sender="projectsender20@gmail.com",
        recipients=["projectsender20@gmail.com"])
        msg.body = "Some problem arise in processing the request for Customer Account No "+ Account+  ". \
            The file can have a wrong format. Please try again to create another Request."
        mail.send(msg)
    except Exception as e:
        return('The Reply File is NOT created, the file can have a wrong format. Mail are NOT created, some issues arise.')


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
    ProductOfferID =""
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
            csv_writer=csv.writer(csv_file,lineterminator='\r\n')
            csv_writer.writerow(header)
            csv_writer.writerow(data)

        shutil.copy(filePathIn, filePathWaiting)

        ftp = FTP(serverName)
        ftp.login(username,password)
        ftp.cwd(FTPdirectoryIn)
        with open(filePathIn, mode='rb') as f:
            ftp.storbinary('STOR ' + fileName, f,1024)

        fileNameRES = []
        fileNameRES = os.listdir( basePath+"Waiting")

        ftp.cwd(FTPdirectoryOut)
        sleep(60)

        while fileNameRES:
            for checkfileE in fileNameRES:
                checkfile=str(checkfileE)
                AccountDigits=[str(s) for s in checkfile if s.isdigit()]
                Account=''
                for f in AccountDigits:
                    temp=Account
                    Account=temp+str(f[0])

                fileNameOut = 'WNN'+Account+'_RES2.csv'
                filePathOut = basePath + "Outgoing/" + fileNameOut
                emailcode=0

                if fileNameOut in ftp.nlst():
                    with open(filePathOut, mode='wb') as f:
                        ftp.retrbinary("RETR " + fileNameOut, f.write)
                    emailcode=1
                else:
                    timelastmodif = os.path.getmtime(basePath+"Waiting/"+checkfile)
                    now = datetime.now()
                    controlfile='WNN'+Account+'_RES1.csv'
                    if now-datetime.fromtimestamp(timelastmodif)> timedelta(minutes=5) and not(controlfile in ftp.nlst()):
                        emailcode=2

                if emailcode==1:
                    fileNameRES.remove(checkfile)
                    os.remove(basePath+"Waiting/"+checkfile)
                    res2info=check_reply(Account,basePath)
                    mail1=send_mail_good_activation(Account,basePath,filePathOut,fileNameOut, res2info)
                    flag=1
                elif emailcode==2:
                    fileNameRES.remove(checkfile)                    
                    os.remove(basePath+"Waiting/"+checkfile)
                    mail1=send_mail_bad(Account)

            sleep(60)

        ftp.quit()
        return  render_template('submit.html')
    return render_template('newactivation.html')








if __name__ == "__main__":
    app.run(debug=True)

























