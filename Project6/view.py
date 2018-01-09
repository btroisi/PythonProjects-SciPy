#Brandon Troisi
#2/21/17
#view.py

import numpy as np
import math

class View:

	def __init__(self):
		#Calls the reset method
		self.reset()
		
	def reset(self):
		#Initializes the fields
		self.vrp=np.matrix([0.5,0.5,1])
		self.vpn=np.matrix([0,0,-1])
		self.vup=np.matrix([0,1,0])
		self.u=np.matrix([-1,0,0])
		self.extent=[1,1,1]
		self.screen=[400,400]
		self.offset=[20,20]
		
		
	def build(self):
		#Builds the view transfomation matrix (vtm)
		vtm=np.identity(4,float)
		
		t1 = np.matrix( [[1, 0, 0, -self.vrp[0, 0]],
					[0, 1, 0, -self.vrp[0, 1]],
					[0, 0, 1, -self.vrp[0, 2]],
					[0, 0, 0, 1] ] )
				
		vtm=t1*vtm
		
		tu=np.cross(self.vup,self.vpn)
		tvup=np.cross(self.vpn,tu)
		tvpn=np.copy(self.vpn)
		
		
		
		self.u=self.normalize(tu).copy()
		self.vup=self.normalize(tvup).copy()
		self.vpn=self.normalize(tvpn).copy()
	
		
		r1 = np.matrix( [[ tu[0, 0], tu[0, 1], tu[0, 2], 0.0 ],
					[ tvup[0, 0], tvup[0, 1], tvup[0, 2], 0.0 ],
					[ tvpn[0, 0], tvpn[0, 1], tvpn[0, 2], 0.0 ],
					[ 0.0, 0.0, 0.0, 1.0 ] ] )

		vtm=r1*vtm
		
		vtm = np.matrix( [[1, 0, 0, 0.5*self.extent[0]],
					[0, 1, 0, 0.5*self.extent[1]],
					[0, 0, 1, 0],
					[0, 0, 0, 1] ] )* vtm
		
		
		vtm = np.matrix( [[-self.screen[0] / self.extent[0], 0, 0, 0],
					[0, -self.screen[1] / self.extent[1], 0, 0],
					[0, 0, 1.0 / self.extent[2], 0],
					[0, 0, 0, 1] ] )* vtm
		
		vtm = np.matrix( [[1, 0, 0, self.screen[0] + self.offset[0]],
					[0, 1, 0, self.screen[1] + self.offset[1]],
					[0, 0, 1, 0],
					[0, 0, 0, 1] ] )* vtm
		
		return vtm
		
	def normalize(self,col):
		#Normalizes a specified vectore
		xcomp=col[0,0]
		ycomp=col[0,1]
		zcomp=col[0,2]
		length=math.sqrt(xcomp*xcomp+ycomp*ycomp+zcomp*zcomp)
		vx=col[0,0]/length
		vy=col[0,1]/length
		vz=col[0,2]/length
		norm=np.matrix([vx,vy,vz])
		return norm
		
		
	def clone(self):
		#Creates a copy of the view object 
		
		vobj=View()
		vobj.vrp=np.matrix([0.5,0.5,1])
		vobj.vpn=np.matrix([0,0,-1])
		vobj.vup=np.matrix([0,1,0])
		vobj.u=np.matrix([-1,0,0])
		vobj.extent=[1,1,1]
		vobj.screen=[400,400]
		vobj.offset=[20,20]
		
		return vobj
	
	#Rotate the center of the view plot
	def rotateVRC(self, vupangle,uangle):
	
		
					
		t1=np.matrix( [[1, 0, 0, -(self.vrp[0, 0]+self.vpn[0,0]*self.extent[2]*0.5)],
					[0, 1, 0,  -(self.vrp[0, 1]+self.vpn[0,1]*self.extent[2]*0.5)],
					[0, 0, 1, -(self.vrp[0, 2]+self.vpn[0,2]*self.extent[2]*0.5)],
					[0, 0, 0, 1] ] )
		
		
		Rxyz=np.matrix([[self.u[0,0],self.u[0,1],self.u[0,2],0],
		[self.vup[0,0],self.vup[0,1],self.vup[0,2],0],
		[self.vpn[0,0],self.vpn[0,1],self.vpn[0,2],0],
		[1,0,0,0]])
		
		r1=np.matrix( [[math.cos(vupangle), 0, math.sin(vupangle),0],
					[0, 1, 0, 0],
					[-(math.sin(vupangle)), 0, math.cos(vupangle), 0],
					[0, 0, 0, 1] ] )
					
		r2=np.matrix( [[1, 0,0,0],
					[0, math.cos(uangle), -(math.sin(uangle)), 0],
					[0, math.sin(uangle), math.cos(uangle), 0],
					[0, 0, 0, 1] ] )
			
		t2=np.matrix( [[1, 0, 0, self.vrp[0, 0]+self.vpn[0,0]*self.extent[2]*0.5],
					[0, 1, 0,  self.vrp[0, 1]+self.vpn[0,1]*self.extent[2]*0.5],
					[0, 0, 1, self.vrp[0, 2]+self.vpn[0,2]*self.extent[2]*0.5],
					[0, 0, 0, 1] ] )
					
		tvrc=np.matrix( [[self.vrp[0,0], self.vrp[0,1], self.vrp[0,2], 1.0],
					[self.u[0,0], self.u[0,1], self.u[0,0], 0],
					[self.vup[0,0], self.vup[0,1], self.vup[0,2], 0.0],
					[self.vpn[0,0], self.vpn[0,1], self.vpn[0,2],0.0 ] ] )
		
		tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T
		
		self.vrc=tvrc[0]
		self.u=self.normalize(tvrc[1])
		self.vup=self.normalize(tvrc[2])
		self.vpn=self.normalize(tvrc[3])
# 		
	def main(self):
		self.reset()
		
	
if __name__=="__main__":
	v=View()
	print "Building matrix...", v.build()
	