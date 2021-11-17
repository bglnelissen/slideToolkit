# cat("+++++ Collecting data from analysis +++++\n")
# cleanup
rm(list = ls())

# cat("Working directory: ")
# getwd()

# cat("\n..... loading required libraries\n")
# load the required libraries
library(data.table)
library(DT)

# cat("\n..... parsing arguments\n")
# parse arguments
args = commandArgs(trailingOnly=TRUE)
# debug
# args

# cat("\n..... reading data\n")
# read the data
df = fread(input = paste0(args[1], "_", args[2]), 
           verbose = TRUE, showProgress = TRUE)

# for debug
#df[1:10,]
# str(df)
# dim(df)

# cat("\n..... parsing data\n")
# parse the data 
# specific for a stain
# VAL = sum(df$AreaOccupied_AreaOccupied_NKT_OBJ) / sum(df$AreaOccupied_TotalArea_NKT_OBJ)
# original code
VAL = sum(df$AreaOccupied_AreaOccupied_DAB_object) / sum(df$AreaOccupied_AreaOccupied_Tissue_object)
if (is.na(VAL)) {VAL=0}
cat( VAL )

# cat("\nSession information\n")
# print(version)
# print(sessionInfo())
# cat(paste0("Library path(s) [ ", .libPaths()), "]\n")

# cat("\nCopyright (C) 1979-2021 Sander W. van der Laan | s.w.vanderlaan[at]gmail.com | https://swvanderlaan.github.io.")
