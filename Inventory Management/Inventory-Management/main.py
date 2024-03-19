#import all the modules
from update import main
from add_to_db import main2
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox
import datetime
import math



date=datetime.datetime.now().date()
#temporary list like sessions
products_list=[]
product_price=[]
product_quantity=[]
product_id=[]
r = []


class Application():
    def __init__(self,master,*args,**kwargs):

        self.master=master
        self.left = Frame(master, width=666, height=768, bg='#DDD0C8')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=666, height=768, bg='#DDD0C8')
        self.right.pack(side=RIGHT)


        #components
        self.heading=Label(self.left,text="Inventory Management System",font=('arial 20 bold'),fg='black',bg='#DDD0C8')
        self.heading.place(x=0,y=60)

        self.date_l=Label(self.right,text="Today's Date: "+str(date),font=('arial 10 bold'),bg='#DDD0C8',fg='black')
        self.date_l.place(x=0,y=0)

        #table invoice=======================================================
        self.tproduct=Label(self.right,text="Products",font=('arial 12 bold'),bg='#DDD0C8',fg='black')
        self.tproduct.place(x=0,y=60)

        self.tquantity = Label(self.right, text="Quantity", font=('arial 12 bold'), bg='#DDD0C8', fg='black')
        self.tquantity.place(x=300, y=60)

        self.tamount = Label(self.right, text="Amount", font=('arial 12 bold'), bg='#DDD0C8', fg='black')
        self.tamount.place(x=500, y=60)

        #enter stuff
        self.enterid=Label(self.left,text="Enter Product's ID",font=('arial 12 bold'),fg='black',bg='#DDD0C8')
        self.enterid.place(x=0,y=110)


        self.enteride=Entry(self.left,width=25,font=('arial 12 bold'),bg='lightblue')
        self.enteride.place(x=220,y=110)
        self.enteride.focus()

        
        #button
        self.search_btn=Button(self.left,text="Search",width=22,height=2,fg='white',bg='black', command=self.ajax)
        self.search_btn.place(x=380,y=150)

        # Update Button
        self.update=Button(self.left,text="Update To Database",width=20,height=2,fg='white',bg='black', command=main)
        self.update.place(x=0,y=0)

        # Add to DB Button
        self.add=Button(self.left,text="Add To Database",width=20,height=2,fg='white',bg='black',command=main2)
        self.add.place(x=200,y=0)

        #fill it later by the fuction ajax

        self.productname=Label(self.left,text="",font=('arial 27 bold'),bg='black',fg='steelblue')
        self.productname.place(x=0,y=250)

        self.pprice = Label(self.left, text="", font=('arial 27 bold'), bg='black', fg='steelblue')
        self.pprice.place(x=0, y=290)

        #total label
        self.total_l=Label(self.right,text="",font=('arial 40 bold'),bg='lightblue',fg='black')
        self.total_l.place(x=0,y=600)
    def ajax(self,*args,**kwargs):
        self.conn = mysql.connector.connect(host='localhost',
                                       database='inventory_system',
                                       user='root',
                                       password='')
        self.get_id=self.enteride.get()
        #get the product info with that id and fill i the labels above
        self.mycursor = self.conn.cursor()
        self.mycursor.execute("SELECT * FROM inventory WHERE id= %s",[self.get_id])
        self.pc = self.mycursor.fetchall()
        if self.pc:
          for self.r in self.pc:
            self.get_id=self.r[0]
            self.get_name=self.r[1]
            self.get_price=self.r[3]
            self.get_stock=self.r[2]
          self.productname.configure(text="Product's Name: " +str(self.get_name),fg='black',bg='#DDD0C8')
          self.pprice.configure(text="Price:₹. "+str(self.get_price),fg='black',bg='#DDD0C8')


        #craete the quantity and the discount label
          self.quantityl=Label(self.left,text="Enter Quantity",font=('arial 12 bold'),fg='black',bg='#DDD0C8')
          self.quantityl.place(x=0,y=370)

          self.quantity_e=Entry(self.left,width=25,font=('arial 12 bold'),bg='lightblue')
          self.quantity_e.place(x=190,y=370)
          self.quantity_e.focus()

        #discount
          self.discount_l = Label(self.left, text="Enter Discount in ₹", font=('arial 12 bold'),fg='black',bg='#DDD0C8')
          self.discount_l.place(x=0, y=410)


          self.discount_e = Entry(self.left, width=25, font=('arial 12 bold'), bg='lightblue')
          self.discount_e.place(x=190, y=410)
          self.discount_e.insert(END,0)


        #add to cart button
          self.add_to_cart_btn = Button(self.left, text="Add to Cart", width=22, height=2, bg='black',fg='#DDD0C8', command=self.add_to_cart)
          self.add_to_cart_btn.place(x=350, y=450)

        #genrate bill and change
          self.change_l=Label(self.left,text="Given Amount",font=('arial 12 bold'),fg='black',bg='#DDD0C8')
          self.change_l.place(x=0,y=550)

          self.change_e=Entry(self.left,width=25,font=('arial 12 bold'),bg='lightblue')
          self.change_e.place(x=190,y=550)

          self.change_btn= Button(self.left, text="Calculate Change", width=22, height=2, bg='black',fg='#DDD0C8', command=self.change_func)
          self.change_btn.place(x=350, y=590)

        #geneerate bill button
          self.bill_btn = Button(self.left, text="Generate Bill", width=100, height=2, bg='black',fg='#DDD0C8',command=self.generate_bill)
          self.bill_btn.place(x=0, y=640)
        else:
             messagebox.showinfo("Succesfully Done Everything Smoothly", "Thank you for your recent purchase. We are honored to gain you as a customer and hope to serve you for a long time. We just want to drop a quick note to express our genuine gratitude. Your purchase allows us at Inventory Management System to continue to do what we love and provide you with quality products.")

    def add_to_cart(self,*args,**kwargs):
        self.quantity_value=int(self.quantity_e.get())

        if  self .quantity_value >int(self.get_stock):
            tkinter.messagebox.showinfo("Error","We Don't have that much products in stock.")
        else:
            #calculate the price first
            self.final_price=(float(self.quantity_value) * float(self.get_price))-(float(self.discount_e.get()))
            products_list.append(self.get_name)
            product_price.append(self.final_price)
            product_quantity.append(self.quantity_value)
            product_id.append(self.get_id)

            self.x_index=0
            self.y_index=100
            self.counter=0
            for self.p in products_list:
                self.tempname=Label(self.right,text=str(products_list[self.counter]),font=('arial 12 bold'),bg='#DDD0C8',fg='black')
                self.tempname.place(x=0,y=self.y_index)
                self.tempqt = Label(self.right, text=str(product_quantity[self.counter]), font=('arial 12 bold'), bg='#DDD0C8', fg='black')
                self.tempqt.place(x=300, y=self.y_index)
                self.tempprice = Label(self.right, text=str(product_price[self.counter]), font=('arial 12 bold'), bg='#DDD0C8', fg='black')
                self.tempprice.place(x=500, y=self.y_index)

                self.y_index+=40
                self.counter+=1


                #total confugure
                self.total_l.configure(text="Total : Rs. "+str(sum(product_price)),bg='#DDD0C8',fg='black')
                #delete
                self.quantity_e.place_forget()
                self.discount_l.place_forget()
                self.discount_e.place_forget()
                self.productname.configure(text="")
                self.pprice.configure(text="")
                self.add_to_cart_btn.destroy()
                #autofocus to the enter id
                self.enteride.focus()
                self.quantityl.focus()
                self.enteride.delete(0,END)

  
    def change_func(self,*args,**kwargs):
        self.amount_given=float(self.change_e.get())
        self.our_total=float(sum(product_price))

        self.to_give=self.amount_given-self.our_total

        #label change
        self.c_amount=Label(self.left,text="Change: Rs. "+str(self.to_give),font=('arial 12 bold'),fg='red',bg='#DDD0C8')
        self.c_amount.place(x=0 ,y=600)

    def generate_bill(self,*args,**kwargs):
        self.mycursor.execute("SELECT * FROM inventory WHERE id=%s",[self.get_id])
        self.pc = self.mycursor.fetchall()
        for r in self.pc:
            self.old_stock=r[2]
        for i in products_list:
            for r in self.pc:
                self.old_stock = r[2]
            self.new_stock=int(self.old_stock) - int(self.quantity_value)
            #updating the stock
            self.mycursor.execute("UPDATE inventory SET stock=%s WHERE id=%s",[self.new_stock,self.get_id])
            self.conn.commit()

            #inster into transcation
            self.mycursor.execute("INSERT INTO transaction (product_name,quantity,amount,date) VALUES(%s,%s,%s,%s)",[self.get_name,self.quantity_value,self.get_price,date])
            self.conn.commit()
            print("Decreased, Your Item is booked and sent soon within Working Days","Thank you for your recent purchase. We are honored to gain you as a customer and hope to serve you for a long time. We just want to drop a quick note to express our genuine gratitude. Your purchase allows us at Inventory Management to continue to do what we love and provide you with quality products.")


        tkinter.messagebox.showinfo("Succesfully Done Everything Smoothly", "Thank you for your recent purchase. We are honored to gain you as a customer and hope to serve you for a long time. We just want to drop a quick note to express our genuine gratitude. Your purchase allows us at Inventory Management to continue to do what we love and provide you with quality products.")
        tkinter.messagebox.showinfo("Thank You","You Will Get your order soon")




root=tk.Tk()
Application(root)
root.geometry("1366x768+0+0")
root.title( "Inventory Management by Aditya Konda")
root.mainloop()