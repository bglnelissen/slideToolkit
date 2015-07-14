CellProfiler Pipeline: http://www.cellprofiler.org
Version:1
SVNRevision:11710

LoadImages:[module_num:1|svn_version:\'Unknown\'|variable_revision_number:11|show_window:False|notes:\x5B\'# Goal\x3A Measure total tissue area, DAB area and DAB positive cells\', \'# Outlines\x3A  Nuclei blue, DAB area yellow, DAB nuclei red\'\x5D]
    File type to be loaded:individual images
    File selection method:Text-Exact match
    Number of images in each group?:3
    Type the text that the excluded images have in common:.counted
    Analyze all subfolders within the selected folder?:All
    Input image file location:Default Input Folder\x7CNone
    Check image sets for missing or duplicate files?:Yes
    Group images by metadata?:No
    Exclude certain files?:Yes
    Specify metadata fields to group by:
    Select subfolders to analyze:
    Image count:1
    Text that these images have in common (case-sensitive):.tile.tissue.png
    Position of this image in each group:1
    Extract metadata from where?:File name
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
    Rescale intensities?:Yes

UnmixColors:[module_num:2|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'Split HE and DAB into separate channels\'\x5D]
    Stain count:2
    Color image:Original
    Image name:DAB
    Stain:DAB
    Red absorbance:0.363092
    Green absorbance:0.651435
    Blue absorbance:0.666181
    Image name:Hematoxylin
    Stain:Hematoxylin
    Red absorbance:0.627888
    Green absorbance:0.685713
    Blue absorbance:0.368178

ApplyThreshold:[module_num:3|svn_version:\'6746\'|variable_revision_number:5|show_window:False|notes:\x5B\'Define HE positive area\'\x5D]
    Select the input image:Hematoxylin
    Name the output image:Area_Hematoxyin
    Select the output image type:Binary (black and white)
    Set pixels below or above the threshold to zero?:Below threshold
    Subtract the threshold value from the remaining pixel intensities?:No
    Number of pixels by which to expand the thresholding around those excluded bright pixels:0.0
    Select the thresholding method:Otsu Global
    Manual threshold:0.0
    Lower and upper bounds on threshold:0.1,1.0
    Threshold correction factor:0.8
    Approximate fraction of image covered by objects?:0.01
    Select the input objects:None
    Two-class or three-class thresholding?:Two classes
    Minimize the weighted variance or the entropy?:Entropy
    Assign pixels in the middle intensity class to the foreground or the background?:Foreground
    Select the measurement to threshold with:None

ApplyThreshold:[module_num:4|svn_version:\'6746\'|variable_revision_number:5|show_window:False|notes:\x5B\'Define DAB positive area\'\x5D]
    Select the input image:DAB
    Name the output image:Area_DAB
    Select the output image type:Binary (black and white)
    Set pixels below or above the threshold to zero?:Below threshold
    Subtract the threshold value from the remaining pixel intensities?:No
    Number of pixels by which to expand the thresholding around those excluded bright pixels:0.0
    Select the thresholding method:Otsu Global
    Manual threshold:0.0
    Lower and upper bounds on threshold:0.1,1.0
    Threshold correction factor:1.3
    Approximate fraction of image covered by objects?:0.01
    Select the input objects:None
    Two-class or three-class thresholding?:Three classes
    Minimize the weighted variance or the entropy?:Weighted variance
    Assign pixels in the middle intensity class to the foreground or the background?:Foreground
    Select the measurement to threshold with:None

MeasureImageAreaOccupied:[module_num:5|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'Measure DAB and HE area\'\x5D]
    Hidden:2
    Measure the area occupied in a binary image, or in objects?:Binary Image
    Select objects to measure:None
    Retain a binary image of the object regions?:No
    Name the output binary image:Stain
    Select a binary image to measure:Area_Hematoxyin
    Measure the area occupied in a binary image, or in objects?:Binary Image
    Select objects to measure:None
    Retain a binary image of the object regions?:No
    Name the output binary image:Stain
    Select a binary image to measure:Area_DAB

IdentifyPrimaryObjects:[module_num:6|svn_version:\'Unknown\'|variable_revision_number:8|show_window:False|notes:\x5B"Identify DAB positive area\'s"\x5D]
    Select the input image:DAB
    Name the primary objects to be identified:DAB_object
    Typical diameter of objects, in pixel units (Min,Max):9,10000
    Discard objects outside the diameter range?:Yes
    Try to merge too small objects with nearby larger objects?:Yes
    Discard objects touching the border of the image?:No
    Select the thresholding method:Otsu Global
    Threshold correction factor:0
    Lower and upper bounds on threshold:0.1,1.0
    Approximate fraction of image covered by objects?:0.01
    Method to distinguish clumped objects:None
    Method to draw dividing lines between clumped objects:Shape
    Size of smoothing filter:10
    Suppress local maxima that are closer than this minimum allowed distance:7
    Speed up by using lower-resolution image to find local maxima?:Yes
    Name the outline image:object_DAB
    Fill holes in identified objects?:Yes
    Automatically calculate size of smoothing filter?:Yes
    Automatically calculate minimum allowed distance between local maxima?:Yes
    Manual threshold:0.0
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

MaskImage:[module_num:7|svn_version:\'Unknown\'|variable_revision_number:3|show_window:False|notes:\x5B\'Create a mask to identify tissue inwhich we count DAB positive objects\'\x5D]
    Select the input image:Hematoxylin
    Name the output image:DAB_object_mask
    Use objects or an image as a mask?:Objects
    Select object for mask:DAB_object
    Select image for mask:DAB
    Invert the mask?:No

IdentifyPrimaryObjects:[module_num:8|svn_version:\'Unknown\'|variable_revision_number:8|show_window:False|notes:\x5B\'Find DAB positive nuclei\'\x5D]
    Select the input image:DAB_object_mask
    Name the primary objects to be identified:nuclei_DAB_only
    Typical diameter of objects, in pixel units (Min,Max):8,40
    Discard objects outside the diameter range?:Yes
    Try to merge too small objects with nearby larger objects?:No
    Discard objects touching the border of the image?:No
    Select the thresholding method:Otsu Global
    Threshold correction factor:1
    Lower and upper bounds on threshold:0.3,1.0
    Approximate fraction of image covered by objects?:0.01
    Method to distinguish clumped objects:Shape
    Method to draw dividing lines between clumped objects:Intensity
    Size of smoothing filter:10
    Suppress local maxima that are closer than this minimum allowed distance:7
    Speed up by using lower-resolution image to find local maxima?:Yes
    Name the outline image:nuclei_DAB
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

IdentifyPrimaryObjects:[module_num:9|svn_version:\'Unknown\'|variable_revision_number:8|show_window:False|notes:\x5B\'Find HE positive nuclei\'\x5D]
    Select the input image:Hematoxylin
    Name the primary objects to be identified:nuclei_hematoxylin
    Typical diameter of objects, in pixel units (Min,Max):8,40
    Discard objects outside the diameter range?:Yes
    Try to merge too small objects with nearby larger objects?:No
    Discard objects touching the border of the image?:No
    Select the thresholding method:Otsu Global
    Threshold correction factor:1
    Lower and upper bounds on threshold:0.3,1.0
    Approximate fraction of image covered by objects?:0.01
    Method to distinguish clumped objects:Shape
    Method to draw dividing lines between clumped objects:Intensity
    Size of smoothing filter:10
    Suppress local maxima that are closer than this minimum allowed distance:7
    Speed up by using lower-resolution image to find local maxima?:Yes
    Name the outline image:nuclei_all
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

OverlayOutlines:[module_num:10|svn_version:\'Unknown\'|variable_revision_number:2|show_window:False|notes:\x5B\'Overlay outlines of identified objects\'\x5D]
    Display outlines on a blank image?:No
    Select image on which to display outlines:Original
    Name the output image:OrigOverlay
    Select outline display mode:Color
    Select method to determine brightness of outlines:Max of image
    Width of outlines:1
    Select outlines to display:object_DAB
    Select outline color:Yellow
    Select outlines to display:nuclei_all
    Select outline color:Blue
    Select outlines to display:nuclei_DAB
    Select outline color:Red

SaveImages:[module_num:11|svn_version:\'Unknown\'|variable_revision_number:7|show_window:False|notes:\x5B\'Save outlined images for validating objects\'\x5D]
    Select the type of image to save:Image
    Select the image to save:OrigOverlay
    Select the objects to save:None
    Select the module display window to save:None
    Select method for constructing file names:From image filename
    Select image name for file prefix:Original
    Enter single file name:OrigBlue
    Do you want to add a suffix to the image file name?:Yes
    Text to append to the image name:.counted
    Select file format to use:jpeg
    Output file location:Default Output Folder\x7CNone
    Image bit depth:8
    Overwrite existing files without warning?:Yes
    Select how often to save:Every cycle
    Rescale the images? :No
    Save as grayscale or color image?:Grayscale
    Select colormap:Default
    Store file and path information to the saved image?:No
    Create subfolders in the output folder?:No

ExportToDatabase:[module_num:12|svn_version:\'Unknown\'|variable_revision_number:20|show_window:False|notes:\x5B\'Export findings to database for further analysis\'\x5D]
    Database type:MySQL / CSV
    Database name:CellProfiler
    Add a prefix to table names?:No
    Table prefix:
    SQL file prefix:SQL_
    Output file location:Default Output Folder\x7CNone
    Create a CellProfiler Analyst properties file?:No
    Database host:localhost
    Username:cp
    Password:Count!
    Name the SQLite database file:DefaultDB.db
    Calculate the per-image mean values of object measurements?:Yes
    Calculate the per-image median values of object measurements?:Yes
    Calculate the per-image standard deviation values of object measurements?:Yes
    Calculate the per-well mean values of object measurements?:Yes
    Calculate the per-well median values of object measurements?:Yes
    Calculate the per-well standard deviation values of object measurements?:Yes
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
    Include information for all images, using default values?:No
    Hidden:1
    Hidden:1
    Hidden:0
    Select an image to include:None
    Use the image name for the display?:No
    Image name:Channel1
    Channel color:red
    Do you want to add group fields?:No
    Enter the name of the group:
    Enter the per-image columns which define the group, separated by commas:ImageNumber, Image_Metadata_Plate, Image_Metadata_Well
    Do you want to add filter fields?:No
    Automatically create a filter for each plate?:No
