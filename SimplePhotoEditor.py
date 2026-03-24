import tkinter as tk
from tkinter import filedialog
from PIL import Image as I
from PIL import ImageTk as ITK
import os

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

# BuildMainWindow is the function that builds the window with all the eding features for the user, like the import button, rotate button and the size button. Need to rearrange them more
# to look nicer.
def BuildMainWindow():
    global BASE_DIR, SetSizeWidth, SetSizeHeight
    ImageNames = ['10.png','-10.png','DownArrow.png','UpArrow.png','ImportPhoto.png','TextEditorTitle.png','Save.png','Undo.png','Redo.png','SetSize.png']
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
    WidthUBtn.place(x=140,y=500)
    
    WidthDBtn = tk.Button(root,image=uiImages[2],bg='#c3e8bd',activebackground='#c3e8bd', command=lambda: WidthUpDown(-10))
    WidthDBtn.image = uiImages[2]
    WidthDBtn.place(x=365,y=500)
    
    HeightDBtn = tk.Button(root,image=uiImages[2],bg='#c3e8bd',activebackground='#c3e8bd', command=lambda: HeightUPDown(-10))
    HeightDBtn.image = uiImages[2]
    HeightDBtn.place(x=365,y=719)
    
    heightUBtn = tk.Button(root,image=uiImages[3],bg='#c3e8bd',activebackground='#c3e8bd', command=lambda: HeightUPDown(10))
    heightUBtn.image = uiImages[3]
    heightUBtn.place(x=140,y=719)
    
    SetSizeBtn = tk.Button(root,bg='#c3e8bd',activebackground='#c3e8bd', command=lambda: ResizeImg(),image=uiImages[9])
    SetSizeBtn.image = uiImages[9]
    SetSizeBtn.place(x=50,y=600)
    
    SetSizeWidth = tk.Text(root, width=3, height=1,font=["Helvetica", 53],padx=5, bg='#c3e8bd',foreground='grey',)
    SetSizeWidth.place(x = 230, y = 500)
    
    SetSizeHeight = tk.Text(root, width=3, height=1, font=['Helvetica',53], padx=5, bg='#c3e8bd', foreground='grey')
    SetSizeHeight.place(x = 230, y= 719)
    
    UnDoBtn = tk.Button(root, bg='#c3e8bd', activebackground='#c3e8bd', command=lambda: redo_or_undo('undo'), image=uiImages[7])
    UnDoBtn.image = uiImages[7]
    UnDoBtn.place(x=600,y=600)
    
    ReDoBtn = tk.Button(root, bg='#c3e8bd', activebackground='#c3e8bd', command=lambda: redo_or_undo('redo'), image=uiImages[8])
    ReDoBtn.image = uiImages[8]
    ReDoBtn.place(x=600,y=750)
    
    SaveBtn = tk.Button(root, bg='#c3e8bd', activebackground='#c3e8bd', image=uiImages[6], command=lambda: Save_Image())
    SaveBtn.image = uiImages[6]
    SaveBtn.place(x=50, y=370)

# import_file functioin allows the user to import a file and als allows a user to save an image before importing another file
def import_file(): #imports an image of the users choosing, to be edited.
    global Iimg, Cimg, Image_Activated
    fName = ''
    if Image_Activated:
        ask_to_save()
        return
    try:
        Iimg = I.open(fp=(filedialog.askopenfilename(title='Choose an Image',filetypes=[("PNG Files", "*.png"), ("All files", "*.*")])))
        print(Iimg)
        x = len(Iimg.filename) - 1
        while x != 0: # Sets the Iimg file name from the source of the file, to the files actual name
            if (Iimg.filename[x] == '/') or (Iimg.filename[x] == ':'):
                Iimg.filename = fName
                x = 0
            else:
                fName = f'{Iimg.filename[x]}{fName}'
                x = x - 1

        Cimg = Iimg
        Cimg = Cimg.convert('RGBA')
        BuildPreviewWindow()
    except:
        return
    
# reset_edits function resets the image so that if the image is deleted from the program, so is all the edit orders, history and rotation angle and width, height
def reset_edits():
    global rotationAngle, hIstory, Image_Activated, eOrder
    Image_Activated = False
    rotationAngle = 0
    hIstory = []
    eOrder = []

# ask_to_save function asks the user to save their work through a separate window. This makes all the other windows inactive whils this happens
def ask_to_save():
    global IPWindow, Image_Activated,SWindow
    SWindow = tk.Toplevel(root, height=200, width=400)
    Build_Save_Window()
    SWindow.focus_force()
    SWindow.transient(root)
    SWindow.grab_set()
    SWindow.wait_window(window=SWindow)
    Image_Activated = False
    
# Save_Image function actually saves the image that the user is working on.
def Save_Image():
    global Cimg, SWindow, IPWindow, Iimg, Image_Activated
    if Image_Activated == False:
        Build_Error_Window('You need to import an image first')
        return
    print(Cimg.info)
    Cimg.save(fp=filedialog.asksaveasfilename(title=f'Save As',initialfile=f'{Iimg.filename}',filetypes=[("PNG Files", "*.png"), ("All files", "*.*")]))
    SWindow.destroy()
    IPWindow.destroy()
    
def Build_Error_Window(Message):
    global SWindow
    SWindow = tk.Toplevel(root,height=200, width=400)
    SWindow.maxsize(width=400, height=200)
    SWindow.minsize(width=400, height=200)
    MSG = tk.Label(SWindow,text=f'{Message}')
    MSG.place(x=125,y = 50)
    BTN = tk.Button(master=SWindow,width=4,height=1, text='OK', command=lambda:(SWindow.destroy()))
    BTN.place(x=200, y=100)
    SWindow.focus_force()
    SWindow.transient(root)
    SWindow.grab_set()
    SWindow.wait_window(window=SWindow)
    
    
    
    
