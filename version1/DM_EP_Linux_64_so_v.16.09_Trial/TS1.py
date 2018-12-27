import os
import numpy as np
import cv2
import math
import warnings
import pdb
from matplotlib import pyplot as plt
warnings.filterwarnings("ignore")

def Cal_Modulation(input_img, input_img_rows, input_img_cols, input_img_MDSZ_row, input_img_MDSZ_col, input_img_GT, input_img_SC, input_Polarity, input_Type):
   output_Table_2 = [0,0,0,0,0]
   img_height, img_width, img_ch = input_img.shape
   Contrast_Uniformity = 1000
   Limit_1 = 0.4
   Limit_2 = 0.6
   for i in range(input_img_rows):
     for j in range(input_img_cols):
       if(((i+1)*input_img_MDSZ_row-1)<=img_height and ((j+1)*input_img_MDSZ_col-1)<=img_width):
         Module_temp = input_img[(i*input_img_MDSZ_row):((i+1)*input_img_MDSZ_row-1), (j*input_img_MDSZ_col):((j+1)*input_img_MDSZ_col-1)]
       else:
         Module_temp = Data_Region_1[(i*input_img_MDSZ_row):(img_height-1), (j*input_img_MDSZ_col):(img_width-1)]

       Module_temp = cv2.cvtColor(Module_temp,cv2.COLOR_BGR2GRAY)
       II,JJ= Module_temp.shape
       R = np.float32(1000)
       MOD_grade = 0
       Module_avg = np.float32(0)
       for ii in range(int(II*Limit_1), int(II*Limit_2)+1, 1):
         for jj in range(int(JJ*Limit_1), int(JJ*Limit_2)+1, 1):
           Module_avg = Module_avg + np.float32(Module_temp[ii,jj])
           #if(abs(np.float32(Module_temp[ii,jj])-input_img_GT) < abs(R-input_img_GT)): #The original version, I select the average valut of the module to represent the R, not the value similar to GT, so as to increast FPD grade to approach the 2DTG
            #  R = np.float32(Module_temp[ii,jj])
       
       R_height =  int(II*Limit_2)+1 - int(II*Limit_1) 
       R_width = int(JJ*Limit_2)+1 - int(JJ*Limit_1) 
       R = np.float32(Module_avg / (R_height*R_width))
       
       
       MOD = 2*abs(R-input_img_GT)/input_img_SC
       if(MOD<Contrast_Uniformity):
          Contrast_Uniformity = MOD
       if((MOD >= 0.50)):
         MOD_grade = 4
       elif((MOD >= 0.40) and (MOD < 0.50)):
         MOD_grade = 3
       elif((MOD >= 0.30) and (MOD < 0.40)):
         MOD_grade = 2
       elif((MOD >= 0.20) and (MOD < 0.30)):
         MOD_grade = 1
       elif((MOD < 0.20)):
         MOD_grade = 0
       input_OddEven = (i+j)%2 #0 means: module numbers are:1 3 5 7 9, 1 means: 2 4 6 8 modules, this is designed for Timing Pattern 
       MOD_grade = UpDate_MOD(R, MOD_grade, input_Polarity, input_Type, input_img_GT, input_OddEven)

       if(MOD_grade==4):
        output_Table_2[0] += 1
       elif(MOD_grade==3):
        output_Table_2[1] += 1
       elif(MOD_grade==2):
        output_Table_2[2] += 1
       elif(MOD_grade==1):
        output_Table_2[3] += 1
       elif(MOD_grade==0):
        output_Table_2[4] += 1
   
   return output_Table_2, Contrast_Uniformity

