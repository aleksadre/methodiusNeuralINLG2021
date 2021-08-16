import sys
import os, re, string 
from collections import Counter
import numpy as np


 
def sym_diff_measure_beam_tupled(file):  
    with open(file, 'r') as rfile:   
        rfile_lines = rfile.readlines()  
        sdiff_measure = np.array([0., 0., 0., 0.]) 
        h_length = 0  
        num_groups = [] 
        for i in rfile_lines:   
            if re.search(r"H-(\d+)\t",i):  
                num = re.search(r"H-(\d+)\t",i).group(1)  
                numg = [z for z in rfile_lines if re.search(r"H-{}\t".format(str(num)), z)] 
                t = "" 
                for j in rfile_lines: 
                    if re.search(r"T-{}\t".format(str(num)), j): 
                        t+=j         
                numg.append(t)                   
                if numg not in num_groups: 
                    num_groups.append(numg) 
        for k in num_groups: 
            summa = np.array([0., 0., 0., 0.])  
            for e in k[:-1]: 
                summa = np.add(summa, np.true_divide(diff_hyp_ref_tupled(e, k[-1]), len(k[:-1]))) 
            sdiff_measure = np.add(sdiff_measure, summa) 
        print(sdiff_measure/len(num_groups)) 
        print(len(num_groups)) 
                                                                                                                                                                               

def sym_diff_measure_beam(file):  
    with open(file, 'r') as rfile:   
        rfile_lines = rfile.readlines()  
        sdiff_measure = 0  
        h_length = 0  
        num_groups = [] 
        for i in rfile_lines:   
            if re.search(r"H-(\d+)\t",i):  
                num = re.search(r"H-(\d+)\t",i).group(1)  
                numg = [z for z in rfile_lines if re.search(r"H-{}\t".format(str(num)), z)] 
                t = "" 
                for j in  rfile_lines: 
                    if re.search(r"T-{}\t".format(str(num)), j): 
                        t+=j   
                numg.append(t)                   
                if numg not in num_groups: 
                    num_groups.append(numg) 
        for k in num_groups: 
            summa = 0 
            for e in k[:-1]: 
                summa += diff_hyp_ref(e, k[-1])/len(k[:-1]) 
            sdiff_measure += summa 
        print(sdiff_measure/len(num_groups)) 
        print(len(num_groups)) 
                                                                                                                                                                               

def diff_hyp_ref_tupled(i_text, t_text):  
    t_list = []   
    i_list = []   
    t_text_lower = t_text.lower()  
    i_text_lower = i_text.lower()   
    print(t_text_lower, "\n AND \n", i_text_lower)  
    sdiff_repeat  = 0. #repeating actual material  
    sdiff_drop = 0.    #dropping actual material  
    sdiff_haluc = 0.    #halucinating   
    sdiff_inter_under = 0.  #undergenerating actual material  
    for be_token in t_text_lower.split():           
        if (be_token.startswith("begin") and be_token.endswith("end")) or re.search(r"[a-z]+\d", be_token):   
            t_list.append(be_token)              
    for ie_token in i_text_lower.split():   
        if (ie_token.startswith("begin") and ie_token.endswith("end")) or re.search(r"[a-z]+\d", ie_token):  
            i_list.append(ie_token)  
    inter = set(i_list)&set(t_list)  
    set_sym_diff = set(i_list) ^ set(t_list)    
    print("intresection is ", inter)  
    print("symmetric difference is", set_sym_diff)      
    for s in set_sym_diff:          
        if s in set(t_list):  
            sdiff_drop   += t_list.count(s)  
            print("\t dropping", s)  
        else:     
            sdiff_haluc  += i_list.count(s)  
            print("\t halucinating", s)  
    for se in inter:  
        if t_list.count(se) > i_list.count(se):  
            sdiff_inter_under += t_list.count(se) - i_list.count(se)  
            print("\t under generating:", se)  
        if t_list.count(se) < i_list.count(se):  
            sdiff_repeat += i_list.count(se) - t_list.count(se)  
            print("\t repeating:", se)              
    print(sdiff_repeat, " repeating actual material\n", sdiff_drop, '  dropping actual material\n', sdiff_haluc, "   halucinating\n", sdiff_inter_under, "    undergenerating actual material")  
    print(str(np.array([sdiff_repeat, sdiff_drop, sdiff_haluc, sdiff_inter_under])))
    print('repeat, drop, haluc, inter_under')
    return np.array([sdiff_repeat, sdiff_drop, sdiff_haluc, sdiff_inter_under]) 
                                                                                                                                                                               

