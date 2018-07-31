#g++ `pkg-config --cflags opencv` -o sideNormalize slideNormalize.cpp
g++ `pkg-config opencv --cflags --libs` -o slideNormalize slideNormalize.cpp