def UpDate_MOD(input_MOD, input_MOD_grade, input_input_Polarity, input_input_Type, input_input_img_GT, input_input_OddEven):
  out_MOD_grade = input_MOD_grade
  #print input_MOD,input_input_img_GT
  if(input_input_Polarity==1):#Code region is Dark, Backround region is light
    if(input_input_Type==1):
      out_MOD_grade = input_MOD_grade
      return out_MOD_grade #Type0 means no update
    elif(input_input_Type==1 and input_MOD<input_input_img_GT): #QZ1 QZ2 SC1 SC2
      out_MOD_grade = 0
      return out_MOD_grade
    elif(input_input_Type==2 and input_MOD>input_input_img_GT): #L1 L2
      out_MOD_grade = 0
      return out_MOD_grade
    elif(input_input_Type==3): #TP1
      if(input_input_OddEven==0 and input_MOD>input_input_img_GT):
        out_MOD_grade = 0
        return out_MOD_grade
      elif(input_input_OddEven==1 and input_MOD<input_input_img_GT):
        out_MOD_grade = 0
        return out_MOD_grade
      else:
        return out_MOD_grade
    elif(input_input_Type==4): #TP2
      if(input_input_OddEven==0 and input_MOD<input_input_img_GT):
        out_MOD_grade = 0
        return out_MOD_grade
      elif(input_input_OddEven==1 and input_MOD>input_input_img_GT):
        out_MOD_grade = 0
        return out_MOD_grade
      else:
        return out_MOD_grade
    else:
      return out_MOD_grade
  elif(input_input_Polarity==0):
    if(input_input_Type==0):
      out_MOD_grade = input_MOD_grade
      return out_MOD_grade #Type0 means no update
    elif(input_input_Type==1 and input_MOD>input_input_img_GT): #QZ1 QZ2 SC1 SC2
      out_MOD_grade = 0
      return out_MOD_grade
    elif(input_input_Type==2 and input_MOD<input_input_img_GT): #L1 L2
      out_MOD_grade = 0
      return out_MOD_grade
    elif(input_input_Type==3): #TP1 TP2
      if(input_input_OddEven==0 and input_MOD<input_input_img_GT):
        out_MOD_grade = 0
        return out_MOD_grade
      elif(input_input_OddEven==1 and input_MOD>input_input_img_GT):
        out_MOD_grade = 0
        return out_MOD_grade
      else:
        return out_MOD_grade
    elif(input_input_Type==4): #TP2
      if(input_input_OddEven==0 and input_MOD>input_input_img_GT):
        out_MOD_grade = 0
        return out_MOD_grade
      elif(input_input_OddEven==1 and input_MOD<input_input_img_GT):
        out_MOD_grade = 0
        return out_MOD_grade
      else:
        return out_MOD_grade
    else:
      return out_MOD_grade
    

def Cal_Table6_From_Table5(input_Table5_item): #QuietZone Region Pullution Percentage
  output_Table6_item = 0
  if(input_Table5_item == 0):
    output_Table6_item = 4
  elif(input_Table5_item>0 and input_Table5_item<=0.09):
    output_Table6_item = 3
  elif(input_Table5_item>0.09 and input_Table5_item<=0.13):
    output_Table6_item = 2
  elif(input_Table5_item>0.13 and input_Table5_item<=0.17):
    output_Table6_item = 1
  elif(input_Table5_item>0.17):
    output_Table6_item = 0
  
  return output_Table6_item

def Cal_Table6_From_Table5_2(input_Table5_item): #SameColor Region Pullution Percentage
  output_Table6_item = 0
  if(input_Table5_item < 0.1):
    output_Table6_item = 4
  elif(input_Table5_item>=0.1 and input_Table5_item<0.15):
    output_Table6_item = 3
  elif(input_Table5_item>=0.15 and input_Table5_item<0.20):
    output_Table6_item = 2
  elif(input_Table5_item>=0.20 and input_Table5_item<0.25):
    output_Table6_item = 1
  elif(input_Table5_item>=0.25):
    output_Table6_item = 0
  #lse:
   # output_Table6_item = 0
  
  return output_Table6_item

def Cal_Table6_From_Table5_3(input_Table5_item): # Self-Correction for approaching the 2DTG
  output_Table6_item = 0
  if(input_Table5_item < 0.1):
    output_Table6_item = 4
  elif(input_Table5_item>=0.1 and input_Table5_item<0.15):
    output_Table6_item = 3
  elif(input_Table5_item>=0.15 and input_Table5_item<0.20):
    output_Table6_item = 2
  elif(input_Table5_item>=0.20 and input_Table5_item<0.25):
    output_Table6_item = 1
  elif(input_Table5_item>=0.25):
    output_Table6_item = 0
  #lse:
   # output_Table6_item = 0
  
  return output_Table6_item
    

