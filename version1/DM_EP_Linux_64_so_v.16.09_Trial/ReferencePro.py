import os
import numpy as np
import cv2
import math
import warnings
import pdb
from matplotlib import pyplot as plt
warnings.filterwarnings("ignore")

Img_Num = 40
for img_index in range(Img_Num):
    img_index += 1
    input_img_path = '/home/chezhaohui/2DTG/DM_EP_Linux_64_so_v.16.09_Trial/images/pass/test' + str(img_index) + '.bmp'
    save_img_path = '/home/chezhaohui/2DTG/DM_EP_Linux_64_so_v.16.09_Trial/images/Reference/test' + str(img_index) + '.bmp'
    command1 = './mydemo_dyn_load.out' + ' ' + input_img_path
    print(command1)
    pipe = os.popen(command1)
    ground_truth = pipe.read()
    print("The ground-truths are:")
    print(ground_truth)
    pipe.close

    command2 = './InputParaC.out' + ' ' + input_img_path
    pipe =  os.popen(command2)
    print("The input parameters from C++ files are:")
    ParaC = pipe.read()
    print(ParaC)
    pipe.close

    #Obtain Parameters from C++ files
    SuccOrFail = ParaC[7:11]
    SuccOrFail = int(SuccOrFail)
    #print("SuccOrFail is (0 means decode success) :", SuccOrFail)

    if(SuccOrFail==0):
        print("The Reference Decoding Algorithm Success!!!")

        print("SuccOrFail is (0 means decode success) :", SuccOrFail)

        DimRow = ParaC[27:29]
        DimRow = int(DimRow)
        print("Dimension of Row is :", DimRow)

        DimCol = ParaC[34:36]
        DimCol = int(DimCol)
        print("Dimension of Col is :", DimCol)

        Up_Left_row = ParaC[48:52]
        #print("BL:",Up_Left_row)
        Up_Left_row = int(Up_Left_row)
        Up_Left_col = ParaC[53:57]
        #print("BL:",Up_Left_col)
        Up_Left_col = int(Up_Left_col)
        print("The Row and Col Locations of the upper-left corner are :", Up_Left_row, Up_Left_col)

        Bottom_Left_row = ParaC[63:67]
        #print("BL:",Bottom_Left_row)
        Bottom_Left_row = int(Bottom_Left_row)
        Bottom_Left_col = ParaC[68:72]
        #print("BL:",Bottom_Left_col)
        Bottom_Left_col = int(Bottom_Left_col)
        print("The Row and Col Locations of the bottom-left corner are :", Bottom_Left_row, Bottom_Left_col)

        Bottom_Right_row = ParaC[78:82]
        #print("BL:",Bottom_Right_row)
        Bottom_Right_row = int(Bottom_Right_row)
        Bottom_Right_col = ParaC[83:87]
        #print("BL:",Bottom_Right_col)
        Bottom_Right_col = int(Bottom_Right_col)
        print("The Row and Col Locations of the bottom-left corner are :", Bottom_Right_row, Bottom_Right_col)

        Up_Right_row = ParaC[93:97]
        #print("BL:",Up_Right_row)
        Up_Right_row = int(Up_Right_row)
        Up_Right_col = ParaC[98:102]
        #print("BL:",Up_Right_col)
        Up_Right_col = int(Up_Right_col)
        print("The Row and Col Locations of the bottom-left corner are :", Up_Right_row, Up_Right_col)
    else:
        print("The Reference Decoding Algorithm Fails!!!")

        print("SuccOrFail is (1 means NON,2 means NODATAMATRIX,3 means BYCRIT,5 means REEDSOLOMON,99 means NOMEMORY,100 means UNKNOWN,200 means DISCNNECTED", SuccOrFail)

        Up_Left_row = ParaC[23:27]
        #print("BL:",Up_Left_row)
        Up_Left_row = int(Up_Left_row)
        Up_Left_col = ParaC[28:32]
        #print("BL:",Up_Left_col)
        Up_Left_col = int(Up_Left_col)
        print("The Row and Col Locations of the upper-left corner are :", Up_Left_row, Up_Left_col)

        Bottom_Left_row = ParaC[38:42]
        #print("BL:",Bottom_Left_row)
        Bottom_Left_row = int(Bottom_Left_row)
        Bottom_Left_col = ParaC[43:47]
        #print("BL:",Bottom_Left_col)
        Bottom_Left_col = int(Bottom_Left_col)
        print("The Row and Col Locations of the bottom-left corner are :", Bottom_Left_row, Bottom_Left_col)

        Bottom_Right_row = ParaC[53:57]
        #print("BL:",Bottom_Right_row)
        Bottom_Right_row = int(Bottom_Right_row)
        Bottom_Right_col = ParaC[58:62]
        #print("BL:",Bottom_Right_col)
        Bottom_Right_col = int(Bottom_Right_col)
        print("The Row and Col Locations of the bottom-right corner are :", Bottom_Right_row, Bottom_Right_col)

        Up_Right_row = ParaC[68:72]
        #print("BL:",Up_Right_row)
        Up_Right_row = int(Up_Right_row)
        Up_Right_col = ParaC[73:77]
        #print("BL:",Up_Right_col)
        Up_Right_col = int(Up_Right_col)
        print("The Row and Col Locations of the up-right corner are :", Up_Right_row, Up_Right_col)

    if(SuccOrFail==0):    
        img_ori_py = cv2.imread(input_img_path)
        

        img_rows,img_cols,img_ch = img_ori_py.shape
        DataRegion_Height = (np.float32(Up_Left_row)-np.float32(Bottom_Left_row))**2 + (np.float32(Up_Left_col)-np.float32(Bottom_Left_col))**2
        DataRegion_Height = math.sqrt(DataRegion_Height)
        #print("DataRegion_Height is:",DataRegion_Height)
        DataRegion_Width = (np.float32(Up_Left_row)-np.float32(Up_Right_row))**2 + (np.float32(Up_Left_col)-np.float32(Up_Right_col))**2
        DataRegion_Width = math.sqrt(DataRegion_Width)
        #print("DataRegion_Height is:",DataRegion_Width)
        
        Up_Left_After_row = 100
        Up_Left_After_col = 100
        #pts1 = np.float32([[Up_Left_row,Up_Left_col],[Bottom_Left_row,Bottom_Left_col],[Up_Right_row,Up_Right_col],[Bottom_Right_row,Bottom_Right_col]])
        #pts2 = np.float32([[Up_Left_After_row,Up_Left_After_col],[Up_Left_After_row + DataRegion_Height, Up_Left_After_col],[Up_Left_After_row,Up_Left_After_col + DataRegion_Width], [Up_Left_After_row + DataRegion_Height, Up_Left_After_col + DataRegion_Width]])
        
        #Pay Attention!!! The perspective transformation of the opencv is set as follows: the pts1 and pts2 represent 4 points, and the Col(x value) first, then Row(y value)
        pts1 = np.float32([[Up_Left_col,Up_Left_row],[Bottom_Left_col,Bottom_Left_row],[Up_Right_col,Up_Right_row],[Bottom_Right_col,Bottom_Right_row]])
        pts2 = np.float32([[Up_Left_After_col,Up_Left_After_row],[Up_Left_After_col, Up_Left_After_row + DataRegion_Height],[Up_Left_After_col + DataRegion_Width, Up_Left_After_row], [Up_Left_After_col + DataRegion_Width, Up_Left_After_row + DataRegion_Height]])
        #for eachitem in pts1:
        #   print eachitem
        #for eachitem in pts2:
        #   print eachitem
        
        M = cv2.getPerspectiveTransform(pts1,pts2)
        
        img_scale_row = int(2*Up_Left_After_row + DataRegion_Height)
        img_scale_col = int(2*Up_Left_After_col + DataRegion_Width)
        img_PT = cv2.warpPerspective(img_ori_py,M,(img_scale_row,img_scale_col))#Perspective Transformation Version

        Data_Region_1 = img_PT[int(Up_Left_After_row - 1):int(Up_Left_After_row + DataRegion_Height + 1),int(Up_Left_After_col - 1):int(Up_Left_After_col + DataRegion_Width + 1)] # no Quite Zone
        DR1_rows,DR1_cols,DR1_ch = Data_Region_1.shape
        #Quite_Zone_Scale = int(np.float32(DR1_rows)/np.float32(DimRow))
        Module_Size_row = int(DR1_rows/DimRow)
        Module_Size_col = int(DR1_cols/DimCol)
        Data_Region_2 = img_PT[int(Up_Left_After_row - Module_Size_row):int(Up_Left_After_row + DataRegion_Height + Module_Size_row),int(Up_Left_After_col - Module_Size_col):int(Up_Left_After_col + DataRegion_Width + Module_Size_col)] # including Quite Zone
        DR1_rows,DR1_cols,DR1_ch = Data_Region_1.shape
        DR2_rows,DR2_cols,DR2_ch = Data_Region_2.shape
        '''
        Feature1, decoding grade
        '''
        my_decode_grade = 4 #feature1, decoding grade
        #print("The Decode Grade is :", my_decode_grade)
        '''
        Feature2, Symbol Contrast grade
        '''
        DR_gray = cv2.cvtColor(Data_Region_2,cv2.COLOR_BGR2GRAY)
        #DR2_rows,DR2_cols = DR_gray.shape #PAY ATTENTION: gray image can not be written as rows,cols,ch=gray.shape! just only rows and cols
        R_max = 0
        R_min = 255
        for i in range(DR2_rows):
          for j in range(DR2_cols):
            R_max = max(R_max,DR_gray[i,j])
            R_min = min(R_min,DR_gray[i,j])
        my_symbol_contrast = np.float32(R_max - R_min) / np.float32(255)
        #print R_max,R_min
        if((my_symbol_contrast >= 0.70) and (my_symbol_contrast <= 1.0)):
          my_symbol_contrast_grade = 4
        elif((my_symbol_contrast >= 0.55) and (my_symbol_contrast < 0.70)):
          my_symbol_contrast_grade = 3
        elif((my_symbol_contrast >= 0.40) and (my_symbol_contrast < 0.55)):
          my_symbol_contrast_grade = 2
        elif((my_symbol_contrast >= 0.20) and (my_symbol_contrast < 0.40)):
          my_symbol_contrast_grade = 1
        elif((my_symbol_contrast >= 0.00) and (my_symbol_contrast < 0.20)):
          my_symbol_contrast_grade = 0
        #print("The Symbol Contrast and SC_Grade are :", my_symbol_contrast,my_symbol_contrast_grade)#feature2 Symbol Contrast grade

        '''
        Feature3 Modulation grade
        '''
        GT = (np.float32(R_max) + np.float32(R_min))/2 
        #print R_max,R_min,GT # if not change the R_max/R_min into float format, the int will overflow!!!
        SC = my_symbol_contrast* np.float32(255)
        #Module_Size_row = (DR1_rows/DimRow)
        #Module_Size_col = (DR1_cols/DimCol) #because the module size of X and Y directions may be different
        #print Module_Size_row,Module_Size_col

        R = np.float32(1000)
        MOD_grade = 0
        Contrast_Uniformity = 1000
        Table_MOD_2=[0,0,0,0,0] # Page18 Table7 of the ISO15415 file, Chinese Version
        Table_MOD_3=[0,0,0,0,0]
        Table_MOD_4=[0,0,0,0,0]
        Table_MOD_5=[0,0,0,0,0]
        Table_MOD_6=[0,0,0,0,0]
        Table_MOD_7=[0,0,0,0,0]
        Table_MOD_8=[0,0,0,0,0]
        Data_Region_2_gray = cv2.cvtColor(Data_Region_2,cv2.COLOR_BGR2GRAY)
        Thresh1 = int(GT)
        ret,Data_Region_2_bw = cv2.threshold(Data_Region_2_gray, Thresh1, 255, cv2.THRESH_BINARY)
        SameColor1 = Data_Region_2_bw[0:Module_Size_row, Module_Size_col:DR2_cols-Module_Size_col]
        SameColor2 = Data_Region_2_bw[Module_Size_row:DR2_rows-Module_Size_row, DR2_cols-Module_Size_col:DR2_cols]
        average_SameColor1 = map(sum,SameColor1)
        average_SameColor1 = sum(average_SameColor1)
        height_SC1, width_SC1 = SameColor1.shape
        average_SameColor1 = np.float32(average_SameColor1)/np.float32(height_SC1*width_SC1)
        Polarity = 1
        if(average_SameColor1>GT):
          Polarity = 1 #code region is dark, while background region is light
        else:
          Polarity = 0
        #print("The Polarity of the Code(1 means Code Region is Dark, while 0 means Code Region is Light)", Polarity)


        '''
        M = cv2.getPerspectiveTransform(pts1,pts2)
        
        img_scale_row = int(2*Up_Left_After_row + DataRegion_Height)
        img_scale_col = int(2*Up_Left_After_col + DataRegion_Width)
        img_PT = cv2.warpPerspective(img_ori_py,M,(img_scale_row,img_scale_col))#Perspective Transformation Version

        Data_Region_1 = img_PT[int(Up_Left_After_row - 1):int(Up_Left_After_row + DataRegion_Height + 1),int(Up_Left_After_col - 1):int(Up_Left_After_col + DataRegion_Width + 1)] # no Quite Zone
        DR1_rows,DR1_cols,DR1_ch = Data_Region_1.shape
        #Quite_Zone_Scale = int(np.float32(DR1_rows)/np.float32(DimRow))
        Module_Size_row = int(DR1_rows/DimRow)
        Module_Size_col = int(DR1_cols/DimCol)
        Final_Height = int(Up_Left_After_row + DataRegion_Height + Module_Size_row) - int(Up_Left_After_row - Module_Size_row)
        Final_Width = int(Up_Left_After_col + DataRegion_Width + Module_Size_col) - int(Up_Left_After_col - Module_Size_col)
        Final = max(Final_Height,Final_Width)
        #Data_Region_2 = img_PT[int(Up_Left_After_row - Module_Size_row):int(Up_Left_After_row + DataRegion_Height + Module_Size_row),int(Up_Left_After_col - Module_Size_col):int(Up_Left_After_col + DataRegion_Width + Module_Size_col)] # including Quite Zone
        Data_Region_2 = img_PT[int(Up_Left_After_row - Module_Size_row):int(Up_Left_After_row - Module_Size_row)+Final, int(Up_Left_After_col - Module_Size_col):int(Up_Left_After_col - Module_Size_col)+Final] # including Quite Zone
        if(Polarity==0):
            Res = cv2.copyMakeBorder(Data_Region_2, 3*Module_Size_col, 3*Module_Size_col, 3*Module_Size_col, 3*Module_Size_col, cv2.BORDER_CONSTANT, value=[0,0,0])
        elif(Polarity==1):
            Res = cv2.copyMakeBorder(Data_Region_2, 3*Module_Size_col, 3*Module_Size_col, 3*Module_Size_col, 3*Module_Size_col, cv2.BORDER_CONSTANT, value=[255,255,255])
        
        Res = cv2.resize(Res,(256,256),interpolation = cv2.INTER_CUBIC)
        #Res = np.zeros([256,256,3],np.uint8)
        #Res = cv2.resize(Data_Region_2,(256,256),interpolation = cv2.INTER_CUBIC)
        #Res = Data_Region_2
        cv2.imwrite(save_img_path,Res)
        '''





        M = cv2.getPerspectiveTransform(pts1,pts2)
        
        img_scale_row = int(2*Up_Left_After_row + DataRegion_Height)
        img_scale_col = int(2*Up_Left_After_col + DataRegion_Width)
        img_PT = cv2.warpPerspective(img_ori_py,M,(img_scale_row,img_scale_col))#Perspective Transformation Version

        Data_Region_1 = img_PT[int(Up_Left_After_row - 1):int(Up_Left_After_row + DataRegion_Height + 1),int(Up_Left_After_col - 1):int(Up_Left_After_col + DataRegion_Width + 1)] # no Quite Zone
        DR1_rows,DR1_cols,DR1_ch = Data_Region_1.shape
        #Quite_Zone_Scale = int(np.float32(DR1_rows)/np.float32(DimRow))
        Module_Size_row = int(DR1_rows/DimRow)
        Module_Size_col = int(DR1_cols/DimCol)
        Final_Height = int(Up_Left_After_row + DataRegion_Height + 2*Module_Size_row) - int(Up_Left_After_row - 2*Module_Size_row)
        Final_Width = int(Up_Left_After_col + DataRegion_Width + 2*Module_Size_col) - int(Up_Left_After_col - 2*Module_Size_col)
        Final = max(Final_Height,Final_Width)
        #Data_Region_2 = img_PT[int(Up_Left_After_row - Module_Size_row):int(Up_Left_After_row + DataRegion_Height + Module_Size_row),int(Up_Left_After_col - Module_Size_col):int(Up_Left_After_col + DataRegion_Width + Module_Size_col)] # including Quite Zone
        Data_Region_2 = img_PT[int(Up_Left_After_row - 2*Module_Size_row):int(Up_Left_After_row - 2*Module_Size_row)+Final, int(Up_Left_After_col - 2*Module_Size_col):int(Up_Left_After_col - 2*Module_Size_col)+Final] # including Quite Zone
        #if(Polarity==0):
         #   Res = cv2.copyMakeBorder(Data_Region_2, 3*Module_Size_col, 3*Module_Size_col, 3*Module_Size_col, 3*Module_Size_col, cv2.BORDER_CONSTANT, value=[0,0,0])
        #elif(Polarity==1):
         #   Res = cv2.copyMakeBorder(Data_Region_2, 3*Module_Size_col, 3*Module_Size_col, 3*Module_Size_col, 3*Module_Size_col, cv2.BORDER_CONSTANT, value=[255,255,255])
        Res = Data_Region_2
        Res = cv2.resize(Res,(256,256),interpolation = cv2.INTER_CUBIC)
        #Res = np.zeros([256,256,3],np.uint8)
        #Res = cv2.resize(Data_Region_2,(256,256),interpolation = cv2.INTER_CUBIC)
        #Res = Data_Region_2
        cv2.imwrite(save_img_path,Res)