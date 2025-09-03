# It is a Console Based Application which uses python and MySQL

import pymysql
import random
import datetime

class Bank:
    def __init__(self):

        print(" 1.Do you want to login to your account \n 2.Do you want to create new account \n 3.Do you want to delete your account \n 4.History  \n 5.Exit")
        choice=int(input("Choose your option:"))

        self.con=pymysql.connect(host='localhost',user='root',password='Ayyappa@888',database="ayyappa")
        self.cursor=self.con.cursor()

        if choice==1:
            name=input("Enter your name:")
            ac=int(input("enter your account-no:"))
            pas=input("Enter Password:")
            self.pas=pas
            self.name=name.capitalize()
            self.ac=ac
            q3="select BALANCE from SBI where ACNO=%s and NAME='%s' and PASSWORD='%s';"
            self.cursor.execute(q3 %(self.ac,self.name,self.pas))
            d=self.cursor.fetchone()
            self.d=d
            
            if self.d!=None:
                fl=0

                while fl==0:
                    print(" 1.Withdraw \n 2.Deposit \n 3.Balance Enquiry \n 4.Exit")  
                    ch1=int(input("Enter your choice:"))  


                    if ch1==1:
                        self.withdraw()


                    elif ch1==2:
                        self.deposit() 


                    elif ch1==3:
                        self.checkbalance()  

                        

                    print("do you want to continute YES/NO")
                    a=input()
                    

                    if a=='YES' or a=='yes' or a=='Yes' or a=='y' or a=='Y':
                        fl=0
                    else:
                        fl+=1
            else:
                print("Please enter correct details!")
        elif choice==2:
            self.createaccount()

        elif choice==3:
            self.deleteacount()
        elif choice==4:
            self.history()
        else:
            self.close()

    def withdraw(self):   
                
            b=int(input("enter how much amount to withdraw:"))
            q1="select BALANCE from SBI where ACNO=%s and NAME='%s' and PASSWORD='%s';"
            self.cursor.execute(q1 %(self.ac,self.name,self.pas))
            d1=self.cursor.fetchone()
            for i in d1:
                a=i
            
            if b<=a:
                c=datetime.datetime.now()

                x=c.strftime("%y-%m-%d %H:%M:%S")
                bal=a-b
                q2="update SBI set BALANCE=%s where ACNO=%s;" 
                self.cursor.execute(q2 %(bal,self.ac))   
                self.con.commit()
                

            print(f"please take your amount {b}!")
            print(f"your total balance is ₹{bal}")

            q1="select DATE1 from SBI where ACNO=%s;"
            self.cursor.execute(q1 %(self.ac))
            d1=self.cursor.fetchone()
            for i in d1:
                a1=i

            q2="select DATE2 from SBI where ACNO=%s;"
            self.cursor.execute(q2 %(self.ac))
            d2=self.cursor.fetchone()
            for i in d2:
                a2=i

            q3="select DATE3 from SBI where ACNO=%s;"
            self.cursor.execute(q3 %(self.ac))
            d3=self.cursor.fetchone()
            for i in d3:
                a3=i
                

            
            
            if a1==None:
                q4="update SBI set DATA1='WITHDRAW', AMOUNT1=%s ,DATE1='%s' where ACNO=%s;"
                self.cursor.execute(q4 %(b,x,self.ac))
                self.con.commit()

                
            
            elif a2==None:
                    
                    q4="update SBI set DATA2='WITHDRAW', AMOUNT2=%s ,DATE2='%s' where ACNO=%s;"
                    self.cursor.execute(q4 %(b,x,self.ac))
                    self.con.commit()

            elif a3==None:
                    
                    q4="update SBI set DATA3='WITHDRAW', AMOUNT3=%s ,DATE3='%s' where ACNO=%s;"
                    self.cursor.execute(q4 %(b,x,self.ac))
                    self.con.commit()
            
            
            else:
                    if a1!=None and a2!=None and a3!=None:
                        if a1<=a2 and a1<=a3:
                            q4="update SBI set DATA1='WITHDRAW', AMOUNT1=%s ,DATE1='%s' where ACNO=%s;"
                            self.cursor.execute(q4 %(b,x,self.ac))
                            self.con.commit()

                    
                        elif a2<=a1 and a2<=a3:
                            q4="update SBI set DATA2='WITHDRAW', AMOUNT2=%s ,DATE2='%s' where ACNO=%s;"
                            self.cursor.execute(q4 %(b,x,self.ac))
                            self.con.commit()

                    
                        else:
                            q4="update SBI set DATA3='WITHDRAW', AMOUNT3=%s ,DATE3='%s' where ACNO=%s;"
                            self.cursor.execute(q4 %(b,x,self.ac))
                            self.con.commit()
        
    def deposit(self):
        b=int(input("enter how much amount to deposit:"))
        q1="select BALANCE from SBI where ACNO=%s and NAME='%s' and PASSWORD='%s';"
        self.cursor.execute(q1 %(self.ac,self.name,self.pas))
        d1=self.cursor.fetchone()
        for i in d1:
            a=i
        c=datetime.datetime.now()

        x=c.strftime("%y-%m-%d %H:%M:%S")
        bal=a+b
        q2="update SBI set BALANCE=%s where ACNO=%s;" 
        self.cursor.execute(q2 %(bal,self.ac))   
        self.con.commit()
        
        print(f"you have deposited ₹{b} to your account {self.ac} ")
        print(f"your total balance is ₹{bal}")   

        q1="select DATE1 from SBI where ACNO=%s;"
        self.cursor.execute(q1 %(self.ac))
        d1=self.cursor.fetchone()
        for i in d1:
            a1=i


        q2="select DATE2 from SBI where ACNO=%s;"
        self.cursor.execute(q2 %(self.ac))
        d2=self.cursor.fetchone()
        for i in d2:
            a2=i

        q3="select DATE3 from SBI where ACNO=%s;"
        self.cursor.execute(q3 %(self.ac))
        d3=self.cursor.fetchone()
        for i in d3:
            a3=i
        

        
        if a1==None:
            q4="update SBI set DATA1='DEPOSIT', AMOUNT1=%s ,DATE1='%s' where ACNO=%s;"
            self.cursor.execute(q4 %(b,x,self.ac))
            self.con.commit()

            
        
        elif a2==None:
                
                q4="update SBI set DATA2='DEPOSIT', AMOUNT2=%s ,DATE2='%s' where ACNO=%s;"
                self.cursor.execute(q4 %(b,x,self.ac))
                self.con.commit()

        elif a3==None:
                
                q4="update SBI set DATA3='DEPOSIT', AMOUNT3=%s ,DATE3='%s' where ACNO=%s;"
                self.cursor.execute(q4 %(b,x,self.ac))
                self.con.commit()



        else:
                if a1!=None and a2!=None  and a3!=None:    
                    if a1<=a2 and a1<=a3:
                            q4="update SBI set DATA1='DEPOSIT', AMOUNT1=%s ,DATE1='%s' where ACNO=%s;"
                            self.cursor.execute(q4 %(b,x,self.ac))
                            self.con.commit()


                
                    elif a2<=a1 and a2<=a3:
                        q4="update SBI set DATA2='DEPOSIT', AMOUNT2=%s ,DATE2='%s' where ACNO=%s;"
                        self.cursor.execute(q4 %(b,x,self.ac))
                        self.con.commit()
                
                    
                
                    else:
                        q4="update SBI set DATA3='DEPOSIT', AMOUNT3=%s ,DATE3='%s' where ACNO=%s;"
                        self.cursor.execute(q4 %(b,x,self.ac))
                        self.con.commit()
                


    def checkbalance(self):

        q1="select BALANCE from SBI where ACNO=%s and NAME='%s' AND PASSWORD='%s';"
        self.cursor.execute(q1 %(self.ac,self.name,self.pas))
        d1=self.cursor.fetchone()
        for i in d1:
            a=i
        print(f"your total balance is ₹{a}")  
    
    def createaccount(self):
        name=input("Enter your name:")
        name=name.capitalize()
        Z=input("Enter your password:")
        balance=int(input("Enter how much you want to deposit:"))
        q6="select PASSWORD from SBI where NAME='%s';"
            
        self.cursor.execute(q6 %(name))
        d3=self.cursor.fetchone()
        
        if d3==None:    
            q4="select count(*) from SBI;"
            self.cursor.execute(q4)
            d2=self.cursor.fetchone()
            for i in d2:
                a=i
            q5="select count(*) from SBI_DELETED;"
            self.cursor.execute(q5)
            d5=self.cursor.fetchone()
            for i in d5:
                c=i
                
            b=10000+(a+c+1)
            
            
            c=datetime.datetime.now()

            x=c.strftime("%y-%m-%d %H:%M:%S")
            
            

            q5="insert into SBI value(%s,'%s','%s',%s,'%s','null',null,null,'null',null,null,'null',null,null);" 
            self.cursor.execute(q5 %(b,name,Z,balance,x))   
            self.con.commit()
            print(f"You have created your account succesfully. your account number is:{b}  and Your password: {Z}(PLEASE NOTE IT FOR FUTURE USE)")
            print(f"Your total balance is ₹{balance}")

        elif d3!=None:
            q7="select ACNO from SBI where PASSWORD='%s';"
            self.cursor.execute(q7 %(Z))
            d4=self.cursor.fetchone()
            if d4==None:
                q4="select count(*) from SBI;"
                self.cursor.execute(q4)
                d2=self.cursor.fetchone()
                for i in d2:
                    a=i
                q4="select count(*) from SBI_DELETED;"
                self.cursor.execute(q4)
                d5=self.cursor.fetchone()
                for i in d5:
                    c=i
                
                    
                b=10000+(a+c+1)

                c=datetime.datetime.now()

                x=c.strftime("%y-%m-%d %H:%M:%S")
                
                

                q5="insert into SBI value(%s,'%s','%s',%s,'%s','null',null,null,'null',null,null,'null',null,null);" 
                self.cursor.execute(q5 %(b,name,Z,balance,x))   
                self.con.commit()
                print(f"You have created your account succesfully. your account number is:{b} and Your password: {Z}")
                print(f"Your total balance is ₹{balance}")
            elif d4!=None:
                ab=0
                while ab==0:
                    password1=input("please enter another password :")
                        
                    q7="select ACNO from SBI where PASSWORD='%s';"
                    self.cursor.execute(q7 %(password1))
                    d4=self.cursor.fetchone()
                    if d4==None:
                        ab+=1

                q4="select count(*) from SBI;"
                self.cursor.execute(q4)
                d2=self.cursor.fetchone()
                for i in d2:
                    a=i
                q4="select count(*) from SBI_DELETED;"
                self.cursor.execute(q4)
                d5=self.cursor.fetchone()
                for i in d5:
                    c=i
            

                b=10000+(a+c+1)
                c=datetime.datetime.now()

                x=c.strftime("%y-%m-%d %H:%M:%S")
                
                q5="insert into SBI value(%s,'%s','%s',%s,'%s','null',null,null,'null',null,null,'null',null,null);" 
                self.cursor.execute(q5 %(b,name,password1,balance,x))   
                self.con.commit()
                print(f"You have created your account succesfully. your account number is:{b}  and Your password: {password1}")
                print(f"Your total balance is ₹{balance}")

        else:
                print("Please enter correct details!") 
            

    
        
    


    def deleteacount(self):
        name=input("Enter your name:")
        ac=int(input("enter your account-no:"))
        passw=input("enter password:")
        
        q6="select balance from SBI where ACNO=%s and NAME='%s' and PASSWORD='%s';"
        self.cursor.execute(q6 %(ac,name,passw))
        
        d=self.cursor.fetchone()
        for i in d:
            b2=i
        if d!=None:

            q2="insert into sbi_deleted select * from sbi where ACNO=%s;" 
            self.cursor.execute(q2 %(ac))
            self.con.commit()


            q7="delete from SBI where ACNO=%s and NAME='%s';"
            self.cursor.execute(q7 %(ac,name))
            self.con.commit()
            print(f"Your account has been deleted.please take your money :₹ {b2}")




    def history(self):
        name=input("Enter your name:")
        ac=int(input("enter your account-no:"))
        passw=input("enter password:")
        print("type-------Money------Date&time")
        qu1="select DATA1,AMOUNT1,DATE1 from SBI where ACNO=%s and NAME='%s'and PASSWORD='%s';"
        self.cursor.execute(qu1 %(ac,name,passw))
        s1=self.cursor.fetchone()
        for i in s1:
            print(i,end="-----")
        print()
        qu2="select DATA2,AMOUNT2,DATE2 from SBI where ACNO=%s and NAME='%s'and PASSWORD='%s';"
        self.cursor.execute(qu2 %(ac,name,passw))
        s2=self.cursor.fetchone()
        for i in s2:
            print(i,end="-----")
        print()    
        qu3="select DATA3,AMOUNT3,DATE3 from SBI where ACNO=%s and NAME='%s'and PASSWORD='%s';"
        self.cursor.execute(qu3 %(ac,name,passw))
        s3=self.cursor.fetchone()
        for i in s3:
            print(i,end="-----")
        print()    
    
    
    
    def close(self):
            
        self.con.commit()            
        self.cursor.close()
        self.con.close()                 


ANU=Bank()

    


         
         




        