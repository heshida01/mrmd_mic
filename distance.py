# *_*coding:utf-8 *_*
import numpy as np
from prepdata import  prepData


def Euclidean(feaData,feanum):

    dlist=[]
    for i in range(feanum):
        sum = 0
        for j in range(feanum):
            if (i==j):
                continue
            vec1 = np.array(feaData[i])
            vec2 = np.array(feaData[j])
            sum+=np.linalg.norm(vec1 - vec2)
        dlist.append(sum/feanum)
        # np_dlist=np.array(dlist)
        # print(dlist)
        # np_dlist.max()
    dlist=np.array(dlist)
    Edlist=dlist/dlist.max()
    return Edlist
def fun():
    return 1,2
if __name__ == '__main__':
    data = prepData("D:\\20D.libsvm").getInstance()
    feanum=len(data.T)
    feadata=data.T
    d=Euclidean(feadata,feanum)
    print(d)

