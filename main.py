import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

formulalist, graphlist = [], [] #List of used formulas for luminosity over angle and list of graph instances

L0 = 1e52   #Starting luminosity
t = np.arange(0, 1.6, .01)  #Theta variable
Flim = 10 ** (-9)   #Sensor sensitivity

f = open("formulas.txt", "r") #Read formulas from a text file (new ones are written to this file as well)
for x in f:
    formulalist.append(x)
f.close()

root= tk.Tk()   #Root window
root.winfo_toplevel().title("GRB and GW Models")
header = tk.Frame() #Header and label

label = tk.Label(
    master=header,
    text="GRB and GW Models",
    fg="black",
    bg="white",
    width=10,
    height=2,
    font=("Courier", 32)
)
label.pack(fill=tk.X)
header.pack(fill=tk.X)

newformula = tk.Frame(bg="white")
newformula.pack(fill=tk.X)

class ScrollableFrame(tk.Frame):    #Enables scrolling in the list of formulas
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(master=self, width=150, height=515)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

selection = ScrollableFrame(root)
selection.pack(side=tk.LEFT, anchor="n")

class GRBGraphObject:   #Graph object
    def __init__(self, formula):
        for i in graphlist:
            i.graph.pack_forget()
        self.graph = tk.Frame()

        self.fig, self.ax = plt.subplots(2, 2)
        self.fig.set_size_inches(5, 5)
        self.fig.subplots_adjust(bottom=0.12, hspace=0.42, right=0.96)

        self.l1 = self.ax[0,0].plot(t, eval(formula))   #Luminosity over angle
        self.l2 = self.ax[0,1].plot(t, np.sqrt(eval(formula)/(4*np.pi*Flim)))   #Luminosity distance over angle
        self.l2 = self.ax[1,0].plot(t, 2*np.pi*(1-np.cos(t)))   #Solid angle
        self.l2 = self.ax[1,1].plot(t, (np.sqrt(eval(formula)/(4*np.pi*Flim)))**3 * 2*np.pi*(1-np.cos(t)))  #Number of events

        self.ax[0,0].set(xlabel='Inclination angle (radians)', ylabel='Luminosity (erg/s)')
        self.ax[0,0].set_title('Luminosity for given angle', y=1.04)
        self.ax[0,1].set(xlabel='Inclination angle (radians)', ylabel='distance dL')
        self.ax[0,1].set_title('Luminosity distance for given angle', y=1.04)
        self.ax[1,0].set(xlabel='t (radians)', ylabel='Solid Angle Ω')
        self.ax[1,0].set_title('Solid Angle? for t', y=1.04)
        self.ax[1,1].set(xlabel='t (radians)', ylabel='# events')
        self.ax[1,1].set_title('Number of events?', y=1.04)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph)
        self.toolbar.update()

        self.button = tk.Button(selection.scrollable_frame, text=formula, width=20, command= lambda: self.change())

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.graph.pack(side=tk.RIGHT,anchor="n")
        self.button.pack()

    def change(self):
        for i in graphlist:
            i.graph.pack_forget()
        self.graph.pack(side=tk.RIGHT,anchor="n")

class GWGraphObject:   #Graph object
    def __init__(self, formula):
        self.graph = tk.Frame()

        self.fig, self.ax = plt.subplots(2, 3)
        self.fig.set_size_inches(8, 5)
        self.fig.subplots_adjust(bottom=0.12, hspace=0.42, left=0.074, right=0.96)

        self.l1 = self.ax[0,0].plot(t, eval(formula))   #Luminosity over angle
        self.l2 = self.ax[0,1].plot(t, np.sqrt(eval(formula)/(4*np.pi*Flim)))   #Luminosity distance over angle
        self.l2 = self.ax[1,0].plot(t, 2*np.pi*(1-np.cos(t)))   #Solid angle
        self.l2 = self.ax[1,1].plot(t, (np.sqrt(eval(formula)/(4*np.pi*Flim)))**3 * 2*np.pi*(1-np.cos(t)))  #Number of events

        self.ax[0,0].set(xlabel='Inclination angle (radians)', ylabel='Luminosity (erg/s)')
        self.ax[0,0].set_title('Luminosity for given angle', y=1.04)
        self.ax[0,1].set(xlabel='Inclination angle (radians)', ylabel='distance dL')
        self.ax[0,1].set_title('Luminosity distance for given angle', y=1.04)
        self.ax[1,0].set(xlabel='t (radians)', ylabel='Solid Angle Ω')
        self.ax[1,0].set_title('Solid Angle for t', y=1.04)
        self.ax[1,1].set(xlabel='t (radians)', ylabel='# events')
        self.ax[1,1].set_title('Number of events', y=1.04)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph)
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.graph.pack(side=tk.RIGHT,anchor="n")

class CombiGraphObject:   #Graph object
    def __init__(self, formula):
        self.graph = tk.Frame()

        self.fig, self.ax = plt.subplots(2, 1)
        self.fig.set_size_inches(3, 5)
        self.fig.subplots_adjust(bottom=0.12, hspace=0.42)

        self.l1 = self.ax[0].plot(t, eval(formula))   #Luminosity over angle
        self.l2 = self.ax[1].plot(t, np.sqrt(eval(formula)/(4*np.pi*Flim)))   #Luminosity distance over angle

        self.ax[0].set(xlabel='Inclination angle (radians)', ylabel='Luminosity (erg/s)')
        self.ax[0].set_title('Luminosity for given angle', y=1.04)
        self.ax[1].set(xlabel='Inclination angle (radians)', ylabel='distance dL')
        self.ax[1].set_title('Luminosity distance for given angle', y=1.04)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph)
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.graph.pack(side=tk.RIGHT,anchor="n")

def new(newformula):
    graphlist.append(GRBGraphObject(newformula))
    f = open("formulas.txt", "a")
    f.write(newformula + "\n")
    f.close()

CombiGraphs = CombiGraphObject("L0 * np.cos(t)")
CombiGraphs.graph.pack(side=tk.RIGHT,anchor="n")

Graphs = GWGraphObject("L0 * np.cos(t)")
Graphs.graph.pack(side=tk.RIGHT,anchor="n")

for i in formulalist:
    graphlist.append(GRBGraphObject(i))
    graphlist[-1].graph.pack_forget()
graphlist[0].graph.pack(side=tk.RIGHT,anchor="n")

entry = tk.Entry(newformula,width=48)
confirmbutton = tk.Button(newformula, text='Confirm', width=8, command= lambda: new(entry.get()))
entry.pack()
confirmbutton.pack(anchor="e")

root.mainloop()
