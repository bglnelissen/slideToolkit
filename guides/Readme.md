*For installation instructions regarding your specific platform also see the INSTALL.xxx file in this directory that matches your system.

---

README
============

### slideToolkit: an assistive toolset for the histological quantification of whole slide images

Hi,

If you do not know where to start, this should be the right place. In this file we discuss what the slideToolkit does, and how to use it. Just keep on reading.

A little introduction first. The demand for accurate and reproducible phenotyping of a disease trait increases with the rising number of biobanks and genome wide association studies. Detailed analysis of histology is a powerful way of phenotyping human tissues. Nonetheless, purely visual assessment of histological slides is time-consuming and liable to sampling variation and optical illusions and thereby observer variation, and external validation may be cumbersome.

Therefore computerised quantification of digitized histological slides is often preferred as a more precise and reproducible, and sometimes more sensitive approach. Relatively few free toolkits are, however, available for fully digitized microscopic slides, usually known as whole slides images.In order to comply with this need, we developed the slideToolkit as a fast method to handle large quantities of low contrast whole slides images using advanced cell detecting algorithms. The slideToolkit has been developed for modern personal computers and high-performance clusters (HPCs) and is a set of scripts that requires other programs and libraries to run.

Our goal is to provide a free, powerful and versatile collection of tools for automated feature analysis of whole slide images to create reproducible and meaningful phenotypic data sets.

The paper were we introduce the slideToolkit can be found on PlosONE (link). Please cite to this paper when using the slideToolkit for your research.

Good luck,

Bas

---

### The slideToolkit workflow

The slideToolkit is a collection of open-source scripts to handle each step from digital slide to the storage of your results. A common slideToolkit workflow consists of four consecutive steps.

In the first step, “acquisition”, whole slide images are collected and converted to TIFF files. In the second step, “preparation”, all the required files are created and organized. The third step, “tiles”, creates multiple manageable tiles to count. The fourth step, “analysis”, is the actual tissue analysis and saves the results in a meaningful data set.

A set of tools is designed for each step. Instructions on how to use each tool can be found running the `--help` flag (e.g. `slideConvert --help`).

Here you can find a [graphical workflow](slideToolkit.workflow.tif?raw=true) for the slideToolkit.

##### Step 1 - acquisition
Most slide scanners are, in addition to their own proprietary format, capable of storing the digital slides in pyramid TIFF files. The slideToolkit uses the Bio-Formats library to convert other microscopy formats (Bio-Formats supports over 120 different file formats, [openmicroscopy.org](www.openmicroscopy.org)) into the compatible pyramid TIFF format if needed. TIFF is a tag-based file format for raster images. A TIFF file can hold multiple images in a single file, this is known as a multi-layered TIFF. The term "Pyramid TIFF" is used to describe a multi-layered TIFF file that wraps a sequence of raster images that each represents the same image at increasing resolutions (figure 2). The different layers contain, among others, the slide label and multiple enlargements of the tissue on the slide.
To read whole slide images, the open-source libTIFF libraries and the OpenSlide libraries are used. These libraries are also applied to extract metadata (e.g. scan time, magnification and image compression) of the scanned slides. Descriptive information about the slide is stored as metadata and contains, for example, pixels per micrometer, presence of different layers, and scan date. For image processing we use ImageMagick. ImageMagick is a command-line image manipulation tool that is fast, highly adjustable and capable of handling big pyramid TIFF files.

The tools designed for step 1:

- slideConvert, converts any whole slide image file to TIFF format
- slideRename, Batch rename files. Supports barcodes.
- slideInfo, fetch slide metadata (resolution, dates, magnification, etc)


##### Step 2 - preparation
In the following steps multiple output files for each slide are created. For each digital slide, a staging directory is constructed in which the slide, and all output data concerning the slide are stored. In digital image manipulation, a mask defines what part of the image will be analyzed and what part will be hidden. Usually a mask can be defined as black (hidden) or white (not hidden). The slideToolkit creates a mask using convert (ImageMagick) and a miniature version of the whole slide image. To create the maks: the image is blurred, this will remove dust and speckles. Now, the white background is identified using a fuzzy, non-stringent selection and then background is replaced with black. Settings for blur and fuzziness can be found and changed in the slideMask tool.

