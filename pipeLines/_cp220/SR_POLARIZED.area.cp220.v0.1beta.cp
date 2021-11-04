CellProfiler Pipeline: http://www.cellprofiler.org
Version:1
SVNRevision:11710

LoadImages:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:11|show_window:False|notes:\x5B\'# Load polorizes SR slides\', \'(b.g.l.nelissen@umcutrecht.nl)\', \'Goal\x3A Measure polarized collagen area (SR_POLARIZED)\', \'We define SR_POLARIZED as blue\'\x5D]
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
    Text that these images have in common (case-sensitive):SR_POLARIZED.scaled.png
    Position of this image in each group:1
    Extract metadata from where?:File name
    Regular expression that finds metadata in the file name:^(?P<STUDYNR>\x5B0-9a-zA-Z\x5D*).(?P<STAIN>\x5B0-9a-zA-Z\x5D*).(?P<REST>.*)
    Type the regular expression that finds metadata in the subfolder path:.*\x5B\\\\/\x5D(?P<Date>.*)\x5B\\\\/\x5D(?P<Run>.*)$
    Channel count:1
    Group the movie frames?:No
    Grouping method:Interleaved
    Number of channels per group:3
    Load the input as images or objects?:Images
    Name this loaded image:SR_POLARIZED
    Name this loaded object:Nuclei
    Retain outlines of loaded objects?:No
    Name the outline image:NucleiOutlines
    Channel number:1
    Rescale intensities?:Yes

RescaleIntensity:[module_num:2|svn_version:\'6746\'|variable_revision_number:2|show_window:False|notes:\x5B\'# SR_POLARIZED\', \'Rescale intensity to re-level the brightness of each image and make further analysis more uniform.\', \'\'\x5D]
    Select the input image:SR_POLARIZED
    Name the output image:Original
    Select rescaling method:Divide by the image\'s maximum
    How do you want to calculate the minimum intensity?:Custom
    How do you want to calculate the maximum intensity?:Custom
    Enter the lower limit for the intensity range for the input image:0
    Enter the upper limit for the intensity range for the input image:1
    Enter the intensity range for the input image:0.000000,1.000000
    Enter the desired intensity range for the final, rescaled image:0.000000,1.000000
    Select method for rescaling pixels below the lower limit:Mask pixels
    Enter custom value for pixels below lower limit:0
    Select method for rescaling pixels above the upper limit:Mask pixels
    Enter custom value for pixels below upper limit:0
    Select image to match in maximum intensity:None
    Enter the divisor:1
    Select the measurement to use as a divisor:None

ColorToGray:[module_num:3|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'# SR_POLARIZED\', \'Create Grayscale image for finding total tissue area\', \'\'\x5D]
    Select the input image:Original
    Conversion method:Combine
    Image type\x3A:Channels
    Name the output image:SR_POLARIZED.Gray
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
    Channel number\x3A:Green\x3A 2
    Relative weight of the channel:1
    Image name\x3A:Channel1

IdentifyPrimaryObjects:[module_num:4|svn_version:\'Unknown\'|variable_revision_number:8|show_window:True|notes:\x5B\'# SR_POLARIZED\', \'Find tissue using the grayscale image.\', \'Diameter is choosen after some testing.\', \'These settings are choosen after multiple tests\'\x5D]
    Select the input image:SR_POLARIZED.Gray
    Name the primary objects to be identified:SR_POLARIZED.TISSUE.blue
    Typical diameter of objects, in pixel units (Min,Max):10,99999999
    Discard objects outside the diameter range?:Yes
    Try to merge too small objects with nearby larger objects?:Yes
    Discard objects touching the border of the image?:No
    Select the thresholding method:Otsu Global
    Threshold correction factor:1
    Lower and upper bounds on threshold:0,1.0
    Approximate fraction of image covered by objects?:0.6
    Method to distinguish clumped objects:None
    Method to draw dividing lines between clumped objects:Intensity
    Size of smoothing filter:10
    Suppress local maxima that are closer than this minimum allowed distance:7
    Speed up by using lower-resolution image to find local maxima?:Yes
    Name the outline image:SR_POLARIZED.TISSUE.blue
    Fill holes in identified objects?:Yes
    Automatically calculate size of smoothing filter?:Yes
    Automatically calculate minimum allowed distance between local maxima?:Yes
    Manual threshold:0.20
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
    Select the measurement to threshold with:Scaling_Original

OverlayOutlines:[module_num:5|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'# SR_POLARIZED\', \'Show what we defined as objects using a blue outline\'\x5D]
    Display outlines on a blank image?:No
    Select image on which to display outlines:SR_POLARIZED
    Name the output image:SR_POLARIZED.Overlay
    Select outline display mode:Color
    Select method to determine brightness of outlines:Max of image
    Width of outlines:1
    Select outlines to display:SR_POLARIZED.TISSUE.blue
    Select outline color:Blue

SaveImages:[module_num:6|svn_version:\'Unknown\'|variable_revision_number:7|show_window:False|notes:\x5B\'# SR_POLARIZED\', \'Save a copy of SR_POLARIZED including measurements outlines in blue.\'\x5D]
    Select the type of image to save:Image
    Select the image to save:SR_POLARIZED.Overlay
    Select the objects to save:None
    Select the module display window to save:None
    Select method for constructing file names:From image filename
    Select image name for file prefix:SR_POLARIZED
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

MeasureImageAreaOccupied:[module_num:7|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'# SR_POLARIZED & SR\', \'Measure area in pixels (green and blue)\', \'Both measurements are done using the same scaled image and can there be used to calculate a ratio.\'\x5D]
    Hidden:1
    Measure the area occupied in a binary image, or in objects?:Objects
    Select objects to measure:SR_POLARIZED.TISSUE.blue
    Retain a binary image of the object regions?:No
    Name the output binary image:Stain
    Select a binary image to measure:None

ExportToSpreadsheet:[module_num:8|svn_version:\'Unknown\'|variable_revision_number:7|show_window:False|notes:\x5B\'# SR_POLARIZED\', "A folder \'SR_Polarized\' is created in the outputfolder and contains \'Image.csv\' with your measurements", "Using \'Press to select measurements\' you can choose to export additional measurements", "Using \'Data to export\' you can choose to export addition datasets"\x5D]
    Select or enter the column delimiter:Comma (",")
    Prepend the output file name to the data file names?:Yes
    Add image metadata columns to your object data file?:No
    Limit output to a size that is allowed in Excel?:No
    Select the columns of measurements to export?:Yes
    Calculate the per-image mean values for object measurements?:No
    Calculate the per-image median values for object measurements?:No
    Calculate the per-image standard deviation values for object measurements?:No
    Output file location:Default Output Folder sub-folder\x7CSR_POLARIZED
    Create a GenePattern GCT file?:No
    Select source of sample row name:Metadata
    Select the image to use as the identifier:None
    Select the metadata to use as the identifier:None
    Export all measurements, using default file names?:No
    Press button to select measurements to export:Image\x7CAreaOccupied_AreaOccupied_SR_POLARIZED.TISSUE.blue,Image\x7CFileName_SR_POLARIZED,Image\x7CPathName_SR_POLARIZED,Image\x7CMetadata_STUDYNR
    Data to export:Image
    Combine these object measurements with those of the previous object?:No
    File name:DATA.csv
    Use the object name for the file name?:Yes
