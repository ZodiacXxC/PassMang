from pickle import POP
import tkinter as tk
from tkinter import ttk
from tkinter import END, ttk, messagebox
import random
import string
import base64
import json
from PyQt5.sip import delete
import pyperclip



def copy_and_show_message(treeview):
    selected_item = treeview.selection()
    if selected_item:
        password_to_copy = treeview.item(selected_item)['values'][2]
        pyperclip.copy(password_to_copy)
        messagebox.showinfo("Password Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Selection", "Please select a row before copying.")

def randomPassword(length=20):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    ranpassword = ''.join(random.choice(characters) for _ in range(length))
    password.delete(0, "end")
    password.insert(0, ranpassword)
    
def savePassword():
    user = name.get()
    pas = password.get()
    plat = site.get()
    if user != "" and pas != "" and plat != "":
        with open("data.json", 'r', encoding='utf-8') as json_file:
            users = json.load(json_file)
    
    
        users[user] = (plat,pas)
        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(users, json_file, ensure_ascii=False, indent=4)
    
        name.delete('0',END)
        site.delete("0",END)
        password.delete(0, "end")
    else:
        messagebox.showerror("Error","Plase fill all entry !!")

def showPassword():
    def selectRow(treeview):
        selected_item = treeview.selection()
        if selected_item:
            item = treeview.item(selected_item)
            data = item["values"]
            newName.delete("0",END)
            newName.insert(0,data[0])
            newSite.delete("0",END)
            newSite.insert(0,data[1])
        else:
            messagebox.showwarning("No Selection", "Please select a row before Controling.")
        

    def editPass():
        selected_item = treeview.selection()
        item = treeview.item(selected_item)
        data = item["values"]
        if selected_item:
            new_name = newName.get()
            new_site = newSite.get()
            treeview.item(selected_item, values=(new_name, new_site,data[2]))
            newName.delete(0, tk.END)
            newSite.delete(0,END)
            users[new_name] = (new_site,users.pop(data[0]))
            with open("data.json", "w", encoding="utf-8") as json_file:
                json.dump(users, json_file, ensure_ascii=False, indent=4)
    
    def deletePass():
        selected_item = treeview.selection()
        item = treeview.item(selected_item)
        data = item["values"]
        if selected_item:
            treeview.delete(selected_item)
            del users[data[0]]
            newName.delete(0, tk.END)
            newSite.delete(0,END)
            with open("data.json", "w", encoding="utf-8") as json_file:
                json.dump(users, json_file, ensure_ascii=False, indent=4)
        
    
    showFrame = tk.Toplevel(root)
    showFrame.title("Password Manger")
    showFrame.resizable(False, False)
    showFrame.iconbitmap(default="shield_icon.ico")
    showFrame.geometry("+%d+%d" % ((root.winfo_screenwidth() - showFrame.winfo_reqwidth()) / 2,
                                       (root.winfo_screenheight() - showFrame.winfo_reqheight()) / 2))
    custom_fonts = ("Helvetica", 12)
    showLabel = ttk.Label(showFrame, text="Password Manger", font=custom_fonts)
    showLabel.grid(row=0, column=0, sticky="nsew", padx=(200,0), pady=10)
    
    treeFrame = ttk.Frame(showFrame)
    treeFrame.grid(row=1, column=0, pady=10, padx=10)
    
    treeScroll = ttk.Scrollbar(treeFrame)
    treeScroll.pack(side="right", fill="y")
    cols = ("Name","Platform", "Password")
    treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=11)
    treeview.column("Name", width=150)
    treeview.column("Platform", width=170)
    treeview.column("Password", width=170)
    treeview.bind("<Double-Button-1>", lambda e: copy_and_show_message(treeview))
    treeview.bind("<ButtonRelease-1>",lambda e: selectRow(treeview))
    treeview.pack()
    treeScroll.config(command=treeview.yview)

    treeview.heading("#1", text="Name")
    treeview.heading("#2", text="Platform")
    treeview.heading("#3", text="Password")
    
    with open("data.json", 'r', encoding='utf-8') as json_file:
            users = json.load(json_file)
    for key, value in users.items():
        treeview.insert('', tk.END, values=(key, value[0],value[1])) 
        
    showFrame.grab_set()
    
    buttonFrame = ttk.LabelFrame(showFrame,text="Control")
    buttonFrame.grid(row=2,column=0,pady=10,padx=10)
    
    newName = ttk.Entry(buttonFrame)
    newName.grid(row=0,column=0,pady=10,padx=5)
    newSite = ttk.Entry(buttonFrame)
    newSite.grid(row=0,column=1,pady=10,padx=5)
    editButton = ttk.Button(buttonFrame,text="Edit",command=editPass)
    editButton.grid(row=0,column=2,pady=10,padx=5)
    deleteButton = ttk.Button(buttonFrame,text="Delete",command=deletePass)
    deleteButton.grid(row=0,column=3,pady=10,padx=5)
    showFrame.mainloop()

root = tk.Tk()
root.resizable(False, False)
root.title("Password Generator")
root.iconbitmap(default="shield_icon.ico")
root.geometry("+%d+%d" % ((root.winfo_screenwidth() - root.winfo_reqwidth()) / 2,
                                       (root.winfo_screenheight() - root.winfo_reqheight()) / 2))

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()
custom_font = ("Helvetica", 12) 

mainLabel = ttk.Label(frame, text="Password Generator", font=custom_font)
mainLabel.grid(row=0, column=0, sticky="nsew", padx=(80,0), pady=10)

firstFrame = ttk.LabelFrame(frame,text="Info")
firstFrame.grid(row=1,column=0,padx=5, pady=5)

labelName = ttk.Label(firstFrame,text="Name: ")
labelName.grid(row=0,column=0,padx=5, pady=5)
name = ttk.Entry(firstFrame,width=32)
name.grid(row=0,column=1,padx=5, pady=5)

labelSite = ttk.Label(firstFrame,text="Platform: ")
labelSite.grid(row=1,column=0,padx=5,pady=5)
site = ttk.Entry(firstFrame,width=32)
site.grid(row=1,column=1,padx=5, pady=5)

secFrame = ttk.LabelFrame(frame,text="Password Generator :")
secFrame.grid(row=2,column=0,padx=5, pady=5)

password = ttk.Entry(secFrame,width=32)
password.grid(row=0,column=0,padx=5, pady=5)

button = ttk.Button(secFrame,text="+",width=5,command=randomPassword)
button.grid(row=0,column=1,padx=5)

creatButton = ttk.Button(frame,text="Save",command=savePassword)
creatButton.grid(row=3,column=0,sticky="nsew", padx=10, pady=10)

showButton = ttk.Button(frame,text="Show",command=showPassword)
showButton.grid(row=4,column=0,sticky="nsew", padx=10, pady=(0,10))

root.mainloop()
