# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
# Modifed for Project 4 by Brandon Troisi
# CS 251
# 

import Tkinter as tk
import tkFont as tkf
import math
import random
import os
import tkFileDialog
import data
import view 
import numpy as np
import analysis as an
import scipy.stats as st
# create a class to build and manage the display
class DisplayApp:

	def __init__(self, width, height):

		# create a tk object, which is the root window
		self.root = tk.Tk()


		# width and height of the window
		self.initDx = width
		self.initDy = height

		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

		# set the title of the window
		self.root.title("Random Datapoints")

		# set the maximum size of the window for resizing
		self.root.maxsize( 1600, 900 )

		# setup the menus
		self.buildMenus()

		# build the controls
		self.buildControls()

		# build the Canvas
		self.buildCanvas()

		# bring the window to the front
		self.root.lift()

		# - do idle events here to get actual canvas size
		self.root.update_idletasks()

		# now we can ask the size of the canvas
		print self.canvas.winfo_geometry()

		# set up the key bindings
		self.setBindings()

		# set up the application state
		self.objects = [] # list of data objects that will be drawn in the canvas

		self.data = None # will hold the raw data someday.
		
		self.baseClick = None # used to keep track of mouse movement
		
		#create new view object
		self.v=view.View()
		
		#create new data object
		self.data=data.Data()

		self.linRegLines = []

		self.pcaList = []
		self.num_PCA=0

		self.linRegEndpoints = None
		#created matrix of endpoints of x,y, and z axes
		self.axes=np.matrix([[0,0,0,1],[1,0,0,1],[0,0,0,1],[0,1,0,1],[0,0,0,1],[0,0,1,1]])

		#list to store the lines for the x, y, and z axes
		self.lines=[0,0,0]
		
		#calls buildAxes function
		self.buildAxes()
		
		#create matrix for data points
		self.dataPointMatrix=np.zeros((4,4))
		
		#updates the axes
		self.updateAxes()

		self.updateFits()


		
	def buildAxes(self):
		
		vtm=self.v.build()
		pts = (vtm* self.axes.T).T
		self.lines[0]=(pts[0,0],pts[0,1],pts[1,0],pts[1,1])
		self.lines[1]=(pts[2,0],pts[2,1],pts[3,0],pts[3,1])
		self.lines[2]=(pts[4,0],pts[4,1],pts[5,0],pts[5,1])
		
		
		self.lines[0]=self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1],fill="red",tags="X")
		self.lines[1]=self.canvas.create_line(pts[2,0],pts[2,1],pts[3,0],pts[3,1],fill="blue",tags="Y")
		self.lines[2]=self.canvas.create_line(pts[4,0],pts[4,1],pts[5,0],pts[5,1],fill="green",tags="Z")
		
		#create labels for each of the axes
		
		self.xLabel=tk.Label(self.canvas,text="x")
		self.xLabel.place(x=pts[1,0],y=pts[1,1])
		
		self.yLabel=tk.Label(self.canvas,text="y")
		self.yLabel.place(x=pts[3,0],y=pts[3,1])
		
		self.zLabel=tk.Label(self.canvas,text="z")
		self.zLabel.place(x=pts[5,0],y=pts[5,1])


		
	#updates the axes whenever you want to move or rotate them
	def updateAxes(self):
		
		vtm=self.v.build()
		pts = (vtm* self.axes.T).T
		self.canvas.coords(self.lines[0],pts[0,0],pts[0,1],pts[1,0],pts[1,1])
		self.canvas.coords(self.lines[1],pts[2,0],pts[2,1],pts[3,0],pts[3,1])
		self.canvas.coords(self.lines[2],pts[4,0],pts[4,1],pts[5,0],pts[5,1])
		
		#whenever location of the axes is updated, labels move with updated axes locations
		self.xLabel.place(x=pts[1,0],y=pts[1,1])
		self.yLabel.place(x=pts[3,0],y=pts[3,1])
		self.zLabel.place(x=pts[5,0],y=pts[5,1])
		self.updatePoints()
		self.updateFits()

	
	#updates the location of the points whenever you want to move or rotate them 	
	def updatePoints(self):

		vtm=self.v.build()
		pts = (vtm* self.dataPointMatrix.T).T
		
	
		if len(self.objects)==0:
			return 

		for i in range(len(self.objects)):
			dx=5
			x0=pts[i,0]-dx
			y0=pts[i,1]-dx
			x1=pts[i,0]+dx,
			y1=pts[i,1]+dx
			self.canvas.coords(self.objects[i],x0,y0,x1,y1)
		self.updateFits()

	def buildMenus(self):
		
		# create a new menu
		menu = tk.Menu(self.root)

		# set the root menu to our new menu
		self.root.config(menu = menu)

		# create a variable to hold the individual menus
		menulist = []

		# create a file menu
		filemenu = tk.Menu( menu )
		menu.add_cascade( label = "File", menu = filemenu )
		menulist.append(filemenu)

		# create another menu for kicks
		cmdmenu = tk.Menu( menu )
		menu.add_cascade( label = "Command", menu = cmdmenu )
		menulist.append(cmdmenu)

		# menu text for the elements
		# the first sublist is the set of items for the file menu
		# the second sublist is the set of items for the option menu
		menutext = [ [ '-', '-', 'Quit	\xE2\x8C\x98-Q', 'Open','Linear Regression'],
					 [ 'Command 1', '-', '-','Open', 'Linear Regression' ] ]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
		menucmd = [ [self.clearData, None, self.handleQuit,self.handleOpen,self.handleLinearRegression],
					[self.handleMenuCmd1, None, None, self.handleOpen,self.handleLinearRegression] ]
		
		# build the menu elements and callbacks
		for i in range( len( menulist ) ):
			for j in range( len( menutext[i]) ):
				if menutext[i][j] != '-':
					menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
				else:
					menulist[i].add_separator()

	# create the canvas object
	def buildCanvas(self):
		self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
		self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
		return

	# build a frame and put controls in it
	def buildControls(self):

		### Control ###
		# make a control frame on the right
		rightcntlframe = tk.Frame(self.root)
		rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="Control Panel", width=20 )
		label.pack( side=tk.TOP, pady=10 )


		plotdatabutton = tk.Button( rightcntlframe, text="Plot Data",
							command=self.handlePlotData)
		plotdatabutton.pack(side=tk.TOP)  # default side is top

		linregbutton = tk.Button(rightcntlframe, text="Linear Regression",
								   command=self.handleLinearRegression)
		linregbutton.pack(side=tk.TOP)  # default side is top


		
		# create button that resets view of the data
		resetviewbutton = tk.Button( rightcntlframe, text="Reset View",
							   command=self.resetGraph)
		resetviewbutton.pack(side=tk.TOP)  # default side is top
		
		#create button that resets view of graph and clears data
		cleardatabutton = tk.Button( rightcntlframe, text="Clear Data", 
							   command=self.clearDataAndView)
		cleardatabutton.pack(side=tk.TOP) 
		
		#create quit button
		quitbutton = tk.Button( rightcntlframe, text="Quit", 
							   command=self.handleQuit)
		quitbutton.pack(side=tk.TOP)  # default side is top

		plotPCAbutton = tk.Button( rightcntlframe, text="Plot PCA", command=self.handlePlotPCA)
		plotPCAbutton.pack(side=tk.TOP)

		self.statslabel = tk.Text(self.root, height=1, width=75)
		self.statslabel.pack(side=tk.TOP)
		
		#create text to display how much axes got rotated
		self.rotate=tk.Text(self.root, height=1, width=75)
		self.rotate.pack(side=tk.TOP)
		
		#create text to display how you zoomed in on the axes
		self.zoom=tk.Text(self.root, height=1, width=75)
		self.zoom.pack(side=tk.TOP)

		self.AnalysisWindow = tk.Listbox(rightcntlframe, selectmode=tk.SINGLE, exportselection=0)
		self.AnalysisWindow.pack(side=tk.TOP, padx=0)

		otherframe = tk.Frame(rightcntlframe)
		otherframe.pack(side=tk.TOP, fill=tk.Y)

		AddPCAbutton = tk.Button(otherframe, text="Add PCA",
								 command=self.handlePCA)
		AddPCAbutton.pack(side=tk.LEFT)  # default side is top

		DelPCAbutton = tk.Button(otherframe, text="Delete PCA",
								 command=self.handleDeletePCA)
		DelPCAbutton.pack(side=tk.LEFT)  # default side is top

		ViewPCAbutton = tk.Button(otherframe, text="View PCA",
								 command=self.handleViewPCA)
		ViewPCAbutton.pack(side=tk.LEFT)  # default side is top

		return

	def setBindings(self):
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<Button-2>', self.handleMouseButton2 )
		self.canvas.bind( '<Control-Shift-Button-1>', self.handleMouseButton3 )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
		self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Control-Shift-B1-Motion>', self.handleMouseButton3Motion )
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-o>', self.handleOpen )
	
	#allows user to quit program	
	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()
	
	#allows user to open file that user wants to plot data from 	
	def handleOpen(self,event=None):
		
		fn = tkFileDialog.askopenfilename( parent=self.root,title='Choose a data file', initialdir='.' )
		try: 
			self.data=data.Data(fn)

		except IOError:
			print "You have not selected a file"

	def handleButton1(self):
		print 'handling command button:'
		self.colorOption.get()
		for obj in self.objects:
			self.canvas.itemconfig(obj, fill=self.colorOption.get() )

	def handleMenuCmd1(self):
		print 'handling menu command 1'

	#stores initial base click when you translate the axes
	def handleMouseButton1(self, event):
		
	   print 'handle mouse button 1: %d %d' % (event.x, event.y)
	   self.baseClick = (event.x, event.y)
	   
	#stores initial base click when you want to rotate the axes
	def handleMouseButton2(self, event):
		
		self.baseClick = (event.x, event.y)
		self.clone=self.v.clone()
		
		print 'handle mouse button 2: %d %d' % (event.x, event.y)
	
	#stores initial base click when you want to zoom in on axes
	def handleMouseButton3(self, event):
	
		print 'handle mouse button 3: %d %d' % (event.x, event.y)
		self.baseClick = (event.x, event.y)
		clone=self.v.clone()
		self.origExtent=self.v.extent[:]
	

	# This is called if the first mouse button is being moved
	#Translates the axes 
	def handleMouseButton1Motion(self, event):
		# calculate the difference in x and y direction
		diff=(event.x - self.baseClick[0], event.y - self.baseClick[1])

		print 'handle button1 motion %d %d' % (diff[0], diff[1])
		delta0=float(diff[0])/self.v.screen[0]*self.v.extent[0]
		delta1=float(diff[1])/self.v.screen[1]*self.v.extent[1]
		
		self.v.vrp=delta0 * self.v.u + delta1 * self.v.vup
		self.updateAxes()
		
		# update base click
		#self.baseClick = ( event.x, event.y )
		

			
	# This is called if the second button of a real mouse has been pressed
	# and the mouse is moving. Or if the control key is held down while
	# a person moves their finger on the track pad.
	#Rotates the axes
	def handleMouseButton2Motion(self, event):
		
		dx=float(event.x - self.baseClick[0])
		dy=float(event.y - self.baseClick[1])
	
		delta0=dx/400*math.pi
		delta1=dy/400*math.pi
		
		self.v=self.clone.clone()
		self.v.rotateVRC(-delta0,delta1)
		
		
		
		self.rotate.delete('1.0', tk.END)
		self.rotate.insert(tk.END, "Rotation: ")
		self.rotate.insert(tk.END, delta0)
		self.rotate.insert(tk.END, ",")
		self.rotate.insert(tk.END, delta1)
		
		self.updateAxes()
		
		
	# This is called if the thrid button of a real mouse has been pressed
	# and the mouse is moving. Or if the control and shift keys have been pressed is held down while
	# a person moves their finger up and down on the track pad.
	#Zooms in or out of the axes the axes
	def handleMouseButton3Motion(self, event):
		dy= float(event.y - self.baseClick[1])
		
		factor=1.0+dy/self.canvas.winfo_height()
		factor=max(min(factor,3.0),0.1)
		self.v.extent=[self.origExtent[0]*factor,self.origExtent[1]*factor,self.origExtent[2]*factor]
		
		
		self.zoom.delete('1.0',tk.END)
		self.zoom.insert(tk.END, "Zoom Percentage: ")
		self.zoom.insert(tk.END, int((1-factor)*100))
		self.zoom.insert(tk.END, "%")
		
		self.updateAxes()
		
		
	def handlePlotData(self, event=None):
		#allows user to plot data 
		self.handleChooseAxes()
	
	def handleChooseAxes(self):
		#allow user to choose axes (dimension) to plot data on including x,y,z, color, and size
		self.dialog=DataDialogBox(self.root,self.data)
		self.buildPoints(self.dialog.getDatacols())

	def buildPoints(self, headers):
		# Plots data based on what user chose for dimensions for specific columns of data
		# Takes in a list of headers from dialog box selections
		self.clearData()

		if len(self.pcaList)>0:
			idx = self.AnalysisWindow.index(tk.ACTIVE)
			self.data=self.pcaList[idx]

		norm = an.normalize_columns_separately(self.data, headers[0:3])
		zeromatrix = np.zeros(norm.shape[0])
		onesmatrix = np.ones(norm.shape[0])

		# x and y are automatically first two dimensions
		xdata = headers[0]
		ydata = headers[1]

		# if the length of the headers is 2, only plot data on  x and y axes
		if len(headers) == 2:
			zdata = None
			colorpt = None
			sizept = None

		# if the length of the headers is 3, only plot data on x, y, and z axes
		# z axis is third dimension of data
		# user must choose to plot x,y, and z axes in that order if header is length 3
		if len(headers) == 3:
			zdata = headers[2]
			colorpt = None
			sizept = None

		# if the length of the headers is 4, only plot data on x, y, z, and color axes
		# z axis is third dimension of data
		# color axis is fourth dimension of data
		# user must choose to plot x,y,z, and color axes in that order
		if len(headers) == 4:
			zdata = headers[2]
			colorpt = headers[3]
			sizept = None

		# if the length of the headers is 5, plot data on x, y, z, color, and size axes
		# z axis is third dimension of data
		# color axis fourth dimension of data
		# size axis is the fifth dimension of data
		# user must choose to plot x,y,z, color, and size in that order
		if len(headers) == 5:
			zdata = headers[2]
			colorpt = headers[3]
			sizept = headers[4]

		if xdata != None and ydata != None:
			dmatrix = np.matrix(norm)
			nmatrix = np.matrix((zeromatrix, onesmatrix)).T
			self.dataPointMatrix = np.hstack((dmatrix, nmatrix))

		if xdata != None and ydata != None and zdata != None:
			dmatrix = np.matrix(norm)
			nmatrix = np.matrix((onesmatrix)).T
			self.dataPointMatrix = np.hstack((dmatrix, nmatrix))

		vtm = self.v.build()
		pts = (vtm * self.dataPointMatrix.T).T

		self.factorlist = []
		self.colorlist = []

		# if user chooses color and size dimensions for data
		# convert data set that user chose for color dimension to colors with a blue to yellow
		# gradient, blue being minimum value and yellow representing maximum value
		# Also convert data set that user chose for size dimension to size of data points
		# The size of data points range from 0 to 7
		if colorpt != None and sizept != None:
			self.clearData()
			colornorm = an.normalize_columns_separately(self.data, [colorpt])
			self.colorlist = []
			for i in range(colornorm.shape[0]):
				alpha = colornorm[i, 0] * 255
				self.colorlist.append((int(255 - alpha), int(255 - alpha), int(alpha)))

			sizenorm = an.normalize_columns_separately(self.data, [sizept])

			for i in range(sizenorm.shape[0]):
				self.factorlist.append(sizenorm[i, 0] * 7)

			for i in range(pts.shape[0]):
				dx = self.factorlist[i]
				x = pts[i, 0]
				y = pts[i, 1]
				self.color = self.colorlist[i]
				pt = self.canvas.create_oval(x - dx, y - dx, x + dx, y + dx, fill="#%02X%02X%02X" % self.color,
											 outline='')
				self.objects.append(pt)

		# if user chooses color and size dimensions for data
		# convert data set that user chose for color dimension to colors with a blue to yellow
		# gradient, blue being minimum value and yellow representing maximum value
		# Draw all data points with size 5
		elif colorpt != None and sizept == None:

			self.clearData()

			colornorm = an.normalize_columns_separately(self.data, [colorpt])
			for i in range(colornorm.shape[0]):
				alpha = colornorm[i, 0] * 255
				self.colorlist.append((int(255 - alpha), int(255 - alpha), int(alpha)))

			for i in range(pts.shape[0]):
				self.factorlist.append(5)
				dx = self.factorlist[i]
				x = pts[i, 0]
				y = pts[i, 1]
				self.color = self.colorlist[i]
				pt = self.canvas.create_oval(x - dx, y - dx, x + dx, y + dx,
											 fill="#%02X%02X%02X" % self.color, outline='')
				self.objects.append(pt)

		elif colorpt == None and sizept == None:
			self.clearData()
			# del self.factorlist[:]
			for i in range(pts.shape[0]):
				self.factorlist.append(5)
				self.colorlist.append('red')
				self.color = self.colorlist[i]
				x = pts[i, 0]
				y = pts[i, 1]
				dx = self.factorlist[i]
				pt = self.canvas.create_oval(x - dx, y - dx, x + dx, y + dx,
											 fill=self.color, outline='')
				self.objects.append(pt)

	def handleLinearRegression(self):

		self.dialog=DialogBox(self.root,self.data)

		if len(self.dialog.headers)==0:
			print "Select a file"
			self.handleOpen()

		if self.dialog.getDatacols()== None:
			return

		self.clearData()
		self.clearLinRegLines()
		self.resetGraph()
		self.buildLinearRegression(self.dialog.getDatacols())
		self.updateAxes()



	def buildLinearRegression(self,headers):

		norm = an.normalize_columns_separately(self.data, headers)
		zeromatrix = np.zeros(norm.shape[0])
		onesmatrix = np.ones(norm.shape[0])

		# x and y are automatically first two dimensions
		xdatahead = headers[0]
		ydatahead = headers[1]


		if xdatahead != None and ydatahead != None:
			dmatrix = np.matrix(norm)
			nmatrix = np.matrix((zeromatrix, onesmatrix)).T
			self.dataPointMatrix = np.hstack((dmatrix, nmatrix))

		vtm = self.v.build()
		pts = (vtm * self.dataPointMatrix.T).T

		for i in range(pts.shape[0]):
			x = pts[i, 0]
			y = pts[i, 1]
			dx = 5
			pt = self.canvas.create_oval(x - dx, y - dx, x + dx, y + dx,
										 fill='blue', outline='')
			self.objects.append(pt)

		xdata=np.array(self.data.get_data([xdatahead]).T)[0]
		ydata=np.array(self.data.get_data([ydatahead]).T)[0]

		slope, intercept, r_value, p_value, slope_std_error = st.linregress(xdata,ydata)
		predict_y = intercept + slope * xdata
		pred_error = ydata - predict_y
		degrees_of_freedom = len(xdata) - 2
		r2_value=r_value*r_value
		residual_std_error = np.sqrt(np.sum(pred_error ** 2) / degrees_of_freedom)

		rangex =an.data_range(self.data,[xdatahead])
		rangey=an.data_range(self.data,[ydatahead])

		yend0=((rangex[0,0]*slope+intercept)-rangey[0,0])/(rangey[0,1]-rangey[0,0])
		yend1=((rangex[0,1]*slope+intercept)-rangey[0,0])/(rangey[0,1]-rangey[0,0])

		print "minx", rangex[0,0]
		print "maxx", rangex[0,1]
		print "miny", rangey[0,0]
		print "maxy", rangey[0,1]

		linemtrxcol1=np.matrix([[0.0],[yend0],[0.0],[1.0]])
		linemtrxcol2=np.matrix([[1.0],[yend1],[0.0],[1.0]])
		self.linRegEndpoints=np.hstack((linemtrxcol1,linemtrxcol2))
		print "vtm", vtm
		print "linRegEndpoints", self.linRegEndpoints
		le=vtm*self.linRegEndpoints
		print "le", le
		
		self.linRegLines.append(self.canvas.create_line(le[0, 0], le[1, 0], le[0, 1], le[1, 1], fill="red", tags="X"))


		self.statslabel.delete('1.0', tk.END)
		self.statslabel.insert(tk.END, "Slope: "+str(slope) + " " + "Intercept: " + str(intercept)+ " " + "r^2 value: "+ str(r2_value))


	def updateFits(self):

		if self.linRegEndpoints==None:
			return

		vtm = self.v.build()
		pts = vtm * self.linRegEndpoints
		self.canvas.coords(self.linRegLines[0], pts[0, 0], pts[1, 0], pts[0,1], pts[1, 1])

	# Resets the view of graph with data
	def resetGraph(self, event=None):
		
		self.v=view.View()
		self.rotate.delete('1.0', tk.END)
		self.zoom.delete('1.0', tk.END)
		self.statslabel.delete('1.0',tk.END)
		
				
	#Clear all data points from screen		
	def clearData(self, event=None):
		for obj in self.objects:
			self.canvas.delete(obj)
		self.objects=[]

	def clearLinRegLines(self, event=None):
		for line in self.linRegLines:
			self.canvas.delete(line)
		self.linRegLines=[]
	
	#Resets the view of the graph and clears the data
	def clearDataAndView(self, event=None): 
		self.clearData()
		self.resetGraph()
		self.clearLinRegLines()

	def handlePCA(self,event=None):

		self.PCAdialog = PCADialogBox(self.root, self.data)

		self.pcaList.append(an.pca(self.data,self.PCAdialog.getDatacols(),self.PCAdialog.getNormalized()))


		if self.PCAdialog.getName() == None:
			name="PCA #" + str(self.num_PCA)
			self.num_PCA +=1

		else:
			name=self.PCAdialog.getName()

		print name
		self.AnalysisWindow.insert(tk.END,name)

		if self.PCAdialog.headers == None:
			print "Select a file"
			self.handleOpen()

		if self.PCAdialog.getDatacols() == None:
			return

		print "data: ", self.PCAdialog.getDatacols()

		#self.AnalysisWindow.insert(tk.END, self.pcaList)

	#Delete PCA object
	def handleDeletePCA(self,event=None):

		idx=self.AnalysisWindow.index(tk.ACTIVE)
		self.AnalysisWindow.delete(idx)

	#View PCA object
	def handleViewPCA(self, event=None):
		if len(self.pcaList)>0:
			idx = self.AnalysisWindow.index(tk.ACTIVE)
			evectors = self.pcaList[idx].get_eigenvectors()
			evals = self.pcaList[idx].get_eigenvalues()
			rawHeaders = self.pcaList[idx].get_raw_headers()
			headers= self.pcaList[idx].get_data_headers()
			#origdata=self.data
			#self.data=self.pcaList[idx]
			#self.curPCA=self.pcaList[idx]
			#self.data=origdata
			self.eigenBox=EigenBox(self.root, headers, evectors, evals, rawHeaders)
			#self.eigenBox=EigenBox(self.root,headers,evectors,evals,headers)

		return

	#Plot PCA object
	def handlePlotPCA(self,event=None):
		if len(self.pcaList)>0:
			idx = self.AnalysisWindow.index(tk.ACTIVE)
			self.eigenBoxDisplay=EigenvectorDisplayBox(self.root,self.pcaList[idx])
			self.buildPoints(self.eigenBoxDisplay.getDatacols())
		return

	def main(self):
		print 'Entering main loop'
		self.root.mainloop()


