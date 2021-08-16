model_name=".t5_large"
currentdata_dirname=$(basename "$PWD")
data_dirname=$(echo "$currentdata_dirname" | sed -e "s/$model_name$//")
testpfx=$1

filesarr=($testpfx.mr $testpfx.lx hyp.$testpfx.txt)
filesarr2=($testpfx.lx hyp.$testpfx.txt)


for file in ${filesarr[@]}; do cp $file cpied_$file; done


for file in ${filesarr2[@]}; do while IFS= read -r line; do zzi=$(echo "$line" | cut -f 1 -d ' '); yyi=$(echo "$line" | cut -f 1 -d ' ' --complement); sed -i "s/$yyi/$zzi/g" cpied_$file; tr '[:upper:]' '[:lower:]'< cpied_$file > l_cpied_$file; done < substnewwords.txt; done

tr '[:upper:]' '[:lower:]'< substnewwords.txt > l_substnewwords.txt


while IFS= read -r line; do zzi=$(echo "$line" | cut -f 1 -d ' '); yyi=$(echo "$line" | cut -f 1 -d ' ' --complement); sed -i "s/$yyi/$zzi/g" cpied_$testpfx.mr; done < l_substnewwords.txt


awk '{print "T-"NR-1,$0}' OFS='\t' l_cpied_$testpfx.lx > int_$testpfx.lx

awk '{print "S-"NR-1,$0}' OFS='\t' cpied_$testpfx.mr > int_$testpfx.mr

awk '{print "H-"NR-1,$0}' OFS='\t' l_cpied_hyp.$testpfx.txt > int_hyp.$testpfx.txt

for ifile in int_$testpfx.lx int_hyp.$testpfx.txt; do sed -i "s/\([\.\,\;]\)/ \1/g" $ifile; done

paste -d '\n' int_$testpfx.mr int_$testpfx.lx int_hyp.$testpfx.txt > deinfl_gen.t5hugface.$testpfx.txt

rm int_$testpfx.lx int_$testpfx.mr int_hyp.$testpfx.txt l_cpied_$testpfx.lx l_cpied_hyp.$testpfx.txt cpied_$testpfx.mr cpied_$testpfx.lx cpied_hyp.$testpfx.txt
