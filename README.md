# mrmd_mic
MRMD_MIC 特征选择主要依赖最大信息系数MIC（Maximal information coefficient），使用随机森林进行分类。
Enviroment:
python2(需要工具包：numpy scipy sklearn minepy)，99服务器下已弄好，可以直接使用

目前仅支持libsvm格式

Usage Example：
   python MRMD_MIC.py -i ~/188D.libsvm  -o outfile.libsvm -a mic_valuefile   -t 100 -n 4 -c -t 100 acc_f1.csv
除了参数-i其中可以省去，提供缺省值.具体如下
参数：

   -i  文件的路径（仅支持libsvm）  
 可选参数  
   -o  特征选择后的文件路径（如果没有指定，自动生成一个）  
   -a  输出MIC分数和排序信息的路径（如果没有指定，自动生成一个）  
   -n  进程数（默认1，若想要提升速度可以与电脑核数一致，但是会占用不少的系统资源）  
   -t  决策数量  
   -c  输出的csv名字（包含accuracy和f1_score）  
   -h  程序说明  

如果有任何问题请联系我（heshida01@gmail.com）
  
