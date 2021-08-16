import sys, os 
import random 
import numpy as np 
from statsmodels.stats.contingency_tables import mcnemar


def join_lists(*lists):
    return sum(lists, [])

def relscore_annotated(hyplist, reflist): 
    hypl = [] 
    for k in zip(hyplist, reflist): 
        if (k[0].lower().count(' like') ==1 and (' unlike' not in k[0].lower())  and ' like' in k[1].lower()) or (k[0].lower().count(' unlike')==1 and (' like' not in k[0].lower()) and ' unlike' in k[1].lower()) or ('like' not in k[0].lower() and 'like' not in k[1].lower()):
            hypl.append(0)   
        else:   
            hypl.append(1) 
    return hypl 



def relscore_annotated_over_files(hypFile, refFile):
    with open(hypFile, 'r') as hypF, open(refFile, 'r') as refF:
        hyplist = hypF.readlines()
        reflist = refF.readlines()
        hypl = [] 
        for k in zip(hyplist, reflist):
            if (k[0].lower().count(' like') ==1 and (' unlike' not in k[0].lower())  and ' like' in k[1].lower()) or (k[0].lower().count(' unlike')==1 and (' like' not in k[0].lower()) and ' unlike' in k[1].lower()) or ('like' not in k[0].lower() and 'like' not in k[1].lower()):
                hypl.append(0)   
            else:   
                hypl.append(1) 
        return hypl 



def mcNemar_onlist(l1, l2, pvalue=0.05):
    yesyes = yesno = noyes = nono = 0

    yesyes = sum(first == second == 0 for (first, second) in zip(l1, l2))
    yesno = sum(first == 0 and second == 1 for (first, second) in zip(l1, l2))
    noyes = sum(first == 1 and second == 0 for (first, second) in zip(l1, l2))
    nono = sum(first == second == 1 for (first, second) in zip(l1, l2))
    
    table = [[yesyes, noyes], [yesno, nono]]
    result = mcnemar(table, exact=False, correction=True)
   
    print('McNemar is performed on the table:', table)

    if result.pvalue > pvalue:
        print('McNemar CANNOT reject Null Hyp due to the McNemar significane = ', result.pvalue )
    else:
        print('McNemar REJECTS Null Hyp as the McNemar significane = ', result.pvalue )


def significance_test_rel_onlists(l1, l2, Rnumber=999, pvalue=0.05):
    al=[] 
    for z in range(Rnumber):
        l3 = [] 
        zp = list(zip(l1,l2)) 
        for i,k in enumerate(np.random.randint(2, size=len(l1))): 
            if k == 1: 
                l3.append((zp[i][0], zp[i][1])) 
            else: 
                l3.append((zp[i][1], zp[i][0])) 
        al.append(l3) 

    sumlist=[]
    for i in al: 
        s1=s2=0 
        for j in i: 
            s1+=j[0] 
            s2+=j[1] 
        sumlist.append(abs(s1-s2)) 

    act_diff = abs(sum(l1) - sum(l2))

    significance = (len([x for x in sumlist if x >= act_diff])+1)/(len(sumlist)+1)

    print('Approximated Randomziation (AR) is done on the list with mistakes: ', sum(l1), sum(l2))

    if significance < pvalue:
        print(f'AR REJECTS Null Hyp as the AR significance {significance}, which LESS than {pvalue}')
    else:
        print(f'AR CANNOT reject Null Hyp as the AR significance {significance}, which is MORE than {pvalue}')



def significance_test_rel_onlists_withMcNemar(l1, l2, Rnumber=999, pvalue=0.05):
    al=[] 
    for z in range(Rnumber):
        l3 = [] 
        zp = list(zip(l1,l2)) 
        for i,k in enumerate(np.random.randint(2, size=len(l1))): 
            if k == 1: 
                l3.append((zp[i][0], zp[i][1])) 
            else: 
                l3.append((zp[i][1], zp[i][0])) 
        al.append(l3) 

    sumlist=[]
    for i in al: 
        s1=s2=0 
        for j in i: 
            s1+=j[0] 
            s2+=j[1] 
        sumlist.append(abs(s1-s2)) 

    act_diff = abs(sum(l1) - sum(l2))

    significance = (len([x for x in sumlist if x >= act_diff])+1)/(len(sumlist)+1)

    print('Approximated Randomziation (AR) is done on the list with mistakes: ', sum(l1), sum(l2))

    if significance < pvalue:
        print(f'AR REJECTS Null Hyp as the AR significance {significance}, which LESS than {pvalue}')
    else:
        print(f'AR CANNOT reject Null Hyp as the AR significance {significance}, which is MORE than {pvalue}')

    mcNemar_onlist(l1, l2, pvalue=0.05)




    

