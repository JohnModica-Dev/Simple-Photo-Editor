import tkinter as tk
from tkinter import filedialog
from PIL import Image as I
from PIL import ImageTk as ITK
import os
import math

hIstory = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #file directory to the program
Iimg=Cimg=Pimg = 0 #image variables Import 
#Iimg must be the import image and is in the format of Pillow
#Cimg is a copy of the imported image and is in the formate of Pillow
#Pimg is a copy of the Copied image and is in the format of TKinter
IPWindow = IPFrame = 0 #Image preview window
SWindow = 0
pReview = 0 #Variable to tell if the window is open or not, prob dont need it and can check through seeing if IPWindow is not equal to 0
rotationAngle = 0
Image_Activated = False

def BuildMainWindow():
    Oimage = tk.PhotoImage(file=os.path.join(BASE_DIR,'TextEditorTitle.png'))
    oPtionsLabel = tk.Label(root,image=Oimage,border=0)
    oPtionsLabel.image = Oimage
    oPtionsLabel.place(x=0,y=0)
    rEsizeLabel = tk.Label(root, height=10,width=50,bg='dark blue')
    rEsizeLabel.place(x=0,y=100)
    importFileBTN = tk.Button(root, height=10,width=50,command=import_file,text='Import File')
    importFileBTN.place(x=500,y=500)
    rotateBtn = tk.Button(root, height = 10, width = 50, command=lambda:RotateImg(10))
    rotateBtn.place(x=100,y=100)

def import_file(): #imports an image of the users choosing, to be edited.
    global Iimg, Cimg, Image_Activated
    if Image_Activated:
        ask_to_save()
        return
    try:
        Iimg = I.open(fp=(filedialog.askopenfilename(title='Choose an Image',filetypes=[("PNG Files", "*.png"), ("All files", "*.*")])))
        print(Iimg)
        Cimg = Iimg
        Cimg.convert('RGBA')
        BuildPreviewWindow()
    except:
        return
    
def reset_edits():
    global rotationAngle, hIstory, Image_Activated
    Image_Activated = False
    rotationAngle = 0
    hIstory = []

def ask_to_save():
    global IPWindow, Image_Activated,SWindow
    SWindow = tk.Toplevel(root, height=200, width=400)
    Build_Save_Window()
    SWindow.focus_force()
    SWindow.transient(root)
    SWindow.grab_set()
    SWindow.wait_window(window=SWindow)
    Image_Activated = False
    
def Save_Image():
    global Cimg, SWindow, IPWindow, Iimg
    print(Cimg.info)
    Cimg.save(fp=filedialog.asksaveasfilename(title=f'Save As',initialfile=f'{Iimg.filename}',filetypes=[("PNG Files", "*.png"), ("All files", "*.*")]))
    SWindow.destroy()
    IPWindow.destroy()
    
    

    
def Build_Save_Window():
    global SWindow, IPWindow, Image_Activated
    SWindow.maxsize(400,200)
    SWindow.minsize(400,200)
    YBTN = tk.Button(master=SWindow,width=4,height=1, text='YES', command=lambda:Save_Image())
    YBTN.place(x=125, y=100)
    NBTN = tk.Button(master=SWindow,width=4,height=1, text='NO',command=lambda:(SWindow.destroy(), IPWindow.destroy(), reset_edits(), import_file()))
    NBTN.place(x=250,y=100)
    

def BuildPreviewWindow(): #initial making of the image preview window
    global IPWindow, IPFrame, root, pReview, Image_Activated
    Image_Activated = True
    pReview = 1
    IPWindow = tk.Toplevel(root,height=1000,width=1000)
    IPWindow.maxsize(width=1000, height=1000)
    IPWindow.minsize(width=1000,height=1000)
    IPFrame = tk.Frame(IPWindow,width=1000,height=1000)
    IPFrame.place(x=0,y=0)
    UpdatePreviewWindow()
    IPWindow.mainloop()
    

def UpdatePreviewWindow(): #updates the preview window when maing changes #imcomplete
    global IPWindow, IPFrame, Cimg, Pimg
    resizeTemp = 0
    resizeTemp = Cimg
    resolution = resizeTemp.height/resizeTemp.width
    if resizeTemp.height > resizeTemp.width:
        resizeTemp = resizeTemp.resize(size=[int(700/resolution),700])
    if resizeTemp.width > resizeTemp.height:
        resizeTemp = resizeTemp.resize(size=[700,int(700*resolution)])
               
    Pimg = ITK.PhotoImage(image=resizeTemp)
    ImagePreview = tk.Label(IPFrame,image=Pimg,height=700,width=700,bg='green')
    ImagePreview.place(x=IPFrame['width']//2,y=IPFrame['height']//2,anchor='center')
    
    
def ResizeImg(Width, Height): #resizes the given image
    global Cimg
    Cimg = Cimg.resize([Width,Height])
    UpdatePreviewWindow()
    
def RotateImg(degrees): #rotates teh given image
    global Cimg,Iimg, rotationAngle
    if rotationAngle == 360:
        rotationAngle = 0
    rotationAngle = rotationAngle + degrees
    Cimg = Iimg.convert('RGBA')
    Cimg = Iimg.rotate(angle=rotationAngle,expand=True)
    UpdatePreviewWindow()
    


root = tk.Tk(className=' Simple Photo Editor') #root window of the application
root.geometry(newGeometry='1000x1000')
root.minsize(1000,1000)
root.maxsize(1000,1000)
root.config(bg='#8eb897')
print(root.attributes())
BuildMainWindow()









root.mainloop()
