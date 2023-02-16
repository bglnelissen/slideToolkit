# ORIGINAL CODE
# find  AE* -maxdepth 0 | while read line; do
# 	if [ $(ls "$line"/cp_output/CD* | wc -l) -eq 7 ]; then
# 		echo $line
# 		rm "$line"/*.TIF
# 		completed=$((completed+1))
# 		echo $completed	
# 	else
# 		rm -v -rf "$line"/cp_output
# 		rm -v -rf "$line"/*tiles*
# 		rm -v "$line"/*.png
# 		rm -v "$line"/result.txt
# 		rm -v "$line"/processanda.txt
# 		rm -v -rf "$line"/magick*
# 	fi
# done
# 
# echo "total plaques"
# find AE* -maxdepth 0 | wc -l


# UPDATED code

find  AE* -maxdepth 0 | while read line; do
	if find "$line"/cp_output/cp_output -mindepth 1 | read; then
		echo $line
		ls "$line"/cp_output/cp_output
		rm "$line"/*.tif
	else
		rm -v -rf "$line"/cp_output
		rm -v -rf "$line"/*tiles*
		rm -v "$line"/*.png
		rm -v "$line"/result.txt
		rm -v "$line"/processanda.txt
		rm -v -rf "$line"/magick*
	fi
done
echo "total plaques"
find AE* -maxdepth 0 | wc -l
echo completed plaques
ls AE*/cp_output/cp_output/Output_Image.csv | wc -l


