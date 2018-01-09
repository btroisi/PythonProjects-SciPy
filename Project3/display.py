# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
# Modifed for Project3 by Brandon Troisi
# CS 251
# 

import Tkinter as tk
import tkFont as tkf
import math
import random
import os
import view
import numpy as np

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
		
		#created matrix of endpoints of x,y, and z axes
		self.axes=np.matrix([[0,0,0,1],[1,0,0,1],[0,0,0,1],[0,1,0,1],[0,0,0,1],[0,0,1,1]])

		#list to store the lines for the x, y, and z axes
		self.lines=[0,0,0]
		
		#calls buildAxes function
		self.buildAxes()
		
		#calls updateAxes function
		self.updateAxes()
	
	#draws the x, y, and z axes in display window	
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
		menutext = [ [ '-', '-', 'Quit	\xE2\x8C\x98-Q' ],
					 [ 'Command 1', '-', '-' ] ]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
		menucmd = [ [self.clearData, None, self.handleQuit],
					[self.handleMenuCmd1, None, None] ]
		
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

		

		
		# create reset button
		resetbutton = tk.Button( rightcntlframe, text="Reset", 
							   command=self.resetGraph)
		
		resetbutton.pack(side=tk.TOP)  # default side is top
		
		#create quit button
		quitbutton = tk.Button( rightcntlframe, text="Quit", 
							   command=self.handleQuit)
		
		quitbutton.pack(side=tk.TOP)  # default side is top
		
		#create text to display how much axes got rotated
		self.rotate=tk.Text(self.root, height=1, width=75)
		self.rotate.pack(side=tk.TOP)
		
		#create text to display how you zoomed in on the axes
		self.zoom=tk.Text(self.root, height=1, width=75)
		self.zoom.pack(side=tk.TOP)
		
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
	
	#Quits the application
	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()
	
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
		
		
	# Resets the graph	
	def resetGraph(self, event=None):
		
		self.v=view.View()
		self.updateAxes()
		self.rotate.delete('1.0', tk.END)
		self.zoom.delete('1.0', tk.END)
		
			
	#Clear all data points from screen		
	def clearData(self, event=None):
		for obj in self.objects:
			self.canvas.delete(obj)
		self.objects=[]
		
	def main(self):
		print 'Entering main loop'
		self.root.mainloop()



if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()


