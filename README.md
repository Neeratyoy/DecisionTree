DecisionTree
============

The function cv(data,label,folds,shuffle) is to be called for execution.

It takes 4 arguments.

1) data : the list of lists containing the training data, including the label column
2) label : the index of the column in 'data' which is to be taken as the label column (index starts from 0)
3) folds : specifies the k in k-fold cross validation
4) shuffle : if 1, the row vectors in 'data' will be shuffled

The function prints the testing error on each fold and finally the average error on k-fold cross validation.

Note:
1) The data MUST be only real-valued
2) The labels can be quantitative and qualitative, i.e., numeric, real, or string
3) The label column vector must be included in 'data'
4) There should be no mmissing values


Example:
=========
For the iris data set,
data = [[5.1,3.5,1.4,0.2,'I. setosa'],[4.9,3.0,1.4,0.2,'I. setosa'],...,[5.9,3.0,5.1,1.8,'I. virginica']]
since the strings are labels and is in the 5th index of each row vector, 
label = 4

so to do a 10-fold cross validation on 'data', the function call has to be so:

cv(data,4,10,1)