def stratified_significance_test_rel_on_list(hypl1, hypl2, hypl3, fact_hypl1, fact_hypl2, fact_hypl3, Rnumber=999, pvalue=0.05):  
    zip_hyps      = zip(hypl1, hypl2, hypl3)  
    zip_fact_hyp  = zip(fact_hypl1, fact_hypl2, fact_hypl3)  
 
  
    al=[]   
    zp = list(zip(zip_hyps, zip_fact_hyp))  
    for z in range(Rnumber):  
        l3 = []          
        for i in range(len(hypl1)):  
            n = random.randint(0,3)  
            lst_hyp =      [zp[i][0][0], zp[i][0][1], zp[i][0][2]]  
            lst_fact_hyp = [zp[i][1][0], zp[i][1][1], zp[i][1][2]]  
            if n==0:  
                l3.append((lst_hyp, lst_fact_hyp))  
            else:  
                create_lst_hyp = []  
                create_lst_fact_hyp = []  
                for _ in range(n):  
                    em1 = lst_hyp.pop(random.randrange(len(lst_hyp)))  
                    create_lst_hyp.append(em1)  
                for _ in range(n):  
                    em2 = lst_fact_hyp.pop(random.randrange(len(lst_fact_hyp)))  
                    create_lst_fact_hyp.append(em2)  
                new_lst_hyp =  lst_hyp + create_lst_fact_hyp                          
                new_lst_fact_hyp =  lst_fact_hyp + create_lst_hyp  
                l3.append((new_lst_hyp, new_lst_fact_hyp))  
        al.append(l3)  
  
    meanSum_hyps = (sum(hypl1)+sum(hypl2)+sum(hypl3))/(3*len(hypl1))  
    meanSum_fact_hyps = (sum(fact_hypl1)+sum(fact_hypl2)+sum(fact_hypl3))/(3*len(hypl1))  
  
    sumsPsedustats = []  
    for i in al:   
        meanPerPseduostat_0=meanPerPseduostat_1=0  
        for j in i:   
            meanPerPseduostat_0+=j[0][0]+j[0][1]+j[0][2]  
            meanPerPseduostat_1+=j[1][0]+j[1][1]+j[1][2]  
        sumsPsedustats.append(abs(meanPerPseduostat_0-meanPerPseduostat_1)/(3*len(hypl1)))  
  
    mean_act_diff = abs(meanSum_hyps - meanSum_fact_hyps)  
      
    significance = (len([x for x in sumsPsedustats if x >= mean_act_diff])+1)/(len(sumsPsedustats)+1)  
  
    if significance < pvalue:  
        print(f'Approximated Stratified (AR) significance is {significance}, which LESS than {pvalue}: REJECT Null Hyp')  
    else:  
        print(f'Approximated Stratified (AR) Significance is {significance}, which is MORE than {pvalue}: CANNOT Reject Null Hyp')  
    print('Mean ACT diff = ', mean_act_diff, 'Mean Hyp = ', meanSum_hyps, 'Mean fact = ', meanSum_fact_hyps)  
    print(len([x for x in sumsPsedustats if x >= mean_act_diff])+1)  

    print(sum(hypl1), sum(hypl2), sum(hypl3)) 
    
    print(sum(fact_hypl1),sum(fact_hypl2),sum(fact_hypl3)) 


    hyp_numbers = [(hypl1, sum(hypl1)), (hypl2, sum(hypl2)), (hypl3, sum(hypl3))]
    fact_hyp_numbers = [(fact_hypl1, sum(fact_hypl1)), (fact_hypl2, sum(fact_hypl2)), (fact_hypl3, sum(fact_hypl3))]
    hyp_numbers.sort(key=lambda x:x[1])
    fact_hyp_numbers.sort(key=lambda x:x[1])
    
    worstHyp = hyp_numbers[0][0]
    BestFact = fact_hyp_numbers[2][0]
    
    
    print('AR and McNemar are performed on the files with the largest difference')
    significance_test_rel_onlists_withMcNemar(worstHyp, BestFact, Rnumber, pvalue)
    print('--------------------------------------------------------------------')
 
    midHyp = hyp_numbers[1][0]
    midFact = fact_hyp_numbers[1][0]

    print('AR and McNemar are performed on the median resulting systems')
    significance_test_rel_onlists_withMcNemar(midHyp, midFact, Rnumber, pvalue)
    print('_____________________________________________________________________')
    print('_____________________________________________________________________')


