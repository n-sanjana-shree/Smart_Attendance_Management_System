import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import time
import re
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import email.encoders as Encoders
import os
import smtplib
from twilio.rest import Client

account_sid = "AC29d90d28dd6bba8f6ec5bee14e5055ed"
auth_token = "87cc8a6feb1ed778b0d76603cc896e21"

client = Client(account_sid, auth_token)

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)
 
window.geometry('1280x720')
window.configure(background='Grey')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

ts = time.time()      
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour,Minute,Second=timeStamp.split(":")
fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"


# message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System" ,bg="Green"  ,fg="white"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 

# message.place(x=200, y=20)

lbl = tk.Label(window, text="Enter Student ID",width=18  ,height=2  ,fg="Black"  ,bg="White" ,font=('Arial', 15, ' bold ') ) 
lbl.place(x=350, y=50)

txt = tk.Entry(window,width=15  ,bg="White" ,fg="Black",font=('Arial', 15, ' bold '))
txt.place(x=620, y=60)

lbl2 = tk.Label(window, text="Enter Student Name",width=18  ,fg="Black"  ,bg="White"    ,height=2 ,font=('Arial', 15, ' bold ')) 
lbl2.place(x=350, y=150)

txt2 = tk.Entry(window,width=15  ,bg="White"  ,fg="Black", font=('Arial', 15, ' bold ')  )
txt2.place(x=620, y=160)

lbl3 = tk.Label(window, text="Enter Phone NO",width=18  ,fg="Black"  ,bg="White"    ,height=2 ,font=('Arial', 15, ' bold ')) 
lbl3.place(x=350, y=250)

txt3 = tk.Entry(window,width=15  ,bg="White"  ,fg="Black", font=('Arial', 15, ' bold ')  )
txt3.place(x=620, y=260)

lbl4 = tk.Label(window, text=" Updates: ",width=15  ,fg="Black"  ,bg="White"  ,height=2 ,font=('Arial', 15, ' bold ')) 
lbl4.place(x=350, y=430)

message = tk.Label(window, text="" ,bg="White"  ,fg="Black"  ,width=35  ,height=2, activebackground = "Green" ,font=('Arial', 15, ' bold ')) 
message.place(x=550, y=430)

lbl5 = tk.Label(window, text="Attendance : ",width=15  ,fg="Black"  ,bg="White"  ,height=3 ,font=('Arial', 15, ' bold ')) 
lbl5.place(x=350, y=580)


message2 = tk.Label(window, text="" ,fg="Black"   ,bg="White",activeforeground = "green",width=35  ,height=3  ,font=('Arial', 15, ' bold ')) 
message2.place(x=550, y=580)

date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')


f=open("Database.txt", 'a')
f.write("\nDATE \t TIME \t \t \t TEACHER NAME \t \t STUDENT NAME\n ")
print('Executing the script')
f.close()


