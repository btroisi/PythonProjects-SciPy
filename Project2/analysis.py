import data
import numpy as np

#returns the range of columns of data by returning min and max of data column as ordered pair
def data_range(data, column_headers):
	
	data=data.get_data(column_headers)
	mins=np.min(data, axis=0)
	maxs=np.max(data,axis=0)
	range=np.hstack([mins.T,maxs.T])
	return range

#returns the mean of a specified set of columns of data
def mean(data, column_headers):
	
	data=data.get_data(column_headers)
	mean=np.mean(data,axis=0)
	meanmatrix=np.hstack([mean])
	return meanmatrix

#returns the standard deviation of a specified set of columns of data
def stdev(data, column_headers):
	
	data=data.get_data(column_headers)
	std=np.std(data,axis=0)
	std=np.hstack([std])
	stdmatrix=np.hstack([std])
	return stdmatrix
	
#Goes through set of specified set of columns maps min value of column to 0 and max value to 1
def normalize_columns_separately(data, column_headers):
	
	data=data.get_data(column_headers)
	mins=np.min(data, axis=0)
	maxs=np.max(data,axis=0)
	dtmp=data-mins
	norm=dtmp/(maxs-mins)
	normmatrix=np.hstack([norm])
	return normmatrix

#Goes through set of specified set of columns maps min value of all of specified columns to 0 and max value to 1
def normalize_columns_together(data, column_headers):
	
	data=data.get_data(column_headers)
	mins=np.min(data)
	maxs=np.max(data)
	dtmp=data-mins
	norm=dtmp/(maxs-mins)
	normmatrix=np.hstack([norm])
	return normmatrix

#tests above methods for 2015 NFL defense statistics by team
#data being analyzed is everything from column 1 on because
#column 0 contains numeric data irrelevant for analysis
def main():
	d = data.Data('DEF.csv')
	headers=d.get_headers();
	head=headers[1:]
	print "relevant data headers"
	print head
	print "datarange"
	print data_range(d,head)
	print "mean"
	print mean(d,head)
	print "standard deviation"
	print stdev(d,head)
	print "normalizing columns separately"
	print normalize_columns_separately(d,head)
	print "normalizing columns together"
	print normalize_columns_together(d,head)
	
	
if __name__=='__main__':
	main()
	