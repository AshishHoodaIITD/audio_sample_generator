while read p; do grep --include=\*.$1 -rnwi $2 -e "$p"; done < search_phrases.txt > results.txt