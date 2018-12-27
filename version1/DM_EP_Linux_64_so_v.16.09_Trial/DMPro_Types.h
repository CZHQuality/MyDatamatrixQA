#ifndef DM_PRO_TYPES_H
#define DM_PRO_TYPES_H

enum CELL_COLOR{
 CL_BLACKONWHITE = 1,
 CL_WHITEONBLACK = 2,
 CL_ANY          = 3
};

enum MIRROR_MODE{
 MM_NORMAL   = 1,
 MM_MIRROR   = 2,
 MM_ANY      = 3
};

enum DECODER_SPEED{
 SP_ROBUST          = 0,
 SP_FAST            = 1,
 SP_GRID_ADJUSTMENT = 2,
 SP_EQUALIZATION    = 3, //!< re-equalization of regions probable Data Matrix
 SP_EQUAL_GRADJ     = 4,
 SP_ACCURATE        = 5  
};

/// the aliases:
enum DM_SPEED{
 DMSP_ULTIMATE      = SP_ACCURATE,    //!< most careful and time-expensive
 DMSP_REGULAR       = SP_EQUAL_GRADJ, //!< recommended ratio "speed/quality"
 DMSP_EXPRESS       = SP_ROBUST       //!< basic algorithm (more fast)
};

enum LABEL_MODE{
 LM_STANDARD  = 0,     //!<-ISO 16022
 LM_DOTPEEN   = 1,
 LM_FAX       = 2,
 LM_ST_DOT    = 3      //!< Combines Standard & Dotpeen
};

/// \enum QUALITY_MASK bits of mask:
enum QUALITY_MASK{
 DM_QM_NO       = 0X0000,
 DM_QM_AXNU     = 0X0001,
 DM_QM_PRGR     = 0X0002,
 DM_QM_SYMCTR   = 0X0004,
 DM_QM_CELLINFO = 0X0008,
 DM_QM_ALL      = 0x7FFF
};

enum FILTER_MODE{
 FM_NON         = 0, //!< No filter
 FM_SHARP1      = 1, //!< First  Filter Mode (recursive sharpening)
 FM_SHARP2      = 2, //!< Second Filter Mode (recursive sharpening)
 FM_SHARPMASK   = 3, //!< Sharpening Mask Filter
 FM_AUTO        = 4  //!< Auto selection of sharpening parameters
,FM_BWR         = 5  //!< Bar Width Reduction (spaces enlargement)
,FM_SM_BWR      = 6  //!< Sharpening Mask + Bar Width Reduction
};

enum DMQZ_MODE
{
 DMQZ_NORMAL   = 0, //!< allows QZ>= 5.7 pixels
 DMQZ_SMALL    = 1 //!< allows QZ>= 4.5 pixels, affects speed and robustness
};

enum DM_REJECTION_REASON{
 DM_RR_OK            = 0,
 DM_RR_NON           = 1,
 DM_RR_NODATAMATRIX  = 2,
 DM_RR_BYCRIT        = 3,
 DM_RR_REEDSOLOMON   = 5,
 DM_RR_NOMEMORY      = 99,
 DM_RR_UNKNOWN       = 100,
 DM_RR_DISCONNECTED  = 200
};

enum DM_BREAK_REASON{    //!< invalid anyware except of TI platform 
//----------------------
 DM_ALL_INSPECTED    = 0 //!< no breaks occurred
,DM_TIMEOUT          = 1 //!< termination by time out
,DM_TERMINATED       = 2 //!< termination by user break
};
//=========================================

/// decoder option modes
struct TDM_OptMode
{
  int maxDMCount;   //!< from 1 to 100. 1 by default
  int cellColor;    //!< CL_ANY by default
  int mirrorMode;   //!< MM_NORMAL by default
  int speedMode;    //!< SP_ROBUST by default
  int qualityMask;  //!< DM_QM_NO by default
  int labelMode;    //!< LM_NORMAL by default
  int timeOut;      //!< timeOut in mls. Timeout <= 0  means infinite timeout
  int filterMode;   //!< FM_NON by default
  int qzMode;
};

/// results of decoding the whole Image
struct TDM_ImageInfo
{
  int DMCount;        //!< number of well decoded symbols within image
  int RejectionReason;//!< not DM_RR_OK if no one matrix has been well decoded
  int BreakReason;    //!< 0 - normal termination, 1 - termination by time-out
  int AU_Validation;  //!< = 1 AUTHENTICATION File is Valid
  int AF_Mode;        //!< actually applied: 0 - no Filter, 1 - Small, 2 - Big
 };

/// Data Matrix Quality Parameters
struct TDM_Quality
{
    float symbol_contrast;
    float axial_nonuniformity;
    float grid_nonuniformity;
    float fixed_pattern_damage;       //!< the aggregate grade
    float unused_error_correction;
    float vertical_print_growth;
    float horizontal_print_growth;

