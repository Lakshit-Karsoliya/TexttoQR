import customtkinter as ctk
from settings import *
import pyqrcode
import png
from pyqrcode import QRCode
from cv2 import imread , imshow  , waitKey , destroyAllWindows
import os
import sys
try:
    from ctypes import windll , byref , sizeof ,c_int
except:
    pass


def resource_path(relative_path):
    """https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile"""
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = BLACK)
        self.title('')
        self.geometry('400x220')
        self.resizable(False,False)
        self.iconbitmap(resource_path("tp.ico"))
        self.change_title_bar_color()
        self.text = ctk.StringVar()
        MainLabel(self)
        TextEntry(self,textvariable=self.text)
        ClearButton(self,self.text)
        GenerateQR(self,self.text)
        InfoLabel(self)
        self.mainloop()

    def change_title_bar_color(self):
        try:
            HNWD = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TILE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HNWD,DWMWA_ATTRIBUTE,byref(c_int(COLOR)),sizeof(c_int))
        except:
            pass

class TextEntry(ctk.CTkEntry):
    def __init__(self,parent,textvariable = None):
        super().__init__(master=parent,fg_color=BLACK,border_color=LIGHT_GRAY,height=40,width=380,font=(FONT,20),textvariable=textvariable)
        self.grid(column = 0,row =1,pady=10,padx=10   ,sticky='w')
    

class MainLabel(ctk.CTkLabel):
    def __init__(self,parent):
        # font = (family=FONT,size=20,weight='bold')
        super().__init__(master=parent,text='Enter Your Text',font=ctk.CTkFont(family=FONT,size=29,weight='bold'))
        self.grid(column=0,row=0,pady=10)

class GenerateQR(ctk.CTkButton):
    def __init__(self,parent,text):
        super().__init__(master=parent,text='Generate QR',command=lambda:self.doit())
        self.grid(column=0,row=3,pady=10)
        self.text = text
        self.image_path = None
    def doit(self):
        # print(self.text.get())
        url = pyqrcode.create(str(self.text.get())[:300])
        url.png('myqr.png', scale = 10)
        # print('qr generated')
        self.image_path = resource_path("myqr.png")
        if self.image_path:
            img = imread(self.image_path)
            imshow('QR',img)
            waitKey(0)
            destroyAllWindows()

class ClearButton(ctk.CTkButton):
    def __init__(self,parent,text):
        super().__init__(master=parent,text='Clear',command=lambda:self.clear(),fg_color=WARNING_RED,hover_color=GRAY)
        self.grid(column=0,row=2)
        self.text = text
    def clear(self):
        self.text.set('')

class InfoLabel(ctk.CTkLabel):
    def __init__(self,parent):
        font  = ctk.CTkFont(family=FONT,size=TEXT_SIZE_NANO)
        super().__init__(master=parent,text='This version only support only 300 characters. Get updates from https://github.com/Lakshit-Karsoliya',font=font)
        self.grid(column=0,row=4,padx=5)
        
if __name__ == '__main__':
    App()
