#define cimg_display_type 0
#include <iostream> 
#include <string>
#include <Magick++.h>
#include "CImg.h"
#include <fstream>
#include <map>
#include <algorithm>
#include <cmath>
#include <vector>
#include <set>
#include <ctime>
#include <stdio.h>

using namespace cimg_library;
using namespace std;
#include "slideToolKit.h"
using namespace Magick;

//Compiling on MacOSX:
//g++ -o slideEMask slideEMask.cpp -O2 -lm -lpthread -I/usr/X11R6/include -L/usr/X11R6/lib -lm -lpthread -lX11 -ltiff `Magick++-config --cxxflags --cppflags --ldflags --libs`

void print_help()  {

	cout << "slideEMask: Determine a tissue mask image from a slide TIFF using an image entropy filter (a measure for image texture)" << endl << endl << "usage" << endl << "  slideEMask <filename> (-c/--cp/--cellprofiler)" << endl;
	cout << "  -c/--cp/--cellprofiler: " << endl << "\t Whether to prepare the image for CellProfiler (save as bmp instead of png, and prepend \"ENTROPY_\" to the filename), default 'false'" << endl << endl;
	cout << "description" << endl;
	cout << "  slideEMask determines a tissue mask image by assessing image texture. " << endl << "This information is captured by using the standard formula for information entropy to determine the image entropy at each pixel point." << endl << "This works because highly textured areas (foreground, tissue) can be considered \"chaotic\" in terms of entropy, and can thus be separated from non-texturized regions (background) using this measure." << endl << endl << "To this extent, a 3x3 pixel 'neighborhood' is defined around each pixel. The center pixel's entropy value is calculated by taking the entropy of it's surrounding 3x3 neighborhood." << endl << endl << "These values are then averaged in a 4x4 pixel neighborhood to smoothen the image (removing small gaps)." << endl << endl;
	cout << "slideEMask was written by Tim Bezemer. For questions/comments please contact t.bezemer-2@umcutrecht.nl" << endl << endl;
	cout << "slideEMask uses the CImg library, released under the CeCILL license" << endl;
}

int main(int argc,char **argv) 
{ 

	std::string filename = "";
	std::string layer = "";

	bool CellProfiler = false;

	//Check if at least 1 command line arg was passed
	if(argc < 2) { print_help(); return 1; }

	//Check if the user requests help or a usage instruction
	if (std::string(argv[1]) == "--help" || std::string(argv[1]) == "-h" || std::string(argv[1]) == "--usage" || std::string(argv[1]) == "usage") { print_help(); return 0; }

	//Parse the command line args: see if the CellProfiler flag was set.
	for (int i = 1; i < argc; ++i) {
       
       if (std::string(argv[i]) == "-c" || std::string(argv[i]) == "--cp" || std::string(argv[i]) == "--cellprofiler") {

       		CellProfiler = true;

       }
       else if (std::string(argv[i]) == "-l" || std::string(argv[i]) == "--layer") {

       	layer = std::string(argv[i+1]);
       	i++;
       }
       else {

       	filename = std::string(argv[i]);

       }


    }

	if (is_file_exist(filename.c_str()) == false) {

		cerr << "Could not access file " << filename << endl;

        return 1;

	}
	else {

		if (CellProfiler) {
			cout << "Creating entropy image for " << filename << endl;
		}
		else {

			cout << "Automasking " << filename << endl;

		}
	}

	InitializeMagick(*argv);

    // Construct the image object. Seperating image construction from the 
    // the read operation ensures that a failure to read the image file 
    // doesn't render the image object useless. 
    Image image;

    // layer 0 = Thumbnail
    // layer 5 = Macro
    // layer 3 = default layer for slide2Tiles

	try { 

		//Start the clock, to measure elapsed time:
		clock_t begin = clock();

		std::string extension = getExtension(filename);

		std::string to_open = "";

		if (!CellProfiler) {

			//ADD A CHECK FOR TIFF-LIKE FORMAT FILENAME!

			//FIRST WE SAVE THE MACRO IMAGE, AS THE EXTRACTION IS DONE USING IMAGEMAGICK, AND THE ENTROPY PROCESSING BY CImg, A DIFFERENT LIBRARY.
			cout << "\t...Extracting macro image" << endl;
			
			if (layer == "") {
				image = getMacroLayer(filename);
			}
			else {
				image = getCustomLayer(filename, layer);
			}
			//Resize the macro image to 2000x2000 pixels
			//image.resize("2000x2000");

			// Write the image to a file 
			std::string new_filename = replaceString(filename, "." + extension, ".macro.png");

			image.write( new_filename ); 

		  	to_open = new_filename;
		  

	  	}
	  	else {

	  		cout << "\t...Loading tile image" << endl;
	  		to_open = filename;

	  	}

	  	CImg<float> src( to_open.c_str() );

	    cout << "\t...Converting to gray scale" << endl;
	  	
	    src = src.get_RGBtoYCbCr().get_channel(0);

	  	CImg<float> dest(src,false);

	  	cout << "\t...Applying entropy filter" << endl;

	  	// Define a 3x3 neighborhood as a 3x3 image.
	  	CImg<> N(3,3);

	  	//Calculate the Entropy for a 3x3 square
	  	// 3x3 neighborhood loop (see CImg docs), loop over x,y z-slice 0 (only 1 z-layer), color channel 0 (grayscale), store in Neighborhood image 'N' (defined above), treat as array of floats
	  	cimg_for3x3(src,x,y,0,0,N,float) {

	  		float H = entropy(N, 9);

	  		dest(x,y) = H;

	  	}

	  	cout << "\t...Smoothing entropy mask" << endl;
	  	//Calculate the average gray value for a 5x5 square, to remove white spots from the tissue area
	  	CImg<> N2(5,5); 

	  	// 5x5 neighborhood loop (see CImg docs), loop over x,y z-slice 0 (only 1 z-layer), color channel 0 (grayscale), store in Neighborhood image 'N2' (defined above), treat as array of floats
	  	cimg_for5x5(src,x,y,0,0,N2,float) {

	  		float avg = N2.sum()/(5*5);

	      //If the average gray value of this neighborhood exceeds value 210, set the pixel value to white, else black (this value was found empirically).
	  		if(avg > 210) { dest(x,y) = 0; }
	  		else { dest(x,y) = 255; }

	  	}

	  	//Display functions for optimization/debugging purposes
	    //!!! Only works when #define cimg_display_type 0 (line 1) is removed!!
		  //CImgList<unsigned char> visu(src,dest);
		  //visu.display("Original + Entropy");       // Display both original and filtered image.
	  
	  	std::string new_fn = "";

	  	if (CellProfiler) {
	  		new_fn = "ENTROPY_" + replaceString(to_open, ".png", ".bmp");
	  	}
	  	else {
	  		new_fn = replaceString(to_open, ".png", ".emask.png");
	  	}
	  	 

	  	//Save, but cast new filename to c_str first, because C++ doesn't accept std::string instead of const *char
	  	dest.save(new_fn.c_str());
	  	cout << "\t...Saved as " << new_fn << endl;

	  	if (CellProfiler) { remove(to_open.c_str()); }

	    clock_t end = clock();
	    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	    cout << "\t...Processing took " << elapsed_secs << " seconds" << endl;

	} 
	catch( Exception &error_ ) {

		cout << "Caught exception: " << error_.what() << endl; 
		return 1; 
	} 

	return 0; 

}