#Dialog class
class Dialog(tk.Toplevel):

	#Constructor
	def __init__(self, parent, title = None):

		tk.Toplevel.__init__(self, parent)
		self.transient(parent)

		if title:
			self.title(title)

		self.parent = parent

		self.result = None

		body = tk.Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)

		self.buttonbox()

		self.grab_set()

		if not self.initial_focus:
			self.initial_focus = self

		self.protocol("WM_DELETE_WINDOW", self.cancel)

		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		self.initial_focus.focus_set()

		self.wait_window(self)

	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	#
	# standard button semantics

	def ok(self, event=None):

		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()

		self.apply()

		self.cancel()

	def cancel(self, event=None):

		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	#
	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override

class DataDialogBox(Dialog):

	# Constructor
	def __init__(self, parent, data):
		print "within dialog box"
		self.selectVal = 0
		self.shapeVal = 0
		self.numDataPoints = 10
		self.datacols = []
		self.headerXVal = 0
		self.headerYVal = 0
		self.headerZVal = 0
		self.headers = data.get_headers()
		self.colorSelect = None
		Dialog.__init__(self, parent)

	# Creates dialog box so user can choose which axes to plot columns of data on
	# Axes options include x,y,z, color, and size
	def body(self, parent):

		dialogFrame = tk.Frame(self)
		dialogFrame.pack(side=tk.LEFT)
		label = tk.Label(dialogFrame, text="X axis", width=20)

		label.pack(side=tk.TOP, pady=10)

		self.headerXWindow = tk.Listbox(dialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.headerXWindow.pack(side=tk.TOP, padx=5)

		print "headers: ", self.headers
		for i in range(len(self.headers)):
			self.headerXWindow.insert(tk.END, self.headers[i])

		label = tk.Label(dialogFrame, text="Y axis", width=20)
		label.pack(side=tk.TOP, pady=10)

		self.headerYWindow = tk.Listbox(dialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.headerYWindow.pack(side=tk.TOP, padx=5)

		for i in range(len(self.headers)):
			self.headerYWindow.insert(tk.END, self.headers[i])

		label = tk.Label(dialogFrame, text="Z axis", width=20)
		label.pack(side=tk.TOP, pady=10)

		self.headerZWindow = tk.Listbox(dialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.headerZWindow.pack(side=tk.TOP, padx=5)

		for i in range(len(self.headers)):
			self.headerZWindow.insert(tk.END, self.headers[i])

		otherdialogFrame = tk.Frame(self)
		otherdialogFrame.pack(side=tk.LEFT)

		label = tk.Label(otherdialogFrame, text="Color", width=20)
		label.pack(side=tk.TOP, pady=10)

		self.colorWindow = tk.Listbox(otherdialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.colorWindow.pack(side=tk.TOP, padx=5)

		for i in range(len(self.headers)):
			self.colorWindow.insert(tk.END, self.headers[i])

		label = tk.Label(otherdialogFrame, text="Size", width=20)
		label.pack(side=tk.TOP, pady=10)

		self.sizeWindow = tk.Listbox(otherdialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.sizeWindow.pack(side=tk.TOP, padx=5)

		for i in range(len(self.headers)):
			self.sizeWindow.insert(tk.END, self.headers[i])

		self.dataPoints = tk.Entry(self)
		self.dataPoints.pack()

	def apply(self):
		# User can choose 2,3,4,or 5 columns of data to plot
		# x and y are first two dimensions of data
		# z axis is third dimension of data
		# color axis is fourth dimension of data
		# size axis is fifth dimension of data

		self.sizeSelectVal = None
		self.colorSelectVal = None

		headerXVal = self.headerXWindow.curselection()
		if len(headerXVal) > 0:
			self.datacols.append(self.headers[self.headerXWindow.curselection()[0]])
			self.headerXVal = self.headerXWindow.curselection()[0]

		headerYVal = self.headerYWindow.curselection()
		if len(headerYVal) > 0:
			self.datacols.append(self.headers[self.headerYWindow.curselection()[0]])
			self.headerYVal = self.headerYWindow.curselection()[0]

		headerZVal = self.headerZWindow.curselection()
		if len(headerZVal) > 0:
			self.datacols.append(self.headers[self.headerZWindow.curselection()[0]])
			self.headerZVal = self.headerZWindow.curselection()[0]

		colorSelect = self.colorWindow.curselection()
		if len(colorSelect) > 0:
			self.datacols.append(self.headers[self.colorWindow.curselection()[0]])
			self.colorSelectVal = self.colorWindow.curselection()[0]

		sizeSelect = self.sizeWindow.curselection()
		if len(sizeSelect) > 0:
			self.datacols.append(self.headers[self.sizeWindow.curselection()[0]])
			self.sizeSelectVal = self.sizeWindow.curselection()[0]

		print 'Data Points ->', self.dataPoints.get()
		numDataString = self.dataPoints.get().strip()

		if numDataString:
			self.numDataPoints = int(numDataString)
			print self.numDataPoints

		print "Order which data is plotting: ", self.getDatacols()

		# returns list of headers that user chose to plot on x,y,z, color, and size axes
	def getDatacols(self):
		return self.datacols



#Dialog box class
class PCADialogBox(Dialog):
	
	#Constructor
	def __init__(self,parent,d):
		print "within dialog box"
		self.headers = d.get_headers()
		self.rawheaders=d.get_raw_headers()
		self.name=""
		Dialog.__init__(self,parent)
	
	#Creates dialog box so user can choose which data columns to do PCA on
	def body(self,parent):
	
		dialogFrame=tk.Frame(self)
		dialogFrame.pack(side=tk.LEFT)

		label=tk.Label(dialogFrame,text="Data Columns", width=20)
		label.pack(side=tk.TOP,pady=10)
		
		self.PCAWindow=tk.Listbox(dialogFrame,selectmode=tk.MULTIPLE,exportselection=0)
		self.PCAWindow.pack(side=tk.TOP,padx=5)
		
		print "headers: ", self.headers
		for i in range(len(self.headers)):
			self.PCAWindow.insert(tk.END,self.headers[i])
		self.var=tk.StringVar()
		namelabel=tk.Label(dialogFrame,text="Name your PCA")
		namelabel.pack(side=tk.TOP)
		self.typename=tk.Entry(dialogFrame, textvariable = self.var)
		self.typename.pack(side= tk.TOP, padx=5)

		self.checked= tk.IntVar()
		self.c=tk.Checkbutton(dialogFrame,text="Normalize", variable=self.checked)
		self.c.pack()



	def apply(self):
		#User chooses which columns to do PCA on

		self.datacols=[]

		selectedheaders=self.PCAWindow.curselection()
		if len(selectedheaders)>0:
			for i in range(len(selectedheaders)):
				self.datacols.append(self.headers[self.PCAWindow.curselection()[i]])

		self.name=self.typename.get()
		self.normalized = self.var.get()
		if self.normalized==0:
			"You decided not to normalize the data"
		else:
			"You decided to normalize the data"

	def getNormalized(self):
		if self.normalized==0:
			return False
		else:
			return True


	#returns list of headers that user chose to plot on x,y,z, color, and size axes
	def getDatacols(self):
		return self.datacols

	def getName(self):
		if self.name=="":
			return None
		else:
			return self.name

#Creates Dialog Box so user can view eigenvectors and eigenvalues of PCA object on a grid
class EigenBox(Dialog):
	def __init__(self, parent, headers, evecs, evals, rawheaders):
		self.evalues=evals
		self.energy=[]
		self.headers=headers
		self.eHeaders=rawheaders
		self.evectors=evecs
		Dialog.__init__(self,parent)

	def body(self,parent):
		#Make the grid to display eigenvectors and eigenvalues

		dialogFrame = tk.Frame(self)
		dialogFrame.pack(side=tk.LEFT)

		tk.Label(dialogFrame, text="Eigenvalue", bg="blue", fg="white").grid(row=0, column=1, sticky=tk.E+tk.W)
		for i in range(self.evalues.shape[0]):
			tk.Label(dialogFrame, text="%1.5f"%(self.evalues[i]), bg="blue", fg="white").grid(row=i+1,column=1,sticky=tk.E+tk.W)

		print "Values", self.evalues

		tk.Label(dialogFrame, text="Eigenvector", bg="green",fg = "white").grid(row=0, column=0, sticky=tk.E + tk.W)
		for i in range(len(self.eHeaders)):
			if i%2:
				tk.Label(dialogFrame, text=self.headers[i], bg="white", fg = "green").grid(row=0, column=i + 2, sticky=tk.E + tk.W)
			else:
				tk.Label(dialogFrame, text=self.headers[i], bg="green", fg = "white").grid(row=0, column=i+2, sticky=tk.E+tk.W)


		for i in range(self.evalues.shape[0]):
			if i%2:
				tk.Label(dialogFrame, text=self.eHeaders[i], bg="green", fg = "white").grid(row=i+1, column=0, sticky=tk.E + tk.W)
			else:
				tk.Label(dialogFrame, text= self.eHeaders[i], bg="white", fg = "green").grid(row=i+1, column=0, sticky=tk.E+tk.W)


		print "Vectors", self.evectors
		for i in range(self.evectors.shape[0]):
			for j in range(self.evectors.shape[1]):
				if i%2:
					tk.Label(dialogFrame, text="%1.5f" % (self.evectors[i,j]), bg="white", fg = "green").grid(row=i+1, column=j + 2, sticky=tk.E + tk.W)
				else:
					tk.Label(dialogFrame, text="%1.5f" % (self.evectors[i,j]), bg="green", fg = "white").grid(row=i+1, column=j+2, sticky=tk.E+tk.W)



class EigenvectorDisplayBox(Dialog):
	def __init__(self, parent, pcadata):
		print "within dialog box"
		self.selectVal = 0
		self.shapeVal = 0
		self.numDataPoints = 10
		self.datacols = []
		self.headerXVal = 0
		self.headerYVal = 0
		self.headerZVal = 0
		self.eheaders = pcadata.get_raw_headers()
		self.colorSelect = None
		Dialog.__init__(self, parent)

	# Creates dialog box so user can choose which axes to plot eigenvectors of PCA data object on
	# Axes options include x,y,z, color, and size
	def body(self, parent):

		dialogFrame = tk.Frame(self)
		dialogFrame.pack(side=tk.LEFT)
		label = tk.Label(dialogFrame, text="X axis", width=20)

		label.pack(side=tk.TOP, pady=10)

		self.headerXWindow = tk.Listbox(dialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.headerXWindow.pack(side=tk.TOP, padx=5)

		print "headers: ", self.eheaders
		for i in range(len(self.eheaders)):
			self.headerXWindow.insert(tk.END, self.eheaders[i])

		label = tk.Label(dialogFrame, text="Y axis", width=20)
		label.pack(side=tk.TOP, pady=10)

		self.headerYWindow = tk.Listbox(dialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.headerYWindow.pack(side=tk.TOP, padx=5)

		for i in range(len(self.eheaders)):
			self.headerYWindow.insert(tk.END, self.eheaders[i])

		label = tk.Label(dialogFrame, text="Z axis", width=20)
		label.pack(side=tk.TOP, pady=10)

		self.headerZWindow = tk.Listbox(dialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.headerZWindow.pack(side=tk.TOP, padx=5)

		for i in range(len(self.eheaders)):
			self.headerZWindow.insert(tk.END, self.eheaders[i])

		otherdialogFrame = tk.Frame(self)
		otherdialogFrame.pack(side=tk.LEFT)

		label = tk.Label(otherdialogFrame, text="Color", width=20)
		label.pack(side=tk.TOP, pady=10)

		self.colorWindow = tk.Listbox(otherdialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.colorWindow.pack(side=tk.TOP, padx=5)

		for i in range(len(self.eheaders)):
			self.colorWindow.insert(tk.END, self.eheaders[i])

		label = tk.Label(otherdialogFrame, text="Size", width=20)
		label.pack(side=tk.TOP, pady=10)

		self.sizeWindow = tk.Listbox(otherdialogFrame, selectmode=tk.SINGLE, exportselection=0)
		self.sizeWindow.pack(side=tk.TOP, padx=5)

		for i in range(len(self.eheaders)):
			self.sizeWindow.insert(tk.END, self.eheaders[i])

		self.dataPoints = tk.Entry(self)
		self.dataPoints.pack()

	def apply(self):
		# User can choose 2,3,4,or 5 columns of eigenvectors to project data onto
		# x and y are first two dimensions of data
		# z axis is third dimension of data
		# color axis is fourth dimension of data
		# size axis is fifth dimension of data

		self.sizeSelectVal = None
		self.colorSelectVal = None

		headerXVal = self.headerXWindow.curselection()
		if len(headerXVal) > 0:
			self.datacols.append(self.eheaders[self.headerXWindow.curselection()[0]])
			self.headerXVal = self.headerXWindow.curselection()[0]

		headerYVal = self.headerYWindow.curselection()
		if len(headerYVal) > 0:
			self.datacols.append(self.eheaders[self.headerYWindow.curselection()[0]])
			self.headerYVal = self.headerYWindow.curselection()[0]

		headerZVal = self.headerZWindow.curselection()
		if len(headerZVal) > 0:
			self.datacols.append(self.eheaders[self.headerZWindow.curselection()[0]])
			self.headerZVal = self.headerZWindow.curselection()[0]

		colorSelect = self.colorWindow.curselection()
		if len(colorSelect) > 0:
			self.datacols.append(self.eheaders[self.colorWindow.curselection()[0]])
			self.colorSelectVal = self.colorWindow.curselection()[0]

		sizeSelect = self.sizeWindow.curselection()
		if len(sizeSelect) > 0:
			self.datacols.append(self.eheaders[self.sizeWindow.curselection()[0]])
			self.sizeSelectVal = self.sizeWindow.curselection()[0]

		print 'Data Points ->', self.dataPoints.get()
		numDataString = self.dataPoints.get().strip()

		if numDataString:
			self.numDataPoints = int(numDataString)
			print self.numDataPoints

		print "Order which data is plotting: ", self.getDatacols()

		# returns list of headers that user chose to plot on x,y,z, color, and size axes
	def getDatacols(self):
		return self.datacols

if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()


