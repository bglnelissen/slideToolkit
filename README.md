[slideToolkit](https://github.com/swvanderlaan/slideToolkit)
============

**slideToolkit**: _an assistive toolset for the histological quantification of whole slide images_

The demand for accurate and reproducible phenotyping of a disease trait increases with the rising number of biobanks and genome wide association studies. Detailed analysis of histology is a powerful way of phenotyping human tissues. Nonetheless, purely visual assessment of histological slides is time-consuming and liable to sampling variation and optical illusions and thereby observer variation, and external validation may be cumbersome. Therefore, computerized quantification of digitized histological slides is often preferred as a more precise and reproducible, and sometimes more sensitive approach. Relatively few free toolkits are, however, available for fully digitized microscopic slides, usually known as whole slides images.

In order to comply with this need, we developed the **slideToolkit** as a fast method to handle large quantities of low contrast whole slides images using advanced cell detecting algorithms. At the core **slideToolkit** uses [CellProfiler](http://cellprofiler.org) to analyze the whole slide images efficiently. The **slideToolkit** has been developed for modern personal computers and high-performance clusters (HPCs) and is available as an open-source project on GitHub(https://swvanderlaan.github.io/slideToolkit/).

A typical workflow consists of four consecutive steps. 
- In the first step (acquisition), whole slide images are collected and converted to TIFF files. 
- In the second step (preparation), files are organized. 
- The third step (tiles), creates multiple manageable tiles to count. 
- In the fourth step (analysis), tissue is analyzed and results are stored in a data set. Using this method, two consecutive measurements of 303 slides showed an intraclass correlation of 0.99 ([Vrijenhoek JE _et al._](https://www.ncbi.nlm.nih.gov/pubmed/25541691)).

In conclusion, **slideToolkit** provides a free, powerful and versatile collection of tools for automated feature analysis of whole slide images to create reproducible and meaningful phenotypic datasets.

-----------------------------------------------
> Installation instructions for CentOS 6+, Ubuntu and Mac OS X Mountain Lion+ can be found in [guides](https://github.com/swvanderlaan/slideToolkit/tree/master/guides).



-----------------------------------------------
#### Citations
- Nelissen BGL, van Herwaarden JA, Moll FL, van Diest PJ, Pasterkamp G (2014) _SlideToolkit: An Assistive Toolset for the Histological Quantification of Whole Slide Images._ **PLoS One. 2014 Nov 5;9(11):e110289**. doi: 10.1371/journal.pone.0110289. Direct link: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110289.
- Vrijenhoek J.E.P., Nelissen B.G.L., Velema E., Vons K., de Vries J.P.P.M., Eijkemans M.J.C., den Ruijter H.M., de Borst G.J., Moll F.L., Pasterkamp G (2014) _High Reproducibility of Histological Characterization by Whole Virtual Slide Quantification; An Example Using Carotid Plaque Specimens._ **PLoS One. 2014 Dec 26;9(12):e115907.**. doi: 10.1371/journal.pone.0115907. Direct link: http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115907


-----------------------------------------------
#### Licence
The MIT License (MIT): <http://opensource.org/licenses/MIT>.
Copyright (c) 2014-2018, [Bas G.L. Nelissen](https://github.com/bglnelissen) & [Sander W. van der Laan](https://github.com/swvanderlaan), UMC Utrecht, Utrecht, the Netherlands.
