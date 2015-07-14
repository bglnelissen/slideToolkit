CellProfiler Pipeline: http://www.cellprofiler.org
Version:1
SVNRevision:11710

LoadImages:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:11|show_window:False|notes:\x5B\'# Pipeline created for HPC (b.g.l.nelissen@umcutrecht.nl)\', \'# Goal\x3A Measure total tissue area, DAB area and DAB positive cells\', \'# Outlines\x3A Tissue blue, DAB nuclei green\'\x5D]
    File type to be loaded:individual images
    File selection method:Text-Exact match
    Number of images in each group?:3
    Type the text that the excluded images have in common:.overlay
    Analyze all subfolders within the selected folder?:All
    Input image file location:Default Input Folder\x7CNone
    Check image sets for missing or duplicate files?:Yes
    Group images by metadata?:No
    Exclude certain files?:Yes
    Specify metadata fields to group by:
    Select subfolders to analyze:
    Image count:1
    Text that these images have in common (case-sensitive):.png
    Position of this image in each group:1
    Extract metadata from where?:None
    Regular expression that finds metadata in the file name:^(?P<NR>\x5B^.\x5D*)\\.(?P<STAIN>\x5B^.\x5D*).*\\.X(?P<X>\x5B0-9\x5D{1,4}).*\\.Y(?P<Y>\x5B0-9\x5D{1,4})
    Type the regular expression that finds metadata in the subfolder path:.*\x5B\\\\/\x5D(?P<Date>.*)\x5B\\\\/\x5D(?P<Run>.*)$
    Channel count:1
    Group the movie frames?:No
    Grouping method:Interleaved
    Number of channels per group:3
    Load the input as images or objects?:Images
    Name this loaded image:Original
    Name this loaded object:Nuclei
    Retain outlines of loaded objects?:No
    Name the outline image:NucleiOutlines
    Channel number:1
    Rescale intensities?:No