def diff_hyp_ref(i_text, t_text):  
    t_list = []   
    i_list = []   
    t_text_lower = t_text.lower()  
    i_text_lower = i_text.lower()   
    print(t_text_lower, "AAANNNDDD", i_text_lower)  
    sdiff_repeat  = 0 #repeating actual material  
    sdiff_drop = 0    #dropping actual material  
    sdiff_haluc = 0    #halucinating   
    sdiff_inter_under = 0  #undergenerating actual material  
    for be_token in t_text_lower.split():           
        if (be_token.startswith("begin") and be_token.endswith("end")) or re.search(r"[a-z]+\d", be_token):   
            t_list.append(be_token)              
    for ie_token in i_text_lower.split():   
        if (ie_token.startswith("begin") and ie_token.endswith("end")) or re.search(r"[a-z]+\d", ie_token):  
            i_list.append(ie_token)  
    inter = set(i_list)&set(t_list)  
    set_sym_diff = set(i_list) ^ set(t_list)    
    print("intresection is ", inter)  
    print("symmetric difference is", set_sym_diff)      
    for s in set_sym_diff:          
        if s in set(t_list):  
            sdiff_drop   += t_list.count(s)  
            print("dropping", s)  
        else:     
            sdiff_haluc  += i_list.count(s)  
            print("halucinating", s)  
    for se in inter:  
        if t_list.count(se) > i_list.count(se):  
            sdiff_inter_under += t_list.count(se) - i_list.count(se)  
            print("under generating:", se)  
        if t_list.count(se) < i_list.count(se):  
            sdiff_repeat += i_list.count(se) - t_list.count(se)  
            print("repeating:", se)              
    print(sdiff_repeat, " repeating actual material\n", sdiff_drop, '  dropping actual material\n', sdiff_haluc, "   halucinating\n", sdiff_inter_under, "    undergenerating actual material")  
    return sdiff_repeat + sdiff_drop + sdiff_haluc + sdiff_inter_under 
                                                                         



def counter_of_relation(file_rst): 
    with open(file_rst, 'r') as rrl:  
        rrlines0 = rrl.readlines()  
        uu_found = 0 
        ll_found = 0 
        ul_found = 0 
        lu_found = 0 
        no_rel_found = 0 
        other_cases = 0 
        more_than1_like_found  = 0
        more_than1_unlike_found= 0 
        uu_list = []  
        ll_list = [] 
        ul_list = [] 
        lu_list = []  
        no_rel_list = [] 
        other_cases_list = [] 
        for i in rrlines0:  
            for j in rrlines0:  
                if re.search(r"H-\d+\t",i, re.IGNORECASE) and re.search(r"T-\d+\t",j, re.IGNORECASE): 
                    if re.search(r"H-(\d+)\t",i, re.IGNORECASE).group(1)==re.search(r"T-(\d+)\t",j, re.IGNORECASE).group(1):  
                        num = re.search(r"H-(\d+)\t",i, re.IGNORECASE).group(1)                          
                        if ' unlike' in j and i.count(' unlike')==1 and (' like' not in i): 
                            print(" >> unlike unlike")
                            uu_found +=1                                     
                            uu_list.append((i,j))
                            print(i)
                            print(j)
                            print(rrlines0[rrlines0.index(i)-2])
                            print(" << unlike unlike")
                        elif ' like' in j and i.count(' like')==1 and (' unlike' not in i) and (' however' not in i): 
                            print(" >> like like")
                            ll_found += 1 
                            ll_list.append((i,j)) 
                            print(i)
                            print(j)
                            print(rrlines0[rrlines0.index(i)-2])
                            print(" << like like")
                        elif ' unlike' in j and ' like' in i and ' unlike' not in i: 
                            print(" >> unlike like")
                            ul_found +=1 
                            ul_list.append((i,j)) 
                            print(i)
                            print(j)
                            print(rrlines0[rrlines0.index(i)-2])
                            print(" << unlike like")
                        elif ' like' in j and ' unlike' in i and ' like' not in i: 
                            print(" >> like unlike")
                            lu_found +=1  
                            lu_list.append((i,j)) 
                            print(i)
                            print(j)
                            print(rrlines0[rrlines0.index(i)-2])
                            print(" << like unlike")
                        elif ' like' in j and i.count(' like') > 1 and ' unlike' not in i:
                            print(" >> more than 1 like")
                            more_than1_like_found +=1                             
                            print(i)
                            print(j)
                            print(rrlines0[rrlines0.index(i)-2])
                            print(" << more than 1 like")
                        elif ' unlike' in j and i.count(' unlike') > 1 and ' like' not in i:
                            print(" >> more than 1 unlike")
                            more_than1_unlike_found +=1  
                            print(i)
                            print(j)
                            print(rrlines0[rrlines0.index(i)-2])
                            print(" << more than 1 unlike")
                        elif 'like' not in j and 'like' not in i: 
                            no_rel_found +=1 
                            print(i)
                            print(j)
                            print(rrlines0[rrlines0.index(i)-2])
                            print(" << norel norel")
                        else: 
                            print(">> An other case")
                            other_cases +=1 
                            other_cases_list.append((i,j))
                            print(i)
                            print(j)
                            print(rrlines0[rrlines0.index(i)-2])
                            print("<< An other case")

        print("Unlike ", uu_found) 
        print("Like ", ll_found) 
        print("Unlike VS Like ", ul_found) 
        print("Like VS Unlike ", lu_found) 
        print('More than one Like ', more_than1_like_found)
        print('More than one Unlike ', more_than1_unlike_found) 
        print("No relation in both ", no_rel_found) 
        print("The rest of cases ", other_cases) 
        print("-----------------------------------------------------------------------------------")
        print(uu_found, ll_found, ul_found, lu_found, no_rel_found, other_cases) 
        print("<><><><><><><><><><><><><><>")
        #print("Mistakes: "+str(799-uu_found-ll_found-no_rel_found))
        print("Mistakes: "+str(other_cases+more_than1_unlike_found+more_than1_like_found+lu_found+ul_found))
         




if __name__ == "__main__":
    if len(sys.argv) == 2:
        sym_diff_measure_beam_tupled(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] == 'relcount':
        counter_of_relation(sys.argv[1])    
