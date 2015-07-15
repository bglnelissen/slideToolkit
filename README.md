[slideToolkit](http://bglnelissen.github.io/slideToolkit)
============

slideToolkit: an assistive toolset for the histological quantification of whole slide images

The demand for accurate and reproducible phenotyping of a disease trait increases with the rising number of biobanks and genome wide association studies. Detailed analysis of histology is a powerful way of phenotyping human tissues. Nonetheless, purely visual assessment of histological slides is time-consuming and liable to sampling variation and optical illusions and thereby observer variation, and external validation may be cumbersome. Therefore, computerized quantification of digitized histological slides is often preferred as a more precise and reproducible, and sometimes more sensitive approach. Relatively few free toolkits are, however, available for fully digitized microscopic slides, usually known as whole slides images.

In order to comply with this need, we developed the slideToolkit as a fast method to handle large quantities of low contrast whole slides images using advanced cell detecting algorithms. The slideToolkit has been developed for modern personal computers and high-performance clusters (HPCs) and is available as an open-source project on github.com.

A workflow consists of four consecutive steps. In the first step (acquisition), whole slide images are collected and converted to TIFF files. In the second step (preparation), files are organized. The third step (tiles), creates multiple manageable tiles to count. In the fourth step (analysis), tissue is analyzed and results are stored in a data set. Using this method, two consecutive measurements of 303 slides showed an intraclass correlation of 0.99.

In conclusion, slideToolkit provides a free, powerful and versatile collection of tools for automated feature analysis of whole slide images to create reproducible and meaningful phenotypic datasets.

Citation: Nelissen BGL, van Herwaarden JA, Moll FL, van Diest PJ, Pasterkamp G (2014) <i>SlideToolkit: An Assistive Toolset for the Histological Quantification of Whole Slide Images.</i> <bold>PLoS ONE 9(11): e110289</bold>. doi:10.1371/journal.pone.0110289. 

Direct link: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110289.

The MIT License (MIT): <http://opensource.org/licenses/MIT>.

Copyright (c) 2014-2015, UMC Utrecht, Bas Nelissen

-----------------------------------------------
> Installation instructions can be found in [guides](guides).
