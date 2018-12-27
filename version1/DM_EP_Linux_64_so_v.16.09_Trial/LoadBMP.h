//---------------------------------------------------------------------------

#if !defined(INCLUDED_LoadBMP_H)
#define INCLUDED_LoadBMP_H

//typedef unsigned char       icByte;               // 0..255
//typedef unsigned short      icWord   ;            // 0..65535
//typedef unsigned long       icDWord  ;            // 0..4294967295
//typedef   signed long       icLongint;            // -2147483648..2147483647
//typedef          icByte*      icPByte  ;
//typedef          icPByte*     icPPByte ;


int  LoadBMP ( char* lpFileName, unsigned char**  A, int*  He, int* Wi);

#endif
