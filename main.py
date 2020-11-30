import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

formulalist, graphlist = [], []

L0 = 1e52

t = np.arange(0, 1.6, .01)
t2 = np.arange(0, 1.6, .01)

Flim = 10 ** (-9)

f = open("formulas.txt", "r")
for x in f:
    formulalist.append(x)
f.close()

root= tk.Tk()
root.winfo_toplevel().title("GRB Models")
header = tk.Frame()

label = tk.Label(
    master=header,
    text="GRB Models",
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

class ScrollableFrame(tk.Frame):
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

class GRBGraphObject:
    def __init__(self, formula):
        for i in graphlist:
            i.graph.pack_forget()
        self.graph = tk.Frame()

        self.fig, self.ax = plt.subplots(1, 2)
        self.fig.set_size_inches(7, 3)
        self.fig.subplots_adjust(bottom=0.2)
        self.mdfig = plt.figure()
        self.mdax1 = self.mdfig.add_subplot(121)
        self.mdax2 = self.mdfig.add_subplot(122, projection='3d')
        self.mdfig.set_size_inches(4, 3)
        self.mdfig.subplots_adjust(bottom=0.2)

        self.l1 = self.ax[0].plot(t, eval(formula))
        self.l2 = self.ax[1].plot(t, np.sqrt(eval(formula)/(4*np.pi*Flim)))
        self.mdax1.plot(t2, 2*np.pi*(1-np.cos(t2)))
        self.mdax2.plot(t, t2, (np.sqrt(eval(formula)/(4*np.pi*Flim)))**3 * 2*np.pi*(1-np.cos(t2)))

        self.ax[0].set(xlabel='Inclination angle (radians)', ylabel='Luminosity (erg/s)')
        self.ax[0].set_title('Luminosity for given angle', y=1.04)
        self.ax[1].set(xlabel='Inclination angle (radians)', ylabel='distance dL')
        self.ax[1].set_title('Luminosity distance for given angle', y=1.04)
        self.mdax1.set(xlabel='t2 (radians)', ylabel='Solid Angle Ω', title='Solid Angle? for t2')
        self.mdax2.set(xlabel='t (radians)', ylabel='t2 (radians)', zlabel="# events", title='Number of events?')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph)
        self.toolbar.update()

        self.mdcanvas = FigureCanvasTkAgg(self.mdfig, master=self.graph)
        self.mdcanvas.draw()
        self.mdtoolbar = NavigationToolbar2Tk(self.mdcanvas, self.graph)
        self.mdtoolbar.update()

        self.button = tk.Button(selection.scrollable_frame, text=formula, width=20, command= lambda: self.change())

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.mdcanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.mdcanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.graph.pack(side=tk.RIGHT,anchor="n")
        self.button.pack()

    def change(self):
        for i in graphlist:
            i.graph.pack_forget()
        self.graph.pack(side=tk.RIGHT,anchor="n")

def new(newformula):
    graphlist.append(GRBGraphObject(newformula))
    f = open("formulas.txt", "a")
    f.write(newformula + "\n")
    f.close()

for i in formulalist:
    graphlist.append(GRBGraphObject(i))
    graphlist[-1].graph.pack_forget()
graphlist[0].graph.pack(side=tk.RIGHT,anchor="n")

entry = tk.Entry(newformula,width=48)
confirmbutton = tk.Button(newformula, text='Confirm', width=8, command= lambda: new(entry.get()))
entry.pack()
confirmbutton.pack(anchor="e")

root.mainloop()
