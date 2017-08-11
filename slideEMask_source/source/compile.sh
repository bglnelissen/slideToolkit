g++ -o slideEMask slideEMask.cpp -O2 -I . -L/usr/X11R6/lib -lm -lpthread -lX11 -lX11 -ltiff `Magick++-config --cxxflags --cppflags --ldflags --libs` -std=c++11
mv slideEMask ../../
