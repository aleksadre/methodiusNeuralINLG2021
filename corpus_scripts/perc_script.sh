#!/bin/bash

nshot=$1

totmp=subsets_Text_and_Structure_$nshot
train_num=$(cat ./train_without_few.tsv | wc -l)
valid_num=$(cat ./valid.tsv | wc -l)
echo $train_num

for iter in 1 2 3 4 5; do
for p in 1 3 5 10 20 50; do
  dest=$iter-set-$p
  mkdir -p $totmp/$dest

train_perc=$(($train_num*p/100 +1))
valid_perc=$(($valid_num*p/100 +1))

shuf -n $train_perc ./train_without_few.tsv > $totmp/$dest/train_without_few.tsv
shuf -n $valid_perc ./valid.tsv > $totmp/$dest/valid.tsv

cp test.tsv 237test.mr-ar.tsv $totmp/$dest 


if [ -z "$nshot" ]
then
      cp $totmp/$dest/train_without_few.tsv $totmp/$dest/tmptrain.tsv;
else
      cat $nshot.tsv $totmp/$dest/train_without_few.tsv > $totmp/$dest/tmptrain.tsv
fi

if [ -z "$nshot" ]
then
      cp $totmp/$dest/train_without_few.tsv $totmp/$dest/tmptrain.tsv      
elif [[ "$nshot" =~ ^10UnlikeLike.* ]]
then cat $totmp/$dest/train_without_few.tsv 10UnlikeLike.tsv > $totmp/$dest/tmptrain.tsv      
elif [[ "$nshot" =~ ^few.* ]]
then  cat $totmp/$dest/train_without_few.tsv few.tsv > $totmp/$dest/tmptrain.tsv
else echo "Wrong argument, I'massuming it's a zero shot case" 
      cp $totmp/$dest/train_without_few.tsv $totmp/$dest/tmptrain.tsv      
fi



sort -u $totmp/$dest/tmptrain.tsv | shuf > $totmp/$dest/train.tsv
rm $totmp/$dest/tmptrain.tsv $totmp/$dest/train_without_few.tsv

for i in train valid 237test.mr-ar test; do 
awk -F "\t" '{print $1}' $totmp/$dest/$i.tsv | tr '[:upper:]' '[:lower:] ' > $totmp/$dest/$i.mr
awk -F "\t" '{print $2}' $totmp/$dest/$i.tsv > $totmp/$dest/$i.lx
done

echo "]" > $totmp/$dest/indivisible_tokens.txt
grep -Eoi '\[[^[:space:]]+' $totmp/$dest/train.mr | sort -u >> $totmp/$dest/indivisible_tokens.txt


mkdir $totmp/text_$dest

cat > $totmp/text_$dest/indivisible_tokens.txt <<EOF
madeupword000
madeupword001
EOF

for i in $(ls $totmp/$dest/*tsv); do name=$(basename "$i"); cp -- "$i" "$totmp/text_$dest/stru_$name"; done;

for i in $(ls $totmp/text_$dest/stru_*tsv); do name=$(basename "$i"); python textVersions.py $i $totmp/text_$dest/"${name#stru_}"; mv $i "$i"stru; sed -i '/^[[:space:]]*$/d' $totmp/text_$dest/"${name#stru_}"; done;

#for i in $(ls $totmp/text_$dest/*tsv); do bash post_clean_script.sh $i; done


for i in train valid test 237test.mr-ar; do
awk -F "\t" '{print $1}' $totmp/text_$dest/$i.tsv | tr '[:upper:]' '[:lower:] ' > $totmp/text_$dest/$i.mr
awk -F "\t" '{print $2}' $totmp/text_$dest/$i.tsv > $totmp/text_$dest/$i.lx
done


mkdir $totmp/fact_text_$dest

cp -r $totmp/text_$dest/* $totmp/fact_text_$dest
for filen in $(ls $totmp/fact_text_$dest/*mr); do sed -i 's/likewise //g' $filen;  sed -i 's/however //g' $filen; done;

python alt_fact_test_train_valid_tsvVersion.py $totmp/$dest

#created $totmp/Fact_$dest

for i in train valid test 237test.mr-ar; do
awk -F "\t" '{print $1}' $totmp/Fact_$dest/$i.tsv | tr '[:upper:]' '[:lower:] ' > $totmp/Fact_$dest/$i.mr
awk -F "\t" '{print $2}' $totmp/Fact_$dest/$i.tsv > $totmp/Fact_$dest/$i.lx
done

echo "]" > $totmp/Fact_$dest/indivisible_tokens.txt
grep -Eoi '\[[^[:space:]]+' $totmp/Fact_$dest/train.mr | sort -u >> $totmp/Fact_$dest/indivisible_tokens.txt

done 

done
