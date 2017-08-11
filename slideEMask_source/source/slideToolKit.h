#include <iostream> 
#include <string>
#include <tiffio.h>
#include <fstream>
#include <Magick++.h>

using namespace std;
using namespace Magick;

bool is_file_exist(const char *fileName)
{
    std::ifstream infile(fileName);
    return infile.good();
}

void to_uppercase(std::string str) {
	
	//We use the transform function to convert all lower case letters to upper case letters
	//using the toupper function in the C headers (not std::toupper, hence the '::')
	std::transform(str.begin(), str.end(), str.begin(), ::toupper);

}

float entropy(float N[], int numlen) {

	map<float , int> frequencies ;

	for (int i=0; i<numlen - 1; ++i) {

		frequencies[ N[i] ] ++ ;

	}

	float H = 0;

  float fNumlen = float(numlen);

	//For every pixel in this window:
	for (int i = 0; i < numlen-1; ++i ) {

		//And calculate the probability of the value, by taking its frequency, and dividing it by the total number of pixels in the neighborhood
		float p = frequencies[ N[i] ] / fNumlen;

		H += (p * log(p));

	}
	
	H = H * -1;
	return(H);

}

std::string getExtension(std::string subject) {

	std::string extension = subject.substr( subject.find_last_of(".")+1 );
	to_uppercase(extension);

	return extension;

}
std::string replaceString(std::string subject, const std::string& search,
                          const std::string& replace) {
    size_t pos = 0;
    while((pos = subject.find(search, pos)) != std::string::npos) {
         subject.replace(pos, search.length(), replace);
         pos += replace.length();
    }
    return subject;
}


std::string getScannerType(std::string filename)
{

    TIFF* tif = TIFFOpen(filename.c_str(), "r");
	
	if (tif) {

		TIFFReadDirectory(tif);

		char* model_name = NULL;
		    
		TIFFGetField(tif, TIFFTAG_MODEL, &model_name);

		std::string output( model_name );

		TIFFClose(tif);

    	return output;

    }

    return "Error";

}

Magick::Image getThumbLayer(std::string filename) {

	//APERIO NEEDS TESTING
	Magick::Image image;

 	std::string ScannerType = getScannerType(filename);

 	if (ScannerType == "iScan HT") {image.read( filename.append("[0]") );}
 	if (ScannerType == "iScan") {image.read( filename.append("[0]") );}
 	if (ScannerType == "Hamamatsu") {image.read( filename.append("[10]") );}
 	if (ScannerType == "Leica") {image.read( filename.append("[1]") );}
 	if (ScannerType == "Aperio") {

 		TIFF* tif = TIFFOpen(filename.c_str(), "r");

 		//Count the number of labels:
 		int n_layers = 0;
		do { n_layers++; } while (TIFFReadDirectory(tif));

 		int N_LABEL = n_layers - 2;
 		int N_TISSUE = n_layers - 1;

 		Magick::Image im_label, im_tissue;

 		im_label.read( filename.append("[" + std::to_string(N_LABEL) + "]") );
 		im_label.resize("1024px");

 		im_tissue.read( filename.append("[" + std::to_string(N_TISSUE) + "]") );
 		im_tissue.resize("1024px");
 		im_tissue.rotate(90);

		// std::list<Magick::Image> imlist = {im_label, im_tissue};

 	// 	appendImages( &image, imlist.begin(), imlist.end() );


 	}


 	return image;

 }

Magick::Image getMacroLayer(std::string filename, std::string layer = "-1") {

	Magick::Image image;

	if (layer != "-1") {

		int LAYER = -1;

	 	std::string ScannerType = getScannerType(filename);

	 	if (ScannerType == "iScan HT") {LAYER = 8;}
	 	if (ScannerType == "iScan") {LAYER = 7;}
	 	if (ScannerType == "Hamamatsu") {LAYER = 5;}
	 	if (ScannerType == "Leica") {LAYER = 5;}
	 	if (ScannerType == "Aperio") {

	 		TIFF* tif = TIFFOpen(filename.c_str(), "r");

	 		int n_layers = 0;
			do {
			    n_layers++;
			} while (TIFFReadDirectory(tif));

	 		LAYER = n_layers - 3;
	 	}

	 	image.read( filename.append("[" + std::to_string(LAYER) + "]") );

	 	return image;
 	}

 else {

 	image.read( filename.append("[" + layer + "]") );

 	return image;

 }
}