import mysql.connector as conn
from random import randint
myconn=conn.connect(host='localhost',user='root',passwd='a@123',database='ATM')
if myconn.is_connected()==False:
    print('...........ERROR...........')
if myconn.is_connected()==True:
    print('...........CONNECTION SUCCESSFUL...........')

cursor=myconn.cursor()

#cursor.execute('DROP TABLE IF EXISTS ATM')
#cursor.execute('''CREATE TABLE ATM(ACCNO CHAR(8) NOT NULL PRIMARY KEY,
 #                       ACC_NM VARCHAR(30) NOT NULL,
  #                      CUSTOMERID CHAR(5),
   #                     PHONENO CHAR(10),
    #                    BALANCE INT,
     #                  PIN INT)''')
#myconn.commit()



# New account
def new_acc():
    name=input('ENTER ACCOUNT HOLDER\'S NAME :  ')
    phno=int(input('ENTER ACCOUNT HOLDER\'S PHONE NUMBER :  '))
    pin=int(input('ENTER PIN(4-DIGIT) : '))
    bal=int(input('ENTER OPENING BALANCE: '))
    accno=str(randint(10000000,99999999))
    cusid='SA'+str(accno[-4:-1])
    
    sql='INSERT INTO ATM VALUES("{}","{}","{}","{}",{},{})'.format(accno,name,cusid,phno,bal,pin)
    cursor.execute(sql)
    myconn.commit()
    sql='SELECT * FROM ATM WHERE ACCNO={}'.format(accno,)
    try:
        cursor.execute(sql)
        record=cursor.fetchall()
        for r in record:
            for i in r:
                print(i)
    except:
        myconn.rollback()
    print("================================================================================")
        
#Existing account
def acc(ID,pin):
    sql='SELECT * FROM ATM WHERE CUSTOMERID="{}" AND PIN={}'.format(ID,pin)
    try:
        cursor.execute(sql)
        rec=cursor.fetchall()
        if rec==[]:
            print('...........WRONG DATA ENTERED...........')
    except:
        myconn.rollback()
    print("================================================================================")


def deposit(ID):
    amt=int(input("Enter the money to be deposited: "))
    print("================================================================================")
    sql='update atm set balance=balance + {} where CUSTOMERID="{}"'.format(amt,ID)
    cursor.execute(sql)
    myconn.commit()
    print("sucessfully deposited")

   
    
def withdraw(ID):
    amt=int(input("Enter the money to withdraw: "))
    print("================================================================================")
    ah='select BALANCE from atm where CUSTOMERID="{}"'.format(ID)
    cursor.execute(ah)
    m=cursor.fetchone()
    if amt<m[0]:
        sql='update atm set balance=balance - {} where CUSTOMERID="{}"'.format(amt,ID)
        cursor.execute(sql)
        myconn.commit()
        print("Sucessfully updated")
        
    else:
        print("Your are having less than",amt)
        print("Please try again")
        print("=====================================================")
    
    
    
    
def balance(ID):
    ma='select balance from atm where CUSTOMERID="{}"'.format(ID)
    cursor.execute(ma)
    k=cursor.fetchone()
    print("Balance in your account=",k[0])
    print("================================================================================")


def upin(ID):
    pin=int(input("Enter the pin: "))
    print("================================================================================")

    sql='update atm set pin={} where CUSTOMERID="{}"'.format(pin,ID)
    cursor.execute(sql)
    myconn.commit()
    print("PIN updated")
 
    
def upn(ID):
    phn=int(input("Enter the new phone number: "))
    print("================================================================================")

    sql='update atm set phoneno={} where CUSTOMERID="{}"'.format(phn,ID)
    cursor.execute(sql)
    myconn.commit()
    print("Phone number updated")

    
def delete(ID):
    print("================================================================================")

    sql='delete from atm where CUSTOMERID="{}"'.format(ID)
    cursor.execute(sql)
    myconn.commit()
    print("Record deleted")
    


def menu(ID):
    while True:
        print('...........MENU...........')
        print('1. DEPOSIT AMOUNT')
        print('2. WITHDRAW AMOUNT')
        print('3. CHECK BALANCE')
        print('4. UPDATE PIN')
        print('5. UPDATE PHONE NUMBER')
        print('6. DELETE ACCOUNT')
        print('7. EXIT')
        ch=int(input('ENTER YOUR CHOICE:  '))
        if ch==1:
            deposit(ID)
        elif ch==2:
            withdraw(ID)
        elif ch==3:
            balance(ID)
        elif ch==4:
            upin(ID)
        elif ch==5:
            upn(ID)
        elif ch==6:
            delete(ID)
        else:
            break


def main():
    while True:
        print('...........TO LOGIN...........')
        print('1. NEW ACCOUNT')
        print('2. EXISTING ACCOUNT')
        print('3. EXIT')
        ch=int(input('ENTER YOUR CHOICE:  '))
        print("================================================================================")
        if ch==1:
            new_acc()
        elif ch==2:
            ID=input('ENTER CUSTOMER ID :  ')
            pin=int(input('ENTER PIN :  '))
            acc(ID,pin)
            menu(ID)
        else:
            break

main()
