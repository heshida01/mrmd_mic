#-*- coding: UTF-8 -*-
'''
from multiprocessing import Pool


def run(cls_instance, i):
    return cls_instance.func(i)


class Runner(object):
    def __init__(self):
        pool = Pool(processes=5)
        for i in range(5):
            pool.apply_async(run, (self, i))
        pool.close()
        pool.join()

    def func(self, i):
        print i
        return i


runner = Runner()
'''

'''
import multiprocessing

def proxy(cls_instance, args):
    return cls_instance.test(args)


class A(object):

    def __init__(self):
        pass

    def run(self):
        sheets = ['a', 'b', 'c', 'd', 'e']
        result = []

        pool = multiprocessing.Pool(processes=5)

        for index, sheet in enumerate(sheets):
            result.append(pool.apply_async(proxy, (self, sheet)))

        pool.close()
        pool.join()

        for data in result:
            print data.get()

    def test(self, args):
       return args


if __name__ == '__main__':
     A().run()
'''

import matplotlib.pyplot as plt
fig = plt.figure(2)


fig.show()