import sys
import re
import glob

def rewrite(inp,out):
    outpt = open(out,'w')
    txt = open(inp,'r').read()
    lines = txt.split('\n')
    #pre = (set(re.findall('fact_.*?(?= )',txt)))
    sublist = ['\[', '\]','_','entity0','entity1','entityplural','arg1','arg2','fact','optional','type','(?<!\w) ',' (?!\w)']
    for lin in lines:
        #print('OG line:',lin)
        new = lin
        new = re.sub('compare_additive ','',new)
        fct = re.findall('fact_.*?\](?= \])|option.*?\](?= \])',new)
        entity0type = re.search('(?:(optional)|(fact))_type \[__arg1 entity0.*?\] \]',new)
        entity1type = re.search('(?:(optional)|(fact))_type \[__arg1 entity0.*?\] \]',new)
        entitypluraltype = re.search('(?:(optional)|(fact))_type \[__arg1 entityplural.*?\] \]',new)
        if entity0type:
            entity0type = entity0type[0]
            for sub in sublist:
                entity0type = re.sub(sub,'',entity0type)
        if entity1type:
            entity1type = entity1type[0]
            for sub in sublist:
                entity1type = re.sub(sub,'',entity1type)
        if entitypluraltype:
            entitypluraltype = entitypluraltype[0]
            for sub in sublist:
                entitypluraltype = re.sub(sub,'',entitypluraltype)
        for f in fct:
            #print('fct:',f)
            #print('new:',new)
            one = re.search('(?<=g1 ).*?(?= ])',f)[0]
            if one == 'entity0':
                one = f'This {entity0type}'
            if one == 'entity1':
                one = f'The previously seen {entity1type}'
            if one == 'entityplural':
                #one = f'The previously seen {entitypluraltype}'
                one = f"Each of the {entitypluraltype} you've previously seen"
            else:
                one = one
            two = re.search('(?<=g2 ).*?(?= ])',f)[0]
            p = re.search('fact_.*?(?= )|option.*?(?= )',f)[0]
            out = ''
            if re.search('option',p):
                out = out
                #if re.search('entity0',f):
                #    out = f'This is a(n) {two}.'
                #else:
                #    out =f'The previous exhibit is a(n) {two}.'
            if p == 'fact_helmet_type':
                out = f'{one} belongs to {two}.'
            if p == 'fact_type':
                out = f'{one} is a {two}.'
            if p == 'fact_original_location':
                out = f'{one} originates in {two}.'
            if p == 'fact_exhibit_characteristics':
                out = f'{one} {two}.'
            if p == 'fact_creation_time':
                out = f'{one} was created {two}.'
            if p == 'fact_made_of':
                out = f'{one} is made of {two}.'
            if p == 'fact_sculpted_by':
                out = f'{one} was sculpted by {two}.'
            if p == 'fact_person_story':
                out = f'{one} {two}.'
            if p == 'fact_exhibit_story':
                out = f'{two[0].upper()+two[1:]}.'
            if p == 'fact_city':
                out = f'{one} is in {two}.'
            if p == 'fact_copy_info':
                out = f'{one} is a {two}.'
            if p == 'fact_historical_period_time':
                out = f'The {str(one)[0].upper()+str(one)[1:]} was between {two}.'
            if p == 'fact_inscription_says':
                out = f'The inscription on {one[0].lower()+one[1:]} states {two}.'
            if p == 'fact_exhibit_purpose':
                out = f'{one} {two}.'
            if p == 'fact_exhibit_height':
                out = f'{one} is {two} high.'
            if p == 'fact_helmet_type':
                out = f'{one} is constructed in {two}.'
            if p == 'fact_exhibit_portrays':
                out = f'{one} portrays {two}.'
            if p == 'fact_painting_style':
                out = f'{one} is painted in {two}.'
            if p == 'fact_painted_by':
                out = f'{one} is painted by {two}.'
            if p == 'fact_person_information':
                out = f'{one[0].upper()+one[1:]} {two}.'
            if p == 'fact_location_found':
                out = f'{one} was found in {two}.'
            if p == 'fact_potter_is':
                out =f'{two[0].upper()+two[1:]} constructed {one[0].lower()+one[1:]}.'
            if p == 'fact_exhibit_form':
                out = re.sub(out,f'{one} {two}.',out)
            if p == 'fact_opposite_technique':
                out = f'{one} is the opposite of {two}.'
            if p == 'fact_island':
                out = f'{one[0].upper()+one[1:]} is on {two}.'
            if p == 'fact_region':
                out = f'{one} is in {two}.'
            if p == 'fact_creation_period':
                out = f'{one} was created in the {two}.'
            if p == 'fact_current_location':
                out = f'{one} is currently located in {two}.'
            if p == 'fact_style_description':
                out = f'{one[0].upper()+one[1:]} {two}.'
            if p == 'fact_technique_description':
                out = f'{one[0].upper()+one[1:]} {two}.'
            if p == 'fact_location_information':
                out = f'{one[0].upper()+one[1:]} {two}.'
            if p == 'fact_other_work':
                out = f'{two[0].upper()+re.sub("his",one[0].lower()+one[1:],two[1:])}.'
            if p == 'fact_historical_period_description':
                out = f'{one} {two}.'
            if p == 'fact_exhibit_depicts':
                out = f'{one} depicts {two}.'
            if p == 'fact_exhibit_style':
                out = f'{one} is in {two}.'
            if p == 'fact_painting_technique_used':
                out = f'{one} is painted with the {two}.'
            #print(out)
            new = re.sub(re.escape(f),out,new)
        new = re.sub('__(?!(rst|content))',' ',new)
        new = re.sub('b\.c\.','B.C.',new)
        content = re.findall('((\[__content.*? )(.*\])( \]))', new)
        for con in content:
            #for c in con:
            #    print("content:", c)
            new = re.sub(re.escape(con[0]), con[2], new)
        simplerst = re.findall('((\[__rst_joint.*? ).*?]( ])+)',new)
        for r in simplerst:
            rprime = re.sub(re.escape(r[1]),'',r[0])
            rprime = re.sub('\. \] \]','. ]', rprime)
            new = re.sub(re.escape(r[0]),rprime,new)
        #print(new)
        othersimplerst = re.findall('((\[__rst_el.*? ).*?]( ])+)',new)
        for r in othersimplerst:
            rprime = re.sub(re.escape(r[1]),'',r[0])
            rprime = re.sub('\. \] \]','. ]', rprime)
            new = re.sub(re.escape(r[0]),rprime,new)
        #print(new)
        rst = re.findall('((\[__rst_con.*? ).*?(\[.*?\])\s?(\[.*?\])?\s?(\[.*?\])?\s?(\[.*?\] \]))',new)
        for r in rst:
            if 'con' in r[0]:
                #print("found con:",r)
                #print("lenght of con is:",len(r))
                #for x,y in enumerate(r):
                #    print(f"{y}:",x)
                rprime = re.sub(re.escape(r[2]), f'{r[2]} However', r[0])
                rprime = re.sub(re.escape(r[1]),'',rprime)
                rprime = re.sub('\. \] \]','. ]',rprime)
                new = re.sub(re.escape(r[0]),rprime,new)
        otherrst = re.findall('((\[__rst_sim.*? ).*?(\[.*?\])\s?(\[.*?\])?\s?(\[.*?\])?\s?(\[.*?\] \]))',new)
        #print(new)
        for r in otherrst:
            if 'sim' in r[0]:
                print("found sim:",r)
                print("length of sim is:",len(r))
                for x,y in enumerate(r):
                    print(f"{y}:",x)
                if '\] \]' in r[3]:
                    rprime = re.sub(re.escape(r[3]),f'Likewise {r[3]}',r[0])
                elif r[4] != '':
                   rprime = re.sub(re.escape(r[4]),f'Likewise {r[4]}',r[0])
                elif r[5] != '':
                    rprime = re.sub(re.escape(r[5]), f'Likewise {r[5]}',r[0])
                rprime = re.sub(re.escape(r[1]),'',rprime)
                rprime = re.sub('\. \] \]','. ]',rprime)
                new = re.sub(re.escape(r[0]),rprime,new)
        new = re.sub(' \]|\[ | (?= )','',new)
        new = re.sub('(?<=However)|(?<=Likewise) The',' the',new)
        new = re.sub(re.escape(' [text]'),'\t[text]',new)
        new = re.sub('black_*kantharos','black kantharos',new,re.IGNORECASE)
        new = re.sub('grave','relief tomb stele',new,re.IGNORECASE)
        new = re.sub('the The','The',new,re.IGNORECASE)
        new = re.sub('the This','This',new,re.IGNORECASE)
        new = re.sub('\.\.','.',new)
        print('new:',new,'\n')
        outpt.write(new+'\n')
#rewrite('train.tsv','nostructure.tsv')

'''remove ending sentences (concerning type). Substitute the type for every reference to the exhibits. For non-topic exhibits the x you recently viewed.'''

'''For entity pl write The previously seen entity plural is plural or Each entity plural you recently saw.'''
'''Grave substited by relief tomb stele.'''

if __name__ == "__main__":
    rewrite(str(sys.argv[1]), str(sys.argv[2]))
