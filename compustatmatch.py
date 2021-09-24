#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
read stata file: 
!!!!!!!!!!!!!!!will need to change the path of the file to its location in your computer
then run it
then "to_csv" this function can transfer stata files into  csv files in yout computer

'''
import pandas as pd
# convert stata to csv
data = pd.io.stata.read_stata('/Users/abcdefg/Downloads/Ben Osswald - Patent Data-selected/assigneetomatch_cleaned.dta')
data.to_csv('assigneetomatch_cleaned_new.csv')


data1 = pd.io.stata.read_stata('/Users/abcdefg/Downloads/Ben Osswald - Patent Data-selected/Compustat_for_name_match.dta')
data1.to_csv('Compustat_new.csv')


# In[ ]:


'''
read csv files you get from above to dataframe:
!!!!!!!!!!!!!!!change the path of file
then run it
'''

# read file
import pandas as pd
compustat = pd.read_csv('/Users/abcdefg/Downloads/Compustat_new.csv')
assignee = pd.read_csv('/Users/abcdefg/Downloads/assigneetomatch_cleaned_new.csv')


# In[ ]:


''' 
just run it and do not need to change anything
'''
# convert companyname and conml to uppercase
compustat["conml"] = compustat["conml"].str.upper()
#compustat["companyname"] = compustat["companyname"].str.upper()
assignee["companyname"] = assignee["companyname"].str.upper()
# remove ,  " in assignee file
assignee["companyname"] = assignee["companyname"].str.replace('"', '')
assignee["companyname"] = assignee["companyname"].str.replace(",","")
#assignee["companyname"] = assignee["companyname"].str.replace(".", "")
compustat["conml"] = compustat["conml"].str.replace('"', '')
compustat["conml"] = compustat["conml"].str.replace(",","")


# In[ ]:


'''
just run it and do not need to change anything
can add other abbreviations
'''
# for compustat csv
# remove INC CORP LLC LTD and everything followed in companyname
# create a new column "firstname" for name without those abbreviations
# can add other abbreviations
compustat['firstname'] = ""

for i in range(len(compustat)):
    if type(compustat['conml'][i]) == str:
        split = compustat['conml'][i].split()
        if "INC" in split:
            name = split[0:split.index("INC")]
        elif "INC." in split:
            name = split[0:split.index("INC.")]
        elif "CORP" in split:
            name = split[0:split.index("CORP")]
        elif "CORP." in split:
            name = split[0:split.index("CORP.")]
        elif "LLC" in split:
            name = split[0:split.index("LLC")]
        elif "LLC." in split:
            name = split[0:split.index("LLC.")]
        elif "LTD" in split:
            name = split[0:split.index("LTD")]
        elif "LTD." in split:
            name = split[0:split.index("LTD.")]
        elif "CORPORATION" in split:
            name = split[0:split.index("CORPORATION")]
        elif "CORPORATION." in split:
            name = split[0:split.index("CORPORATION.")]
        elif "CO" in split:
            name = split[0:split.index("CO")]
        elif "CO." in split:
            name = split[0:split.index("CO.")]
        else:
            name = split
        compustat['firstname'][i] = " ".join(str(x) for x in name)
        print(i, compustat['conml'][i], compustat['firstname'][i])
    else:
        continue

        
    


# In[ ]:


'''
just run it and do not need to change anything
can add other abbreviations
'''

# on assignee csv
# remove INC CORP LLC LTD and everything followed in companyname
# create a new column "firstname" for name without those abbreviations
# can add other abbreviations
# be careful there exists NaN in companyname from 629967 to 629988 (in old file)
assignee['firstname'] = ""
for i in range(len(assignee)):
    if type(assignee['companyname'][i]) == str:
        split = assignee['companyname'][i].split()
        if "INC" in split:
            name = split[0:split.index("INC")]
        elif "INC." in split:
            name = split[0:split.index("INC.")]
        elif "CORP" in split:
            name = split[0:split.index("CORP")]
        elif "CORP." in split:
            name = split[0:split.index("CORP.")]
        elif "LLC" in split:
            name = split[0:split.index("LLC")]
        elif "LLC." in split:
            name = split[0:split.index("LLC.")]
        elif "LTD" in split:
            name = split[0:split.index("LTD")]
        elif "LTD." in split:
            name = split[0:split.index("LTD.")]
        elif "CORPORATION" in split:
            name = split[0:split.index("CORPORATION")]
        elif "CORPORATION." in split:
            name = split[0:split.index("CORPORATION.")]
        elif "CO" in split:
            name = split[0:split.index("CO")]
        elif "CO." in split:
            name = split[0:split.index("CO.")]
        else:
            name = split
        assignee['firstname'][i] = " ".join(str(x) for x in name)
        print(i, assignee['companyname'][i], assignee['firstname'][i])
    else:
        continue


        


# In[ ]:


'''
just run it and do not need to change anything

