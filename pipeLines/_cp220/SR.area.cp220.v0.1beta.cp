CellProfiler Pipeline: http://www.cellprofiler.org
Version:1
SVNRevision:11710

LoadImages:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:11|show_window:False|notes:\x5B\'# Load brightfield and polorizes SR slides\', \'(b.g.l.nelissen@umcutrecht.nl)\', \'Goal\x3A Measure collagen and total tissue area (SR_POLARIZED and SR)\', \'We define SR_POLARIZED as blue and SR as green\'\x5D]
    File type to be loaded:individual images
    File selection method:Text-Exact match
    Number of images in each group?:3
    Type the text that the excluded images have in common:TIF
    Analyze all subfolders within the selected folder?:All
    Input image file location:Default Input Folder\x7CNone
    Check image sets for missing or duplicate files?:Yes
    Group images by metadata?:No
    Exclude certain files?:No
    Specify metadata fields to group by:
    Select subfolders to analyze:
    Image count:1
    Text that these images have in common (case-sensitive):SR.scaled.png
    Position of this image in each group:1
    Extract metadata from where?:File name
    Regular expression that finds metadata in the file name:^(?P<STUDYNR>\x5B0-9a-zA-Z\x5D*).(?P<STAIN>\x5B0-9a-zA-Z\x5D*).(?P<REST>.*)
    Type the regular expression that finds metadata in the subfolder path:.*\x5B\\\\/\x5D(?P<Date>.*)\x5B\\\\/\x5D(?P<Run>.*)$
    Channel count:1
    Group the movie frames?:No
    Grouping method:Interleaved
    Number of channels per group:3
    Load the input as images or objects?:Images
    Name this loaded image:SR
    Name this loaded object:Nuclei
    Retain outlines of loaded objects?:No
    Name the outline image:NucleiOutlines
    Channel number:1
    Rescale intensities?:Yes

