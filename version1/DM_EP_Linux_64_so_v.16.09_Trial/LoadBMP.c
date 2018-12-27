// may be #define True3Color
//---------------------------------------------------------------------------
#include "stdio.h"
#include "LoadBMP.h"
//---------------------------------------------------------------------------

#define bool int
#define false 0
#define true  1

typedef struct 
{
 unsigned char R,G,B;
} CL3;

int  LoadBMP (          char*  lpFileName ,
               unsigned char** A      ,
               int           * He     ,
               int           * Wi     )
//----------------------------
{
   FILE *F;
   int res = 0;
   unsigned char A1,A2,A3,A4;
   unsigned char RR,GG,BB,AA;
   unsigned long B;
#define Read_1(A)  {res = fread((void *) &A, 1, 1, F);}
#define Read_2(A)  Read_1(A1);Read_1(A2);\
                   B=(A2<<8)|A1;\
                   A=(unsigned short)B

#define Read_4(A) Read_1(A1);Read_1(A2);Read_1(A3);Read_1(A4);\
                  B=(A4<<24)|(A3<<16)|(A2<<8)|A1;\
                  A=B;

#define Skip(A)  fseek(F,A,1);

   int          i,j ;
   unsigned int      ui;

   int Color,Aij;

  //tagBITMAPFILEHEADER
   unsigned short       bfType       ; // 0000  2
   unsigned long        bfSize       ; // 0002  4
   unsigned short       bfReserved1  ; // 0006  2 
   unsigned short       bfReserved2  ; // 0008  2
   unsigned long        bfOffBits    ; // 000A  4
  //endBITMAPFILEHEADER

  //tagBITMAPINFOHEADER
   unsigned long        biSize       ; // 000E  4 
     signed long        biWidth      ; // 0012  4
     signed long        biHeight     ; // 0016  4
   unsigned short       biPlanes     ; // 001A  2
   unsigned short       biBitCount   ; // 001C  2

   unsigned long        biCompression     ; // 001E 4
   unsigned long        biSizeImage       ; // 0022 4
     signed long        biXPelsPerMeter   ; // 0026 4
     signed long        biYPelsPerMeter   ; // 002A 4
   unsigned long        biClrUsed         ; // 002E 4
   unsigned long        biClrImportant    ; // 0032 4
   //endBITMAPINFOHEADER

   long                 delta;
   bool                 NegbiHeight=false;
   #define ROW (NegbiHeight?(biHeight-1-i):i)

   CL3 CL[256];

   F = fopen(
       lpFileName,	// pointer to filename
       "rb"	// action and attributes
   );

   if (!F) return (-100);

   Read_2(bfType);

   if (bfType != 0x4D42) return (-1); // Not Bitmap

   Read_4(bfSize           );

   Read_2(bfReserved1      );
   Read_2(bfReserved2      );
   Read_4(bfOffBits        );

   Read_4(biSize           );

   if (biSize >= 40)        // Windows Bitmap
   {
     Read_4(biWidth         );
     Read_4(biHeight        );
       if(biHeight<0){biHeight=-biHeight;NegbiHeight=true;}

     if ((biWidth>*Wi) || (biHeight>*He)){
       fclose(F);
       return(-5);          // too large image
     }

     Read_2(biPlanes        );
     Read_2(biBitCount      );
    
     if (biPlanes!=1){
       fclose(F);
       return(-2);         // unsupported format
     };

     Read_4(biCompression   );
     Read_4(biSizeImage     );
     Read_4(biXPelsPerMeter );
     Read_4(biYPelsPerMeter );
     Read_4(biClrUsed       );
     Read_4(biClrImportant  );

       if (biClrUsed==0){
       if (biBitCount==8)biClrUsed =256;else
       if (biBitCount==4)biClrUsed =16;else
       if (biBitCount==1)biClrUsed =2;
     }

     for (ui=0;ui<biClrUsed;ui++)
     {
       res = fread( &CL[ui].B ,1,1,F);
       res = fread( &CL[ui].G ,1,1,F);
       res = fread( &CL[ui].R ,1,1,F);
       Skip(1);

     }
   }//(biSize != 40)
   else
   if (biSize==12)             // OS/2 Bitmap
   {
     Read_2(biWidth         );
     Read_2(biHeight        );
       if(biHeight<0){biHeight=-biHeight;NegbiHeight=true;}

     if ((biWidth > *Wi) || (biHeight > *He)){
       fclose(F);
       return(-5);          // too large image
     }

     Read_2(biPlanes        );
     Read_2(biBitCount      );
     if (biPlanes!=1){
       fclose(F);
       return(-2);
     };

     if (biBitCount==8)biClrUsed =256;else
     if (biBitCount==4)biClrUsed =16;else
     if (biBitCount==1)biClrUsed =1;else
                       biClrUsed =0;

     for (ui=0;ui<biClrUsed;ui++)
     {
       res = fread( &CL[ui].B ,1,1,F);
       res = fread( &CL[ui].G ,1,1,F);
       res = fread( &CL[ui].R ,1,1,F);
     }

   }//(biSize != 40) (biSize != 12)
   else
   {
      fclose(F);
      return(-4);            // not Windows or OS/2 Bitmap
   };

   if (biBitCount==32)      // truecolor
   {
     delta = 0;
   }else
   if (biBitCount==24)      // truecolor
   {
     delta = (biWidth*3) %4;
     if (delta!=0) delta=4-delta;
   }else
   if (biBitCount==8)       // 256 colors
   {
     delta = (biWidth) %4;
     if (delta!=0) delta=4-delta;
   }else
   if (biBitCount==4)      // 16 colors
   {
     delta = ((biWidth+1)/2) %4;
     if (delta!=0) delta=4-delta;
   }else
   if (biBitCount==1)     // monochrome
   {
     //delta=0;
     delta = ((biWidth+7)/8) %4;
     if (delta!=0) delta=4-delta;
   }

   fseek(F,bfOffBits,0);

   if (biPlanes==1)
   { 
     if ( biBitCount==32 )
     {
       for (i=biHeight-1;i>=0;i--)
       {
         for (j=0;j<biWidth;j++)
         {
           Read_1( AA );
           Read_1( BB );
           Read_1( GG );
           Read_1( RR );
           //Color = (RR+ GG+ BB)/3;

           #ifdef True3Color
           Color = (RR*30 + GG*59+ BB*11)/100;
           #else
           Color = (RR + GG + BB)/3;
           #endif

           A [ROW][j] = (unsigned char)Color;
           //AA = (unsigned char)(AA <<1);
         };
         Skip(delta);
       };
     }else
     if ( biBitCount==24 )
     {
       for (i=biHeight-1;i>=0;i--)
       {
         for (j=0;j<biWidth;j++){
           Read_1( BB );
           Read_1( GG );
           Read_1( RR );
           //Color = (RR+ GG+ BB)/3;
           #ifdef True3Color
           Color = (RR*30 + GG*59+ BB*11)/100;
           #else
           Color = (RR + GG+ BB)/3;
           #endif
           if (i==0)
             Color=Color+0;

           A [ROW][j] = (unsigned char)Color;
           //AA = (unsigned char)(AA <<1);
         };
         Skip(delta);
       };
     }else
     if ( biBitCount==8 )
     {
       for (i=biHeight-1;i>=0;i--){
         res = fread( A [ROW] ,biWidth,1,F);
         Skip(delta);
         for (j=0;j<biWidth;j++){
           Aij = A [ROW][j];
           #ifdef True3Color
           Color = (CL [Aij].R*30 + CL [Aij].G*59+ CL [Aij].B*11) /100;
           #else
           Color = (CL [Aij].R+ CL [Aij].G+ CL [Aij].B)/3;
           #endif
           A [ROW][j] = (unsigned char) Color;
         }
       };
     }else
     if ( biBitCount==4 )
     {
       for (i=biHeight-1;i>=0;i--)
       {
         for (j=0;j<biWidth;j++)
         {
           if ((j % 2) ==0 ) Read_1( AA );
           Aij = AA >>4;
           #ifdef True3Color
           Color = (CL [Aij].R*30 + CL [Aij].G*59+ CL [Aij].B*11) /100;
           #else
           Color = (CL [Aij].R+ CL [Aij].G+ CL [Aij].B)/3;
           #endif
           A [ROW][j] = (unsigned char)Color;
           AA = (unsigned char)(AA <<4);
         };
         Skip(delta);
       };
     }else
     if ( biBitCount==1 )
     {
       for (i=biHeight-1;i>=0;i--){
         for (j=0;j<biWidth;j++){
           if ((j % 8) ==0 ) Read_1(AA);
           Aij = AA >>7;
           #ifdef True3Color
           Color = (CL [Aij].R*30 + CL [Aij].G*59+ CL [Aij].B*11) /100;
           #else
           Color = (CL [Aij].R+ CL [Aij].G+ CL [Aij].B)/3;
           #endif
           A [ROW][j] = (unsigned char)Color;
           AA = (unsigned char)(AA <<1);
         };
         Skip(delta);
       };
     }else{
       fclose(F);
       return -2;  //unsupported format
     };
   }else{
     fclose(F);
     return -2; //unsupported format
   };
   *He = biHeight;
   *Wi = biWidth;
   fclose(F);

   return(0);
#undef Read_4
#undef Read_2
#undef Read_1

}//LoadBMP
//---------------------------------------------------------------------------
