import os
import numpy as np
import pandas as pd
import glob
from functools import reduce

stainlist = ["CD68", "CD34", "EVG", "SMA", "HE", "SR", "FIBRIN", "SR_POLARIZED", "CD66b","GLYCC"]
stainlisthpc = ["CD68_2", "CD34", "EVG", "SMA", "HE", "FIBRIN", "SR_POLARIZED","SR","ndpiSR"]
pathbasebulk = "/data/isi/d/dhl/ec/VirtualSlides/AE-SLIDES/"
pathbasehpc = "/hpc/dhl_ec/VirtualSlides/"
dflistbulk = []
dflisthpc = []

for i in stainlist:
    pathlist = []
    aelist = []
    for directory, child, output in os.walk(pathbasebulk+i):
        if len(output) > 1 and "OTHER" not in directory and "RENAME" not in directory and "OKAY" not in directory:
            for file in output:
                if ".TIF" in file or ".ndpi" in file:
                    pathlist.append(directory+"/"+file)
                    aelist.append(file[file.index("AE"):file.index(".")])
        if len(output) == 1:
            if ".TIF" in output or ".ndpi" in output:
                pathlist.append(directory+"/"+output[0])
                aelist.append(output[output.index("AE"):output.index(".")])
    dflistbulk.append(pd.DataFrame({'AE':aelist,'FILEPATH_'+i:pathlist}))
bulkdf = reduce(lambda x, y: pd.merge(x,y,on='AE',how='outer'),dflistbulk)

for i in stainlisthpc:
    reslist = []
    aelist = []
    for directory,child,output in os.walk(pathbasehpc+i):
        if output:
            if "txt" in output[0] or "csv" in output[0]:
                if "cp_output" in directory and "AE" in directory:
                    reslist.append("yes")
                    aelist.append(directory[directory.index("AE"):directory.index(".")])
    dflisthpc.append(pd.DataFrame({'AE':aelist,'RESULTCHECK_'+i:reslist}))
hpcdf = reduce(lambda x, y: pd.merge(x,y,on='AE',how='outer'),dflisthpc)

full_report = pd.merge(bulkdf,hpcdf,on='AE',how='outer')
full_report.drop_duplicates(inplace=True)
full_report.to_csv(path_or_buf="assessment.csv",sep=";",index=False)