def Cal_FPD(input_Table, input_type2):
    output_Table_3 = [0,0,0,0,0]
    output_Table_4 = [0,0,0,0,0]
    output_Table_5 = [0,0,0,0,0]
    output_Table_6 = [0,0,0,0,0]
    output_Table_7 = [0,0,0,0,0]
    Final_max = 0
    
    Total_Module_Num = input_Table[0] + input_Table[1] + input_Table[2] + input_Table[3] + input_Table[4]
    output_Table_3[0] = input_Table[0]
    output_Table_3[1] = output_Table_3[0] + input_Table[1]
    output_Table_3[2] = output_Table_3[1] + input_Table[2]
    output_Table_3[3] = output_Table_3[2] + input_Table[3]
    output_Table_3[4] = output_Table_3[3] + input_Table[4]

    output_Table_4[0] = Total_Module_Num - output_Table_3[0]
    output_Table_4[1] = Total_Module_Num - output_Table_3[1]
    output_Table_4[2] = Total_Module_Num - output_Table_3[2]
    output_Table_4[3] = Total_Module_Num - output_Table_3[3]
    output_Table_4[4] = Total_Module_Num - output_Table_3[4]

    output_Table_5[0] = np.float32(output_Table_4[0]) / np.float32(Total_Module_Num) 
    output_Table_5[1] = np.float32(output_Table_4[1]) / np.float32(Total_Module_Num)
    output_Table_5[2] = np.float32(output_Table_4[2]) / np.float32(Total_Module_Num)
    output_Table_5[3] = np.float32(output_Table_4[3]) / np.float32(Total_Module_Num)
    output_Table_5[4] = np.float32(output_Table_4[4]) / np.float32(Total_Module_Num)
    
    if(input_type2 == 0):
      output_Table_6[0] = Cal_Table6_From_Table5(output_Table_5[0])
      output_Table_6[1] = Cal_Table6_From_Table5(output_Table_5[1])
      output_Table_6[2] = Cal_Table6_From_Table5(output_Table_5[2])
      output_Table_6[3] = Cal_Table6_From_Table5(output_Table_5[3])
      output_Table_6[4] = Cal_Table6_From_Table5(output_Table_5[4])
    else:
      output_Table_6[0] = Cal_Table6_From_Table5_2(output_Table_5[0])
      output_Table_6[1] = Cal_Table6_From_Table5_2(output_Table_5[1])
      output_Table_6[2] = Cal_Table6_From_Table5_2(output_Table_5[2])
      output_Table_6[3] = Cal_Table6_From_Table5_2(output_Table_5[3])
      output_Table_6[4] = Cal_Table6_From_Table5_2(output_Table_5[4])


    output_Table_7[0] = min(4,output_Table_6[0])
    output_Table_7[1] = min(3,output_Table_6[1])
    output_Table_7[2] = min(2,output_Table_6[2])
    output_Table_7[3] = min(1,output_Table_6[3])
    output_Table_7[4] = min(0,output_Table_6[4])
    
    for i in range(5):
      if(output_Table_7[i]>Final_max):
        Final_max=output_Table_7[i]

    #return output_Table_7
    return Final_max

def Cal_BW_List_Hori(input_img_band, input_dim):
    output_list = [0 for i in range(input_dim)]
    #print output_list
    height_4, width_4 = input_img_band.shape    
    step_Hori = int(width_4)/int(input_dim)
    start_p = int(step_Hori/2)
    end_p = int(width_4) - int(step_Hori/2)
    j = 0
    for i in range(start_p, end_p, step_Hori):
      temp = input_img_band[int(height_4/2), i]
      if(j<=input_dim-1):
        output_list[j] = temp
      j += 1    
    #print output_list #shan
    T_c = 0
    for i in range(1, input_dim, 1):
      if(output_list[i] != output_list[i-1]):
        T_c += 1
    return T_c


def Cal_BW_List_Verti(input_img_band, input_dim):
    output_list = [0 for i in range(input_dim)]
    #print output_list
    height_4, width_4 = input_img_band.shape    
    step_Hori = int(height_4)/int(input_dim)
    start_p = int(step_Hori/2)
    end_p = int(height_4) - int(step_Hori/2)
    j = 0
    for i in range(start_p, end_p, step_Hori):
      temp = input_img_band[i, int(width_4/2)]
      if(j<=input_dim-1):
        output_list[j] = temp
      j += 1
    #print output_list #shan
    T_c = 0
    for i in range(1, input_dim, 1):
      if(output_list[i] != output_list[i-1]):
        T_c += 1
    return T_c



