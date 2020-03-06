import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from track import Track

class GUI:
    def __init__(self,  window):
        window.title("GPX evaluation tool")
        window.minsize(700,400)


        openFrame = Frame(window)
        openFrame.pack()
        evalFrame = Frame(window)
        evalFrame.pack()
        grafFrame = Frame(window)
        grafFrame.pack()
        textFrame = Frame(window)
        textFrame.pack()
        saveFrame = Frame(window)
        self.saveFrame = saveFrame



        self.srcLabel = Label(openFrame, text="Izberi GPX file: ")
        self.srcLabel.config(font=("Arial", 18))
        self.srcLabel.pack(side=LEFT, padx=25)

        self.lokacija = StringVar()

        self.srcVnos = Entry(openFrame, width="50")
        self.srcVnos["textvariable"] = self.lokacija
        self.srcVnos.config(font=("Arial", 18))
        self.srcVnos.pack(side=LEFT)

        self.openButton = Button(openFrame, text="brskaj", command=self.izberiFile)
        self.openButton.pack(side=LEFT, padx=5)
        self.openButton.config(font=("Arial", 18))

        self.resultLabel = Entry(textFrame, state='readonly', borderwidth=0, highlightthickness=0, width=50)
        self.var = StringVar()
        self.var.set('')
        self.resultLabel.config(textvariable=self.var, relief='flat',font=("Arial", 18))
        self.resultLabel.pack()



        self.evaluateButton = Button(evalFrame, text="Analiziraj GPX", command=self.obdelajFile)
        self.evaluateButton.config(font=("Arial", 18))
        self.evaluateButton.pack(side=LEFT)

        self.dstLabel = Label(saveFrame, text="Izberi kam se shrani: ")
        self.dstLabel.config(font=("Arial", 18))

        self.destinacija = StringVar()
        self.dstVnos = Entry(saveFrame, width="50")
        self.dstVnos["textvariable"] = self.destinacija
        self.dstVnos.config(font=("Arial", 18))
        self.saveButton = Button(saveFrame, text="brskaj", command=self.izberiFileZaShranit)
        self.saveButton.config(font=("Arial", 18))
        self.saveButton2 = Button(saveFrame, text="Shrani!", command=self.shraniFile)
        self.saveButton2.config(font=("Arial", 18))

        self.window = window
        self.canvas = None


    def izberiFile(self):
        filename = filedialog.askopenfilename(parent=window, title='Izberi GPX datoteko', filetypes=(("GPX sledi", "*.gpx"),))
        self.lokacija.set(filename)
        if filename:
            self.gpx_file = open(filename,'r')
        print(self.lokacija)
        #elif self.lokacija.get():
            #self.gpx_file = open(self.lokacija.get(), 'r')

    def izberiFileZaShranit(self):
        file = filedialog.asksaveasfile(parent=window, title='Izberi kam se shrani lep GPX', defaultextension=".gpx")
        if file:
            self.destinacija.set(file.name)
            self.destinacijaTxt = file.name
        file.close()

    def shraniFile(self):
        print(self.destinacijaTxt)
        if self.sled.saveFiltered(self.destinacijaTxt):
            messagebox.showinfo("Informacija", "Datoteka shranjena")
        else:
            messagebox.showwarning("Informacija", "Prišlo je do napake")

    def obdelajFile(self):
        try:
            self.sled = Track(self.gpx_file)
            self.sled.process()
            self.sled.processElevation()
            self.printVrednosti()
            self.narisiGraf()
            self.saveFrame.pack()
            self.dstLabel.pack(side=LEFT, padx=25)
            self.dstVnos.pack(side=LEFT)
            self.saveButton.pack(side=LEFT, padx=5)
            self.saveButton2.pack(side=LEFT, padx=5, pady=20)
        except Exception as e:
            self.var.set("Izberi GPX datoteko!")
            self.resultLabel.config(textvariable=self.var, relief='flat')
            print(e)

    def printVrednosti(self):
        self.var.set( "Na gor: {}m  Na dol: {}m   Dolžina: {}km".format(self.sled.naGor(),self.sled.naDol(),self.sled.posrek()))
        self.resultLabel.config(textvariable=self.var, relief='flat')

    def narisiGraf(self):

        fig = Figure(figsize=(12, 6), facecolor='#d9d9d9')
        a = fig.add_subplot(111)
        a.plot(self.sled.grafDataRaw()[0], self.sled.grafDataRaw()[1], label="original", c="#c9c9c9")
        a.plot(self.sled.grafData()[0],self.sled.grafData()[1], label="filtriran", c="#658f2c")

        a.set_title("Višinski profil", fontsize=16)
        a.set_ylabel("m", fontsize=14)
        a.set_xlabel("km", fontsize=14)
        a.legend()

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.saveFrame.pack_forget()
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()


window = Tk()
start = GUI(window)
window.mainloop()