'''
#search by unique names instead of name at each row 
compustat_unique_name = list(compustat["firstname"].unique())
assignee_unique_name = list(assignee["firstname"].unique())


# In[ ]:


#just see how many names
print(len(compustat_unique_name))
print(len(assignee_unique_name))


# In[ ]:


'''
just run it and do not need to change anything

'''
#create three more empty columns in compustat
compustat['name_find'] = ""
compustat['similarity'] = ""
compustat['assigneeid'] = ""  
    


# In[ ]:


'''
just run it and do not need to change anything

'''
#create two same dataframe for cutoffs 1 and 0.55
compustat_1 = compustat.copy(deep = True)
compustat_0_55 = compustat.copy(deep = True)


# In[ ]:


#count for number of names with different cutoffs, just ignore it if you do not need
count = 0 
count1 = 0
count2 = 0
count_char = 0


# In[ ]:


'''
just run it and do not need to change anything

'''
# compustatname_match: the conml in compustat used to find name in assignee
def find_best_ratio(name_need_to_find, names_first_letter):
    import difflib
    matched_firstword = []
    matched_secondword = []
    ratio_list = {}
    name_need_to_find_list = name_need_to_find.split()
    #compustatname_match_list = compustatname_match.split()
    for i in range(len(names_first_letter)):
        name_compare = names_first_letter[i]
        name_compare_list = name_compare.split()
        #print(name_compare)
        if name_compare == "":
            continue
        #print(name_compare == compustatname_match)
        if name_compare == name_need_to_find:
            return name_compare, 1.0
        elif name_compare.replace(" ", "") == name_need_to_find.replace(" ", ""):
            return name_compare, 1.0
        else:
            if len(name_need_to_find_list) >= 1 and len(name_compare_list) >= 1:
                if name_compare_list[0] == name_need_to_find_list[0]:
                    matched_firstword.append(name_compare)
    if len(matched_firstword) == 0:
        for i in range(len(names_first_letter)):
            name_compare = names_first_letter[i]
            ratio_list[name_compare]=similarity_score(name_need_to_find, name_compare)
        key_list = list(ratio_list.keys())
        val_list = list(ratio_list.values())
        position = val_list.index(max(val_list))
        return key_list[position], val_list[position]
    if len(name_need_to_find_list) >= 2:
        for i in range(len(matched_firstword)):
            name_compare = matched_firstword[i]
            name_compare_list = name_compare.split()
            if len(name_compare_list) >= 2 and name_compare_list[1] == name_need_to_find_list[1]:
                matched_secondword.append(name_compare)
    if len(matched_secondword) == 0:
        for i in range(len(matched_firstword)):
            name_compare = matched_firstword[i]
            name_compare_list = name_compare.split()
            if len(name_compare_list) == 1 or len(name_need_to_find_list) == 1:
                ratio_list[name_compare]=similarity_score(name_need_to_find, name_compare)*2
            else:
                ratio_list[i]=similarity_score(name_need_to_find, name_compare)
        key_list = list(ratio_list.keys())
        val_list = list(ratio_list.values())
        position = val_list.index(max(val_list))
        return key_list[position], val_list[position]
    
    matched_third = []

    if len(name_need_to_find_list) >= 3:
        for i in range(len(matched_secondword)):
            name_compare = matched_secondword[i]
            name_compare_list = name_compare.split()
            if len(name_compare_list) >= 3 and name_compare_list[2] == name_need_to_find_list[2]:
                matched_third.append(name_compare)

                
    if len(matched_third) == 0:
        for i in range(len(matched_secondword)):
            name_compare = matched_secondword[i]
            ratio_list[name_compare]=similarity_score(name_need_to_find, name_compare)
        key_list = list(ratio_list.keys())
        val_list = list(ratio_list.values())
        position = val_list.index(max(val_list))
        return key_list[position], val_list[position]
                               
    for i in range(len(matched_third)):
        name_compare = matched_third[i]
        ratio_list[name_compare]=similarity_score(name_need_to_find, name_compare)
        
    key_list = list(ratio_list.keys())
    val_list = list(ratio_list.values())
    position = val_list.index(max(val_list))
    return key_list[position], val_list[position]
           
    #max_ratio = max(ratio_list)
    #index_max = ratio_list.index(max_ratio)
    #max_value_keys = [key for key in ratio_list.keys() if ratio_list[key] == max(ratio_list.values())]
    
import math
from collections import Counter
def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)
def length_similarity(c1, c2):
    lenc1 = sum(len(x) for x in c1)
    lenc2 = sum(len(x) for x in c2)
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))
def similarity_score(l1, l2):
    l1 = l1.split()
    l2 = l2.split()
    c1, c2 = Counter(l1), Counter(l2)
    return length_similarity(c1, c2) * counter_cosine_similarity(c1, c2)  


# In[ ]:


'''
Before you start this section, make sure you run the four functions above: 
    find_best_ratio: go through each unique name in compustat, and for each of them, find the most similar one by 
        going through each unique name in assignee. Finding most similar one in this way: for each unique name in 
        compustat, extract those in assignee with same first letter. If exist, find first same word, then first 
        two words...until no more same words can be found, finally find the most similar one among those with same 
        first 2 or 3 or 4 words.
    counter_cosine_similarity
    length_similarity
    similarity_score
