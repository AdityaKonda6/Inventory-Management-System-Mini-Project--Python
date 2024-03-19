#import all the modules
from tkinter import *
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox

conn=mysql.connector.connect(host='localhost',
                                       database='inventory_system',
                                       user='root',
                                       password='')
mycursor = conn.cursor()
mycursor.execute("SELECT Max(id) from inventory")
result = mycursor.fetchall()
for r in result:
    id=r[0]

class Database:
    def __init__(self,master,*args,**kwargs):
         self.master=master
         self.heading=Label(master,text="Update to the databse",font=('arial 40 bold'),fg='steelblue')
         self.heading.place(x=400,y=0)

         #label and entry for id
         self.id_le=Label(master,text="Enter ID",font=('arial 18 bold'))
         self.id_le.place(x=0,y=70)

         self.id_leb=Entry(master,font=('arial 18 bold'),width=10)
         self.id_leb.place(x=380,y=70)

         self.btn_search=Button(master,text="search",width=15,height=2,bg='orange',command=self.search)
         self.btn_search.place(x=550,y=70)

         #lables  for the window
         self.name_l=Label(master,text="Enter Product Name",font=('arial 18 bold'))
         self.name_l.place(x=0,y=120)

         self.stock_l=Label(master,text="Enter Stocks",font=('arial 18 bold'))
         self.stock_l.place(x=0,y=170)

         self.cp_l = Label(master, text="Enter Cost Price ", font=('arial 18 bold'))
         self.cp_l.place(x=0, y=220)


        #enteries for window

         self.name_e=Entry(master,width=25,font=('arial 18 bold'))
         self.name_e.place(x=380,y=120)

         self.stock_e = Entry(master, width=25, font=('arial 18 bold'))
         self.stock_e.place(x=380, y=170)

         self.cp_e = Entry(master, width=25, font=('arial 18 bold'))
         self.cp_e.place(x=380, y=220)


         #button to add to the database
         self.btn_add=Button(master,text='Update Database',width=25,height=2,bg='steelblue',fg='white',command=self.update)
         self.btn_add.place(x=520,y=300)



          #text box for the log
         self.tbBox=Text(master,width=60,height=18)
         self.tbBox.place(x=750,y=70)
         self.tbBox.insert(END,"ID has reached up to:"+str(id))

    def search(self, *args, **kwargs):
         mycursor.execute("SELECT * FROM inventory WHERE id=%s",[self.id_leb.get()])
         result = mycursor.fetchall()
         for r in result:
              self.n1 = r[1]  # name
              self.n2 = r[2]  # stock
              self.n3 = r[3]  # cp
         conn.commit()

          #inster into the enteries to update
         self.name_e.delete(0,END)
         self.name_e.insert(0, str(self.n1))

         self.stock_e.delete(0, END)
         self.stock_e.insert(0, str(self.n2))

         self.cp_e.delete(0, END)
         self.cp_e.insert(0, str(self.n3))

    def update(self,*args,**kwargs):
          self.u1=self.name_e.get()
          self.u2 = self.stock_e.get()
          self.u3 = self.cp_e.get()


          mycursor.execute("UPDATE  inventory SET name=%s,stock=%s,price=%s WHERE id=%s",[self.u1,self.u2,self.u3,self.id_leb.get()])
          conn.commit()
          tkinter.messagebox.showinfo("Success","Update Database successfully")

def main():
     root=Tk()
     b=Database(root)
     root.geometry("1366x768+0+0")
     root.title("Update to the database")
     root.mainloop()