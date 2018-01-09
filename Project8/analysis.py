import data
import numpy as np
import scipy.stats as st
import scipy.cluster.vq as vq
import random
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

#Calculates linear regression for a data set with an independent and dependent header
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

#Calculates PCA for a data object with a specified set of headers
def pca(d,headers,normalized=True):
	if(normalized):
		A = normalize_columns_separately(d, headers)
	else:
		A=d.get_data(headers)

	m = np.mean(A, axis=0)
	D=A-m

	U,S,V=np.linalg.svd(D,full_matrices=False)

	N=A.shape[0]
	evals=(S*S)/(N-1)

	projected=(V*D.T).T

	pcaData= data.PCAData(headers,projected,evals,V,m)
	return pcaData

#Kmeans algorithm using numpy
def kmeans_numpy(d,headers,K,whiten=True):

	A=d.get_data(headers)
	W=vq.whiten(A)
	codebook,bookerror=vq.kmeans(W,K)
	codes,error=vq.vq(W,codebook)
	return codebook, codes, error

#Creates k means for every cluster that is made
def kmeans_init(data,K,categories=None):

	clustermeans=[]
	row=random.randint(0,data.shape[0])
	if categories==None:
		#If no categories are given choose K random data points
		for i in range(K):
			row1=random.randint(0,data.shape[0]-1)
			if row!=row1:
				clustermeans.append(data[row1].tolist()[0])
			else:
				row1=random.randint(0,data.shape[0]-1)
				clustermeans.append(data[row1].tolist()[0])

	else:
		#If categories are chosen, compute the mean values for each categories
		#set those as initial means
		for i in range(K):
			idx=np.array(categories.T)[0]
			if i==0:
				clustermeans=np.mean(data[idx==i,:],axis=0)
			else:
				clustermeans=np.vstack((clustermeans,np.mean(data[idx==i,:],axis=0)))

	return np.matrix(clustermeans)



def kmeans_classify(data,clustermeans):
	#Assigns data point to a cluster id by computing distance to nearest mean

	idvals=np.matrix(np.zeros((data.shape[0],1)),dtype=np.int)
	dist= np.matrix(np.zeros((data.shape[0],1)),dtype=np.float)

	for i in range(data.shape[0]):
		tempdist=[]
		pts=data[i]
		for j in range(clustermeans.shape[0]):
			mean=clustermeans[j]
			tempdist.append(np.linalg.norm(mean-pts))
		distarr=np.asarray(tempdist).copy()
		distarr.sort()
		dist[i,0]=distarr[0]
		idvals[i,0]=tempdist.index(distarr[0])

	return idvals, dist

def kmeans_algorithm(A, means):
	# set up some useful constants
	MIN_CHANGE = 1e-7
	MAX_ITERATIONS = 100

	D = means.shape[1]
	K = means.shape[0]
	N = A.shape[0]

	# iterate no more than MAX_ITERATIONS
	for i in range(MAX_ITERATIONS):
		# calculate the codes
		codes, errors = kmeans_classify( A, means )

		# calculate the new means
		newmeans = np.zeros_like( means )
		counts = np.zeros( (K, 1) )
		for j in range(N):
			newmeans[codes[j,0],:] += A[j,:]
			counts[codes[j,0],0] += 1.0


		# finish calculating the means, taking into account possible zero counts
		for j in range(K):
			if counts[j,0] > 0.0:
				newmeans[j,:] /= counts[j,0]
			else:
				newmeans[j,:] = A[random.randint(0,A.shape[0]),:]

		# test if the change is small enough
		diff = np.sum(np.square(means - newmeans))
		means = newmeans
		if diff < MIN_CHANGE:
			break

	# call classify with the final means
	codes, errors = kmeans_classify( A, means )

	# return the means, codes, and errors

	return (means, codes, errors)

def kmeans(d, headers, K, whiten=True, categories=None):
	'''Takes in a Data object, a set of headers, and the number of clusters to create
	   Computes and returns the codebook, codes and representation errors.
	   If given an Nx1 matrix of categories, it uses the category labels
	   to calculate the initial cluster means.
	   '''
	A=d.get_data(headers)
	if whiten==True:
		W=vq.whiten(A)
	else:
		W=A

	codebook=kmeans_init(W,K,categories)
	codebook,codes,errors=kmeans_algorithm(W,codebook)

	return codebook,codes,errors
#tests above methods for 2015 NFL defense statistics by team
#data being analyzed is everything from column 1 on because
#column 0 contains numeric data irrelevant for analysis
def main():
	testdata = data.Data('pcatest.csv')
	testheaders = dnoisy.get_headers();
	print pca(testdata,testheaders)
	
	
if __name__=='__main__':
	main()
	