def stratified_significance_test_rel(file1, file2, file3, fact_file1, fact_file2, fact_file3, ref_file, Rnumber=999, pvalue=0.05):  
    with open(file1, 'r') as hyp1, open(file2, 'r') as hyp2, open(file3, 'r') as hyp3,  open(fact_file1, 'r') as fact_hyp1, open(fact_file2, 'r') as fact_hyp2,  open(fact_file3, 'r') as fact_hyp3, open(ref_file, 'r') as ref:  
        hyp1list = hyp1.readlines()   
        hyp2list = hyp2.readlines()   
        hyp3list = hyp3.readlines()  
        fact_hyp1list = fact_hyp1.readlines()  
        fact_hyp2list = fact_hyp2.readlines()  
        fact_hyp3list = fact_hyp3.readlines()  
        reflist = ref.readlines()  
  
    hypl1 = relscore_annotated(hyp1list, reflist)   
    hypl2 = relscore_annotated(hyp2list, reflist) 
    hypl3 = relscore_annotated(hyp3list, reflist)   
    fact_hypl1 = relscore_annotated(fact_hyp1list, reflist) 
    fact_hypl2 = relscore_annotated(fact_hyp2list, reflist)   
    fact_hypl3 = relscore_annotated(fact_hyp3list, reflist) 
 
    zip_hyps      = zip(hypl1, hypl2, hypl3)  
    zip_fact_hyp  = zip(fact_hypl1, fact_hypl2, fact_hypl3)  
 
  
    al=[]   
    zp = list(zip(zip_hyps, zip_fact_hyp))  
    for z in range(Rnumber):  
        l3 = []          
        for i in range(len(hypl1)):  
            n = random.randint(0,3)  
            lst_hyp =      [zp[i][0][0], zp[i][0][1], zp[i][0][2]]  
            lst_fact_hyp = [zp[i][1][0], zp[i][1][1], zp[i][1][2]]  
            if n==0:  
                l3.append((lst_hyp, lst_fact_hyp))  
            else:  
                create_lst_hyp = []  
                create_lst_fact_hyp = []  
                for _ in range(n):  
                    em1 = lst_hyp.pop(random.randrange(len(lst_hyp)))  
                    create_lst_hyp.append(em1)  
                for _ in range(n):  
                    em2 = lst_fact_hyp.pop(random.randrange(len(lst_fact_hyp)))  
                    create_lst_fact_hyp.append(em2)  
                new_lst_hyp =  lst_hyp + create_lst_fact_hyp                          
                new_lst_fact_hyp =  lst_fact_hyp + create_lst_hyp  
                l3.append((new_lst_hyp, new_lst_fact_hyp))  
        al.append(l3)  
  
    meanSum_hyps = (sum(hypl1)+sum(hypl2)+sum(hypl3))/(3*len(hypl1))  
    meanSum_fact_hyps = (sum(fact_hypl1)+sum(fact_hypl2)+sum(fact_hypl3))/(3*len(hypl1))  
  
    sumsPsedustats = []  
    for i in al:   
        meanPerPseduostat_0=meanPerPseduostat_1=0  
        for j in i:   
            meanPerPseduostat_0+=j[0][0]+j[0][1]+j[0][2]  
            meanPerPseduostat_1+=j[1][0]+j[1][1]+j[1][2]  
        sumsPsedustats.append(abs(meanPerPseduostat_0-meanPerPseduostat_1)/(3*len(hypl1)))  
  
    mean_act_diff = abs(meanSum_hyps - meanSum_fact_hyps)  
      
    significance = (len([x for x in sumsPsedustats if x >= mean_act_diff])+1)/(len(sumsPsedustats)+1)  
  
    if significance < pvalue:  
        print(f'Approximated Stratified AR Significance is {significance}, which LESS than {pvalue}: Reject Null Hyp')  
    else:  
        print(f'Approximated Stratified AR Significance is {significance}, which is MORE than {pvalue}: Cannot Reject Null Hyp')  
    print('Mean ACT diff = ', mean_act_diff, 'Mean Hyp = ', meanSum_hyps, 'Mean fact = ', meanSum_fact_hyps)  
    print(len([x for x in sumsPsedustats if x >= mean_act_diff])+1)  
    print(sumsPsedustats[1:3]+sumsPsedustats[20:30]) 
    print(len(hypl1)) 
    print(len(hypl2)) 
    print(len(hypl3)) 
    print(len(fact_hypl1),len(fact_hypl2),len(fact_hypl3)) 
    print(sum(hypl1)) 
    print(sum(hypl2)) 
    print(sum(hypl3)) 
    print(sum(fact_hypl1),sum(fact_hypl2),sum(fact_hypl3)) 


    hyp_numbers = [(hypl1, sum(hypl1)), (hypl2, sum(hypl2)), (hypl3, sum(hypl3))]
    fact_hyp_numbers = [(fact_hypl1, sum(fact_hypl1)), (fact_hypl2, sum(fact_hypl2)), (fact_hypl3, sum(fact_hypl3))]
    hyp_numbers.sort(key=lambda x:x[1])
    fact_hyp_numbers.sort(key=lambda x:x[1])
    
    medHyp = hyp_numbers[1][0]
    medFact = fact_hyp_numbers[1][0]
    
    significance_test_rel_onlists_withMcNemar(medHyp, medFact, Rnumber, pvalue)