just run it and do not need to change anything

'''
#after most similar name and id are found, fill in those info into compustat file, if score>=1, fill in into 
#compustat_1 file, the same for other cutoff like 0.55
for i in range(len(compustat_unique_name)):
    #first_10 += 1
    #if first_10 > 50:
        #break
    name_need_to_find = compustat_unique_name[i]
    if name_need_to_find == "":
        continue
    names_first_letter = []
    for ele in assignee_unique_name:
        if ele != "" and ele[0] == name_need_to_find[0]:
            names_first_letter.append(ele)
    if len(names_first_letter) == 0:
        print(i, "compustat:",name_need_to_find, 0.0,"      assignee:", "NULL")
        continue
    #print(len(names_first_letter))
    #if (name_need_to_find[1].isalpha() == False):
        #count_char += 1
  
    assigneename, max_ratio = find_best_ratio(name_need_to_find, names_first_letter)
    #print(type(assigneename))
    if (type(assigneename) != str):
        #print(1)
        continue
    id_match = " ".join(list(assignee[assignee['firstname'] == assigneename]['assigneeid'].unique()))
    compustat.loc[compustat['firstname']== name_need_to_find,"name_find"] = assigneename
    compustat.loc[compustat['firstname']== name_need_to_find,"similarity"] = max_ratio
    compustat.loc[compustat['firstname']== name_need_to_find,"assigneeid"] = id_match
    #print(id_match)
    if max_ratio >= 1.0:
        count += 1
        count1 += 1
        count2 += 1
        compustat_1.loc[compustat_1['firstname']== name_need_to_find,"name_find"] = assigneename
        compustat_1.loc[compustat_1['firstname']== name_need_to_find,"similarity"] = max_ratio
        compustat_1.loc[compustat_1['firstname']== name_need_to_find,"assigneeid"] = id_match
        print(i, "compustat:",name_need_to_find, "      assignee:",assigneename, "      ", max_ratio, id_match, "YES")
    if max_ratio >= 0.55:
        count1 += 1
        count2 += 1
        compustat_0_55.loc[compustat_0_55['firstname']== name_need_to_find,"name_find"] = assigneename
        compustat_0_55.loc[compustat_0_55['firstname']== name_need_to_find,"similarity"] = max_ratio
        compustat_0_55.loc[compustat_0_55['firstname']== name_need_to_find,"assigneeid"] = id_match
        print(i, "compustat:",name_need_to_find, "      assignee:",assigneename, "      ", max_ratio, id_match)
    else: 
        print(i, "compustat:",name_need_to_find, "      assignee:",assigneename, "      ", max_ratio, id_match) 


    #compustat['name_find'][i] = assigneename
    #compustat['similarity'][i] = max_ratio
    #compustat['assigneeid'][i] = id_match   
    
    


# In[ ]:


'''
!!!!!!!!!!!!change the path to where you want the final results to be at
'''
#convert dataframe to csv
compustat.to_csv('/Users/abcdefg/Downloads/Compustat_for_name_match_new.csv')
compustat_1.to_csv('/Users/abcdefg/Downloads/Compustat_for_name_match_new_cutoff_1.csv')
compustat_0_55.to_csv('/Users/abcdefg/Downloads/Compustat_for_name_match_new_cutoff_0.55.csv')

