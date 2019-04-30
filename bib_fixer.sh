grep -iv "abstract = " library.bib > library_fixed-tmp.bib
grep -iv "file = " library_fixed-tmp.bib > library_fixed.bib
sed -i "s/title = {{\(.*\)}}/title = {\1}/" library_fixed.bib
sed -i "s/{jan}/Jan/g" library_fixed.bib
sed -i "s/{feb}/Feb/g" library_fixed.bib
sed -i "s/{mar}/Mar/g" library_fixed.bib
sed -i "s/{apr}/Apr/g" library_fixed.bib
sed -i "s/{may}/May/g" library_fixed.bib
sed -i "s/{jun}/Jun/g" library_fixed.bib
sed -i "s/{jul}/Jul/g" library_fixed.bib
sed -i "s/{aug}/Aug/g" library_fixed.bib
sed -i "s/{sep}/Sep/g" library_fixed.bib
sed -i "s/{oct}/Oct/g" library_fixed.bib
sed -i "s/{nov}/Nov/g" library_fixed.bib
sed -i "s/{dec}/Dec/g" library_fixed.bib

tail -n+6 library_fixed.bib > library_fixed-tmp.bib
bibtool -s -i library_fixed-tmp.bib -o library_fixed.bib
rm library_fixed-tmp.bib
