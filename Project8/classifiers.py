# Template by Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

import sys
import data
import analysis as an
import numpy as np

class Classifier:

    def __init__(self, type):
        '''The parent Classifier class stores only a single field: the type of
        the classifier.  A string makes the most sense.

        '''
        self._type = type

    def type(self, newtype = None):
        '''Set or get the type with this function'''
        if newtype != None:
            self._type = newtype
        return self._type

    def confusion_matrix( self, truecats, classcats ):
        '''Takes in two Nx1 matrices of zero-index numeric categories and
        computes the confusion matrix. The rows represent true
        categories, and the columns represent the classifier output.

        '''
        uniquetruecats, mappingTrue = np.unique(np.array(truecats.T), return_inverse=True)
        uniqueclasscats, mappingClass = np.unique(np.array(classcats.T), return_inverse=True)

        uniquetruecats=uniquetruecats.tolist()
        uniqueclasscats=uniqueclasscats.tolist()


        unique=np.unique(np.array(uniquetruecats))

        confmatrix=np.matrix(np.zeros((unique.shape[0],unique.shape[0])))

        for i in range(truecats.shape[0]):
            confmatrix[mappingTrue[i],mappingClass[i]]+=1

        return confmatrix

    def confusion_matrix_str( self, cmtx ):

        '''Takes in a confusion matrix and returns a string suitable for printing.'''
        s = '%10s' %('True->')

        for i in range(cmtx.shape[1]):
            s+="%5d_True"%(i,)
        s+="\n"

        for i in range(cmtx.shape[0]):
            s += "Pred_Cat%2d" %(i,)
            for j in range(cmtx.shape[1]):
                s += "%10d" % (cmtx[i,j],)
            s+="\n"
        return s

    def __str__(self):
        '''Converts a classifier object to a string.  Prints out the type.'''
        return str(self._type)



class NaiveBayes(Classifier):
    '''NaiveBayes implements a simple NaiveBayes classifier using a
    Gaussian distribution as the pdf.

    '''

    def __init__(self, dataObj=None, headers=[], categories=None):
        '''Takes in a Data object with N points, a set of F headers, and a
        matrix of categories, one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'Naive Bayes Classifier')

        # store the headers used for classification
        self.headers = headers

        # number of classes and number of features
        self.num_classes = 0
        self.num_feats = 0


        # original class labels
        self.origclasslabels = []

        # unique data for the Naive Bayes: means, variances, scales
        self.means=np.matrix([])
        self.vars=np.matrix([])
        self.scales=np.matrix([])

        # if given data,
            # call the build function
        if dataObj!=None:
            self.build(dataobj.get_data(headers),categories)

    def build( self, A, categories ):
        '''Builds the classifier give the data points in A and the categories'''

        A=np.matrix(A)


        # figure out how many categories there are and get the mapping (np.unique)
        uniqueclasses, mapping = np.unique(np.array(categories.T), return_inverse=True)
        # create the matrices for the means, vars, and scales

        self.num_classes=uniqueclasses.size
        self.origclasslabels=uniqueclasses
        self.num_feats=A.shape[1]

        self.means=np.matrix(np.zeros((self.num_classes,self.num_feats)))
        self.vars=np.matrix(np.zeros((self.num_classes,self.num_feats)))
        self.scales=np.matrix(np.zeros((self.num_classes,self.num_feats)))



        for i in range(self.num_classes):
            self.means[i,:]=np.mean(A[(mapping==i),:],axis=0)
            self.vars[i,:]= np.var(A[(mapping==i),:],axis=0)


        for i in range(self.scales.shape[0]):
            for j in range(self.scales.shape[1]):
                self.scales[i,j] = (1/(np.sqrt(2*np.pi*self.vars[i,j])))
        # the output matrices will be categories (C) x features (F)
        # compute the means/vars/scales for each class
        # store any other necessary information: # of classes, # of features, original labels

        return

    def classify( self, A, return_likelihoods=False ):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_likelihoods
        is True, it also returns the NxC likelihood matrix.

        '''
        A=np.matrix(A)
        # error check to see if A has the same number of columns as
        # the class means
        if A.shape[1]!=self.means.shape[1]:
            return


        # make a matrix that is N x C to store the probability of each
        # class for each data point
        N=A.shape[0]
        C=self.num_classes
        P = np.matrix(np.zeros((N,C))) # a matrix of zeros that is N (rows of A) x C (number of classes)



        # calculate the probabilities by looping over the classes
        #  with numpy-fu you can do this in one line inside a for loop
        for i in range(C):
            P[:,i]=np.prod(np.multiply(self.scales[i,:],np.exp(-np.square((A-self.means[i,:]))/(2*self.vars[i,:]))),axis=1)


        # calculate the most likely class for each data point
        # take the argmax of P along axis 1
        cats = np.asarray(np.argmax(P,axis=1))


        # use the class ID as a lookup to generate the original labels
        labels=self.origclasslabels[cats]

        if return_likelihoods:
            return cats, labels, P

        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nNaive Bayes Classifier\n"
        for i in range(self.num_classes):
            s += 'Class %d --------------------\n' % (i)
            s += 'Mean  : ' + str(self.means[i,:]) + "\n"
            s += 'Var   : ' + str(self.vars[i,:]) + "\n"
            s += 'Scales: ' + str(self.scales[i,:]) + "\n"

        s += "\n"
        return s
        
    def write(self, filename):
        '''Writes the Bayes classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the Bayes classifier from the file'''
        # extension
        return

    
