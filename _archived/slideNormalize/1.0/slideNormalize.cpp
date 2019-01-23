// Adapted from https://stackoverflow.com/questions/24341114/simple-illumination-correction-in-images-opencv-c/24341809#24341809

#include <opencv2/opencv.hpp>
#include <vector>       // std::vector
#include <iostream>
#include <fstream>

bool is_file_exist(const char *fileName)
{
    std::ifstream infile(fileName);
    return infile.good();
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

int main(int argc, char** argv)
{

    if (is_file_exist(argv[1]) == false) {

      std::cout << "File not found" << std::endl;
      exit(1);

    }

    // READ RGB color image and convert it to Lab
    cv::Mat bgr_image = cv::imread(argv[1]);
    cv::Mat lab_image;
    cv::cvtColor(bgr_image, lab_image, CV_BGR2Lab);

    // Extract the L channel
    std::vector<cv::Mat> lab_planes(3);
    cv::split(lab_image, lab_planes);  // now we have the L image in lab_planes[0]

    // apply the CLAHE algorithm to the L channel
    cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE();
    clahe->setClipLimit(2);
    cv::Mat dst;
    clahe->apply(lab_planes[0], dst);

    // Merge the the color planes back into an Lab image
    dst.copyTo(lab_planes[0]);
    cv::merge(lab_planes, lab_image);

   // convert back to RGB
   cv::Mat image_clahe;
   cv::cvtColor(lab_image, image_clahe, CV_Lab2BGR);

   // display the results  (you might also want to see lab_planes[0] before and after).
   //cv::imshow("image original", bgr_image);
   //cv::imshow("image CLAHE", image_clahe);
   //cv::waitKey();

   std::string new_filename = replaceString( std::string(argv[1]), ".tile.tissue.png", ".normalized.tile.tissue.png" );
   cv::imwrite(new_filename, image_clahe);
}
