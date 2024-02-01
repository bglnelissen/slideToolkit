CellProfiler Pipeline: http://www.cellprofiler.org
Version:1
SVNRevision:11710

LoadImages:[module_num:1|svn_version:\'11587\'|variable_revision_number:11|show_window:False|notes:\x5B\'1. Find Tissue area (green)\', \'2. Within Tissue area (green) Identify\x3A\', \' b. DAB area (yellow)\'\x5D]
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

ColorToGray:[module_num:2|svn_version:\'10318\'|variable_revision_number:2|show_window:False|notes:\x5B\'Create gray channel, this is used to find tissue (green)\', \'Red is ussually a good channel for tissue.\', \'RGB should also be fine.\'\x5D]
    Select the input image:Original
    Conversion method:Combine
    Image type\x3A:Channels
    Name the output image:OriginalGray
    Relative weight of the red channel:1
    Relative weight of the green channel:1
    Relative weight of the blue channel:1
    Convert red to gray?:Yes
    Name the output image:OrigRed
    Convert green to gray?:No
    Name the output image:OrigGreen
    Convert blue to gray?:No
    Name the output image:OrigBlue
    Channel count:1
    Channel number\x3A:Red\x3A 1
    Relative weight of the channel:1
    Image name\x3A:Channel1

Morph:[module_num:3|svn_version:\'10300\'|variable_revision_number:2|show_window:False|notes:\x5B\'Invert created gray channel\'\x5D]
    Select the input image:OriginalGray
    Name the output image:Tissue_object
    Select the operation to perform:invert
    Number of times to repeat operation:Once
    Repetition number:2
    Scale:3

Smooth:[module_num:4|svn_version:\'10465\'|variable_revision_number:1|show_window:False|notes:\x5B\'Smooth away the dust using a Gaussion Filter. This is used to find Tissue (green)\'\x5D]
    Select the input image:Tissue_object
    Name the output image:OriginalGray_smooth
    Select smoothing method:Gaussian Filter
    Calculate artifact diameter automatically?:No
    Typical artifact diameter, in  pixels:16.0
    Edge intensity difference:0.1
