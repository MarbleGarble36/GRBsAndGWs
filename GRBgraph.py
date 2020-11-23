class graphObject:
    def __init__(self, formula, graphnr):
        for i in graphlist:
            i.graph.pack_forget()
        self.graph = tk.Frame()
        self.graphnr = graphnr

        self.fig, self.ax = plt.subplots(1, 2)
        self.fig.set_size_inches(4, 2)
        self.mdfig = plt.figure()
        self.mdax1 = self.mdfig.add_subplot(121)
        self.mdax2 = self.mdfig.add_subplot(122, projection='3d')

        self.l1 = self.ax[0].plot(t, eval(formula))
        self.l2 = self.ax[1].plot(t, np.sqrt(eval(formula)/(4*np.pi*Flim)))
        self.mdax1.plot(t2, 2*np.pi*(1-np.cos(t2)))
        self.mdax2.plot(t, t2, (np.sqrt(eval(formula)/(4*np.pi*Flim)))**3 * 2*np.pi*(1-np.cos(t2)))

        self.ax[0].set(xlabel='Inclination angle (radians)', ylabel='Luminosity (erg/s)', title='Luminosity for given angle')
        self.ax[1].set(xlabel='Inclination angle (radians)', ylabel='distance dL', title='Luminosity distance for given angle')
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
