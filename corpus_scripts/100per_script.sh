#!/bin/bash

nshot=$1


if [ -z "$nshot" ]
then
      cp train_without_few.tsv train.tsv
      totmp=100subsets_Text_and_Structure_Zshot
elif [[ "$nshot" =~ ^10UnlikeLike.* ]]
then totmp=100subsets_Text_and_Structure_10shot; cat train_without_few.tsv 10UnlikeLike.tsv > train.tsv
elif [[ "$nshot" =~ ^few.* ]]
then totmp=100subsets_Text_and_Structure_FewShot; cat train_without_few.tsv few.tsv > train.tsv
else echo "Wrong argument, I'massuming it's a zero shot case" 
      cp train_without_few.tsv train.tsv
      totmp=100subsets_Text_and_Structure_Zshot
fi



train_num=$(cat ./train.tsv | wc -l)
valid_num=$(cat ./valid.tsv | wc -l)
echo $train_num
p=100

mkdir -p $totmp

for iter in 1 2 3; do
  dest=$iter-set-$p
  mkdir -p $totmp/$dest


shuf ./train.tsv > $totmp/$dest/train.tsv
shuf ./valid.tsv > $totmp/$dest/valid.tsv

cp test.tsv 237test.mr-ar.tsv $totmp/$dest 


for i in train valid; do
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
cp $totmp/$dest/indivisible_tokens.txt $totmp/Fact_$dest/


for i in train valid test 237test.mr-ar; do
awk -F "\t" '{print $1}' $totmp/Fact_$dest/$i.tsv | tr '[:upper:]' '[:lower:] ' > $totmp/Fact_$dest/$i.mr
awk -F "\t" '{print $2}' $totmp/Fact_$dest/$i.tsv > $totmp/Fact_$dest/$i.lx
done

echo "]" > $totmp/Fact_$dest/indivisible_tokens.txt
grep -Eoi '\[[^[:space:]]+' $totmp/Fact_$dest/train.mr | sort -u >> $totmp/Fact_$dest/indivisible_tokens.txt

rm train.tsv
done