def many_stratified_significance_test_rel_on_list(Rnumber=999, pvalue=0.05, **hfLists):  
    if len(hfLists.values()) %2 == 0 and len(hfLists.values()) >= 2:
        l_hfLists = list(hfLists.values())
        length = len(l_hfLists)
        middle_index = length//2
        first_half = l_hfLists[:middle_index]
        second_half = l_hfLists[middle_index:]
        
        zip_hyps      = zip(*first_half)
        zip_fact_hyp  = zip(*second_half)         

        hypl1 = first_half[0]

        al=[]   
        zp = list(zip(zip_hyps, zip_fact_hyp))  
        for z in range(Rnumber):  
            l3 = []          
            for i in range(len(hypl1)):
                lst_hyp = [h for h in zp[i][0]]
                lst_fact_hyp = [f for f in zp[i][1]]
                n = random.randint(0,len(lst_hyp))  
                if n==0:  
                    l3.append((lst_hyp, lst_fact_hyp))  
                else:  
                    create_lst_hyp = []  
                    create_lst_fact_hyp = []  
                    for _ in range(n):  
                        em1 = lst_hyp.pop(random.randrange(len(lst_hyp)))  
                        create_lst_hyp.append(em1)  
                    for _ in range(n):  
                        em2 = lst_fact_hyp.pop(random.randrange(len(lst_fact_hyp)))  
                        create_lst_fact_hyp.append(em2)  
                    new_lst_hyp =  lst_hyp + create_lst_fact_hyp                          
                    new_lst_fact_hyp =  lst_fact_hyp + create_lst_hyp  
                    l3.append((new_lst_hyp, new_lst_fact_hyp))
            al.append(l3)  


        meanSum_hyps = (sum([sum(x) for x in first_half]))/(middle_index*len(hypl1))  
        meanSum_fact_hyps = (sum([sum(x) for x in second_half]))/(middle_index*len(hypl1))  

        sumsPsedustats = []  
        for i in al:   
            meanPerPseduostat_0=meanPerPseduostat_1=0  
            for j in i:   
                meanPerPseduostat_0+=sum(j[0])
                meanPerPseduostat_1+=sum(j[1])
            sumsPsedustats.append(abs(meanPerPseduostat_0-meanPerPseduostat_1)/(middle_index*len(hypl1)))  

        mean_act_diff = abs(meanSum_hyps - meanSum_fact_hyps)  

        significance = (len([x for x in sumsPsedustats if x >= mean_act_diff])+1)/(len(sumsPsedustats)+1)  

        if significance < pvalue:  
            print(f'Approximated Stratified AR significance is {significance}, which LESS than {pvalue}: REJECT Null Hyp')  
        else:
            print(f'Approximated Stratified AR Significance is {significance}, which is MORE than {pvalue}: CANNOT Reject Null Hyp')  
        print('Mean ACT diff = ', mean_act_diff, 'Mean Hyp = ', meanSum_hyps, 'Mean fact = ', meanSum_fact_hyps)  
        print(len([x for x in sumsPsedustats if x >= mean_act_diff])+1)  

        print("RST: ", [sum(x) for x in first_half]) 

        print("FACT: ", [sum(x) for x in second_half]) 


        # hyp_numbers = [(hypl1, sum(hypl1)), (hypl2, sum(hypl2)), (hypl3, sum(hypl3))]
        # fact_hyp_numbers = [(fact_hypl1, sum(fact_hypl1)), (fact_hypl2, sum(fact_hypl2)), (fact_hypl3, sum(fact_hypl3))]
        # hyp_numbers.sort(key=lambda x:x[1])
        # fact_hyp_numbers.sort(key=lambda x:x[1])

        # worstHyp = hyp_numbers[0][0]
        # BestFact = fact_hyp_numbers[2][0]


        # print('AR and McNemar are performed on the files with the largest difference')
        # significance_test_rel_onlists_withMcNemar(worstHyp, BestFact, Rnumber, pvalue)
        # print('-----------------------------------------------------------------------------------------------------------')

        zip_hyps      = zip(*first_half)                                                                                                                     
        zip_fact_hyp  = zip(*second_half)
        A1 = list(zip_hyps)
        B1 = list(zip_fact_hyp)
        A = [sum(list(x)) for x in A1]
        B = [sum(list(x)) for x in B1]

        print('Calculating with tuple swap:')
        significance_test_rel_onlists(A, B, Rnumber, pvalue)

        # A_concat = join_lists(*first_half)
        # B_concat = join_lists(*second_half)

        # print('Calculating Concatanated:') 

        # significance_test_rel_onlists_withMcNemar(A_concat, B_concat, Rnumber, pvalue)

        