# Build_Save_Window function builds the save window that asks the user to save their work before importing another image.
def Build_Save_Window():
    global SWindow, IPWindow, Image_Activated
    SWindow.maxsize(400,200)
    SWindow.minsize(400,200)
    YBTN = tk.Button(master=SWindow,width=4,height=1, text='YES', command=lambda:Save_Image())
    YBTN.place(x=125, y=100)
    NBTN = tk.Button(master=SWindow,width=4,height=1, text='NO',command=lambda:(SWindow.destroy(), IPWindow.destroy(), reset_edits(), import_file()))
    NBTN.place(x=250,y=100)
    
# BuildPreviewWwindow function builds the preview window where the user can actually see their images and information
def BuildPreviewWindow(): #initial making of the image preview window
    global IPWindow, IPFrame, root, pReview, Image_Activated
    Image_Activated = True
    pReview = 1
    IPWindow = tk.Toplevel(root,height=1000,width=1000)
    IPWindow.maxsize(width=1000, height=1000)
    IPWindow.minsize(width=1000,height=1000)
    UpdatePreviewWindow()
    IPWindow.mainloop()
    

# UpdatePreviewWindow funtion allows for the image to be shown to the user on a separate window, it makes sure to resize it so that the image can be seen by the user and the window doesnt cut
# it off. I plan to add statistics to the bottom like the Size of the image, the format and the name of the image.
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
    
    
# The ResizeImg function is used to resize the image to a certain width and certain height that the user wants to put it as.
def ResizeImg(): #resizes the given image 
    global Cimg, SetSizeWidth, SetSizeHeight, eOrder, Image_Activated
    if Image_Activated == False:
        Build_Error_Window('You need to import an image first')
        return
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
    
# HeightUPDown and WidthUPDown function makes sure to add the height and width to the image editing order, it does this through adding up similar height and width adujstments, for example if
# the user wanted to add 10 to width, then add another 70 right after, its a addition of 80 to the width instead of the 10 and then the 70, this allows for further image disruption
# to be avoided.
def WidthUpDown(Value):
    global Cimg, eOrder, rotationAngle, Image_Activated
    if Image_Activated == False:
        Build_Error_Window('You need to import an image first')
        return
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
    
# HeightUPDown and WidthUPDown function makes sure to add the height and width to the image editing order, it does this through adding up similar height and width adujstments, for example if
# the user wanted to add 10 to width, then add another 70 right after, its a addition of 80 to the width instead of the 10 and then the 70, this allows for further image disruption
# to be avoided.
def HeightUPDown(Value):
    global Cimg, eOrder, rotationAngle, Image_Activated
    if Image_Activated == False:
        Build_Error_Window('You need to import an image first')
        return
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

# RotateImg function makes sure to add the degrees of rotation to the image that the user requests. instead of rotating the image in certain degrees and then stopping, it makes 
# sure to add the degrees together to further prevent image clarity disruption. For example, instead of a 10 degreee turn, then another 10 degree turn, its now a 20 degree turn
def RotateImg(degrees): #rotates the given image
    global Cimg,Iimg, rotationAngle,eOrder, undo_Check, Image_Activated
    if Image_Activated == False:
        Build_Error_Window('You need to import an image first')
        return
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
    

# reset_undo function makes sure to clear the history (hIstory) and sets the undo flag (undo_Check) to false
def reset_undo():
    global hIstory, undo_Check, Image_Activated
    if Image_Activated == False:
        Build_Error_Window('You need to import an image first')
        return
    hIstory = []
    undo_Check = False


# redo_o_undo function works by taking the editing order (eOrder), History (hIstory) and the undo check flag (undo_Check). It checks that that when the undo button is pressed,
# atleast one edit is in the editing order before proceeding, if there is non in the editing order, then it cancels further actions. The items in the editing order does not matter
# to the undo button so the undo button by passes the return and goes onto the function. The undo button makes it so that it adds it contents of the last edit to the history list
# and then deletes the contents of the last edit to the editing order, it also makes sure to check the undo flag to True so that the redo button works as intended. The redo button
# makes sure to add the last added edit from undo to the editing order and then deletes that form the History, this allows for the editing order to add back what the user tried to 
# delete, If the undo flag is not True, then the funtion exits.
def redo_or_undo(Text):
    global eOrder, hIstory, undo_Check, Image_Activated
    if Image_Activated == False:
        Build_Error_Window('You need to import an image first')
        return
    if len(eOrder) < 1:
        if Text == 'undo':
            return
    if Text == 'undo':
        hIstory.append(eOrder[len(eOrder)-2])
        hIstory.append(eOrder[len(eOrder)-1])
        eOrder.pop(len(eOrder)-1)
        eOrder.pop(len(eOrder)-1)
        undo_Check = True
        print(hIstory)
        UpdatePreviewWindow()
    elif Text == 'redo':
        if len(hIstory) > 0:
            if undo_Check == True:
                eOrder.append(hIstory[len(hIstory)-2])
                eOrder.append(hIstory[len(hIstory)-1])
                hIstory.pop(len(hIstory)-1)
                hIstory.pop(len(hIstory)-1)
                UpdatePreviewWindow()
            else:
                return
            

# BuildImage function allows for the image to be built based on the editing order (eOrder) of the image to be made. It cycles through the entire editing order for this to happen
# and makes changes as it iterates through it.
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
