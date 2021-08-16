import sys
sys.path.append('../')
from stratAR import *
 
r20_1=relscore_annotated_over_files('1hyp.test.txt', 'test.lx')           
r20_2=relscore_annotated_over_files('2hyp.test.txt', 'test.lx')           
r20_3=relscore_annotated_over_files('3hyp.test.txt', 'test.lx')
r20_4=relscore_annotated_over_files('4hyp.test.txt', 'test.lx')     
r20_5=relscore_annotated_over_files('5hyp.test.txt', 'test.lx')
    
F20_1=relscore_annotated_over_files('F1hyp.test.txt', 'test.lx')            
F20_2=relscore_annotated_over_files('F2hyp.test.txt', 'test.lx')          
F20_3=relscore_annotated_over_files('F3hyp.test.txt', 'test.lx')
F20_4=relscore_annotated_over_files('F4hyp.test.txt', 'test.lx')     
F20_5=relscore_annotated_over_files('F5hyp.test.txt', 'test.lx')          
    

many_stratified_significance_test_rel_on_list(999, h1=r20_1, h2=r20_2, h3=r20_3, h4=r20_4, h5=r20_5, f1=F20_1, f2=F20_2, f3=F20_3, f4=F20_4, f5=F20_5)


