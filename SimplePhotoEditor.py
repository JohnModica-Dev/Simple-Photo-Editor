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
IPWindow = IPFrame = SetSizeWidth = SetSizeHeight = 0 #Image preview window
SWindow = 0
pReview = undo_Check = False #Variable to tell if the window is open or not, prob dont need it and can check through seeing if IPWindow is not equal to 0
rotationAngle = 0
Image_Activated = False
eOrder = []


def BuildMainWindow():
    global BASE_DIR, SetSizeWidth, SetSizeHeight
    ImageNames = ['10.png','-10.png','DownArrow.png','UpArrow.png','ImportPhoto.png','TextEditorTitle.png']
    uiImages = []
    x = 0
    while x != len(ImageNames):
        uiImages.append(tk.PhotoImage(file=os.path.join(BASE_DIR,str(ImageNames[x]))))
        x = x + 1
    
    oPtionsLabel = tk.Label(root,image=uiImages[5],borderwidth=0)
    oPtionsLabel.image = uiImages[5]
    oPtionsLabel.place(x=0,y=0)

    importFileBTN = tk.Button(root,command=import_file,text='Import File',image=uiImages[4],bg='#c3e8bd', activebackground='#c3e8bd')
    importFileBTN.image = uiImages[4]
    importFileBTN.place(x=50,y=250)

    rotateBtn = tk.Button(root,image=uiImages[0], command=lambda:RotateImg(10),bg='#c3e8bd',activebackground='#c3e8bd')
    rotateBtn.image = uiImages[0]
    rotateBtn.place(x=800,y=250)

    NrotateBtn = tk.Button(root, image=uiImages[1],command=lambda:RotateImg(-10),bg='#c3e8bd',activebackground='#c3e8bd')
    NrotateBtn.image = uiImages[1]
    NrotateBtn.place(x=600,y=250)
    
    WidthUBtn = tk.Button(root,image=uiImages[3],bg='#c3e8bd',activebackground='#c3e8bd',command=lambda: WidthUpDown(10))
    WidthUBtn.image = uiImages[3]
    WidthUBtn.place(x=200,y=500)
    
    WidthDBtn = tk.Button(root,image=uiImages[2],bg='#c3e8bd',activebackground='#c3e8bd', command=lambda: WidthUpDown(-10))
    WidthDBtn.image = uiImages[2]
    WidthDBtn.place(x=300,y=500)
    
    HeightDBtn = tk.Button(root,image=uiImages[2],bg='#c3e8bd',activebackground='#c3e8bd', command=lambda: HeightUPDown(-10))
    HeightDBtn.image = uiImages[2]
    HeightDBtn.place(x=300,y=700)
    
    heightUBtn = tk.Button(root,image=uiImages[3],bg='#c3e8bd',activebackground='#c3e8bd', command=lambda: HeightUPDown(10))
    heightUBtn.image = uiImages[3]
    heightUBtn.place(x=200,y=700)
    
    SetSizeBtn = tk.Button(root,width=10,height=10,bg='#c3e8bd',activebackground='#c3e8bd', command=lambda: ResizeImg())
    SetSizeBtn.place(x=300,y=800)
    
    SetSizeWidth = tk.Text(root, width=10, height=10)
    SetSizeWidth.place(x = 500, y = 800)
    
    SetSizeHeight = tk.Text(root, width=10, height=10)
    SetSizeHeight.place(x = 500, y= 900)
    
    UnDoBtn = tk.Button(root, width=10, height=10, bg='#c3e8bd', activebackground='#c3e8bd', command=lambda: redo_or_undo('undo'))
    UnDoBtn.place(x=900,y=600)
    
    ReDoBtn = tk.Button(root, width=10,height=10, bg='#c3e8bd', activebackground='#c3e8bd', comman=lambda: redo_or_undo('redo'))
    ReDoBtn.place(x=900,y=900)

def import_file(): #imports an image of the users choosing, to be edited.
    global Iimg, Cimg, Image_Activated
    if Image_Activated:
        ask_to_save()
        return
    try:
        Iimg = I.open(fp=(filedialog.askopenfilename(title='Choose an Image',filetypes=[("PNG Files", "*.png"), ("All files", "*.*")])))
        print(Iimg)
        Iimg = Iimg.convert('RGBA')
        Cimg = Iimg
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
    UpdatePreviewWindow()
    IPWindow.mainloop()
    

