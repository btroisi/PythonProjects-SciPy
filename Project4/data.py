#Brandon Troisi
#2/14/17
#Data.py

import csv
import numpy as np

class Data:

	def __init__(self,filename=None):
		
		#fields 
		self.raw_headers=[]
		self.raw_types=[]
		self.raw_data=[]
		self.header2raw={}
		self.raw_num_rows=0
		self.raw_num_columns=0
		self.raw_row=[]
		self.raw_value=0
		self.matrix_data = np.matrix([]) # matrix of numeric data
		self.header2matrix = {} # dictionary mapping header string to index of column in matrix data
		self.dataCol=np.matrix([])

		
		#prints name of file being read
		if filename!=None:
			print filename
			self.read(filename)
	
	#reads and processes headers, types of data, and data in CSV file		
	def read(self,filename):
	
		file=open(filename, "rU")
		reader=csv.reader(file,delimiter=',',quotechar='|')
		
		
		self.raw_headers=reader.next() #first line read in is the headers for data being read in
		self.raw_types=reader.next() #second line read in is the type of data being read in
		
		#gets rid of spaces in headers
		for i in range(len(self.raw_headers)):
			self.raw_headers[i]=self.raw_headers[i].strip()
		
		#gets rid of spaces in headers
		for i in range(len(self.raw_types)):
			self.raw_types[i]=self.raw_types[i].strip()
		
		#reads in each row of data in CSV file
		for row in reader:
			for i in range(len(row)):
				row[i]=row[i].strip()
			print row
			self.raw_data.append(row)
			self.raw_num_rows+=1
		
		self.raw_num_columns=len(self.raw_headers)
		
		matrixIdx=0
		dataArr=[]
		cols=0
		#If data that was read in is numeric, convert this data from string to float.
		#Then this numeric data in form of a float gets added to a data matrix
		for i in range(self.get_raw_num_columns()):
			if self.raw_types[i]=="numeric":
				self.header2matrix[self.raw_headers[i]]=matrixIdx
				matrixIdx+=1
				cols+=1
				for j in range(len(self.raw_data)):	
					if self.raw_data[j][i]=='':
						self.raw_data[j][i]=-9999
					dataArr.append((float)(self.raw_data[j][i]))

		#data matrix is created
		self.matrix_data=np.matrix(dataArr).reshape(cols,self.get_raw_num_rows()).T
		print "matrix of data"
		print self.matrix_data
		print "header2matrix", self.header2matrix	
		
	#returns raw headers
	def get_raw_headers(self):
		return self.raw_headers
	
	#returns raw type of data being read in
	def get_raw_type(self):
		return self.raw_types
	
	#returns the raw data
	def get_raw_data(self):
		return self.raw_data
	
	#returns the number of raw rows	
	def get_raw_num_rows(self):
		return self.raw_num_rows
	
	#returns the number of raw columns
	def get_raw_num_columns(self):
		return self.raw_num_columns
	#returns a row of raw data given an index
	def get_raw_row(self,index):
		return self.raw_data[index]
	
	#returns a raw value given a row and a key	
	def get_raw_value(self,row,key):
	
		idx=0
		for i in self.raw_headers:
			if i==key:
				return self.raw_data[row][idx]
			else:
				idx+=1
	
	#returns headers of numeric data
	def get_headers(self):
		return self.header2matrix.keys()
		
	#returns number of columns of numeric data
	def get_num_columns(self): 
		return self.matrix_data.shape[1]
	
	#take row index and returns row of numeric data
	def get_row(self,row):
		return self.matrix_data[row,:]
	
	#returns data in numeric matrix
	def get_value(self,row,header):
		#print "self.header2matrix"
		#print self.header2matrix
		idx=self.header2matrix.get(header)
		print "header:",header
		if idx!=None:
			return self.matrix_data[row,idx]
		else:
			return None
	
	#Returns data matrix for specified column header indices and row indices
	def get_data(self, headers, a=None, b=None):
		data=self.matrix_data[a:b,self.header2matrix[headers[0]]]
		for header in headers[1:]:
			data=np.hstack([data,self.matrix_data[a:b,self.header2matrix[header]]])
		return data
	
	#Executes read function
	def main(self):
		self.read("baddatafile.csv")

#tests methods for data in data matrix		
if __name__== '__main__':
		
	d = Data('DEF.csv')
	headers=d.get_headers()
	print "d.get_headers"
	print headers
	print "d.get_num_columns"
	print d.get_num_columns()
	print "d.get_row(1)"
	print d.get_row(1)
	print "d.get_value(1,spaces)"
	print d.get_value(1,"spaces")
	print "d.get_data all columns but the first"
	print d.get_data(headers[1:])
	


	
	
	
		

		
	