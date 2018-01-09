import data
import numpy as np
import scipy.stats as st
#import display

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

def linearRegression(data, indepheaders, depheader ):

	y=np.matrix(data.get_data([depheader]))
	A0=np.matrix(data.get_data(indepheaders))
	ones=np.ones((A0.shape[0],1))
	A=np.hstack((A0,ones))

	AAinv=np.linalg.inv(np.dot(A.T,A))

	x=np.linalg.lstsq(A,y)

	b=x[0]
	N=y.shape[0]
	C=b.shape[0]
	df_e=N-C

	error=y-np.dot(A,b)

	sse=np.dot(error.T,error)/df_e

	stderr=np.sqrt(np.diagonal(sse[0,0]*AAinv))

	t=b.T/stderr

	p=2*(1-st.t.cdf(abs(t),df_e))

	r2=1-error.var()/y.var()

	return b,sse,r2,t,p

def pca(d,headers,normalized=True):
	if(normalized):
		A = normalize_columns_separately(d, headers)
	else:
		A=d.get_data(headers)


	print A
	m = np.mean(A, axis=0)
	D=A-m

	U,S,V=np.linalg.svd(D,full_matrices=False)
	print "V", V
	print "D", D
	N=A.shape[0]
	evals=(S*S)/(N-1)

	projected=(V*D.T).T
	print "projected data", projected
	pcaData= data.PCAData(headers,projected,evals,V,m)
	return pcaData

#tests above methods for 2015 NFL defense statistics by team
#data being analyzed is everything from column 1 on because
#column 0 contains numeric data irrelevant for analysis
def main():
	testdata = data.Data('pcatest.csv')
	testheaders = dnoisy.get_headers();
	print pca(testdata,testheaders)
	
	
if __name__=='__main__':
	main()
	