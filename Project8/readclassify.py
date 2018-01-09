import classifiers
import sys
import data
'''Reads in a training set and a test set and builds a KNN or Naive-Bayes
    classifiers depending on user input in the command line. Classifies the test data and prints out the
    results.
    '''
def main(argv):
    # usage
    if len(argv) < 3:
        print 'Usage: python %s <classtype> <training data file> <test data file> <optional training category file> <optional test category file>' % (argv[0])
        exit(-1)

    # read the training and test sets
    dtrain = data.Data(argv[2])
    dtest = data.Data(argv[3])


    # get the categories and the training data A and the test data B
    if len(argv) > 5:
        traincatdata = data.Data(argv[4])
        testcatdata = data.Data(argv[5])
        traincats = traincatdata.get_data( [traincatdata.get_headers()[0]] )
        testcats = testcatdata.get_data( [testcatdata.get_headers()[0]] )
        A = dtrain.get_data( dtrain.get_headers() )
        B = dtest.get_data( dtest.get_headers() )
    else:
        # assume the categories are the last column
        traincats = dtrain.get_data( [dtrain.get_headers()[-1]] )
        testcats = dtest.get_data( [dtest.get_headers()[-1]] )
        A = dtrain.get_data( dtrain.get_headers()[:-1] )
        B = dtest.get_data( dtest.get_headers()[:-1] )

    if(argv[1]=="KNN"):
        print "You chose KNN"
        #create knn classifier
        knnc=classifiers.KNN()
        #build knn classifier
        knnc.build(A,traincats)
        trainclasscats, trainclasslabels=knnc.classify(A)
        testclasscats, testclasslabels = knnc.classify(B)
        #use KNN classifier on test data
        traincmtx = knnc.confusion_matrix((traincats),(trainclasscats))
        traincmtxstr = knnc.confusion_matrix_str(traincmtx)
        print "Training Confusion Matrix"
        print traincmtxstr
        testcmtx = knnc.confusion_matrix(testcats, testclasscats)
        testcmtxstr = knnc.confusion_matrix_str(testcmtx)
        print "Testing Confusion Matrix"
        print testcmtxstr

    elif(argv[1]=="Naive-Bayes"):
        print "You chose Naive-Bayes"
        # create Naive-Bayes classifier
        nbc = classifiers.NaiveBayes()
        # build Naive-Bayes classifier
        nbc.build(A, traincats)
        # use Naive-Bayes classifier on test data

        trainclasscats, trainclasslabels = nbc.classify(A)
        testclasscats, testclasslabels = nbc.classify(B)
        # use KNN classifier on test data
        traincmtx = nbc.confusion_matrix(traincats, trainclasscats)
        traincmtxstr = nbc.confusion_matrix_str(traincmtx)
        print "Training Data Confusion Matrix"
        print traincmtxstr
        testcmtx = nbc.confusion_matrix(testcats, testclasscats)
        testcmtxstr = nbc.confusion_matrix_str(testcmtx)
        print "Test Data Confusion Matrix"
        print testcmtxstr


    dtest.addColumn("Classifiers",testclasscats)
    dtest.write("writtendatafile.csv")


if __name__ == "__main__":
    main(sys.argv)