class KNN(Classifier):

    def __init__(self, dataObj=None, headers=[], categories=None, K=None):
        '''Take in a Data object with N points, a set of F headers, and a
        matrix of categories, with one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'KNN Classifier')


        # store the headers used for classification
        self.headers=headers
        # number of classes and number of features
        self.num_classes=0
        self.num_feats=0
        # original class labels
        self.origclasslabels=[]
        # unique data for the KNN classifier: list of exemplars (matrices)
        self.exemplars=[]


        if dataObj!=None:
            self.build(dataObj.get_data(headers),categories)
        # if given data,
            # call the build function

    def build( self, A, categories, K = None ):
        '''Builds the classifier give the data points in A and the categories'''
        A=np.matrix(A)
        # figure out how many categories there are and get the mapping (np.unique)
        uniquecats, mapping = np.unique(np.array(categories.T), return_inverse=True)
        self.num_classes=uniquecats.size
        self.origclasslabels=uniquecats

        # for each category i, build the set of exemplars
        for i in range(self.num_classes):
            # if K is None
            if K==None:
                # append to exemplars a matrix with all of the rows of A where the category/mapping is i
                self.exemplars.append(A[(mapping==i),:])
            # else
            else:
                # run K-means on the rows of A where the category/mapping is i
                codebook=an.kmeans_init(A[(mapping==i),:],K)
                # append the codebook to the exemplars
                self.exemplars.append(codebook)



        return

    def classify(self, A, K=3, return_distances=False):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_distances is
        True, it also returns the NxC distance matrix.

        The parameter K specifies how many neighbors to use in the
        distance computation. The default is three.'''

        A=np.matrix(A)
        # error check to see if A has the same number of columns as the class means
        if A.shape[1]!=self.exemplars[0].shape[1]:
            return

        # make a matrix that is N x C to store the distance to each class for each data point
        N=A.shape[0]
        C=self.num_classes
        D = np.matrix(np.zeros((N,C))) # a matrix of zeros that is N (rows of A) x C (number of classes)

        # for each class i
        for i in range(C):
            # make a temporary matrix that is N x M where M is the number of examplars (rows in exemplars[i])
            M=self.exemplars[i].shape[0]
            tempmtx=np.matrix(np.zeros((N,M)))
                # calculate the distance from each point in A to each point in exemplar matrix i (for loop)
            for j in range(M):
                tempmtx[:, j] = np.sum(np.square(A - self.exemplars[i][j, :]), axis=1)


            # sort the distances by row
            tempmtx.sort(axis=1)

            # sum the first K columns
            sumdist = np.sum(tempmtx[:, :K], axis=1)
            # this is the distance to the first class
            D[:,i]=sumdist


        # calculate the most likely class for each data point
        cats = np.argmin(D,axis=1) # take the argmin of D along axis 1

        # use the class ID as a lookup to generate the original labels
        labels = self.origclasslabels[cats]

        if return_distances:
            return (cats, labels, D)

        return (cats, labels)

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nKNN Classifier\n"
        for i in range(self.num_classes):
            s += 'Class %d --------------------\n' % (i)
            s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
            s += 'Mean of Exemplars  :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

        s += "\n"
        return s


    def write(self, filename):
        '''Writes the KNN classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the KNN classifier from the file'''
        # extension
        return



