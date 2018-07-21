# *_*coding:utf-8 *_*
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from multiprocessing import Pool,Manager
import sys
class skClassifier(object):
    def __init__(self,Xdataset,ylabel,n):
        self.data=Xdataset
        self.target=ylabel
        self.decision_trees=n
    def RandomForest(self):
        clf = RandomForestClassifier(random_state=1,n_estimators=self.decision_trees)
        clf.fit(self.data, self.target)
        scores=cross_val_score(clf,self.data,self.target,cv=10)

        return scores.mean()
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
        strlist = []
        i=1
        for pct in list1:
            strrate = 'the features num ' + str(i) + ' rate: ' + str(pct)
            print strrate
            strlist.append(strrate)
            i += 1


        imax=list1.index(max(list1))+1
        irate=list1[imax-1]

        return imax,irate

    def multi_process_opt(self,q,q_result,MICvalue):

     #   print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        mic_temp_list=[]
        while(not q.empty()):

            num=q.get()
            for i in range(num+1):
                mic_temp_list.append(MICvalue[i][0])

            kmean=skClassifier(self.data[:,mic_temp_list], self.target,self.decision_trees).RandomForest()

            sys.stdout.write('. ')
            sys.stdout.flush()
            q_result.put(kmean)

def proxy(cls_instance, q,q_result,MICvalue):

    return cls_instance.multi_process_opt(q,q_result,MICvalue)
if __name__ == '__main__':

    skClassifier().RandomForest()






