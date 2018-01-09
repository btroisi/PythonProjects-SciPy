# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
# Modifed for Project1 by Brandon Troisi
# CS 251
# 

import Tkinter as tk
import tkFont as tkf
import math
import random
import os

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
		self.dialog=DialogBox(self.root) #new dialogbox object
		self.baseClick = None # used to keep track of mouse movement
		

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

		# make a menubutton
		self.colorOption = tk.StringVar( self.root )
		self.colorOption.set("black")
		colorMenu = tk.OptionMenu( rightcntlframe, self.colorOption, 
										"black", "blue", "red", "green" ) # can add a command to the menu
		colorMenu.pack(side=tk.TOP)
		
		self.numberOption = tk.StringVar( self.root )
		self.numberOption.set("10")
		numberMenu = tk.OptionMenu( rightcntlframe, self.numberOption, 
										"10", "20", "50", "100", "200" ) # can add a command to the menu
		numberMenu.pack(side=tk.TOP)
		

		# make a button in the frame
		# and tell it to call the handleButton method when it is pressed.
		button = tk.Button( rightcntlframe, text="Update Color", 
							   command=self.handleButton1 )
		button1 = tk.Button( rightcntlframe, text="Create Points",
							command=self.createRandomDataPoints)
		button.pack(side=tk.TOP)  # default side is top
		button1.pack(side=tk.TOP)

		return

	def setBindings(self):
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<Button-2>', self.handleMouseButton2 )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
		self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )

		# bind command sequences to the root window
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-n>', self.clearData )

	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()

	def handleButton1(self):
		print 'handling command button:'
		self.colorOption.get()
		for obj in self.objects:
			self.canvas.itemconfig(obj, fill=self.colorOption.get() )

	def handleMenuCmd1(self):
		print 'handling menu command 1'

	def handleMouseButton1(self, event):
		
	   print 'handle mouse button 1: %d %d' % (event.x, event.y)
	   self.baseClick = (event.x, event.y)

	def handleMouseButton2(self, event):
		
		self.baseClick = (event.x, event.y)
		print 'handle mouse button 2: %d %d' % (event.x, event.y)
	

	# This is called if the first mouse button is being moved
	def handleMouseButton1Motion(self, event):
		# calculate the difference
		diff = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )

		# update base click
		self.baseClick = ( event.x, event.y )
		print 'handle button1 motion %d %d' % (diff[0], diff[1])
		for obj in self.objects:
			loc = self.canvas.coords(obj)
			self.canvas.coords( obj, loc[0] + diff[0], loc[1] + diff[1], loc[2] + diff[0], 
			loc[3] + diff[1] )

			
	# This is called if the second button of a real mouse has been pressed
	# and the mouse is moving. Or if the control key is held down while
	# a person moves their finger on the track pad.
	def handleMouseButton2Motion(self, event):
		print 'handle button 2 motion'
		dx = 3
		rgb = "#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )
		oval = self.canvas.create_oval( event.x - dx, event.y - dx, event.x + dx, event.y + dx,
		fill = rgb, outline='')
		self.objects.append( oval )
	
	# Adds data points to display	
	def createRandomDataPoints(self, event=None):
		
		dx=5
		dy=5
		
		print self.dialog.getShapeVal
		
		#If the user chooses to draw data points as a circle
		if self.dialog.getShapeVal()==0:
			print 'Drawing circle'
		
			#If the user chooses a uniform distribution
			if self.dialog.getSelectionVal()==0:
				for i in range(int(self.numberOption.get())):	
					x=random.uniform(0,self.initDx)
					y=random.uniform(0,self.initDy)
				
					pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, 
						fill=self.colorOption.get(), outline='' )
					self.objects.append(pt)	  
			
			#If the user chooses a random distribution
			if self.dialog.getSelectionVal()==1:	 
				for i in range(int(self.numberOption.get())):
					x=random.gauss(self.initDx/2,self.initDx/8)
					#x=random.gauss(0,self.initDx)
					#y=random.gauss(0,self.initDy)
					y=random.gauss(self.initDy/2,self.initDy/8)
					pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, 
						fill=self.colorOption.get(), outline='' )
					self.objects.append(pt)	  
		
		#If the user chooses to draw data points as a square
		if self.dialog.getShapeVal()==1:
			print 'Drawing square'
		
			#If the user chooses a uniform distribution
			if self.dialog.getSelectionVal()==0:
				for i in range(int(self.numberOption.get())):	
					x=random.uniform(0,self.initDx)
					y=random.uniform(0,self.initDy)
				
					pt = self.canvas.create_rectangle( x-dx, y-dx, x+dx, y+dx, 
						fill=self.colorOption.get(), outline='' )
					self.objects.append(pt)		
			
			#If the user chooses a random distribution
			if self.dialog.getSelectionVal()==1:	 
				for i in range(int(self.numberOption.get())):
					x=random.gauss(self.initDx/2,self.initDx/5)
					y=random.gauss(self.initDy/2,self.initDy/5)
					pt = self.canvas.create_rectangle( x-dx, y-dx, x+dx, y+dx, 
						fill=self.colorOption.get(), outline='' )
					self.objects.append(pt)	  
	
			
	#Clear all data points from screen		
	def clearData(self, event=None):
		for obj in self.objects:
			self.canvas.delete(obj)
		self.objects=[]
		
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

#Dialog box class
class DialogBox(Dialog):
	
	#Constructor
	def __init__(self,parent):
		print "within dialog box"
		self.selectVal=0
		self.shapeVal=0
		self.numDataPoints=10
		Dialog.__init__(self,parent)
	
	#Creates dialog box so user can choose between gaussian and random distributions
	#Creates dialog box so that you can choose between square and circular data points to draw
	def body(self,parent):
	
		dialogFrame=tk.Frame(self)
		dialogFrame.pack(side=tk.TOP)
		label=tk.Label(dialogFrame,text="Distribution Type", width=20)
		
		label.pack(side=tk.TOP,pady=10)
		
		self.distWindow=tk.Listbox(dialogFrame,selectmode=tk.SINGLE,exportselection=0)
		self.distWindow.pack(side=tk.TOP,padx=5)
		
		self.distWindow.insert(tk.END,"Uniform")
		self.distWindow.insert(tk.END,"Gaussian")
		
		label=tk.Label(dialogFrame,text="Shape",width=20)
		label.pack(side=tk.TOP,pady=10)
		
		self.shapeWindow=tk.Listbox(dialogFrame,selectmode=tk.SINGLE,exportselection=0)
		self.shapeWindow.pack(side=tk.TOP,padx=5)
		
		self.shapeWindow.insert(tk.END,"Circle")
		self.shapeWindow.insert(tk.END,"Square")
		
		self.dataPoints=tk.Entry(self)
		self.dataPoints.pack()
		
	def apply(self):
		
		selectionVal=self.distWindow.curselection()
		if len(selectionVal)>0:
			self.selectVal=self.distWindow.curselection()[0]
			print self.selectVal
			
		shapeVal=self.shapeWindow.curselection()
		if len(shapeVal)>0:
			self.shapeVal=self.shapeWindow.curselection()[0]
			print self.shapeVal
			
		print 'Data Points ->', self.dataPoints.get()
		numDataString=self.dataPoints.get().strip()
		
		if numDataString:
			self.numDataPoints=int(numDataString)
			print self.numDataPoints
			
	def getSelectionVal(self):
		
		return self.selectVal
		
	def getShapeVal(self):
		
		return self.shapeVal
		
		
	

if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()