ColorToGray:[module_num:2|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'# SR\', \'Create Grayscale image for finding total tissue area\'\x5D]
    Select the input image:SR
    Conversion method:Combine
    Image type\x3A:RGB
    Name the output image:SR.Gray.INV
    Relative weight of the red channel:1
    Relative weight of the green channel:1
    Relative weight of the blue channel:1
    Convert red to gray?:Yes
    Name the output image:OrigRed
    Convert green to gray?:Yes
    Name the output image:OrigGreen
    Convert blue to gray?:Yes
    Name the output image:OrigBlue
    Channel count:1
    Channel number\x3A:Red\x3A 1
    Relative weight of the channel:1
    Image name\x3A:Channel1

ImageMath:[module_num:3|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'# SR\', \'Invert grayscale image for futher analysis\'\x5D]
    Operation:Invert
    Raise the power of the result by:1
    Multiply the result by:1
    Add to result:0
    Set values less than 0 equal to 0?:Yes
    Set values greater than 1 equal to 1?:Yes
    Ignore the image masks?:No
    Name the output image:SR.Gray
    Image or measurement?:Image
    Select the first image:SR.Gray.INV
    Multiply the first image by:1
    Measurement:
    Image or measurement?:Image
    Select the second image:
    Multiply the second image by:1
    Measurement:

ApplyThreshold:[module_num:4|svn_version:\'6746\'|variable_revision_number:5|show_window:False|notes:\x5B\'# SR\', \'We need to get rid of those black marker dots in the corner of the screen\', \'Therefor we want to mask these areas.\', \'A mask needs to be binary (black/white)\', "To identify the black marker dots we set a threshold to identify all black-dark area\'s"\x5D]
    Select the input image:SR.Gray
    Name the output image:SR.mask
    Select the output image type:Binary (black and white)
    Set pixels below or above the threshold to zero?:Below threshold
    Subtract the threshold value from the remaining pixel intensities?:No
    Number of pixels by which to expand the thresholding around those excluded bright pixels:0.0
    Select the thresholding method:Manual
    Manual threshold:0.8
    Lower and upper bounds on threshold:0.000000,1.000000
    Threshold correction factor:1
    Approximate fraction of image covered by objects?:0.01
    Select the input objects:None
    Two-class or three-class thresholding?:Two classes
    Minimize the weighted variance or the entropy?:Weighted variance
    Assign pixels in the middle intensity class to the foreground or the background?:Foreground
    Select the measurement to threshold with:None

Smooth:[module_num:5|svn_version:\'Unknown\'|variable_revision_number:1|show_window:False|notes:\x5B\'# SR\', \'We need to smooth the previous identified black marker dots at bit to fill small holes\'\x5D]
    Select the input image:SR.mask
    Name the output image:SR.mask
    Select smoothing method:Gaussian Filter
    Calculate artifact diameter automatically?:No
    Typical artifact diameter, in  pixels:30
    Edge intensity difference:0.1

ApplyThreshold:[module_num:6|svn_version:\'6746\'|variable_revision_number:5|show_window:False|notes:\x5B\'# SR\', \'The smoothed mask needs to become binary again.\'\x5D]
    Select the input image:SR.mask
    Name the output image:SR.mask
    Select the output image type:Binary (black and white)
    Set pixels below or above the threshold to zero?:Below threshold
    Subtract the threshold value from the remaining pixel intensities?:No
    Number of pixels by which to expand the thresholding around those excluded bright pixels:0.0
    Select the thresholding method:Manual
    Manual threshold:0.2
    Lower and upper bounds on threshold:0.000000,1.000000
    Threshold correction factor:1
    Approximate fraction of image covered by objects?:0.01
    Select the input objects:None
    Two-class or three-class thresholding?:Two classes
    Minimize the weighted variance or the entropy?:Weighted variance
    Assign pixels in the middle intensity class to the foreground or the background?:Foreground
    Select the measurement to threshold with:None

ImageMath:[module_num:7|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'# SR\', \'The mask is now created, we only need to invert it (black = white and white = black)\', \'\'\x5D]
    Operation:Invert
    Raise the power of the result by:1
    Multiply the result by:1
    Add to result:0
    Set values less than 0 equal to 0?:Yes
    Set values greater than 1 equal to 1?:Yes
    Ignore the image masks?:No
    Name the output image:SR.mask
    Image or measurement?:Image
    Select the first image:SR.mask
    Multiply the first image by:1
    Measurement:
    Image or measurement?:Image
    Select the second image:
    Multiply the second image by:1
    Measurement:

MaskImage:[module_num:8|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'# SR\', \'Here we apply the mask and use it to remove the black marker dots\'\x5D]
    Select the input image:SR.Gray
    Name the output image:SR.Gray.masked
    Use objects or an image as a mask?:Image
    Select object for mask:None
    Select image for mask:SR.mask
    Invert the mask?:No

IdentifyPrimaryObjects:[module_num:9|svn_version:\'Unknown\'|variable_revision_number:8|show_window:False|notes:\x5B\'# SR\', \'Find tissue using the grayscale image.\', \'Diameter is choosen after some testing.\', \'These settings are choosen after multiple tests\'\x5D]
    Select the input image:SR.Gray.masked
    Name the primary objects to be identified:SR.TISSUE.green
    Typical diameter of objects, in pixel units (Min,Max):10,99999999
    Discard objects outside the diameter range?:Yes
    Try to merge too small objects with nearby larger objects?:Yes
    Discard objects touching the border of the image?:No
    Select the thresholding method:Otsu Global
    Threshold correction factor:0.8
    Lower and upper bounds on threshold:0.0,1.0
    Approximate fraction of image covered by objects?:0.6
    Method to distinguish clumped objects:None
    Method to draw dividing lines between clumped objects:Intensity
    Size of smoothing filter:10
    Suppress local maxima that are closer than this minimum allowed distance:7
    Speed up by using lower-resolution image to find local maxima?:Yes
    Name the outline image:SR.TISSUE.green
    Fill holes in identified objects?:Yes
    Automatically calculate size of smoothing filter?:Yes
    Automatically calculate minimum allowed distance between local maxima?:Yes
    Manual threshold:0.05
    Select binary image:None
    Retain outlines of the identified objects?:Yes
    Automatically calculate the threshold using the Otsu method?:Yes
    Enter Laplacian of Gaussian threshold:0.5
    Two-class or three-class thresholding?:Two classes
    Minimize the weighted variance or the entropy?:Weighted variance
    Assign pixels in the middle intensity class to the foreground or the background?:Foreground
    Automatically calculate the size of objects for the Laplacian of Gaussian filter?:Yes
    Enter LoG filter diameter:5
    Handling of objects if excessive number of objects identified:Continue
    Maximum number of objects:500
    Select the measurement to threshold with:None

OverlayOutlines:[module_num:10|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'# SR\', \'Show what we defined as objects using a green outline\'\x5D]
    Display outlines on a blank image?:No
    Select image on which to display outlines:SR
    Name the output image:SR.Overlay
    Select outline display mode:Color
    Select method to determine brightness of outlines:Max of image
    Width of outlines:1
    Select outlines to display:SR.TISSUE.green
    Select outline color:Green

SaveImages:[module_num:11|svn_version:\'Unknown\'|variable_revision_number:7|show_window:False|notes:\x5B\'# SR\', \'Save a copy of SR including measurements outlines in green.\'\x5D]
    Select the type of image to save:Image
    Select the image to save:SR.Overlay
    Select the objects to save:None
    Select the module display window to save:None
    Select method for constructing file names:From image filename
    Select image name for file prefix:SR
    Enter single file name:OrigBlue
    Do you want to add a suffix to the image file name?:Yes
    Text to append to the image name:.cellprofiler
    Select file format to use:png
    Output file location:Default Output Folder sub-folder\x7Coutline
    Image bit depth:8
    Overwrite existing files without warning?:Yes
    Select how often to save:Every cycle
    Rescale the images? :No
    Save as grayscale or color image?:Grayscale
    Select colormap:gray
    Store file and path information to the saved image?:Yes
    Create subfolders in the output folder?:No

MeasureImageAreaOccupied:[module_num:12|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'# SR\', \'Measure area in pixels (green and blue)\', \'Both measurements are done using the same scaled image and can there be used to calculate a ratio.\'\x5D]
    Hidden:1
    Measure the area occupied in a binary image, or in objects?:Objects
    Select objects to measure:SR.TISSUE.green
    Retain a binary image of the object regions?:No
    Name the output binary image:Stain
    Select a binary image to measure:None

ExportToSpreadsheet:[module_num:13|svn_version:\'Unknown\'|variable_revision_number:7|show_window:False|notes:\x5B\'# SR\', "A folder \'SR\' is created in the outputfolder and contains \'Image.csv\' with your measurements", "Using \'Press to select measurements\' you can choose to export additional measurements", "Using \'Data to export\' you can choose to export addition datasets"\x5D]
    Select or enter the column delimiter:Comma (",")
    Prepend the output file name to the data file names?:Yes
    Add image metadata columns to your object data file?:No
    Limit output to a size that is allowed in Excel?:No
    Select the columns of measurements to export?:Yes
    Calculate the per-image mean values for object measurements?:No
    Calculate the per-image median values for object measurements?:No
    Calculate the per-image standard deviation values for object measurements?:No
    Output file location:Default Output Folder sub-folder\x7CSR
    Create a GenePattern GCT file?:No
    Select source of sample row name:Metadata
    Select the image to use as the identifier:None
    Select the metadata to use as the identifier:None
    Export all measurements, using default file names?:No
    Press button to select measurements to export:Image\x7CAreaOccupied_AreaOccupied_SR.TISSUE.green,Image\x7CFileName_SR,Image\x7CPathName_SR,Image\x7CMetadata_STUDYNR
    Data to export:Image
    Combine these object measurements with those of the previous object?:No
    File name:DATA.csv
    Use the object name for the file name?:Yes
