[slideToolKit](https://github.com/swvanderlaan/slideToolKit)<img align="right" height="200" src=images/slideToolKit_logo_print_transparent.png>
============

**slideToolKit**: _an assistive toolset for the histological quantification of whole slide images_

The demand for accurate and reproducible phenotyping of a disease trait increases with the rising number of biobanks and genome wide association studies. Detailed analysis of histology is a powerful way of phenotyping human tissues. Nonetheless, purely visual assessment of histological slides is time-consuming and liable to sampling variation and optical illusions and thereby observer variation, and external validation may be cumbersome. Therefore, computerized quantification of digitized histological slides is often preferred as a more precise and reproducible, and sometimes more sensitive approach. Relatively few free toolkits are, however, available for fully digitized microscopic slides, usually known as whole slides images.

In order to comply with this need, we developed the **slideToolKit** as a fast method to handle large quantities of low contrast whole slides images using advanced cell detecting algorithms. At the core **slideToolKit** uses [CellProfiler](http://cellprofiler.org) to analyze the whole slide images efficiently. The **slideToolKit** has been developed for modern personal computers (macOS, Ubuntu) and high-performance clusters (HPCs) and is available as an open-source project on [GitHub](https://swvanderlaan.github.io/slideToolKit/).

A typical [workflow](images/slideToolkit.workflow.png) consists of four consecutive steps. 
- In the first step (acquisition), whole slide images are collected and converted to TIFF files. 
- In the second step (preparation), files are organized. 
- The third step (tiles), creates multiple manageable tiles to count. 
- In the fourth step (analysis), tissue is analyzed and results are stored in a data set. Using this method, two consecutive measurements of 303 slides showed an intraclass correlation of 0.99 ([Vrijenhoek J.E.P. _et al._](https://www.ncbi.nlm.nih.gov/pubmed/25541691)).


<img align="center" width="400" height="314" src=images/slideToolkit.workflow.small.png>

_The slideToolKit workflow._

In conclusion, **slideToolKit** provides a free, powerful and versatile collection of tools for automated feature analysis of whole slide images to create reproducible and meaningful phenotypic datasets.


#### Instructions and usage
Detailed instructions on using **slideToolKit** can be found in the [wiki](https://github.com/swvanderlaan/slideToolKit/wiki).


#### Citations
- Nelissen B.G.L., van Herwaarden J.A., Moll F.L., van Diest P.J., and Pasterkamp G. (2014) _SlideToolkit: An Assistive Toolset for the Histological Quantification of Whole Slide Images._ **PLoS One.** 2014 Nov 5;9(11):e110289. doi: 10.1371/journal.pone.0110289. [Direct link](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0110289).
- Vrijenhoek J.E.P., Nelissen B.G.L., Velema E., Vons K., de Vries J.P.P.M., Eijkemans M.J.C., den Ruijter H.M., de Borst G.J., Moll F.L., and Pasterkamp G (2014) _High Reproducibility of Histological Characterization by Whole Virtual Slide Quantification; An Example Using Carotid Plaque Specimens._ **PLoS One**. 2014 Dec 26;9(12):e115907. doi: 10.1371/journal.pone.0115907. [Direct link](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115907).
- Mekke J.M., Sakkers T.R., Verwer M.C., van den Dungen N.A.M, Song Y., Miller C., Pasterkamp G., Mokry M., den Ruijter H.M., de Kleijn D.P.V., de Borst G.J., Haitjema S., and van der Laan S.W. _Glycophorin C in atherosclerotic plaque is associated with major adverse cardiovascular events after carotid endarterectomy_ preprint **medRxiv** 2021.07.15.21260570; doi: [https://doi.org/10.1101/2021.07.15.21260570](https://doi.org/10.1101/2021.07.15.21260570)


-----------------------------------------------
#### Licence
The MIT License (MIT): <http://opensource.org/licenses/MIT>.

Copyright (c) 2014-2021, [Bas G.L. Nelissen](https://github.com/bglnelissen) & [Sander W. van der Laan](https://github.com/swvanderlaan), UMC Utrecht, Utrecht, the Netherlands.

