import os
import numpy as np
import cv2
import math
import warnings
import pdb
from matplotlib import pyplot as plt
warnings.filterwarnings("ignore")

'''
input_img_path = '/home/chezhaohui/2DTG/QAdatabase/Reference/19.bmp'
command1 = './mydemo_dyn_load.out' + ' ' + input_img_path
print(command1)
pipe = os.popen(command1)
ground_truth = pipe.read()
print("The ground-truths are:")
print(ground_truth)
pipe.close

command3 = './My_Score.out' + ' ' + input_img_path
pipe =  os.popen(command3)
print("The Final Score is:")
FN_Score = pipe.read()
print(FN_Score)
pipe.close

QA_Score = FN_Score[14:20]
print("QA_Score:", QA_Score)
'''



'''
Total_num = 39
path = '/home/chezhaohui/2DTG/DM_EP_Linux_64_so_v.16.09_Trial/images/'
file = open(path + "score.txt", "w")
for i in range(Total_num):
    #path = '/home/chezhaohui/2DTG/DM_EP_Linux_64_so_v.16.09_Trial/images/'
    input_img_path = path + '/test' + str(i) + '.bmp'
    command3 = './My_Score.out' + ' ' + input_img_path
    pipe =  os.popen(command3)    
    FN_Score = pipe.read()    
    pipe.close
    QA_Score = FN_Score[14:20]
    print("QA_Score:", QA_Score)

    context = str(i) + '.bmp' + ' ' + QA_Score + '\n'
    #context = QA_Score + '\n'
    file.write(context)
#print file.read()
file.close()
'''


Total_num = 195
#path = '/home/chezhaohui/2DTG/QAdatabase/Reference/'
path = '/home/chezhaohui/2DTG/QAdatabase/Resolution/'
file = open(path + "score.txt", "w")
for i in range(Total_num):
    i += 1
    #path = '/home/chezhaohui/2DTG/DM_EP_Linux_64_so_v.16.09_Trial/images/'
    input_img_path = path + str(i) + '.bmp'
    command3 = './My_Score.out' + ' ' + input_img_path
    pipe =  os.popen(command3)    
    FN_Score = pipe.read()    
    pipe.close
    QA_Score = FN_Score[14:20]
    print("QA_Score:", QA_Score)

    context = str(i) + '.bmp' + ' ' + QA_Score + '\n'
    #context = QA_Score + '\n'
    file.write(context)
#print file.read()
file.close()


'''
#read line by line, and split each line as image name and image score respectively
path = '/home/chezhaohui/2DTG/DM_EP_Linux_64_so_v.16.09_Trial/images/'
filename = path + 'score.txt'
img_name = []
img_score = []
fa = open(filename, "r")
for line in fa.readlines():
    print line
    str1 = line.split(" ")[-1]
    print str1
    img_score.append(str1)
fa.close()

filename2 = path + "score2.txt"
fb = open(filename2,'a')
#for i in range(len(img_score)):
 #   fb.write(img_score[i])
for i in img_score:
    fb.write(i)
fb.close()
'''


