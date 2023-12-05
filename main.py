import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import askdirectory
import qrcode
from PIL import Image, ImageTk, ImageFilter
import os
import urllib.parse
import CardCreator as cardmodule

#init app
root = Tk()
root.title("QR Generator")
root.geometry('840x680')
root.iconbitmap('qrgenicon.ico')

inputframe_color = "#f5f6fa"
outputframe_color = "#f5f6fa"
label_font = "Helvetica 14 bold"
label_font_color = "#353b48"
entry_font = "Helvetica 12 bold"

frame = tkinter.Frame(root, bg="white", relief=FLAT)
frame.pack()
inputframe = tkinter.LabelFrame(frame, bg=inputframe_color, relief="flat")
inputframe.grid(row=0, column=0, sticky="nsew")
outputframe = LabelFrame(frame, bg=outputframe_color, relief=GROOVE)
outputframe.grid(row=1, column=0, sticky="nsew")

global link
link = StringVar()
global name
name = StringVar()
global dir
with open("text/dirpath.txt") as file:
    dir = file.read()
    file.close()


def decodeUrl(url):
    return urllib.parse.unquote(url)

def getLinkInput():
    return linkInput.get()

def getNameInput():
    return nameInput.get()

def getLink():
    return link

def setLink(lin):
    global link
    link = lin

def getName():
    return name

def setName(nam):
    global name
    name = nam

def getDir():
    return dir

def setDir(di):
    global dir
    dir = di


def findPattern():
    link = getLink()
    pattern = "https://diez.co.il/product/"
    if link.find(pattern) == -1:
        return False
    return True

#buttons:
def clearLink():
    linkInput.delete(0,END)

def clearName():
    nameInput.delete(0,END)

def clearAll():
    linkInput.delete(0, END)
    nameInput.delete(0,END)

def makeUrlPretty():
    decoded = decodeUrl(getLinkInput())
    setLink(decoded)
    linkInput.delete(0,END)
    linkInput.insert(0, decoded)
    if findPattern():
        nameInput.delete(0, END)
        nameInput.insert(0, decoded[27:(len(decoded)-1)])


def updateDirLabel():
    pathLabel.config(text=getDir())

def selectDir():
    path = tkinter.filedialog.askdirectory(title="Select Save Location") + "/"
    setDir(path)
    with open("text/dirpath.txt", 'w') as file:
        file.flush()
        file.write(path)
        file.close()
    updateDirLabel()

def helpPopup():
    with open("text/TroubleshootingQR.txt", "r") as help:
        helpmsg = help.read()
        help.close()
    messagebox.showinfo(title="Trouble Shooting", message=helpmsg)

def on_enter(e):
    e.widget['background'] = "#00a8ff"

def on_enter_icon(e):
    e.widget['background'] = "#0B0B45"


def on_leave(e):
    e.widget['background'] = "#d1d8e0"

def on_leave_icon(e):
    e.widget['background'] = outputframe_color

def createQR():
    # set the link
    setLink(getLinkInput())
    link = getLink()
    if link == "":  # no link input
        tkinter.messagebox.showwarning(title="Empty Field", message="Please enter a link")
        return
    setName(getNameInput())
    if getName() == "":  # no name input
        setName("myQRcode")  # auto generated name
    fail = False  # indication for generating qr process success
    try:
        url = link
        img = qrcode.make(url)  # create a qr code from the link
        img.save(getDir() + getName() + '.jpg', 'JPEG')  # save the qr as an image with the relevant name
    except:
        tkinter.messagebox.showerror(title="Problem Generating QR",
                                     message="There was an error with the process, please check the input fields")
        fail = True
    if not fail:
        successmsg = ("file " + getName() + " was create successfully at " + getDir())
        messagebox.showinfo(title="QR Generated", message=successmsg)

def getBrand():
    return brandInput.get()

def getModel():
    return modelInput.get()

def convertToPixel(cm_num):
    return int(float(cm_num)*38)

def getCardWidth():
    w = widthInput.get()
    if len(w) == 0 or len(w)>100:
        w = '3.5'
    return convertToPixel(w)

def getCardHeight():
    h = heightInput.get()
    if len(h) == 0 or len(h)>100:
        h = '7'
    return convertToPixel(h)

