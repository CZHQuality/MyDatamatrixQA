#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <dlfcn.h>

#include "LoadBMP.c"
#include "DMPro_Types.h"

// the images size
const int maxrowQ = 4000;       // maximum of image rows
const int maxcolQ = 4000;

///////////////////////////////////////////////////////////////////////////////////
//
// Description of pointers to functions called from the library
//
typedef PDM_Decoder   (*PtrConnect_DM_Decoder)    (int, int );
typedef void          (*PtrDisconnect_DM_Decoder) (PDM_Decoder&);
typedef PDM_Options   (*PtrCreate_DM_Options)     (PDM_Decoder, TDM_OptMode);
typedef void          (*PtrDelete_DM_Options)     (PDM_Options&);
typedef int           (*PtrDecodeDM_Bits)         (PDM_Options ,int ,int ,TRow*);
typedef PDM_ImageInfo (*PtrGetDM_ImageInfo)       (PDM_Options);
typedef PDM_Info      (*PtrGetDM_Info)            (PDM_Options ,int);

PtrConnect_DM_Decoder    pConnect_DM_Decoder = NULL;
PtrDisconnect_DM_Decoder pDisconnect_DM_Decoder = NULL;
PtrCreate_DM_Options     pCreate_DM_Options = NULL;
PtrDelete_DM_Options     pDelete_DM_Options = NULL;
PtrDecodeDM_Bits         pDecodeDM_Bits = NULL;
PtrGetDM_ImageInfo       pGetDM_ImageInfo = NULL;
PtrGetDM_Info            pGetDM_Info = NULL;
//////////////////////////////////////////////////////////////////////////////////////

bool LoadLibrary(void)
{
  void* handle = dlopen("libDMatrix.so", RTLD_LAZY);
  if(handle == NULL)
  {
   printf("Failed dlopen\n");
   return false;
  }
  if((pConnect_DM_Decoder    = (PtrConnect_DM_Decoder)   dlsym(handle, "Connect_DM_Decoder")) == NULL) return false;
  if((pDisconnect_DM_Decoder = (PtrDisconnect_DM_Decoder)dlsym(handle, "Disconnect_DM_Decoder")) == NULL) return false;
  if((pCreate_DM_Options     = (PtrCreate_DM_Options)    dlsym(handle, "Create_DM_Options")) == NULL) return false;
  if((pDelete_DM_Options     = (PtrDelete_DM_Options)    dlsym(handle, "Delete_DM_Options")) == NULL) return false;
  if((pDecodeDM_Bits         = (PtrDecodeDM_Bits)        dlsym(handle, "DecodeDM_Bits")) == NULL) return false;
  if((pGetDM_ImageInfo       = (PtrGetDM_ImageInfo)      dlsym(handle, "GetDM_ImageInfo")) == NULL) return false;
  if((pGetDM_Info            = (PtrGetDM_Info)           dlsym(handle, "GetDM_Info")) == NULL) return false;
  
  return true;
}


int main(int argc, char **argv)
{
   TRow*   pbits;
   TRow    pmembits;  // Image in Memory
   int 	   ResLoadBMP;
   int	   rowcount, colcount,  row, result;
   int     i;
   int     k;
   int     rr;
   PDM_Decoder pDecoder;
   PDM_Options dec1;
   TDM_OptMode opt;
   TDM_ImageInfo* pdm_imageinfo;
   TDM_Info* pdm_info;
   clock_t beg, end;
   int fn, sumtime;
   int dmq;
   int welldec;
   
   if(argc != 2){
    printf("Usage:\n");
    printf("demo.out MyImageName.bmp\n");
    return 0;
   }
   
   if(!LoadLibrary())
     return 0;
   
   pmembits = (TRow) malloc(maxrowQ*maxcolQ);       //  Image in Memory
   pbits    = (TRow*) malloc(maxrowQ*sizeof(TRow)); // pointers to ScanLines
   for (row = 0; row < maxrowQ; row++){
     pbits[row] = &pmembits[maxcolQ*row];
   }
   welldec = 0;
   // create Data Matrix decoder 
   pDecoder = pConnect_DM_Decoder(maxrowQ, maxcolQ); 
   if(pDecoder)
   {
     opt.maxDMCount = 100;
     opt.cellColor  = CL_ANY; // equal to default value
     opt.mirrorMode = MM_ANY;
     opt.speedMode  = DMSP_REGULAR; 
     opt.qualityMask = DM_QM_ALL;
     opt.labelMode  = LM_ST_DOT;
     opt.timeOut    = 0;
     opt.filterMode = FM_AUTO;
     opt.qzMode     = DMQZ_NORMAL; 

     dec1 = pCreate_DM_Options(pDecoder,opt);

     fn = 0;
     sumtime = 0;
      //printf("\n filename: ========= %s", argv[1]);

       rowcount = maxrowQ;
       colcount = maxcolQ;
       ResLoadBMP = LoadBMP (argv[1] ,pbits ,&rowcount ,&colcount);
       if(ResLoadBMP == 0)
       {
         beg = clock();
         // decode
	 result = pDecodeDM_Bits(dec1, rowcount, colcount, pbits);
         end = clock();

         //printf("\n result = %4d ",result);
         pdm_imageinfo = pGetDM_ImageInfo(dec1);
         dmq = pdm_imageinfo->DMCount;
         //printf("\n DM count = %4d",dmq);//just consider the case which detect only one DataMatrix
         rr  = pdm_imageinfo->RejectionReason;
         if(dmq>0 && rr == DM_RR_OK)
         {
           welldec++;
           for (i=0;i<=dmq-1;i++){
               printf("\n rr = %4d",rr);
             pdm_info = pGetDM_Info(dec1, i);//a lot of decoding information including follwing stuffs
             
             printf("\n Dimensions: %4d * %4d",
                    pdm_info->VDim, pdm_info->HDim);
             printf("\n rowcols: ");
             for (k=0;k<4;k++){
               printf("(%4d,%4d),   ", (int)(pdm_info->rowcols[2*k])
                                     , (int)(pdm_info->rowcols[2*k+1]));
             }
             printf("\n");
           }
         }else{ // dmq == 0 => dm_info[0] describes the best undecoded symbol
           printf("\n rr = %4d",rr);//the output information is almost the same as the rr==1 case

           //printf("\n Dimensions: %4d * %4d",
            //        pdm_info->VDim, pdm_info->HDim);//maybe should be deleted, because if decode failed, the Dimensions are unknown

           pdm_info = pGetDM_Info(dec1, 0);
           {
             printf("\n rowcols: ");
             for (k=0;k<4;k++){
               printf("(%4d,%4d),   ", (int)(pdm_info->rowcols[2*k])
                                     , (int)(pdm_info->rowcols[2*k+1]));
             }
             printf("\n");
           }
         }
         //printf("\n time = %d\n", (int)((end - beg)*1000 / CLOCKS_PER_SEC));
         sumtime += end - beg;
         fn++;
         
	    }else{
	      printf("\n\nLoadBMP !=0\n");
       }
     pDelete_DM_Options(dec1);  // not necessary
     pDisconnect_DM_Decoder(pDecoder);
   }
   free(pbits);
   free(pmembits);
   return 0;
}
