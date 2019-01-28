library(data.table)
args = commandArgs(trailingOnly=TRUE)
df = fread(paste0(args[1], "_Image.txt"))
VAL = sum(df$AreaOccupied_AreaOccupied_DAB_object_yellow) / sum(df$AreaOccupied_AreaOccupied_Tissue_object_green)
if (is.na(VAL)) {VAL=0}
cat( VAL )