input_img_path = './images/187.bmp'
#input_img_path = '/home/chezhaohui/2DTG/DM_EP_Linux_64_so_v.16.09_Trial/images/patches/test42.bmp'
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
    print("The Decode Grade is :", my_decode_grade)
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
    print("The Symbol Contrast and SC_Grade are :", my_symbol_contrast,my_symbol_contrast_grade)#feature2 Symbol Contrast grade

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
    '''
    for i in range(DimRow): #DimRow
      for j in range(DimCol): #DimCol
        if(((i+1)*Module_Size_row-1<=DR1_rows) and (((j+1)*Module_Size_col-1)<=DR1_cols)):
          Module_temp = Data_Region_1[(i*Module_Size_row):((i+1)*Module_Size_row-1), (j*Module_Size_col):((j+1)*Module_Size_col-1)]
        else:
          Module_temp = Data_Region_1[(i*Module_Size_row):(DR1_rows-1), (j*Module_Size_col):(DR1_cols-1)]
        
        Module_temp = cv2.cvtColor(Module_temp,cv2.COLOR_BGR2GRAY)
        #print Module_temp #shan
        #plt.imshow(Module_temp, 'gray'),plt.title('TEMP'),plt.show()#shan
        II,JJ= Module_temp.shape
        R = np.float32(1000)
        MOD_grade = 0
        for ii in range(int(II*0.4), int(II*0.6)+1, 1):
          for jj in range(int(JJ*0.4), int(JJ*0.6)+1, 1): #range(start, end, step):just select the center region (40%-60% was defined by myself, maybe should be changed) of each module, because the edge region will effect the final result severely
            if(abs(np.float32(Module_temp[ii,jj])-GT) < abs(R-GT)):
              R = np.float32(Module_temp[ii,jj])
        MOD = 2*abs(R-GT)/SC
        if(MOD<Contrast_Uniformity):
          Contrast_Uniformity = MOD
        #print GT,SC,R,MOD
        if((MOD >= 0.50)):
          MOD_grade = 4
        elif((MOD >= 0.40) and (MOD < 0.50)):
          MOD_grade = 3
        elif((MOD >= 0.30) and (MOD < 0.40)):
          MOD_grade = 2
        elif((MOD >= 0.20) and (MOD < 0.30)):
          MOD_grade = 1
        elif((MOD < 0.20)):
          MOD_grade = 0
        #print("GT, SC, R, MOD, and MOD_grade:", GT,SC,R,MOD,MOD_grade) #shan

        if(MOD_grade==4):
          Table_MOD_2[0] += 1
        elif(MOD_grade==3):
          Table_MOD_2[1] += 1
        elif(MOD_grade==2):
          Table_MOD_2[2] += 1
        elif(MOD_grade==1):
          Table_MOD_2[3] += 1
        elif(MOD_grade==0):
          Table_MOD_2[4] += 1
    print("Modulation Table7.2 is :", Table_MOD_2)
    '''
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
    print("The Polarity of the Code(1 means Code Region is Dark, while 0 means Code Region is Light)", Polarity)


    Table_MOD_2, Contrast_Uniformity = Cal_Modulation(Data_Region_1, DimRow, DimCol, Module_Size_row, Module_Size_col, GT, SC, Polarity, 0) # Type=0, dont update
    print ("Modulation Table7.2 is :", Table_MOD_2)
    
    Table_MOD_3[0] = Table_MOD_2[0]
    Table_MOD_3[1] = Table_MOD_3[0] + Table_MOD_2[1]
    Table_MOD_3[2] = Table_MOD_3[1] + Table_MOD_2[2]
    Table_MOD_3[3] = Table_MOD_3[2] + Table_MOD_2[3]
    Table_MOD_3[4] = Table_MOD_3[3] + Table_MOD_2[4]
    print("Modulation Table7.3 is :", Table_MOD_3)
    
    Table_MOD_4[0] = Table_MOD_3[4] - Table_MOD_3[0]
    Table_MOD_4[1] = Table_MOD_3[4] - Table_MOD_3[1]
    Table_MOD_4[2] = Table_MOD_3[4] - Table_MOD_3[2]
    Table_MOD_4[3] = Table_MOD_3[4] - Table_MOD_3[3]
    Table_MOD_4[4] = Table_MOD_3[4] - Table_MOD_3[4]
    print("Modulation Table7.4 is :", Table_MOD_4)
              
    '''
    Feature4 Contrast Uniformity (not necessary)
    '''    
    print("The Contrast Uniformity is:", Contrast_Uniformity)  

    '''
    Feature4 Reflectance Margin (Page 28, ISO15415 file, English Version)
    '''    

    '''
    Feature5 Fixed Pattern Damage
    '''     
    QZL1 = Data_Region_2[0:DR2_rows, 0:Module_Size_col] #two L shapes, and 2 Quite Zone bands
    QZL2 = Data_Region_2[DR2_rows-Module_Size_row:DR2_rows, 0:DR2_cols]
    L1 = Data_Region_2[Module_Size_row:DR2_rows-Module_Size_row, Module_Size_col:2*Module_Size_col]
    L2 = Data_Region_2[DR2_rows-2*Module_Size_row:DR2_rows-Module_Size_row, Module_Size_col:DR2_cols-Module_Size_col]
    
    QZL1_Table_2, shan = Cal_Modulation(QZL1, DimRow, 1, Module_Size_row, Module_Size_col, GT, SC, Polarity, 1) #should be DimRow+2, but test29fails Type=1
    print ("Modulation Table7.2 of QZL1 :", QZL1_Table_2)
    QZL1_grade = Cal_FPD(QZL1_Table_2, 0)
    print ("Grade of QZL1 :", QZL1_grade)

    QZL2_Table_2, shan = Cal_Modulation(QZL2, 1, DimCol, Module_Size_row, Module_Size_col, GT, SC, Polarity, 1) #should be DimCol+2, but test29fails Type=2
    print ("Modulation Table7.2 of QZL2 :", QZL2_Table_2)
    QZL2_grade = Cal_FPD(QZL2_Table_2, 0)
    print ("Grade of QZL2 :", QZL2_grade)

    L1_Table_2, shan = Cal_Modulation(L1, DimRow, 1, Module_Size_row, Module_Size_col, GT, SC, Polarity, 2) # Type=2
    print ("Modulation Table7.2 of L1 :", L1_Table_2)
    L1_grade = Cal_FPD(L1_Table_2, 0)
    print ("Grade of L1 :", L1_grade)

    L2_Table_2, shan = Cal_Modulation(L2, 1, DimCol, Module_Size_row, Module_Size_col, GT, SC, Polarity, 2) # Type=2
    print ("Modulation Table7.2 of L2 :", L2_Table_2)
    L2_grade = Cal_FPD(L2_Table_2, 0)
    print ("Grade of L2 :", L2_grade)

    #Data_Region_2_gray = cv2.cvtColor(Data_Region_2,cv2.COLOR_BGR2GRAY)
    #Thresh1 = int(GT)
    #ret,Data_Region_2_bw = cv2.threshold(Data_Region_2_gray, Thresh1, 255, cv2.THRESH_BINARY)
    #print Data_Region_2_bw
    #SameColor1 = Data_Region_2_bw[0:Module_Size_row, Module_Size_col:DR2_cols-Module_Size_col] #two SameColor bands, and two LocatePatterns
    #SameColor2 = Data_Region_2_bw[Module_Size_row:DR2_rows-Module_Size_row, DR2_cols-Module_Size_col:DR2_cols]
    LocPAT1 = Data_Region_2_bw[Module_Size_row:2*Module_Size_row, Module_Size_col:DR2_cols-Module_Size_col]
    LocPAT2 = Data_Region_2_bw[Module_Size_row:DR2_rows-Module_Size_row, DR2_cols-2*Module_Size_col:DR2_cols-Module_Size_col]

    T_s_1 = Cal_BW_List_Hori(SameColor1, DimCol)    
    T_c_1 = Cal_BW_List_Hori(LocPAT1, DimCol)
    Grade_SCLP_1 = 0
    Score_SCLP_1 = np.float32(max(0, T_s_1-1)) / np.float32(T_c_1)
    if(Score_SCLP_1<0.06):
      Grade_SCLP_1 = 4
    elif(Score_SCLP_1>=0.06 and Score_SCLP_1<0.08):
      Grade_SCLP_1 = 3
    elif(Score_SCLP_1>=0.08 and Score_SCLP_1<0.10):
      Grade_SCLP_1 = 2
    elif(Score_SCLP_1>=0.10 and Score_SCLP_1<0.12):
      Grade_SCLP_1 = 1
    elif(Score_SCLP_1>=0.12):
      Grade_SCLP_1 = 0
    print("Grade of ChangeRate of SameColor&LocatePattern Region 1:", Grade_SCLP_1)


    T_s_2 = Cal_BW_List_Verti(SameColor2, DimRow) 
    T_c_2 = Cal_BW_List_Verti(LocPAT2, DimRow)
    Grade_SCLP_2 = 0
    Score_SCLP_2 = np.float32(max(0, T_s_2-1)) / np.float32(T_c_2)
    if(Score_SCLP_2<0.06):
      Grade_SCLP_2 = 4
    elif(Score_SCLP_2>=0.06 and Score_SCLP_2<0.08):
      Grade_SCLP_2 = 3
    elif(Score_SCLP_2>=0.08 and Score_SCLP_2<0.10):
      Grade_SCLP_2 = 2
    elif(Score_SCLP_2>=0.10 and Score_SCLP_2<0.12):
      Grade_SCLP_2 = 1
    elif(Score_SCLP_2>=0.12):
      Grade_SCLP_2 = 0
    print("Grade of ChangeRate of SameColor&LocatePattern Region 2:", Grade_SCLP_2)

    SC1 = Data_Region_2[0:Module_Size_row, Module_Size_col:DR2_cols-Module_Size_col] #SameColor region and Timing Pattern region, color version, for calculate the Modulation
    SC2 = Data_Region_2[Module_Size_row:DR2_rows-Module_Size_row, DR2_cols-Module_Size_col:DR2_cols]
    TP1 = Data_Region_2[Module_Size_row:2*Module_Size_row, Module_Size_col:DR2_cols-Module_Size_col]
    TP2 = Data_Region_2[Module_Size_row:DR2_rows-Module_Size_row, DR2_cols-2*Module_Size_col:DR2_cols-Module_Size_col]

    SC1_Table_2, shan = Cal_Modulation(SC1, 1, DimCol, Module_Size_row, Module_Size_col, GT, SC, Polarity, 1) 
    print ("Modulation Table7.2 of SC1 :", SC1_Table_2)
    SC1_grade = Cal_FPD(SC1_Table_2, 1)
    print ("Grade of SC1 :", SC1_grade)

    SC2_Table_2, shan = Cal_Modulation(SC2, DimRow, 1, Module_Size_row, Module_Size_col, GT, SC, Polarity, 1) 
    print ("Modulation Table7.2 of SC2 :", SC2_Table_2)
    SC2_grade = Cal_FPD(SC2_Table_2, 1)
    print ("Grade of SC2 :", SC2_grade)

    TP1_Table_2, shan = Cal_Modulation(TP1, 1, DimCol, Module_Size_row, Module_Size_col, GT, SC, Polarity, 3) # Type=3
    print ("Modulation Table7.2 of TP1 :", TP1_Table_2)
    TP1_grade = Cal_FPD(TP1_Table_2, 1)
    print ("Grade of TP1 :", TP1_grade)

    TP2_Table_2, shan = Cal_Modulation(TP2, DimRow, 1, Module_Size_row, Module_Size_col, GT, SC, Polarity, 4) # Type=3
    print ("Modulation Table7.2 of TP2 :", TP2_Table_2)
    TP2_grade = Cal_FPD(TP2_Table_2, 1)
    print ("Grade of TP2 :", TP2_grade)

    Whole_TP_SC_Grade = min(SC1_grade, SC2_grade, TP1_grade, TP2_grade)
    print ("Grade of the whole TimingPattern and SameColor Regions:", Whole_TP_SC_Grade)

    Average_Grade = np.float32((QZL1_grade + QZL2_grade + L1_grade + L2_grade + Whole_TP_SC_Grade)) / np.float32(5)
    print ("The Average Grade of the Finder Pattern: ", Average_Grade)
    
    My_Avg_FPD_Grade = np.float((QZL1_grade + QZL2_grade + L1_grade + L2_grade + Grade_SCLP_1 + Grade_SCLP_2 + Whole_TP_SC_Grade)/7)
    print ("The Average Grade of the Finder Pattern:(My) ", My_Avg_FPD_Grade)
    '''
    # I think this condition is too rigious, so I give up, maybe should be reconsidered 
    if(Average_Grade==np.float32(4):
      my_FPD_grade = 4
    elif(Average_Grade>=3.5 and Average_Grade<4):
      my_FPD_grade = 3
    elif(Average_Grade>=3.0 and Average_Grade<3.5):
      my_FPD_grade = 2
    elif(Average_Grade>=2.5 and Average_Grade<3.0):
      my_FPD_grade = 1
    elif(Average_Grade<2.5):
      my_FPD_grade = 0
    '''

    '''
    #Feature6 Axial Non-Consistency Property (AN)
    '''
    X_avg = np.float32(DR1_cols / DimCol)
    Y_avg = np.float32(DR1_rows / DimRow)
    AN_Score = 2*abs(X_avg-Y_avg) / (X_avg+Y_avg)
    AN_Grade = 4
    if(AN_Score<=0.06):
      AN_Grade = 4
    elif(AN_Score>0.06 and AN_Score<=0.08):
      AN_Grade = 3
    elif(AN_Score>0.08 and AN_Score<=0.10):
      AN_Grade = 2
    elif(AN_Score>0.10 and AN_Score<=0.12):
      AN_Grade = 1
    elif(AN_Score>0.12):
      AN_Grade = 0
    print("The Axial Non-Consistency (AN) is", AN_Score, AN_Grade)

    print("GT and SC:", GT, SC)

    plt.subplot(241),plt.imshow(SameColor1, 'gray'),plt.title('BW SameColor Band1')
    plt.subplot(242),plt.imshow(SameColor2, 'gray'),plt.title('BW SameColor Band2')
    plt.subplot(243),plt.imshow(LocPAT1, 'gray'),plt.title('BW Timing Pattern 1')
    plt.subplot(244),plt.imshow(LocPAT2, 'gray'),plt.title('BW Timing Pattern 2')
    plt.subplot(245),plt.imshow(SC1, 'gray'),plt.title('Gray SameColor Band1')
    plt.subplot(246),plt.imshow(SC2, 'gray'),plt.title('Gray SameColor Band2')
    plt.subplot(247),plt.imshow(TP1, 'gray'),plt.title('Gray Timing Pattern 1')
    plt.subplot(248),plt.imshow(TP2, 'gray'),plt.title('Gray Timing Pattern 2')
    plt.show()

    
    plt.subplot(241),plt.imshow(img_ori_py, 'gray'),plt.title('ORIGINAL')
    plt.subplot(242),plt.imshow(img_PT, 'gray'),plt.title('Perspective Transformation')
    plt.subplot(243),plt.imshow(Data_Region_1, 'gray'),plt.title('DataRegion without QZ')
    plt.subplot(244),plt.imshow(Data_Region_2, 'gray'),plt.title('DataRegion with QZ')
    plt.subplot(245),plt.imshow(QZL1, 'gray'),plt.title('QuietZone1')
    plt.subplot(246),plt.imshow(QZL2, 'gray'),plt.title('QuietZone2')
    plt.subplot(247),plt.imshow(L1, 'gray'),plt.title('L shape 1')
    plt.subplot(248),plt.imshow(L2, 'gray'),plt.title('L shape 2')   
    plt.show()
    








