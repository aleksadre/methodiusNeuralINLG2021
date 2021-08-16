import glob, re, sys

def fewshotstruct_errors(testfilename='237test.mr-ar'):
    refilename='hyp.'+testfilename+'.txt' 

    with open(refilename, 'r') as f1:  
        contents_orig = f1.readlines()  

    with open(testfilename+'.tsv', 'r') as f2:  
        testfilename_contents_orig = f2.readlines()  
    testfilename_contents = [x.replace("relief tomb stele", "grave").replace("black_kantharos", "black kantharos") for x in testfilename_contents_orig] 

    entpl1=[]  
    for i in testfilename_contents:  
        entpl1.append([(x[2], x[3].strip()) for x in re.findall("(\[\_\_optional\_type|\[\_\_fact\_type) (\[\_\_arg1 (entity1|entityplural) \] \[__arg2 (\w+\s(\w+\s)?(\w+\s)?)\])", i)])  

    ent0=[]  
    for i in testfilename_contents:  
        ent0.append([(x[3], x[4].strip()) for x in re.findall("(\[\_\_fact\_type)?(\[\_\_optional\_type|\[\_\_fact\_type|compare_additive) (\[\_\_arg1 (entity0) \] \[__arg2 (\w+\s(\w+\s)?(\w+\s)?)\])", i)]) 

    contents = [x.replace("relief tomb stele", "grave").replace("black_kantharos", "black kantharos") for x in contents_orig] 


    errors = 0  
    rerrors = 0 
    stru_errors = 0 
    textpart=re.compile('\[text.*$')  
    for i in range(len(ent0)):  
        if len(list(dict.fromkeys(re.findall('entity\w+', testfilename_contents[i])))) > 1:  
            #print(ent0[i], "------", entpl1[i], "_________________", list(dict.fromkeys(re.findall('entity\w+', contents[i]))))      
            textref = textpart.search(contents[i]).group() 
            if textref and re.search(ent0[i][0][1].strip(), textref) and re.search(entpl1[i][0][1].strip(), textref):  
                st_ent0   = re.search(ent0[i][0][1].strip(), textref).start() 
                st_entpl1 = re.search(entpl1[i][0][1].strip(), textref).start()  
                if (st_ent0 < st_entpl1 and list(dict.fromkeys(re.findall('entity\w+', testfilename_contents[i])))[0]=="entity0") or (st_ent0 > st_entpl1 and list(dict.fromkeys(re.findall('entity\w+', testfilename_contents[i])))[0] != "entity0"):  
                    pass #print("OK")                  
                elif (st_ent0 == st_entpl1) and ent0[i][0][1] == entpl1[i][0][1]:  pass
                    # print("_______________________________________________")  
                    # print("Still OK")  
                    # print(re.findall('text.*$', contents[i]))  
                    # print("_______________________________________________")  
                else:  
                    print("//////////////////////////////////////////////////////////////")  
                    print("NAH")  
                    print(contents[i])  
                    print(re.findall('text.*$', testfilename_contents[i])) 
                    print(st_ent0, st_entpl1)   
                    print(ent0[i][0][1], entpl1[i][0][1])  
                    print("===============================================================") 
                    if (re.search(r'text\][\t\s]*(.*)$', testfilename_contents[i]).group(1).startswith('Unlike') or re.search(r'text\][\t\s]*(.*)$', testfilename_contents[i]).group(1).startswith('Like')) and not (re.search(r'text\][\t\s]*(.*)$', contents[i]).group(1).startswith('Unlike') or re.search(r'text\][\t\s]*(.*)$', contents[i]).group(1).startswith('Like')): 
                        stru_errors+=1 
                    else: 
                        errors+=1 
            else:  
                #print(ent0[i], "------", entpl1[i], "_________________", list(dict.fromkeys(re.findall('entity\w+', contents[i]))))  
                #print(textref) 
                #print("((((())))))") 
                #print(testfilename_contents[i]) 
                rerrors += 1 
        else: 
            if not re.findall(ent0[i][0][1].strip(), textref): pass 
                #print("<<<<<<<<<<<<<>>>>>>>>>>>>") 
                #print(ent0[i][0][1].strip()) 
                #print(contents[i]) 
                #print(testfilename_contents[i]) 

    return (errors, stru_errors) 

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Result of Errors on Challenge are {}".format(fewshotstruct_errors('237test.mr-ar')))
    else:
        print("Result of Errors on Standard are {}".format(fewshotstruct_errors('test')))
