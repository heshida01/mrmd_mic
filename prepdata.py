# *_*coding:utf-8 *_*
import numpy as np
class prepData(object):

    def __init__(self,filepath):
        self.__filepath=filepath
        self.__labelData = []
        self.__InsData = []

        self.loadData()

    def loadData(self):
        with open(self.__filepath,'r') as fsvm:
            row=0
            for strline in fsvm:
                if strline.isspace():
                    continue
                strline=strline.replace("\n","")
                str_sp = strline.split(' ')         #获取样本数据（每行）

                self.__labelData.append(str_sp[0])    #获取label

                temp_list=[]
                flag=True
                if(flag):
                    self.__fea_num=len(str_sp)-1
                    flag=False
                i=0
                for str in str_sp[1:]:           #获取样本数据

                    temp_list.append(float(str.split(':')[1]))

                self.__InsData.append(temp_list)

    def wirte_result(self,optlist,outputfile):     #保存结果
        datalist=[]
        with open(self.__filepath, 'r') as fsvm,  open(outputfile,"w") as f2:
            str1 = ''
            i=0
            for strline in fsvm:

                if strline.isspace():
                    continue
                datalist.append(strline.split())
                str1=datalist[i][0]
                j=0
                datalist_1_n=datalist[i][1:]
                #print(datalist_1_n)
                for l in optlist:
                    str1+=' '+str(j+1)+':'+datalist_1_n[l-1].split(':')[1]

                    j+=1
                i+=1
                #print(str1)

                f2.write(str1)
                f2.write('\n')
            return datalist
    def getLabel(self):
        return np.array(self.__labelData)

    '''
    
    '''
    def getInstance(self):
        return np.array(self.__InsData)



if __name__ == "__main__":

    data=prepData("D:\\20D.libsvm")
    a=data.getLabel()
    b=data.getInstance()
    print(len(a))
    print(b[0])
