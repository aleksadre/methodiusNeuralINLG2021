for i in test 237test.mr-ar; do bash new_genSTH.sh $i; done

for i in deinfl_gen.t5hugface.test.txt deinfl_gen.t5hugface.237test.mr-ar.txt; do python nmRelCountRoh_measure.py $i > RHO_$i; python nmRelCountRoh_measure.py $i relcount > numRelCount_$i; done