ColorToGray:[module_num:2|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'Create Grayscale image for finding total tissue area\'\x5D]
    Select the input image:Original
    Conversion method:Combine
    Image type\x3A:RGB
    Name the output image:OrigGray
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

Smooth:[module_num:3|svn_version:\'Unknown\'|variable_revision_number:1|show_window:False|notes:\x5B\'Smooth grayscale image to remove dust and small open holes\'\x5D]
    Select the input image:OrigGray
    Name the output image:OrigGraySmooth
    Select smoothing method:Gaussian Filter
    Calculate artifact diameter automatically?:No
    Typical artifact diameter, in  pixels:20
    Edge intensity difference:0.1

ImageMath:[module_num:4|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'Invert grayscale image for futher analysis\'\x5D]
    Operation:Invert
    Raise the power of the result by:1
    Multiply the result by:1
    Add to result:0
    Set values less than 0 equal to 0?:Yes
    Set values greater than 1 equal to 1?:Yes
    Ignore the image masks?:No
    Name the output image:Inverted
    Image or measurement?:Image
    Select the first image:OrigGraySmooth
    Multiply the first image by:1
    Measurement:
    Image or measurement?:Image
    Select the second image:
    Multiply the second image by:1
    Measurement:

IdentifyPrimaryObjects:[module_num:5|svn_version:\'Unknown\'|variable_revision_number:8|show_window:False|notes:\x5B\'Find tissue using the grayscale image.\', \'White is background, non-white is foreground.\', \'Diameter is choosen after some testing.\', "Using theshold method is based on trial and error, MoG Global does a good job of removing dark shaded area\'s in contrast to Threshold.", \'From now on, outlined foreground is called Tissue\'\x5D]
    Select the input image:Inverted
    Name the primary objects to be identified:Tissue
    Typical diameter of objects, in pixel units (Min,Max):40,99999999
    Discard objects outside the diameter range?:Yes
    Try to merge too small objects with nearby larger objects?:No
    Discard objects touching the border of the image?:No
    Select the thresholding method:MoG Global
    Threshold correction factor:0.3
    Lower and upper bounds on threshold:0.06,1.0
    Approximate fraction of image covered by objects?:0.6
    Method to distinguish clumped objects:None
    Method to draw dividing lines between clumped objects:Intensity
    Size of smoothing filter:10
    Suppress local maxima that are closer than this minimum allowed distance:7
    Speed up by using lower-resolution image to find local maxima?:Yes
    Name the outline image:Tissue
    Fill holes in identified objects?:Yes
    Automatically calculate size of smoothing filter?:Yes
    Automatically calculate minimum allowed distance between local maxima?:Yes
    Manual threshold:0.05
    Select binary image:None
    Retain outlines of the identified objects?:Yes
    Automatically calculate the threshold using the Otsu method?:Yes
    Enter Laplacian of Gaussian threshold:0.5
    Two-class or three-class thresholding?:Three classes
    Minimize the weighted variance or the entropy?:Weighted variance
    Assign pixels in the middle intensity class to the foreground or the background?:Foreground
    Automatically calculate the size of objects for the Laplacian of Gaussian filter?:Yes
    Enter LoG filter diameter:5
    Handling of objects if excessive number of objects identified:Continue
    Maximum number of objects:500
    Select the measurement to threshold with:None

MeasureImageAreaOccupied:[module_num:6|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'Measure Tissue areas\'\x5D]
    Hidden:1
    Measure the area occupied in a binary image, or in objects?:Objects
    Select objects to measure:Tissue
    Retain a binary image of the object regions?:No
    Name the output binary image:Stain
    Select a binary image to measure:Tissue

UnmixColors:[module_num:7|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'Unmix the colors, and extract DAB\', \'Create one grayscale DAB channel\'\x5D]
    Stain count:1
    Color image:Original
    Image name:DAB
    Stain:DAB
    Red absorbance:0.363092
    Green absorbance:0.651435
    Blue absorbance:0.666181

MaskImage:[module_num:8|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'Use selected Tissue object to create a mask\', "Only analyse what\'s in the \'Tissue\' area"\x5D]
    Select the input image:DAB
    Name the output image:DAB_masked
    Use objects or an image as a mask?:Objects
    Select object for mask:Tissue
    Select image for mask:Tissue
    Invert the mask?:No

IdentifyPrimaryObjects:[module_num:9|svn_version:\'Unknown\'|variable_revision_number:8|show_window:False|notes:\x5B\'What works for CD3 in AAA tissue is\x3A\', \'Otsu Global\', \'Three classes\', \'Entropy\', \'Foreground\', \'Threshold 1.5\', \'Lower 0.7 Upper 1.0\', \'Shape / Shape\'\x5D]
    Select the input image:DAB_masked
    Name the primary objects to be identified:DAB_Nuclei
    Typical diameter of objects, in pixel units (Min,Max):8,26
    Discard objects outside the diameter range?:Yes
    Try to merge too small objects with nearby larger objects?:No
    Discard objects touching the border of the image?:No
    Select the thresholding method:Otsu Global
    Threshold correction factor:1.5
    Lower and upper bounds on threshold:0.7,1.0
    Approximate fraction of image covered by objects?:0.01
    Method to distinguish clumped objects:Shape
    Method to draw dividing lines between clumped objects:Shape
    Size of smoothing filter:10
    Suppress local maxima that are closer than this minimum allowed distance:7
    Speed up by using lower-resolution image to find local maxima?:No
    Name the outline image:DAB_Nuclei_outline
    Fill holes in identified objects?:Yes
    Automatically calculate size of smoothing filter?:Yes
    Automatically calculate minimum allowed distance between local maxima?:Yes
    Manual threshold:0.0
    Select binary image:None
    Retain outlines of the identified objects?:Yes
    Automatically calculate the threshold using the Otsu method?:Yes
    Enter Laplacian of Gaussian threshold:0.5
    Two-class or three-class thresholding?:Three classes
    Minimize the weighted variance or the entropy?:Entropy
    Assign pixels in the middle intensity class to the foreground or the background?:Foreground
    Automatically calculate the size of objects for the Laplacian of Gaussian filter?:Yes
    Enter LoG filter diameter:5
    Handling of objects if excessive number of objects identified:Continue
    Maximum number of objects:500
    Select the measurement to threshold with:None

MeasureImageAreaOccupied:[module_num:10|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'Measure all DAB areas (within Tissue)\'\x5D]
    Hidden:1
    Measure the area occupied in a binary image, or in objects?:Objects
    Select objects to measure:DAB_Nuclei
    Retain a binary image of the object regions?:No
    Name the output binary image:Stain
    Select a binary image to measure:Tissue

OverlayOutlines:[module_num:11|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'Create outlines for visualisation.\', \'The Tissue outline has a thick blue like\'\x5D]
    Display outlines on a blank image?:No
    Select image on which to display outlines:Original
    Name the output image:Orig_Overlay
    Select outline display mode:Color
    Select method to determine brightness of outlines:Max of image
    Width of outlines:4
    Select outlines to display:Tissue
    Select outline color:Blue

OverlayOutlines:[module_num:12|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'Create outlines for visualisation.\', \'The DAB outline is a thin line\'\x5D]
    Display outlines on a blank image?:No
    Select image on which to display outlines:Orig_Overlay
    Name the output image:Orig_Overlay
    Select outline display mode:Color
    Select method to determine brightness of outlines:Max of image
    Width of outlines:1
    Select outlines to display:DAB_Nuclei_outline
    Select outline color:Green

SaveImages:[module_num:13|svn_version:\'Unknown\'|variable_revision_number:7|show_window:False|notes:\x5B\x5D]
    Select the type of image to save:Image
    Select the image to save:Orig_Overlay
    Select the objects to save:None
    Select the module display window to save:None
    Select method for constructing file names:From image filename
    Select image name for file prefix:Original
    Enter single file name:OrigBlue
    Do you want to add a suffix to the image file name?:Yes
    Text to append to the image name:.outlines
    Select file format to use:jpg
    Output file location:Default Output Folder\x7CNone
    Image bit depth:8
    Overwrite existing files without warning?:Yes
    Select how often to save:Every cycle
    Rescale the images? :No
    Save as grayscale or color image?:Grayscale
    Select colormap:gray
    Store file and path information to the saved image?:No
    Create subfolders in the output folder?:No

ExportToDatabase:[module_num:14|svn_version:\'Unknown\'|variable_revision_number:20|show_window:False|notes:\x5B\x5D]
    Database type:MySQL / CSV
    Database name:DefaultDB
    Add a prefix to table names?:No
    Table prefix:Expt_
    SQL file prefix:SQL_
    Output file location:Default Output Folder\x7CNone
    Create a CellProfiler Analyst properties file?:Yes
    Database host:
    Username:
    Password:
    Name the SQLite database file:DefaultDB.db
    Calculate the per-image mean values of object measurements?:No
    Calculate the per-image median values of object measurements?:No
    Calculate the per-image standard deviation values of object measurements?:No
    Calculate the per-well mean values of object measurements?:No
    Calculate the per-well median values of object measurements?:No
    Calculate the per-well standard deviation values of object measurements?:No
    Export measurements for all objects to the database?:All
    Select the objects:
    Maximum # of characters in a column name:64
    Create one table per object or a single object table?:Single object table
    Enter an image url prepend if you plan to access your files via http:
    Write image thumbnails directly to the database?:No
    Select the images you want to save thumbnails of:
    Auto-scale thumbnail pixel intensities?:Yes
    Select the plate type:None
    Select the plate metadata:None
    Select the well metadata:None
    Include information for all images, using default values?:Yes
    Hidden:1
    Hidden:1
    Hidden:0
    Select an image to include:None
    Use the image name for the display?:Yes
    Image name:Channel1
    Channel color:red
    Do you want to add group fields?:No
    Enter the name of the group:
    Enter the per-image columns which define the group, separated by commas:ImageNumber, Image_Metadata_Plate, Image_Metadata_Well
    Do you want to add filter fields?:No
    Automatically create a filter for each plate?:No

ExportToSpreadsheet:[module_num:15|svn_version:\'Unknown\'|variable_revision_number:7|show_window:False|notes:\x5B\x5D]
    Select or enter the column delimiter:Comma (",")
    Prepend the output file name to the data file names?:Yes
    Add image metadata columns to your object data file?:No
    Limit output to a size that is allowed in Excel?:No
    Select the columns of measurements to export?:No
    Calculate the per-image mean values for object measurements?:No
    Calculate the per-image median values for object measurements?:No
    Calculate the per-image standard deviation values for object measurements?:No
    Output file location:Default Output Folder\x7CNone
    Create a GenePattern GCT file?:No
    Select source of sample row name:Metadata
    Select the image to use as the identifier:None
    Select the metadata to use as the identifier:None
    Export all measurements, using default file names?:Yes
    Press button to select measurements to export:
    Data to export:Do not use
    Combine these object measurements with those of the previous object?:No
    File name:DATA.csv
    Use the object name for the file name?:Yes