def createCardQR():
    # set the link
    setLink(getLinkInput())
    link = getLink()
    if link == "":  # no link input
        tkinter.messagebox.showwarning(title="Empty Field", message="Please enter a link")
        return
    setName(getNameInput())
    if getName() == "":  # no name input
        setName("myQRcode")  # auto generated name
    fail = False  # indication for generating qr process success
    try:
        url = link
        qrimg = qrcode.make(url)  # create a qr code from the link
        brand_card = getBrand()
        model_card = getModel()
        card_width = getCardWidth()
        card_height = getCardHeight()
        cc = cardmodule.CardCreator(brand_card, model_card, qrimg, width=card_width, height=card_height)
        img = cc.getCard()
        img.save(getDir() + getName() + '.jpg', 'JPEG')  # save the card as an image with the relevant name
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror(title="Problem Generating QR",
                                     message="There was an error with the process, please check the input fields or contact help")
        fail = True
    if not fail:
        successmsg = ("file " + getName() + " was create successfully at " + getDir())
        messagebox.showinfo(title="QR Generated", message=successmsg)
#components
delicon = ImageTk.PhotoImage(Image.open('images/delbtn.png').resize((27,25), Image.Resampling.LANCZOS))
diricon = ImageTk.PhotoImage(Image.open('images/dirselect.png').resize((32,26), Image.Resampling.LANCZOS))
helpicon = ImageTk.PhotoImage(Image.open('images/helpiconnobg.png').resize((60,60), Image.Resampling.LANCZOS))
createQRicon = ImageTk.PhotoImage(Image.open('images/playicon.png').resize((100,100), Image.Resampling.LANCZOS))
createCardicon = ImageTk.PhotoImage(Image.open('images/createCardBtn.png').resize((110,110), Image.Resampling.LANCZOS))
linkLabel = Label(inputframe, width=10, padx=20, pady=10, text="Link:", background=inputframe_color, font=label_font, anchor="w", fg=label_font_color)
linkInput = Entry(inputframe, width=80)
clearLinkBtn = Button(inputframe, width=28, height=26, padx=10, pady=5, text="Clear Link", command=clearLink, bg="#f5f6fa", activebackground="#7f8fa6", font="Helvetica",
 relief="flat", image=delicon)

#checkbox = Checkbutton(inputframe, width=40, padx=5, text="Short URL (make a cleaner QR)", variable=short, bg="#f5f6fa", activebackground="#f5f6fa", font="Helvetica 12 bold")

nameLabel = Label(inputframe, width=10, padx=20, pady=10, text="Image name:", background=inputframe_color, font=label_font, anchor="w", fg=label_font_color)
nameInput = Entry(inputframe, width=53, font=entry_font)
clearNameBtn = Button(inputframe, width=28, height=26, padx=10, text="Clear Name", command=clearName, bg=inputframe_color, activebackground="#7f8fa6", font="Helvetica",
 relief="flat", image=delicon)

brandLabel = Label(inputframe, width = 10, padx = 20, pady = 10, text= "Enter brand:", background=inputframe_color, font =label_font, anchor="w",fg=label_font_color)
brandInput = Entry(inputframe, width = 60, font =entry_font)
modelLabel = Label(inputframe, width = 10, padx = 20, pady = 10, text= "Enter model\n(short):", background=inputframe_color, font =label_font, anchor="w",fg=label_font_color)
modelInput = Entry(inputframe, width = 60, font= entry_font)

widthLabel = Label(inputframe, width = 14, padx = 2, pady = 10, text= "Image width in cm:", background=inputframe_color, font =label_font, anchor="w",fg=label_font_color)
widthInput = Entry(inputframe, width = 3, font=entry_font, justify="center")
widthInput.insert(0, "3.5")
heightLabel = Label(inputframe, width = 14, padx = 2, pady = 10, text= "Image height in cm:", background=inputframe_color, font =label_font, anchor="w",fg=label_font_color)
heightInput = Entry(inputframe, width = 3, font=entry_font, justify="center")
heightInput.insert(0, "7")

clearAllBtn = Button(inputframe, width=14, padx=20, pady=5, text="Clear All", command=clearAll, bg="#d1d8e0", activebackground="#7f8fa6", font="Helvetica 12 bold",
 relief="flat")
formatBtn = Button(inputframe, width=14, padx=20, pady=5, text="Format Link", command=makeUrlPretty, bg="#d1d8e0", activebackground="#7f8fa6", font="Helvetica 12 bold",
 relief="flat")

