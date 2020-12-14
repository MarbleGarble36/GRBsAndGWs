from tkinter import *
import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np

formulalist, graphlist = [], [] #List of used formulas for luminosity over angle and list of graph instances

file = open("formulas.txt", "r") #Read formulas from a text file (new ones are written to this file as well)
for x in file:
    formulalist.append(x)
file.close()

root= tk.Tk()   #Root window
root.winfo_toplevel().title("GRB and GW Models")
root.configure(bg='white')
header = tk.Frame() #Header and label
label = tk.Label(
    master=header,
    text="GRB and GW Models",
    fg="black",
    bg="white",
    width=10,
    height=2,
    font=("Helvetica", 32)
)
label.pack(fill=tk.X)
header.pack(fill=tk.X)
newformula = tk.Frame(bg="white")
newformula.pack(fill=tk.X)

class ScrollableFrame(tk.Frame):    #Enables scrolling in the list of formulas
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(master=self, width=150, height=515)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg='white')
        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg='white')
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")
selection = ScrollableFrame(root)
selection.pack(side=tk.LEFT, anchor="n")

th = np.arange(0.01, np.pi/2, .01)  #Theta variable

L0 = 1e52   #Starting luminosity
Flim = 10 ** (-9)   #GRB Sensor sensitivity

phi = np.pi/4 #Phase phi
G = 6.67384e-11 #Gravitational Constant (from BiNaS)
c = 299792458 #speed of light
d = 10000   #Distance between the neutron stars in our binary system
Glim = 10 ** (-22)   #GW Sensor sensitivity
fs = 8677.86029     #Orbital frequency in our binary system
Ms = 1.9884e30      #Mass of the sun
M = 2.8 * Ms    #Mass of one neutron star
SM = (M**2)**(3/5) * (2 * M)**(-1/5)    #Funky M

class GRBGraphObject:   #Graph object for GRBs
    def __init__(self, formula):
        for i in graphlist:
            i.graph.pack_forget()
        self.graph = tk.Frame()

        L = eval(formula)   #Luminosity over angle
        dL = np.sqrt(L/(4*np.pi*Flim))   #Luminosity distance over angle
        SA = 2*np.pi*(1-np.cos(th))   #Solid angle
        nE = np.array(dL**3 * 2*np.pi*(1-np.cos(th))).cumsum()  #Number of events

        self.fig, self.ax = plt.subplots(2, 2)
        self.fig.set_size_inches(7, 7)
        self.fig.subplots_adjust(bottom=0.12, hspace=0.42, right=0.96)

        self.l1 = self.ax[0,0].plot(th, L)
        self.l1 = self.ax[0,1].plot(th, dL)
        self.l1 = self.ax[1,0].plot(th, SA)
        self.l1 = self.ax[1,1].plot(th, nE)

        self.ax[0,0].set(xlabel='Inclination angle θ (radians)', ylabel='Luminosity (erg/s)')
        self.ax[0,0].set_title('Luminosity for given angle', y=1.04)
        self.ax[0,1].set(xlabel='Inclination angle θ (radians)', ylabel='distance dL')
        self.ax[0,1].set_title('Luminosity distance for given angle', y=1.04)
        self.ax[1,0].set(xlabel='θ (radians)', ylabel='Solid Angle Ω')
        self.ax[1,0].set_title('Solid Angle for θ', y=1.04)
        self.ax[1,1].set(xlabel='θ (radians)', ylabel='# events')
        self.ax[1,1].set_title('Number of events', y=1.04)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph)
        self.toolbar.update()

        self.button = tk.Button(selection.scrollable_frame, text=formula, width=20, relief=GROOVE, command= lambda: self.change())

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.graph.pack(side=tk.RIGHT,anchor="n")
        self.button.pack()

    def change(self):
        for i in graphlist:
            i.graph.pack_forget()
        self.graph.pack(side=tk.RIGHT,anchor="n")

class GWGraphObject:   #Graph object
    def __init__(self):
        self.graph = tk.Frame()

        hp = (2*((G*M)**(5/3))*((np.pi*fs)**(2/3)))/(c**4 * d) * (1 + np.cos(th)**2) * np.cos(2 * phi) #Strain in hplus polarisation
        hx = (-4*((G*SM)**(5/3))*((np.pi*fs)**(2/3)))/(c**4 * d) * np.cos(th) * np.sin(2*phi)   #Strain in hcross polarisation
        h = np.sqrt(hp**2 + hx**2)  #Total Strain
        dh = h/(4*np.pi*Glim)   #'Strain distance'
        nE = ((1-np.cos(th))*dh**3).cumsum() #Relative number of events

        self.fig, self.ax = plt.subplots(2, 3)
        self.fig.set_size_inches(10, 7)
        self.fig.subplots_adjust(bottom=0.12, hspace=0.42, left=0.074, right=0.96)

        self.l1 = self.ax[0,0].plot(th, hp, color='red')
        self.l1 = self.ax[0,1].plot(th, hx, color='red')
        self.l1 = self.ax[0,2].plot(th, h, color='red')
        self.l1 = self.ax[1,0].plot(th, dh, color='red')
        self.l1 = self.ax[1,1].plot(th, nE, color='red')

        self.ax[0,0].set(xlabel='Angle i (radians)', ylabel='Strain')
        self.ax[0,0].set_title('Strain in h+', y=1.04)
        self.ax[0,1].set(xlabel='Angle i (radians)', ylabel='Strain')
        self.ax[0,1].set_title('Strain in hx', y=1.04)
        self.ax[0,2].set(xlabel='Angle i (radians)', ylabel='Strain')
        self.ax[0,2].set_title('Total strain', y=1.04)
        self.ax[1,0].set(xlabel='Angle i (radians)', ylabel='Distance dh (m)')
        self.ax[1,0].set_title('Distance', y=1.04)
        self.ax[1,1].set(xlabel='Angle i (radians)', ylabel='# events')
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

        self.l1 = self.ax[0].plot(th, eval(formula))   #Luminosity over angle
        self.l2 = self.ax[1].plot(th, np.sqrt(eval(formula)/(4*np.pi*Flim)))   #Luminosity distance over angle

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

#CombiGraphs = CombiGraphObject("L0 * np.cos(t)")
#CombiGraphs.graph.pack(side=tk.RIGHT,anchor="n")

GWGraphs = GWGraphObject()
GWGraphs.graph.pack(side=tk.RIGHT,anchor="n")

for i in formulalist:
    graphlist.append(GRBGraphObject(i))
    graphlist[-1].graph.pack_forget()
graphlist[0].graph.pack(side=tk.RIGHT,anchor="n")

entry = tk.Entry(newformula,width=48)
confirmbutton = tk.Button(newformula, text='Confirm', width=8, relief=GROOVE, command= lambda: new(entry.get()))
entry.pack()
confirmbutton.pack(anchor="e")

root.mainloop()
