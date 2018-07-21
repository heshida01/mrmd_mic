# *_*coding:utf-8 *_*
from prepdata import prepData
from minepy import MINE
from classifier import skClassifier
import getopt
import sys
from multiprocessing import Pool, Manager
import time

def usage():
    print("only libsvm is supported")
    print("-h , --help :   Print this usage information")
    print("-i , --inputfile :   the inputfile libsvm format name ")
    print("-o , --outputfile :   the outputfile libsvm format name")
    print("-a , --optimize :   the optimized result file name")
    print("-n , --process num :   the number of process , default(1)")
    print("-t , --treesnum :  number of decision trees , default(100)")

def Multi_Process_MIC(feanum, feaData, label, n):  # 多进程计算MIC
    manager = Manager()
    q_index = manager.Queue()
    mic_dict = manager.dict()
    for i in range(feanum):
        q_index.put(i)

    pool = Pool()

    for i in range(n):
        pool.apply_async(MIC, (feanum, feaData, label, q_index, mic_dict))
    pool.close()
    pool.join()
    return mic_dict


def MIC(feanum, feaData, label, q, d):
    Y = label
    mine = MINE(alpha=0.6, c=15)
    while (not q.empty()):
        sys.stdout.write('. ')
        sys.stdout.flush()
        i = q.get()

        X = feaData[i]
        mine.compute_score(X, Y)
        # list1.append(mine.mic())
        d[i] = mine.mic()
        # print(mine.mic())


def write_optimizeResultFile(file, MIC_value, optnum):  # 排序好的最优mic序列
    i = 0
    with open(file, "w") as f:
        s = "{:<8}       {:<8}        {:<8}\n".format('No.', 'feanum', 'MIC_score')
        f.write(s)
        for key, value in MIC_value:
            i += 1
            s = "{:<8}       {:<8}        {:<8}\n".format(i, key, value)  # <左对齐   >右对齐    ^  居中   {:a>8}
            f.write(s)
            if i == optnum:
                break


def main():
    output = "out_random" + str(int(time.time()) % 1000) + ".libsvm"
    optimize_result_file = "opt_sorted_result" + str(int(time.time() * 1000) % 1000) + ".txt"
    np = 4
    decision_trees=100
    #input="20D.libsvm"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:a:n:t:", ["help", "inputfile", "outputfile", "optimizeResult", "process num","decision_trees"])
    except getopt.GetoptError:
        exit(-1)
    for o, v in opts:
        if o in ("h", "help"):
            usage()
            sys.exit()
        elif o in ("-i", "--inputfile"):
            input = v
        elif o in ("-o", "--outputfile"):
            output = v
        elif o in ("-a", "--optimizeResult"):
            optimize_result_file = v
        elif o in ("-n", "--process num"):
            np = int(v)
        elif o in ("-t", "--decision_tress"):
            decision_trees = int(v)

    data = prepData(input)  # 加载数据
    insData = data.getInstance()

    feaData = insData.T
    Y = data.getLabel()
    feanum = len(feaData)

    print("start calculating MIC")
    # list1=MIC(feanum,feaData,Y)         #计算MIC
    list1 = Multi_Process_MIC(feanum, feaData, Y, np)

    MIC_value = sorted(list1.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    print''
    print("MIC= ")
    for key, value in MIC_value:
        print("fea{0} ={1}".format(key, value))

    optnum,rate = skClassifier(insData,Y,decision_trees).getOptlist(MIC_value)

    print("The best feature number =%d" % optnum)
    rate=rate*100
    print("The best rate =%0.2f%%"%rate)
    print('---------------------------------')
    print("start write result...")
    # write_result1(data,MIC_value,optnum)

    l = []
    for i in MIC_value:
        l.append(i[0])
        if len(l) == optnum:
            break
    # print(l)

    data.wirte_result(l, output)
    write_optimizeResultFile(optimize_result_file, MIC_value, optnum)

    print("the output file name is : {0}".format(output))
    print("the name of optimized sorted feature file  is : {0}".format(optimize_result_file))
    print("done!!")


if __name__ == "__main__":
    main()
