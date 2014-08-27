import math
import random
from operator import itemgetter
import statistics


class Tree:
    label = None
    def __init__(self):
        self.attribute = -1
        self.threshold = None
        self.purity = 1
        self.left = None
        self.right = None
        self.predict = None

    def purity_measure(self,A):
        temp = {}
        X = self.label
        for l in A:
            if l[X] in temp:
                temp[l[X]] = temp[l[X]] + 1
            else:
                temp[l[X]] = 1
        self.purity = entropy(temp)        
        return self.purity

    def split_node(self,A):
#        print("*** "+str(len(A))+" ***")
        x = self.attribute
        y = self.label
        E = self.purity
        A = sorted(A,key=itemgetter(x))
        splits = []
        for i in range(len(A)-1):
            if A[i][y] == A[i+1][y]:
                continue
            z = (A[i][x] + A[i+1][x])/2
            splits.append([E-self.split_value(A,y,i),z,i])
        splits = sorted(splits,reverse=True)
#        print("*** "+str(splits)+" ***")
        self.threshold = splits[0][1]
        row = splits[0][2]
        left = []
        right = []
        for i in range(row+1):
            left.append(A[i])
        for i in range(row+1,len(A)):
            right.append(A[i])
        l = []
        l.append(left)
        l.append(right)
        return l

    def split_value(self,A,label,row):
        left = {}
        right = {}
        for i in range(len(A)):
            if i<=row:
                if A[i][label] in left:
                    left[A[i][label]] = left[A[i][label]] + 1
                else:
                    left[A[i][label]] = 1
            else:        
                if A[i][label] in right:
                    right[A[i][label]] = right[A[i][label]] + 1
                else:
                    right[A[i][label]] = 1
        return entropy(left)+entropy(right)

    def partition_data(self,A,X,threshold):
        leftA = []
        rightA = []
        for i in range(len(A)):
            if A[i][X]<threshold:
                leftA.append(A[i])
            else:
                rightA.append(A[i])
        l = []
        l.append(leftA)
        l.append(rightA)
        return l    
    
#end of class Tree


'''======================================================================='''

def mutual_information(A,X,Y):
    variableX = {}
    variableY = {}
    variableJoint = {}
    for l in A:
        if l[X] in variableX:
            variableX[l[X]] = variableX[l[X]] + 1
        else:
            variableX[l[X]] = 1

        if l[Y] in variableY:
            variableY[l[Y]] = variableY[l[Y]] + 1
        else:
            variableY[l[Y]] = 1

        joint = (l[X],l[Y])
        if joint in variableJoint:
            variableJoint[joint] = variableJoint[joint] + 1
        else:
            variableJoint[joint] = 1

    hX = entropy(variableX)
    hY = entropy(variableY)
    hJoint = entropy(variableJoint)
        
    return hX+hY-hJoint
#end of mutual_information()



def entropy(x):
    sum = 0
    for key in x:
        sum = sum + x[key]
    ent = 0    
    for key in x:
        ent = ent + (x[key]/sum)*math.log((x[key]/sum),2)
    return -ent
#end of entropy()



def infoOrdering(A,label):
    info = []
    for i in range(0,len(A[0])):
        if i==label:
            continue
        info.append([mutual_information(A,i,label),i])
    info = sorted(info,reverse=True)
    l = []
    for i in range(len(info)):
        l.append(info[i][1])
    return l
#end of infoA()



def maxLabel(dict):
    l = []
    temp = max(dict.values())
    for key in dict:
        if dict[key] == temp:
            l.append(key)
    return l[random.randint(0,len(l)-1)]
#end of maxLabel()



def print2D(matrix):
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[i])):
            print(matrix[i][j],end=' ')
        print()
#end of print2D()


        
'''======================================================================='''


def growTree(A,label):  
    if len(A) is 0:
        return None
    attributeList = infoOrdering(A,label)
    X = int(attributeList[0])
    node = Tree()
    node.label = int(label)
    node.attribute = X
    node.purity = node.purity_measure(A)
#    print("Purity : "+str(node.purity))
    temp = {1:1}
    if node.purity == 0 or len(A) == 1:
        node.predict = A[0][label]                      # leaf node prediction 
        return node
    l = node.split_node(A)
#    l = node.partition_data(A,X,node.threshold)
    if len(l[0])==0 or len(l[1])==0:
#        print(len(l[0]))
        print(X,node.threshold)
#        print(len(l[1]))
        return l
    node.left = growTree(l[0],label)                    # left branch
    node.right = growTree(l[1],label)                   # right branch
    return node
#end of growTree()



def testTree(root,vector):
    if root.left is None and root.right is None:
        return root.predict
    if vector[root.attribute]<=root.threshold:
        return testTree(root.left,vector)
    else:
        return testTree(root.right,vector)
#end of testTree()

    

def testing(root,testData):
    result = []
    count = 0
    x = root.label
    for l in testData:
        temp = testTree(root,l)
        if type('Hello') == type(l[x]):
            if l[x] != temp:
#                print(l[x],temp,(l[x] is temp))
                count = count + 1
        else:
            if int(l[x]) != int(temp):
                count = count + 1
        result.append([l[x],temp])
    return count*100/len(result)
#end of testing()'




def cv(data,label,folds,shuffle):
    if shuffle == 1:
        random.shuffle(data)
    size = len(data)/folds
    start = 0
    end = 0
    sum = 0
    for i in range(folds):
        start = int(i*size)
        end = int((i+1)*size)
        train = data[start:end]
        test = data[:start]+data[end:]
        root = growTree(train,label)
        temp = testing(root,test)
        print("Fold "+str(i+1)+" : "+str(temp)+"%")
        sum = sum + temp
    print("Average : "+str(sum/folds))
    return
#end of cv()   
