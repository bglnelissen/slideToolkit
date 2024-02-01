# README
Author: Sander W. van der Laan | s.w.vanderlaan@gmail.com

## Log
2021-11-21: Changed version names.
2023-02-10: Fixed image types ('normalized' images instead of 'entropy' masks); fixed metadata extraction; created folder with pipelines using images based on entropy-masking created by slideEMask.

## Folders
_cp220				Contains original CellProfiler 2.2.0 pipelines._legacy_archived		Contains older versions, archived, trial/pilots, faulty of different staining pipelines.
_slideEMask_versions		Contains pipelines using images based on entropy-masking created by slideEMask


### CD3-CD56-NKT
CD3_CD56_NKT.cp413.v2.2.cppipe				> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extraction
CD3_CD56_NKT.cp413.v2.2.cpproj


### CD34CD34.DAB.cp413.v1.1.cppipe				> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extractionCD34.DAB.cp413.v1.1.cpprojCD34.DAB.cp413.v1.1.txt
CD34.LRP.cp413.v1.1.cppipe				> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extractionCD34.LRP.cp413.v1.1.cpprojCD34.LRP.cp413.v1.1.txt

CD34.LRP.cp413.v1.0.cppipe				> file name to png, exports all data, counts entropy filtered data, and normal tiles > moved to _slideEMask_versionsCD34.LRP.cp413.v1.0.cpproj				> moved to _slideEMask_versionsCD34.LRP.cp413.v1.0.txt					> moved to _slideEMask_versions

CD34.DAB.cp413.v1.0.cppipe				> file name to png, exports all data, counts entropy filtered data, and normal tiles > moved to _slideEMask_versionsCD34.DAB.cp413.v1.0.cpproj				> moved to _slideEMask_versionsCD34.DAB.cp413.v1.0.txt					> moved to _slideEMask_versions

### CD66b
CD66b.cp413.v2.1.cppipe					> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extractionCD66b.cp413.v2.1.cpproj

CD66b.cp413.v2.cppipe					> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; faulty meta-data extraction > moved to _legacy_archivedCD66b.cp413.v2.cpproj

CD66b.cp413.v1.cppipe					> file name to png, exports all data, counts entropy filtered data, and normal tiles > moved to _slideEMask_versionsCD66b.cp413.v1.cpproj					> moved to _slideEMask_versions### CD68CD68.cp413.v1.1.cppipe					> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extractionCD68.cp413.v1.1.cpprojCD68.cp413.v1.1.txt

CD68.cp413.v1.0.cppipe					> file name to png, exports all data, counts entropy filtered data, and normal tiles > moved to _slideEMask_versionsCD68.cp413.v1.0.cpproj					> moved to _slideEMask_versionsCD68.cp413.v1.0.txt					> moved to _slideEMask_versions### EVGEVG.cp413.v1.1.cppipe					> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extractionEVG.cp413.v1.1.cpprojEVG.cp413.v1.1.txt

EVG.cp413.v1.0.cppipe					> file name to png, exports all data, counts entropy filtered data, and normal tiles > moved to _slideEMask_versionsEVG.cp413.v1.0.cpproj					> moved to _slideEMask_versions
### FibrinFibrin.cp413.v1.1.cppipeFibrin.cp413.v1.1.cpprojFibrin.cp413.v1.1.txt

Fibrin.cp413.v1.0.cppipe				> file name to png, exports all data, counts entropy filtered data, and normal tiles > moved to _slideEMask_versionsFibrin.cp413.v1.0.cpproj				> moved to _slideEMask_versions

### GLYCC: Changed version name for the right GLYCC pipeline.
GLYCC.cp413.v1.1.cppipe					> exports png, export all data, analyses only normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extractionGLYCC.cp413.v1.1.cpprojGLYCC.cp413.v1.1.imageset_tested.csvGLYCC.cp413.v1.1.txt


GLYCC.cp413.imageasmask.v1.0.cppipe			> GLYCC.cp413.v1.0.cppipe exports png, export all data, analyses only normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; faulty meta-data extraction > moved to _legacy_archived
GLYCC.cp413.imageasmask.v1.0.cpproj			> GLYCC.cp413.v1.0.cpproj; faulty meta-data extraction > moved to _legacy_archived
GLYCC.cp413.imageasmask.v1.0.imageset_tested.csv	> GLYCC.cp413.v1.0.imageset_tested.csv; faulty meta-data extraction > moved to _legacy_archived
GLYCC.cp413.imageasmask.v1.0.txt			> GLYCC.cp413.v1.0.txt; faulty meta-data extraction > moved to _legacy_archived

GLYCC.cp413.v0.9.cppipe					> Does not use normalized images > moved to _legacy_archivedGLYCC.cp413.v0.9.cpproj					> moved to _legacy_archived

Note that the analyses in Mekke JM et al medRxiv 2021 were done using the above pipeline,
under the 'GLYCC.cp413.imageasmask.v1.0.cppipe' filename.


### HE: Changed version name for the right HE pipeline.
HE.cp413.v1.1.cppipe					> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extraction
HE.cp413.v1.1.cpprojHE.cp413.v1.imageset_tested.csvHE.cp413.v1.txt

HE.cp413.v1.0.cppipe					> file name to png, exports all data, only uses normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; errors in meta-data extraction > moved to _legacy_archived
HE.cp413.v1.cpproj					> errors in meta-data extraction > moved to _legacy_archived
HE.cp413.v0.9.cppipe					> file name to png, exports all data, counts entropy filtered data, and normal tiles


## SMA: Pipeline works using normalized tiles
SMA.cp413.v1.1.cppipe					> exports png, export all data, analyses only normalized tiles created by ExpressHist ('crossed tiles') & slideNormalize; correct meta-data extraction
SMA.cp413.v1.1.cpprojSMA.cp413.v1.1.imageset_tested.csvSMA.cp413.v1.1.notes.txt


### Meta-data extraction regular expression syntax
Version for slideEMask - x-y coordinates tiles
^(?P<NR>AE\d{1,4}).?(?P<T_NUMBER>(UMC|T.*?))?.(?P<STAIN>STAIN|STAIN_x\d+\_z\d+).?(?P<Date>[0-9]{4}[0-9]{2}[0-9]{2})?.(?P<X>X\d+).(?P<Y>Y\d+).*$

Version for ExpressHist - tilenumber
^(?P<NR>AE\d{1,4}).?(?P<T_NUMBER>(UMC|T*))?.(?P<STAIN>STAIN|STAIN_x\d+\_z\d+).?(?P<Date>[0-9]{4}[0-9]{2}[0-9]{2})?_(?P<TILENR>\d+).*$


