#!/bin/awk -f
# run command: cat worldcup.txt | sed 's/\[\[\([0-9]*\)[^]]*\]\]/\1/g; s/.*fb|\([A-Za-z]*\)}}/\1/g; s/<sup><\/sup>//g; s/|bgcolor[^|]*//g; s/|align=center[^|]*//g' | grep -v '^|[-0-9]*$' | sed 's/[()]/ /g' | sed 's/,//g' | awk -f awk_worldcup.awk 
/^[A-Z]+$/ {country_code = $0; count = 1;} # matches country code
/\|[0-9]+[ ]+[0-9]+/ {
	
	for (i=2; i<=NF; i++){
		print country_code ", " $i ", " count;		
	}
	count++;
}
/\| —/ {count++}