selectLabel = Label(inputframe, width=16, pady=20, text="Select File Location:", background=inputframe_color, font=label_font, anchor="w", fg=label_font_color)
selectBtn = Button(inputframe, width=32, text="Select Folder", command=selectDir, bg=inputframe_color, activebackground="#7f8fa6", font="Helvetica",
 relief="flat", image=diricon)


dirLabel = Label(outputframe, width=18, padx=10, pady=20, text="File will be saved at:", background=outputframe_color, font=label_font, anchor="w", fg=label_font_color)
pathLabel = Label(outputframe, width = 50, padx=5, text=getDir(), background=outputframe_color, font="Times-New-Roman 12 bold", anchor="w", fg="Black")
createQRLabel = Label(outputframe, width = 20, pady=5, text="Create QR Code", background=outputframe_color, font="Helvetica 12 bold", anchor="n", fg="Black")
createQRBtn = Button(outputframe, width=100, padx=10, pady=2, text="Generate QR", command=createQR, bg=outputframe_color, activebackground="#7f8fa6", font="Helvetica",
 relief="flat", image= createQRicon)
createCardLabel = Label(outputframe, width = 20, pady=5, text="Create Card with QR", background=outputframe_color, font="Helvetica 12 bold", anchor="n", fg="Black")
createCardBtn = Button(outputframe, width=100, padx=10, pady=2, text="Generate Card", command=createCardQR, bg=outputframe_color, activebackground="#7f8fa6", font="Helvetica",
 relief="flat", image= createCardicon)

helpBtn = Button(outputframe, width=62, text="Trouble Shooting", command=helpPopup, bg=inputframe_color, activebackground="#7f8fa6", font="Helvetica",
 relief="flat", image=helpicon)


#bind buttons to hover style
clearLinkBtn.bind("<Enter>", on_enter)
clearLinkBtn.bind("<Leave>", on_leave_icon)
clearNameBtn.bind("<Enter>", on_enter)
clearNameBtn.bind("<Leave>", on_leave_icon)
clearAllBtn.bind("<Enter>", on_enter)
clearAllBtn.bind("<Leave>", on_leave)
formatBtn.bind("<Enter>", on_enter)
formatBtn.bind("<Leave>", on_leave)
selectBtn.bind("<Enter>", on_enter)
selectBtn.bind("<Leave>", on_leave_icon)
createQRBtn.bind("<Enter>", on_enter_icon)
createQRBtn.bind("<Leave>", on_leave_icon)
createCardBtn.bind("<Enter>", on_enter_icon)
createCardBtn.bind("<Leave>", on_leave_icon)
helpBtn.bind("<Enter>", on_enter)
helpBtn.bind("<Leave>", on_leave_icon)



#positions

#input frame:
linkLabel.grid(row=0, column=0, columnspan=2)
linkInput.grid(row=0, column=3, columnspan=2)
clearLinkBtn.grid(row=0, column=5)

nameLabel.grid(row=1, column=0, columnspan=2)
nameInput.grid(row=1, column=3, columnspan=2)
clearNameBtn.grid(row=1, column=5)

clearAllBtn.grid(row=2, column=0, columnspan=4)
formatBtn.grid(row=2, column=4, columnspan=1)

selectLabel.grid(row=3, column=0, columnspan=3)
selectBtn.grid(row=3, column=2, columnspan=2)

brandLabel.grid(row=4, column=0, columnspan=2)
brandInput.grid(row=4, column=2, columnspan=3)

modelLabel.grid(row=5, column=0, columnspan=2)
modelInput.grid(row=5, column=2, columnspan=3)

widthLabel.grid(row=6, column=1, columnspan=3)
widthInput.grid(row=6, column=2, columnspan=3)
heightLabel.grid(row=7, column=1, columnspan=3)
heightInput.grid(row=7, column=2, columnspan=3)

#checkbox.grid(row=4, column=1)

#output frame:

dirLabel.grid(row=0, column=0, columnspan=2)
pathLabel.grid(row=0, column=2)
createQRBtn.grid(row=1, column=0, columnspan=2)
createQRLabel.grid(row=2, column=0, columnspan=2)
createCardBtn.grid(row=1, column=2, columnspan=2)
createCardLabel.grid(row=2, column=2, columnspan=2)
helpBtn.grid(row=2, column=3)








root.mainloop()



