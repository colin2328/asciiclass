#!/bin/awk -f
# run command: cat synsets.txt | sed 's/[0-9]*,//'  | awk -f awk_synset.awk -F ',' | wc -l
# ans 198770
{
# $1 is before the comma (word), $2 is after the comma (def)

split($2, defs, ";");
split($1, words, " "); # words are the words to be defined

for (idx1 in words){
	for (idx2 in defs){
		print words[idx1] ", " defs[idx2]
	}	
}

}
