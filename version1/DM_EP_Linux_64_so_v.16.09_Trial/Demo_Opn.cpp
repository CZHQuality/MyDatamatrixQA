
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <time.h>

#include "LoadBMP.c"
#include "DMPro_Types.h"

// the images size
const int maxrowQ = 4000;       // maximum of image rows
const int maxcolQ = 4000;

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
   
   if(argc != 2)
   {
    printf("Usage:\n");
    printf("demo_pro.out MyImageName.bmp\n");
    return 0;
   }
   pmembits = (TRow) malloc(maxrowQ*maxcolQ);       //  Image in Memory
   pbits    = (TRow*) malloc(maxrowQ*sizeof(TRow)); // pointers to ScanLines
   for (row = 0; row < maxrowQ; row++){
     pbits[row] = &pmembits[maxcolQ*row];
   }
   welldec = 0;
   // create Data Matrix decoder 
   pDecoder = Connect_DM_Decoder(maxrowQ, maxcolQ); 
   if(pDecoder)
   {
     opt.maxDMCount = 100;
     opt.cellColor  = CL_ANY; // equal to default value
     opt.mirrorMode = MM_ANY;
     opt.speedMode  = DMSP_REGULAR;
     opt.qualityMask = DM_QM_ALL;
     opt.labelMode  =  LM_ST_DOT; // LM_STANDARD;
     opt.timeOut    = 0;
     opt.filterMode = FM_AUTO;
     opt.qzMode     = DMQZ_NORMAL; 

     dec1 = Create_DM_Options(pDecoder,opt);

     fn = 0;
     sumtime = 0;
      printf("\n filename: ========= %s", argv[1]);

       rowcount = maxrowQ;
       colcount = maxcolQ;
       ResLoadBMP = LoadBMP (argv[1] ,pbits ,&rowcount ,&colcount);
       if(ResLoadBMP == 0)
       {
         beg = clock();
         // decode
	        result = DecodeDM_Bits(dec1, rowcount, colcount, pbits);
         end = clock();

         printf("\n result = %4d ",result);
         pdm_imageinfo = GetDM_ImageInfo(dec1);
         dmq = pdm_imageinfo->DMCount;
         printf("\n DM count = %4d",dmq);
         rr  = pdm_imageinfo->RejectionReason;
         if((dmq > 0) && (rr == DM_RR_OK))
         {
           welldec++;
           for (i=0;i<=dmq-1;i++){
             pdm_info = GetDM_Info(dec1, i);
             printf("\n vert. & horiz. print_growth  = %7.2f,%7.2f"
                   ,pdm_info->quality.vertical_print_growth
                   ,pdm_info->quality.horizontal_print_growth);
             printf("\n axial_nonuniformity (grade)  = %7.2f  (%d)"
                    ,pdm_info->quality.axial_nonuniformity
                    ,(int)(pdm_info->quality.axial_nonuniformity_grade));
             printf("\n grid_nonuniformity  (grade)  = %7.2f  (%d)"
                    ,pdm_info->quality.grid_nonuniformity
                    ,(int)(pdm_info->quality.grid_nonuniformity_grade));
             printf("\n symbol_contrast     (grade)  = %7.2f%% (%d)"
                    ,pdm_info->quality.symbol_contrast
                    ,(int)(pdm_info->quality.symbol_contrast_grade));
             printf("\n unused_error_corr.  (grade)  = %7.2f  (%d)"
                   , pdm_info->quality.unused_error_correction
                   , (int)(pdm_info->quality.unused_error_correction_grade));
             printf("\n fixed_patt_damage.  (grade)  = %7.2f  (%d)"
                   , pdm_info->quality.fixed_pattern_damage
                   , (int)(pdm_info->quality.fixed_pattern_damage_grade));
             printf("\n (modulation grade)           =          (%d)"
                    ,(int)(pdm_info->quality.modulation_grade));
             printf("\n (decode grade)               =          (%d)"
                    ,(int)(pdm_info->quality.decode_grade));
             printf("\n (overall grade)              =          (%d)"
                    ,(int)(pdm_info->quality.overall_grade));

             printf("\n RSErr = %4d",pdm_info->RSErr);
				         if (pdm_info->pchlen>0)
               printf("\n Decoded array: %s",pdm_info->pch);
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
           printf("\n rr = %4d ",rr);
           pdm_info = GetDM_Info(dec1, 0);
           {
             printf("\n PrGr = %7.2f,%7.2f"
                   ,pdm_info->quality.vertical_print_growth
                   ,pdm_info->quality.horizontal_print_growth);
             printf("\n AxNU   (grade) = %7.2f  (%d)"
                    ,pdm_info->quality.axial_nonuniformity
                    ,(int)(pdm_info->quality.axial_nonuniformity_grade));
             printf("\n GridNU (grade) = %7.2f  (%d)"
                    ,pdm_info->quality.grid_nonuniformity
                    ,(int)(pdm_info->quality.grid_nonuniformity_grade));
             printf("\n SymCtr (grade) = %7.2f%% (%d)"
                    ,pdm_info->quality.symbol_contrast
                    ,(int)(pdm_info->quality.symbol_contrast_grade));
             printf("\n UEC    (grade) = %7.2f  (%d)"
                   , pdm_info->quality.unused_error_correction
                   , (int)(pdm_info->quality.unused_error_correction_grade));
             printf("\n FPD    (grade) = %7.2f  (%d)"
                   , pdm_info->quality.fixed_pattern_damage
                   , (int)(pdm_info->quality.fixed_pattern_damage_grade));
             printf("\n (modulation grade) =      (%d)"
                    ,(int)(pdm_info->quality.modulation_grade));
             printf("\n (decode grade)     =      (%d)"
                    ,(int)(pdm_info->quality.decode_grade));
             printf("\n (overall grade)    =      (%d)"
                    ,(int)(pdm_info->quality.overall_grade));

             printf("\n rowcols: ");
             for (k=0;k<4;k++){
               printf("(%4d,%4d),   ", (int)(pdm_info->rowcols[2*k])
                                     , (int)(pdm_info->rowcols[2*k+1]));
             }
             printf("\n");
           }
         }
         printf("\n time = %d\n", (int)((end - beg)*1000 / CLOCKS_PER_SEC));
         sumtime += end - beg;
         fn++;
         
	    }else{
	      printf("\n\nLoadBMP !=0\n");
       }
     Delete_DM_Options(dec1);  // not necessary
     Disconnect_DM_Decoder(pDecoder);
   }
   free(pbits);
   free(pmembits);
   return 0;
}
