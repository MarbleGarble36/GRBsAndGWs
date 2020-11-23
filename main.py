"""
I plan to replace all the globals()[] variables by creating a class for the graphs so it's a bit neater, but the program works for now.
Originally we had way fewer variables for the graphs so it was just as easy to use the global variables for dynamically creating them
but it has gotten a bit out of hand. The program requires tkinter, which should work on all operating systems but if you experience any
trouble running it, you can contact us for screenshots or a version of the program that just spits out images of the graphs instead of showing the entire gui.
The program requires the formulas.txt file to be in the same directory as the program as that's where it gets the formulas for the luminosity.
Kind regards,
Daan Dietvorst & Lorenzo Termaat
"""

import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

formulalist = []
graphlist = []

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

testgraph = tk.Frame()

testfig, testax = plt.subplots()
testax.plot(t, np.sin(np.pi * t))

testax.set(xlabel='Inclination angle (radians)', ylabel='Luminosity (erg/s)', title='Luminosity for given angle')

testcanvas = FigureCanvasTkAgg(testfig, master=testgraph)
testcanvas.draw()
testcanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

testtoolbar = NavigationToolbar2Tk(testcanvas, testgraph)
testtoolbar.update()
testcanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

testgraph.pack(side=tk.RIGHT,anchor="n")

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

def change(graph):
    graph = graphlist[graph]
    for i in graphlist:
        i.pack_forget()
    graph.pack(side=tk.RIGHT,anchor="n")

def newgraph(formula):
    for k in graphlist:
        k.pack_forget()

    gll = len(graphlist)
    globals()['graph{numb}'.format(numb=gll)] = tk.Frame()

    globals()['fig{numb}'.format(numb=gll)], globals()['ax{numb}'.format(numb=gll)] = plt.subplots(1, 2)
    globals()['l{numb}-1'.format(numb=gll)] = globals()['ax{numb}'.format(numb=gll)][0].plot(t, eval(formula))
    globals()['l{numb}-2'.format(numb=gll)] = globals()['ax{numb}'.format(numb=gll)][1].plot(t, np.sqrt(eval(formula)/(4*np.pi*Flim)))
    globals()['3dfig{numb}'.format(numb=gll)] = plt.figure()
    globals()['3dax1{numb}'.format(numb=gll)] = globals()['3dfig{numb}'.format(numb=gll)].add_subplot(121)
    globals()['3dax2{numb}'.format(numb=gll)] = globals()['3dfig{numb}'.format(numb=gll)].add_subplot(122, projection='3d')
    globals()['3dax1{numb}'.format(numb=gll)].plot(t2, 2*np.pi*(1-np.cos(t2)))
    globals()['3dax2{numb}'.format(numb=gll)].plot(t, t2, (np.sqrt(eval(formula)/(4*np.pi*Flim)))**3 * 2*np.pi*(1-np.cos(t2)))

    globals()['fig{numb}'.format(numb=gll)].set_size_inches(4, 2)

    globals()['ax{numb}'.format(numb=gll)][0].set(xlabel='Inclination angle (radians)', ylabel='Luminosity (erg/s)', title='Luminosity for given angle')
    globals()['ax{numb}'.format(numb=gll)][1].set(xlabel='Inclination angle (radians)', ylabel='distance dL', title='Luminosity distance for given angle')
    globals()['3dax1{numb}'.format(numb=gll)].set(xlabel='t2 (radians)', ylabel='Solid Angle Ω', title='Solid Angle? for t2')
    globals()['3dax2{numb}'.format(numb=gll)].set(xlabel='t (radians)', ylabel='t2 (radians)', zlabel="# events", title='Number of events?')

    globals()['canvas{numb}'.format(numb=gll)] = FigureCanvasTkAgg(globals()['fig{numb}'.format(numb=gll)], master=globals()['graph{numb}'.format(numb=gll)])
    globals()['canvas{numb}'.format(numb=gll)].draw()
    globals()['canvas{numb}'.format(numb=gll)].get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    globals()['3dcanvas{numb}'.format(numb=gll)] = FigureCanvasTkAgg(globals()['3dfig{numb}'.format(numb=gll)], master=globals()['graph{numb}'.format(numb=gll)])
    globals()['3dcanvas{numb}'.format(numb=gll)].draw()
    globals()['3dcanvas{numb}'.format(numb=gll)].get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    globals()['3dtoolbar{numb}'.format(numb=gll)] = NavigationToolbar2Tk(globals()['3dcanvas{numb}'.format(numb=gll)], globals()['graph{numb}'.format(numb=gll)])
    globals()['3dtoolbar{numb}'.format(numb=gll)].update()
    globals()['3dcanvas{numb}'.format(numb=gll)].get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    globals()['toolbar{numb}'.format(numb=gll)] = NavigationToolbar2Tk(globals()['canvas{numb}'.format(numb=gll)], globals()['graph{numb}'.format(numb=gll)])
    globals()['toolbar{numb}'.format(numb=gll)].update()
    globals()['canvas{numb}'.format(numb=gll)].get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    globals()['graph{numb}'.format(numb=gll)].pack(side=tk.RIGHT,anchor="n")

    globals()['button{numb}'.format(numb=gll)] = tk.Button(selection.scrollable_frame, text=formula, width=20, command= lambda: change(gll))
    globals()['button{numb}'.format(numb=gll)].pack()

    graphlist.append(globals()['graph{numb}'.format(numb=gll)])

def new(newformula):
    for j in graphlist:
        j.pack_forget()
    newgraph(newformula)
    f = open("formulas.txt", "a")
    f.write(newformula + "\n")
    f.close()

for i in formulalist:
    newgraph(i)
    for k in graphlist:
        k.pack_forget()
    graphlist[0].pack(side=tk.RIGHT,anchor="n")

testgraph.pack_forget()

entry = tk.Entry(newformula,width=48)
confirmbutton = tk.Button(newformula, text='Confirm', width=8, command= lambda: new(entry.get()))
entry.pack()
confirmbutton.pack(anchor="e")

root.mainloop()