'''
#middle result  set breakpoint at row: 133
134	                   ,pdm_info->quality.horizontal_print_growth);
(gdb) p pdm_info
$38 = (TDM_Info *) 0x644640
(gdb) p *pdm_info
$39 = {rowcols = {45.8299789, 57.9778061, 471.183777, 57.6875801, 471.183777, 
    482.510681, 45.8299789, 483.485596}, pchlen = 15, 
  pch = 0x6481b3 "5564643********", RSErr = 0, VDim = 14, HDim = 14, 
  saTotalSymbolsNumber = 0, saSymbolPosition = 0, saFileID1 = 0, 
  saFileID2 = 0, mirrored = 1, dotpeenstage = 0, matrixcolor = 0, quality = {
    symbol_contrast = 100, axial_nonuniformity = 0.00124861801, 
    grid_nonuniformity = 0.0987112746, fixed_pattern_damage = 4, 
    unused_error_correction = 1, vertical_print_growth = 0.0338409469, 
    horizontal_print_growth = -0.0421940945, symbol_contrast_grade = 4, 
    axial_nonuniformity_grade = 4, grid_nonuniformity_grade = 4, 
    fixed_pattern_damage_grade = 4, unused_error_correction_grade = 4, 
    modulation_grade = 4, decode_grade = 4, overall_grade = 4}}

'''