def UpdatePreviewWindow(): #updates the preview window when maing changes #imcomplete
    global IPWindow, IPFrame, Cimg, Pimg, hIstory, eOrder
    if IPFrame != 0:
        IPFrame.destroy()
    IPFrame = tk.Frame(IPWindow,width=1000,height=1000)
    IPFrame.place(x=0,y=0)
    resizeTemp = 0
    BuildImage()
    
    resizeTemp = Cimg
    resolution = resizeTemp.height/resizeTemp.width
    if resizeTemp.height > resizeTemp.width:
        resizeTemp = resizeTemp.resize(size=[int(700/resolution),700])
    if resizeTemp.width > resizeTemp.height:
        resizeTemp = resizeTemp.resize(size=[700,int(700*resolution)])
               
    Pimg = ITK.PhotoImage(image=resizeTemp)
    ImagePreview = tk.Label(IPFrame,image=Pimg,height=700,width=700,bg='green')
    ImagePreview.place(x=IPFrame['width']//2,y=IPFrame['height']//2,anchor='center')
    
    
def ResizeImg(): #resizes the given image 
    global Cimg, SetSizeWidth, SetSizeHeight, eOrder
    RotateImg(0)
    print(f'the starting width is {Cimg.width} and the starting height is {Cimg.height}')
    try:
        if int(SetSizeWidth.get(1.0,'end')) > Cimg.width:
            WidthUpDown(int(SetSizeWidth.get(1.0,'end')) - Cimg.width)
            print(f'Image upscaled the width to {Cimg.width}')
        else:
            WidthUpDown(int(SetSizeWidth.get(1.0,'end')) - Cimg.width)
            print(f'Image upscaled the width to {Cimg.width}')
        if int(SetSizeHeight.get(1.0,'end')) > Cimg.height:
            HeightUPDown(int(SetSizeHeight.get(1.0,'end')) - Cimg.height)
            print(f'Image upscaled the height to {Cimg.height}')
        else:
            HeightUPDown(int(SetSizeHeight.get(1.0,'end')) - Cimg.height)
            print(f'Image upscaled the height to {Cimg.height}')
    except:
        print(f'I only expect numbers! I expect spaces and letters to throw an error! if you only put the numbers then it might think its a string instead of an integer')
    print(int(SetSizeWidth.get(1.0, 'end')))
    print(int(SetSizeHeight.get(1.0, 'end')))
    reset_undo()
    UpdatePreviewWindow()
    
def WidthUpDown(Value):
    global Cimg, eOrder, rotationAngle
    try:
        if eOrder[len(eOrder)-2] == 'w':
            eOrder[len(eOrder)-1] = eOrder[len(eOrder)-1] + Value
        else:
            eOrder.append('w')
            eOrder.append(Value)
    except:
        eOrder.append('w')
        eOrder.append(Value)
        print(f'No List yet')
    rotationAngle = 0
    reset_undo()
    UpdatePreviewWindow()
    
def HeightUPDown(Value):
    global Cimg, eOrder, rotationAngle
    try:
        if eOrder[len(eOrder)-2] == 'h':
            eOrder[len(eOrder)-1] = eOrder[len(eOrder)-1] + Value
        else:
            eOrder.append('h')
            eOrder.append(Value)
    except:
        eOrder.append('h')
        eOrder.append(Value)
        print(f'No List yet')
    rotationAngle = 0
    reset_undo()
    UpdatePreviewWindow()

def RotateImg(degrees): #rotates the given image
    global Cimg,Iimg, rotationAngle,eOrder, undo_Check
    if (rotationAngle == 360) or (rotationAngle == -360):
        rotationAngle = 0
    rotationAngle = rotationAngle + degrees
    try:
        if eOrder[len(eOrder)-2] == 'r':
            eOrder.pop(len(eOrder)-1)
            eOrder.pop(len(eOrder)-1)
    except:
        print(f'No List yet')
    eOrder.append('r')
    eOrder.append(rotationAngle)
    #Cimg = Iimg.rotate(angle=rotationAngle,expand=True)
    reset_undo()
    UpdatePreviewWindow()
    
def reset_undo():
    global hIstory, undo_Check
    hIstory = []
    undo_Check = False

def redo_or_undo(Text):
    global eOrder, hIstory, undo_Check
    if len(eOrder) < 1:
        return
    if Text == 'undo':
        hIstory.append(eOrder[len(eOrder)-2])
        hIstory.append(eOrder[len(eOrder)-1])
        eOrder.pop(len(eOrder)-1)
        eOrder.pop(len(eOrder)-1)
        undo_Check = True
        UpdatePreviewWindow()
    elif Text == 'redo':
        if undo_Check == True:
            eOrder.append(hIstory[len(hIstory)-2])
            eOrder.append(hIstory[len(hIstory)-1])
            hIstory.pop(len(hIstory)-1)
            hIstory.pop(len(hIstory)-1)
            UpdatePreviewWindow()
            

def BuildImage():
    global eOrder, Cimg, Iimg
    x = 0 
    Cimg = Iimg
    while x != len(eOrder):
        match eOrder[x]:
            case 'r':
                Cimg = Cimg.rotate(angle=eOrder[x+1],expand=True)
                x = x + 2
            case 'h':
                Cimg = Cimg.resize(size=[Cimg.width,Cimg.height+eOrder[x+1]])
                x = x + 2
            case 'w':
                Cimg = Cimg.resize(size=[Cimg.width+eOrder[x+1],Cimg.height])
                x = x + 2
    print(eOrder)
    


root = tk.Tk(className=' Simple Photo Editor') #root window of the application
root.geometry(newGeometry='1000x1000')
root.minsize(1000,1000)
root.maxsize(1000,1000)
root.config(bg='#8eb897')
print(root.attributes())
BuildMainWindow()









root.mainloop()
