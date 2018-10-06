touch a.css
echo /*FONTS*/ > a.css
for i in *.ttf; do
	echo '@font-face {'; > a.css
	echo "  font-family: '${i%.*}';"; > a.css
	echo "  src: url('font/${i}');"; > a.css
	printf "}\n\n"; > a.css
	
done