def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    phone=(txt3.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            #img = cv2.flip(img, 0)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
           
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
            cv2.imshow('frame',img)
            cv2.imwrite('frame.png',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name 
        row = [Id , name, phone]
        with open('StudentDetails\\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric No"
            message.configure(text= res)
        
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)
    now = datetime.datetime.now()
    while True:
        ret, im =cam.read()
       # im = cv2.flip(im, 0)
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            flag=0
            if(conf < 60):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                Id11=[]
                with open('StudentDetails\\StudentDetails.csv', 'a+') as file:
                    reader = csv.reader(file)
                    print(reader)
##                    next(reader)
                    for row in reader:
                        print((type(row[0])))
                        if row[0] == str(Id):
                            print('ppp')
                            print('name {}'.format(row[1]))


                
            else:
                Id='Unknown'                
                tt=str(Id)  
            #if(conf > 40):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                #if flag ==1:
                cv2.imwrite("ImagesUnknown\\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im)
        
        if (cv2.waitKey(1)==ord('q')):
            f=open("Database.txt", 'a')
            if flag ==1:
                flag=0
                
                f.write(str(now)+'\t'+"ffff"+'\t' +str(count1)+'\t'+str(Idr1)+'\n')
                f.write(str(now)+'\t'+"FFFFFFFF"+'\t' +str(count3)+'\t'+str(Idr2)+'\n')
            f.close()
            print('Done')
            ts = time.time()      
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour,Minute,Second=timeStamp.split(":")
            fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
            attendance.to_csv(fileName,index=False)
            cam.release()
            cv2.destroyAllWindows()
            #print(attendance)
            res=attendance
            message2.configure(text= res)
            break


def absent():
    
    f=open("StudentDetails\\StudentDetails.csv", 'r')
    reader1 = csv.reader(f)
    f1=open("Database_new_ct.txt", 'a')
    pj=0
    sd=0
    count =0
    enter =0
    text=f.readlines()
    #while True:
    print('Enter the Attendance Shhet')
    str1=input()
    #str1=str(str)
    print(str1)
    str1=str1+'.csv'
    print(str1)
    text=str(text)       
    i=0
    matched=10
    with open('StudentDetails\\StudentDetails.csv', 'r+') as file:
        reader = csv.reader(file)
        #print(reader)
        next(reader)
        for line in reader:
            print(line)
            with open(str1, 'r+') as file1:
                readerlist = csv.reader(file1)
                next (readerlist)
                print("####")
                
                for line1 in readerlist:
                    print(line1[0])
                    if line[0]==line1[0]:
                        print('ID matches')
                        #print('name {}'.format(line1[1]))
                        matched=1
                        #file.seek(14)
                    else:
                        matched=0
                if matched ==1:
                    print('name {}'.format(line1[1]))
                    matched=10
                if matched==0:
                    print('Absentince Phone{}'.format(line[2]))
                    matched=10
                    phone1= "9663026928" #str(line[2])
                    client.api.account.messages.create(
                        to = "+91"+ phone1,
                        from_="+12166000705" ,  #+1 210-762-4855"
                        body="{} is Absent ".format(line[1]) )

import smtplib
##from email.MIMEMultipart import MIMEMultipart
##from email.MIMEBase import MIMEBase
##from email.MIMEText import MIMEText
##from email.Utils import COMMASPACE, formatdate
##from email import Encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import email.encoders as Encoders
import os

USERNAME = "shreensanjana@gmail.com"
PASSWORD = "finalyearprojectmailid"

def sendMail(to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo_or_helo_if_needed()
        server.starttls()
        server.ehlo_or_helo_if_needed()
        server.login(USERNAME,PASSWORD)
        server.sendmail(USERNAME, to, msg.as_string())
        server.quit()


sendMail( ["kavyagp666@gmail.com"],
        "Section A attendance",
        "Dear Parent,\nPlease note that your child has not attended today's class.Advice him/her to attend the class regularly.Please send the letter regarding the reason for his/her absence. ",
        ["frame.png"] )


clearButton = tk.Button(window, text="Clear", command=clear  ,fg="Black"  ,bg="White"  ,width=10  ,height=1 ,activebackground = "Green" ,font=('times', 15, ' bold '))
clearButton.place(x=830, y=59)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="Black"  ,bg="White"  ,width=10  ,height=1, activebackground = "Green" ,font=('times', 15, ' bold '))
clearButton2.place(x=830, y=159)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="Black"  ,bg="White"  ,width=10  ,height=1, activebackground = "Green" ,font=('times', 15, ' bold '))
clearButton2.place(x=830, y=259)

clearButton2 = tk.Button(window, text="Absent", command=absent, fg="Black"  ,bg="White"  ,width=10  ,height=2, activebackground = "Green" ,font=('times', 15, ' bold '))
clearButton2.place(x=600, y=350)

takeImg = tk.Button(window, text="DataSet", command=TakeImages  ,fg="Black"  ,bg="White"  ,width=10  ,height=2, activebackground = "green" ,font=('times', 15, ' bold '))
takeImg.place(x=300, y=500)
trainImg = tk.Button(window, text="Training", command=TrainImages  ,fg="Black"  ,bg="White"  ,width=10  ,height=2, activebackground = "green" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
trackImg = tk.Button(window, text="Recognition", command=TrackImages  ,fg="Black"  ,bg="White"  ,width=10  ,height=2, activebackground = "green" ,font=('times', 15, ' bold '))
trackImg.place(x=700, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="Black"  ,bg="White"  ,width=10  ,height=2, activebackground = "green" ,font=('times', 15, ' bold '))
quitWindow.place(x=900, y=500)
print(quitWindow)



 
window.mainloop()
