
         The Decode Library for Linux. 
         -------------------------------------------------------
1. Following files are supplied within SDK:

 1.1 Library for application development

  libDMatrix.so	 - library with decoding functions
  
 1.2 Source codes of demo program that applies the library

  DMPro_Types.h   - header file that describes interface of library
  Demo_Opn.cpp, Demo_Opn_Dynamic_Load.cpp - source codes of sample applications that uses our library
  LoadBMP.c, LoadBMP.h - the functions for loading "BMP" files

 1.3 Executable files
  demo_so.out - demo program (applicatiom) that was built from Demo_Opn.cpp
		    source code.
  demo_so_dyn.out - demo program (applicatiom) that was built from Demo_Opn_Dynamic_Load.cpp
		    source code.

 1.4 Short SDK description
  readme.txt	 - this file.


2. Unpack all files into same directory. 
   Copy libDMatrix.so to /usr/lib. 
   Set right "executable" for file "demo_so.out" and "demo_so_dyn.out"
   Run "demo_so.out" or "demo_so_dyn.out".
 	
3. Source .cpp and .h files show how the library functions should be called.
Build Limux demo application by command:

  g++ Demo_Opn.cpp -L./ -lDMatrix -m64 -lm -o mydemo.out
or
  g++ Demo_Opn_Dynamic_Load.cpp -rdynamic -ldl -m64 -lm -o mydemo_dyn_load.out

4. If compilation generates instant executable program "mydemo.out" 
you can run the program in the same way as described in 2.