Generated masks can be adjusted manually in an image editor of choice (such as the freely available GNU Image Manipulation Program; [GIMP](http://www.gimp.org)). Sometimes this is necessary to remove unwanted areas on the whole slide image (like marker stripes or air bubbles under the coverslip).

The tools designed for step 2:

- slideDirectory, create a staging directory per slide.
- slideThumb, create slide thumbnail, including label.
- slideMask, create a scaled mask and macro version from a slide.

##### Step 3 - tiles
Image analysis of memory intensive, whole 20x representations of the digitized slides is currently impossible due to hardware and software limitations. The goal of this step is to create multiple smaller images (i.e. tiles) from the 20x whole slide image. An upscaled version of the mask is placed over the 20x whole slide image (in our example this is layer 3 of the multi layered TIFF). Image manipulation on 20x sized whole slide images requires large amounts of computer RAM. To make it possible for computers without sufficient RAM to handle these files, the slideToolkit uses a memory-mapped disk file of the program memory. Using disk mapped memory files (ImageMagick .mpc files), the slideToolkit can efficiently extract all tiles. Without a mask, a faster and more memory efficient method is used using the openslide library.

The tools designed for step 3:

- slide2Tiles, cut virtual slide into tiles.

##### Step 4 - analysis
At this step, multiple tiles containing tissue data have been made, and the different objects in this tissue will be identified. CellProfiler is designed to quantitatively measure phenotypes from thousands of images automatically without training in computer vision or programming. CellProfiler can run using a graphical user interface (GUI) or a command-line interface (CLI). Using the CellProfiler’s GUI, different algorithms for image analysis are available as individual modules that can be modified and placed in sequential order to form a pipeline. Such a pipeline can be used to identify and measure biological objects and features in images. Pipelines can be stored and reused in future projects. The CLI can be used to run the pipeline for actual image analysis.

An illustrated example on how to create pipelines in CellProfiler is described by Vokes and Carpenter in their manuscript "[Using CellProfiler for Automatic Identification and Measurement of Biological Objects in Images](http://onlinelibrary.wiley.com/doi/10.1002/0471142727.mb1417s82/abstract)".

The tools designed for step 4:

 - slideJobsCellProfiler, outputs a list of jobs for CellProfiler
 - slideSQLheader, fetch table headers from CellProfiler SQL output for CSV file

---
### Hardware
The slideToolkit is developed for any *NIX based operating system. We tested the slideToolkit on a MacMini (2GHz i7 and 16 GB RAM) running OS X - Mavericks 10.9, and the same machine running Linux - Ubuntu 12.04. We also tested the slideToolkit on a high-performance cluster (HPC) running Linux - CentOS 6.5 (8x Intel(R) Xeon(R) CPU E5-2630 0 @ 2.30GHz, 38x Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz, 11x Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz, all with 12 cores and 128 GB RAM per node).

The slideToolkit depends heavily on the *NIX architecture. For this reason we have not planned to create installation instructions for Microsoft Windows. To get the slideToolkit running on Windows, or to create a portable slideToolkit installation, our advise is to run Ubuntu Linux within [VirtualBox](https://www.virtualbox.org) (or any other virtualisation software).

---
 
### Programs and libraries:

A library is a collection of sources and that a computer program can use to add functionality. The libraries we use in this project are mainly open source. Some programs bring there own libraries, some depend on other libraries. This is a list of the programs and libraries the slideToolkit depends on.

For example, the LibTIFF library makes it possible for `ImageMagick` and for `tiffinfo` to handle TIFF files correctly.

The programs and libraries:

- [Bio-Formats Library](http://www.openmicroscopy.org/site/products/bio-formats)
- [CellProfiler](http://cellprofiler.org)
- [GNU Bash](https://www.gnu.org/software/bash/)
- [GNU Parallel](https://www.gnu.org/software/parallel/)
- [ImageMagick](http://www.imagemagick.org)
- [LibTIFF](http://www.remotesensing.org/libtiff/), >=  Version 4
- [Openslide](http://openslide.org)
- [Perl](http://www.perl.org)
- [slideToolkit](https://github.com/bglnelissen/slideToolkit)

*The latest stable version of these programs and libraries should be sufficient. There is one catch, the Lib TIFF library supports the TIFF64 (aka BigTIFF) format since version 4.*

Although the installation of these dependencies can be a hassle, we have provided installation instructions for OS X and Linux.

### Installation instructions:


- [INSTALL - OSX 10.9 - Mavericks](INSTALL.OSX 10.9 - Mavericks.md)
- [INSTALL - Ubuntu 12.04 LTS - Precise Pangolin](INSTALL.Ubuntu 12.04 LTS - Precise Pangolin.md)

*We have not planned to create installation instructions for Microsoft Windows. Try to run Ubuntu 12.04 within [VirtualBox](https://www.virtualbox.org) instead.*