    float symbol_contrast_grade;
    float axial_nonuniformity_grade;
    float grid_nonuniformity_grade;
    float fixed_pattern_damage_grade;
    float unused_error_correction_grade;
    float modulation_grade;
    float decode_grade;               //!< (min of grades)
    float overall_grade; //!< N/A because we don't support several scans
};
// for compatibility with MSVC
/// result of decoding of each Data Matrix symbol in image
struct TDM_Info
{
  float          rowcols[8];	  //!< symbol corner coordinates
  int            pchlen;		     //!< length of decoded byte array
  unsigned char* pch;		        //!< pointer to that array
  int            RSErr;		      //!< number of Reed Solomon errors
  int            VDim, HDim;	  //!< vertical and horizontal dimensions of Data Matrix
  int            saTotalSymbolsNumber //!< structured append: total number of matrices
  //!< value 0xff indicates ReaderProgramming - a special case
                ,saSymbolPosition  	  //!< current matrix index
                ,saFileID1		   //!< file identifier 1
                ,saFileID2;    //!< file identifier 2
  int            mirrored;     //!< true if mirrored Data Matrix
  int            dotpeenstage; //!< true if dot peened Data Matrix
  int            matrixcolor;  //!< detected color of Data Matrix
  TDM_Quality    quality;      //!< symbol Quality Parameters
};

/*
/// result of decoding of each Data Matrix symbol in image
struct TDM_Info
{
  float          rowcols[8];	        //!< symbol corner coordinates
  short int      pchlen;		  //!< length of decoded byte array
  unsigned char* pch;		        //!< pointer to that array
  short int      RSErr;		        //!< number of Reed Solomon errors
  short int      VDim, HDim;	//!< vertical and horizontal dimensions of Data Matrix
  unsigned char  saTotalSymbolsNumber //!< structured append: total number of matrices
                ,saSymbolPosition	  //!< current matrix index
                ,saFileID1		  //!< file identifier 1
                ,saFileID2;           //!< file identifier 2
  bool           mirrored;            //!< true if mirrored Data Matrix
  bool           dotpeenstage;        //!< true if dot peened Data Matrix
  unsigned char  matrixcolor;         //!< detected color of Data Matrix
  TDM_Quality    quality;             //!< symbol Quality Parameters
};
*/

//=========================================
typedef void*           PDM_Decoder;   //!< handler of Data Matrix Decoder
typedef void*           PDM_Options;   //!< handler of Decoder Options
typedef TDM_ImageInfo*  PDM_ImageInfo; //!< pointer to Image Info
typedef TDM_OptMode*    PDM_OptMode;   //!< pointer to Options mode
typedef TDM_Quality*    PDM_Quality;   //!< pointer to symbol Quality
typedef TDM_Info*       PDM_Info;      //!< pointer to symbol Info
typedef unsigned char*  TRow;          //!< pointer to bitmap line
//=========================================

#ifdef __cplusplus
  #define extern_c extern "C"
#else
  #define extern_c
#endif

#define embedded
#ifdef embedded
  #define stdcall
#else
  #define stdcall __stdcall
#endif

#define staticlib
#ifdef staticlib
/// The function creates Data Matrix Decoder and returns Decoder handler
extern_c PDM_Decoder stdcall Connect_DM_Decoder(int maxrow, int maxcol);

/// The function destroys Data Matrix Decoder
extern_c void        stdcall Disconnect_DM_Decoder(PDM_Decoder &pDecoder);

/// The function creates Decoder Options and returns Options handler
extern_c PDM_Options stdcall Create_DM_Options(PDM_Decoder pDecoder, TDM_OptMode optmode);

/// The function destroys Decoder Options
extern_c void        stdcall Delete_DM_Options(PDM_Options &pOptions);

/// The function decodes array ppbits with given Options
extern_c int         stdcall DecodeDM_Bits(PDM_Options pOptions, int rowcount, int colcount, TRow* ppbits);

/// The function returnes the ImageInfo of last decoded Image
extern_c PDM_ImageInfo stdcall GetDM_ImageInfo(PDM_Options pOptions);

/// The function returnes OptMode of current Options
extern_c PDM_OptMode   stdcall GetDM_OptMode(PDM_Options pOptions);

/// The function returnes the DM_Info(dmNum)
extern_c PDM_Info      stdcall GetDM_Info(PDM_Options pOptions, int dmNum);

char* GetVersionDate_DM(); 
char* GetVersionTime_DM(); 

#else // windows DLL
/// The function creates Data Matrix Decoder and returns Decoder handler
typedef PDM_Decoder (stdcall *TConnect_DM_Decoder)(int maxrow, int maxcol);

/// The function destroys Data Matrix Decoder
typedef void        (stdcall *TDisconnect_DM_Decoder)(PDM_Decoder &pDecoder);

/// The function creates Decoder Options and returns Options handler
typedef PDM_Options (stdcall *TCreate_DM_Options)(PDM_Decoder pDecoder, TDM_OptMode optmode);

/// The function destroys Decoder Options
typedef void        (stdcall *TDelete_DM_Options)(PDM_Options &pOptions);

/// The function decodes array ppbits with given Options
typedef int (stdcall *TDecodeDM_Bits)(PDM_Options pOptions, int rowcount, int colcount, TRow* ppbits);

/// The function decodes array ppbits with given Options
typedef int (stdcall *TDecodeBitsF)(PDM_Options pOptions, int rowcount, int colcount, TRow* ppbits);

/// The function returnes the ImageInfo of last decoded Image
typedef PDM_ImageInfo (stdcall *TGetDM_ImageInfo)(PDM_Options pOptions);

/// The function returnes OptMode of current Options
typedef PDM_OptMode   (stdcall *TGetDM_OptMode)(PDM_Options pOptions);

/// The function returnes the DM_Info(dmNum)
typedef PDM_Info      (stdcall *TGetDM_Info)(PDM_Options pOptions, int dmNum);
#endif

#endif


