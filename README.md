slideToolkit
============

slideToolkit: a free toolset for analyzing full size virtual histology slides

With the possibility to create virtual slides using slide scanners,
different automated quantitative scoring methods are now available.
Commercial software that is often accompanied with the scanner, is
capable of quantifying whole slides by looking at simple image
characteristics (measurement of surface area and the detection of
individual blobs). These methods are fast and have good results on high
contrast stained images, preferably using a fluorescent stain, but these
methods are unreliable in more challenging slides with cluttered cells
and low contrast slides. More reliable software packages for analysis
whole slide images use more complex and intricate methods to identify
the cells and there nuclei. These complex measurement methods are
capable of handling our low contrast DAB stains and cluttered cells, but
are considerable slow and can be cost expensive.

We were in favor of an inexpensive and reliable way to automatically
quantify cells on challenging histological slides. Because we are not
aware of one product that explicitly describes fullsize histology slide
analysis for challenging DAB stains, we created the slideToolkit. The
slide toolkit is a collection of guides and open source software to
support the whole process from digital slides to a dataset with
measurements. In short the slideToolkit workflow is as follows, your
extracts the region of interest, converts that region into tiles,
analyses those tiles and save your data a convenient file format for
quantitative analysis.

The slideToolkit itself is a collection of open source software and must
be seen as a swiss army knife for handling, manipulating and analyzing
digital histology slides. The slideToolkit is developed for modern
(2013) personal computers (running *nix system[Linux, OS X, Unix]) but
is also successfully tested on high-performance computing (HPC) systems.
