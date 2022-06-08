import tkinter as tk
import tkinter.ttk as ttk
import json

# globals and constants are put under 
# the main tk.Tk object as some of them are tk objects
# (tk objects need a master to initialize)

tkMain = tk.Tk()
tkMain.title('MajiView')

DEF_IMG = '' 
tkImg = tk.PhotoImage(file=DEF_IMG) 
imgStat = 'image' if DEF_IMG else 'text'

arr, pt = [], 0
LBL_MSG = [
    'Query to get started.', # init
    'No matches! Try another maybe?'
]

def run_query(e):
    global imgStat, arr, pt
    imgStat = 'text' 
    arr, pt= [], 0
    iFileParam = ''

    with open('.\\maji.json') as jsonfile:
        db = json.load(jsonfile)
    queryInst = query.get()
    for ent in db:
        if queryInst in ent['XMP:Keyword']:
            arr.append(ent['SourceFile'])
    if arr: 
        imgStat = 'image'
        iFileParam = arr[0]
        tkMain.focus_set()
    else: 
        lblImg.configure(text=LBL_MSG[1])

    tkImg.configure(file=iFileParam)
    lblImg.configure(compound=imgStat)

def swap_img(e:tk.Event):
    global pt
    if not arr: return

    if e.keysym == 'Left' and pt > 0: pt-=1
    elif e.keysym == 'Right' and pt < len(arr) -1: pt+=1
    tkImg.configure(file=arr[pt])


frmMain = ttk.Frame()
frmMain.grid(row=0, column=0)

lblImg = ttk.Label(frmMain, compound=imgStat, image=tkImg, text=LBL_MSG[0])
lblImg.grid(row=0, column=0, sticky=tk.NSEW)

frmQuery = ttk.Frame(frmMain, padding='0 0 0 2')
frmQuery.grid(row=1, column=0)

query = tk.StringVar()
entQuery = ttk.Entry(frmQuery, textvariable=query)
entQuery.grid(row=0, column=0, sticky=tk.NW, padx=3)

switchRe = tk.IntVar(value=0)
cbRegex = ttk.Checkbutton(frmQuery, text='use regex', variable=switchRe)
cbRegex.grid(row=0, column=1, sticky=tk.NW)

tkMain.bind('<Alt-Left>', swap_img)
tkMain.bind('<Alt-Right>', swap_img)
entQuery.bind('<Return>', run_query)
tkMain.mainloop()
