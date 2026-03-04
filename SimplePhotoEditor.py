import tkinter as tk
from tkinter import filedialog
from turtle import bgcolor, title, update
from PIL import Image as I
import os
import math

hIstory = 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #file directory to the program
Iimg=Cimg=Pimg = 0 #image variables Import 
#Iimg must be the import image and is in the format of Pillow
#Cimg is a copy of the imported image and is in the formate of Pillow
#Pimg is a copy of the Copied image and is in the format of TKinter
IPWindow = IPFrame = 0 #Image preview window
pReview = 0 #Variable to tell if the window is open or not, prob dont need it and can check through seeing if IPWindow is not equal to 0

def BuildMainWindow():
    oPtionsLabel = tk.Label(root,height=1,width=1,bg='dark red')
    oPtionsLabel.place(x=0,y=0)
    rEsizeLabel = tk.Label(root, height=10,width=50,bg='dark blue')
    rEsizeLabel.place(x=0,y=100)
    importFileBTN = tk.Button(root, height=10,width=50,command=import_file)
    importFileBTN.place(x=0,y=0)
    rotateBtn = tk.Button(root, height = 10, width = 50, command=lambda:RotateImg(10))
    rotateBtn.place(x=100,y=100)

def import_file(): #imports an image of the users choosing, to be edited.
    global Iimg, Cimg
    Iimg = I.open(fp=(filedialog.askopenfilename(title='Choose an Image',filetypes=[("PNG Files", "*.png"), ("All files", "*.*")])))
    print(Iimg)
    Cimg = Iimg
    BuildPreviewWindow()
    
def BuildPreviewWindow(): #initial making of the image preview window
    global IPWindow, IPFrame, root, pReview
    pReview = 1
    IPWindow = tk.Toplevel(root,height=1000,width=1000)
    IPWindow.maxsize(width=1000, height=1000)
    IPWindow.minsize(width=1000,height=1000)
    IPFrame = tk.Frame(IPWindow,width=1000,height=1000)
    IPFrame.place(x=0,y=0)
    UpdatePreviewWindow()
    IPWindow.mainloop()
    

def UpdatePreviewWindow(): #updates the preview window when maing changes
    global IPWindow, IPFrame, Cimg, Pimg
    resizeTemp = 0
    if (Cimg.width > 1000) or  (Cimg.height > 1000):
        if Cimg.width > 1000:
            resizeTemp = Cimg.resize(size=[Cimg.width//int(int(math.sqrt((Cimg.width**2) + (Cimg.height**2)))/1000),Cimg.height//int(int(math.sqrt((Cimg.width**2) + (Cimg.height**2)))/1000)])
            resizeTemp.save(fp=os.path.join(BASE_DIR,f'Preview.png'))
        else:
            resizeTemp = Cimg.resize(size=[Cimg.width/(Cimg.height/1000),Cimg.height/(Cimg.height/1000)])
            resizeTemp.save(fp=os.path.join(BASE_DIR,f'Preview.png'))
    else:
        Cimg.save(fp=os.path.join(BASE_DIR,f'Preview.png'))
    Pimg = tk.PhotoImage(file=os.path.join(BASE_DIR,f'Preview.png'))
    ImagePreview = tk.Label(IPFrame,image=Pimg,height=IPFrame['height'],width=IPFrame['width'])
    ImagePreview.place(x=0,y=0,width=1000,height=1000)
    
    
def ResizeImg(Width, Height): #resizes the given image
    global Cimg
    Cimg = Cimg.resize([Width,Height])
    UpdatePreviewWindow()
    
def RotateImg(degrees): #rotates teh given image
    global Cimg
    Cimg = Cimg.rotate(degrees)
    UpdatePreviewWindow()
    


root = tk.Tk(className=' Simple Photo Editor') #root window of the application
root.geometry(newGeometry='1000x1000')
root.minsize(1000,1000)
root.maxsize(1000,1000)
print(root.attributes())
BuildMainWindow()









root.mainloop()
