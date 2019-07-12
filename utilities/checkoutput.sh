find  AE* -maxdepth 0 | while read line; do
	if [ $(ls "$line"/cp_output/CD* | wc -l) -eq 7 ]; then
		echo $line
		rm "$line"/*.TIF
		completed=$((completed+1))
		echo $completed	
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
