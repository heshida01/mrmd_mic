# *_*coding:utf-8 *_*
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from multiprocessing import Pool,Manager
import sys
class skClassifier(object):
    def __init__(self,Xdataset,ylabel,n,c):
        self.data=Xdataset
        self.target=ylabel
        self.decision_trees=n
        self.csv=c

    def RandomForest(self):

        clf = RandomForestClassifier(random_state=1,n_estimators=self.decision_trees)
        clf.fit(self.data, self.target)
        scores=cross_val_score(clf,self.data,self.target,cv=10)
        f1_weighted = cross_val_score(clf, self.data, self.target, cv=10,scoring='f1_weighted')

        return scores.mean(),f1_weighted.mean()
    def getOptlist(self,MICvalue):

        manage=Manager()
        q=manage.Queue()
        q_result=manage.Queue()
        for i in range(len(MICvalue)):
            q.put(i)

        pool = Pool(4)
        print('-------------------------------------------------')
        print('start auto optimizing')
        for i in range(4):
            #pool.apply(proxy, (self, q, q_result, MICvalue,))
            pool.apply_async(proxy,(self,q,q_result,MICvalue,))
        pool.close()
        pool.join()
        list1=[]
        while(not q_result.empty()):
            list1.append(q_result.get(i))

        print ''

        list1=list(list1)
        listrate = []
        i=1

        with open(self.csv,"w") as f1:
            f1.write("features"+","+"accuracy"+","+"F1"+'\n')
            for pct in list1:
                strrate = 'the features num ' + str(i) + ' rate: ' + str(pct[0])
                strf1 = " ,f1_weighted: "+str(pct[1])
                print strrate+strf1
                f1.write("feature num"+str(i)+","+str(pct[0])+','+str(pct[1])+'\n')
                #strlist.append(strrate)
                listrate.append(pct[0])
                i += 1




        imax=listrate.index(max(listrate))+1
        irate=listrate[imax-1]

        return imax,irate

    def multi_process_opt(self,q,q_result,MICvalue):

        mic_temp_list=[]
        while(not q.empty()):

            num=q.get()
            for i in range(num+1):
                mic_temp_list.append(MICvalue[i][0])

            kmean,f1=skClassifier(self.data[:,mic_temp_list], self.target,self.decision_trees,self.csv).RandomForest()
            kmean_f1=(kmean,f1)
            sys.stdout.write('. ')
            sys.stdout.flush()
            q_result.put(kmean_f1)

def proxy(cls_instance, q,q_result,MICvalue): #多进程代理

    return cls_instance.multi_process_opt(q,q_result,MICvalue)
if __name__ == '__main__':

    skClassifier().RandomForest()






