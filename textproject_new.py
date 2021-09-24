#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
Explanation of functions below:

decodee function: 
transfer the txt file to list of strings contains content in each line of the file

extract_part: 
for each list we get from above, extract the content in lines from "Item" to "signature" according to
what we need, and see if there exist those content. If not, this txt file will be removed from extraction after
this function.

extract_item: 
extract company name, filed as of date,
remove meaning less content from the extracted part by functions above: 
     data_1: what we got after removing empty string and <anything>
     data_2: what we got after removing page number(string with only whitespaces and number)
     data_3: what we got after removing "---------------"
for each file, seperate each item and contents followed: get data_4 and data_5
finally, what we got in this function
company name, 
, 
data_5 : In the format of [
                    [item, title, [content]], 
                    [item, title, [content]]
                                                ]
'''
     


# In[ ]:


'''
For this first cell below that includs three functions I described above, you do not need to change anything.
'''


# In[64]:



def decodee(path):
    #####decode
    with open (path, "r", errors='ignore') as txtfile:
        file = txtfile.readlines()
    
    # in line
    lines = []
    import re
    for line in file:
        
        lines.append(line.replace("\t", "").rstrip('\n'))
    #print(lines)
    return lines


def extract_part(lines):
    ######extract from item to signature
    import re
    flag = 0
    for i in range(len(lines)):
        if re.match(r'Item\s+[0-9]{1,}\.', lines[i]) or re.match(r'ITEM\s+[0-9]{1,}\.', lines[i]):
        #if  "Item " in lines[i] and any(char.isdigit() for char in lines[i]):
            flag = 1
            idx = i
            print("start item: ", idx)
            break
    flag1 = 0
    for i in range(len(lines)):
        if "SIGNATURES" in lines[i] or "SIGNATURE" in lines[i]:
            idx_end = i
            flag1 = 1
            print("signature:", idx_end)
            break
    flag_all = 0
    if flag == 1 and flag1 == 1:
        data = lines[idx:idx_end]
        flag_all = 1
    #print(data)
        return data, flag_all
    else: 
        data = 1
        return data, flag_all 

def extract_item(link):
    lines = decodee(link)

    import re
    ######find company name and filed out of date
    for line in lines:
        if "COMPANY CONFORMED NAME:" in line:
            name = line
            name1 = name.split(":")
            name_company = name1[1].rstrip("\t")

        
        if "FILED AS OF DATE:" in line:
            date = line
            date1 = date.split(":")
            date_company = date1[1].rstrip("\t")

    

    data,flag_all = extract_part(lines)
    
    data_1 = [] ######remove empty string and <anything>

    for lines in data:
        if lines != '' and not re.match(r'<[\s\S]+>', lines) and '         <S>              <C>' not in lines:
            data_1.append(lines)



    data_2 = [] ######remove page number(string with only whitespaces and number)
    for i in range(len(data_1)):
        if re.match("^[0-9 ]+$", data_1[i]):
            continue
        data_2.append(data_1[i])
    #print(len(data_1))
    #print(len(data_2)) #for this sample should be difference of 2
    #print(data_2)



    data_3 = [] ######remove "----------"
    for i in range(len(data_2)):
        if not re.match(r'^[_\W]+$', data_2[i]):
            data_3.append(data_2[i])
        #else:
            #print(data_2[i])




    ######seperate each item and contents followed
    idx = []

    for i in range(len(data_3)):
        if re.match(r'Item\s+[0-9]{1,}\.', data_3[i]) or re.match(r'ITEM\s+[0-9]{1,}\.', data_3[i]):
        #if "Item " in data_3[i] and any(char.isdigit() for char in data_3[i]):
            idx.append(i)
    #print(idx)

    data_4 = []
    for i in range(len(idx)):
        if i < len(idx)-1:
            data_4.append(list(data_3[idx[i]:idx[i+1]]))
        if i == len(idx)-1:
            data_4.append(list(data_3[idx[i]:]))

    print("data_4:", data_4)
    data_5 = []
    for i in range(len(data_4)):
        idx_dot = data_4[i][0].find(".")
        print(data_4[i][0])
        if (idx_dot+1)< (len(data_4[i][0])-1):
            while (data_4[i][0][idx_dot+1].isdigit()):
                idx_dot = idx_dot+1
                if (idx_dot+1)>= (len(data_4[i][0])-1):
                    break

        list1 = []
        list1.append(data_4[i][0][:idx_dot+1])
        list1.append(data_4[i][0][idx_dot+2:])
        list1.append(data_4[i][1:])
        data_5.append(list1)
    #print(data_5)

    return name_company, date_company, data_5


# In[ ]:


'''
You can see that I listed the path of each txt file in my computer, 
and in my laptop, folder "8k" includes all the folders whose name is the company CIK, which includes the text files,
like /Users/abcdefg/Downloads/8k/1640967/0001144204-17-046390.txt", CIK is 1640967.
This is the structure of files in the box, and I believe it would be the same structure for the file in your computer.

From the result showed below the cell you can see how it looks like after printing the result. Also, from this part,
CIK is extracted for each text file.
'''


# In[ ]:


'''
!!!!!!!!!!!!!!!!!!!!!!
For this part, you will need to change the basepath below to the path of 8k in your computer.
'''


# In[44]:



import os
basepath = '/Users/abcdefg/Downloads/8k/'
pathlist = []
for folders in os.listdir(basepath):
    if os.path.exists(basepath+folders+"/"):
        for txtfile in os.listdir(basepath+folders+"/"):
            #print(txtfile)
            txtpath = []
            txtpath.append(basepath+folders+"/"+txtfile)
            txtpath.append(folders)
            pathlist.append(txtpath)

#print(pathlist)
        
    


# In[ ]:


'''
Remove the text files with too many meaningless <>
Then, run decodee function and extract_part function.
If the text file includes too many <>, or do not pass the test of extract_part function, then it will be excluded
from the list of path above you see, and will not need to run extract_item function.

The result shows the path, index of Item, signature in this text file, and whether it will be included to run the 
code after.

Text file that will move into next step will be stored in the list "nice_format"
'''


# In[ ]:


'''
You will not need to change anything for the cell below.
'''


# In[45]:


# filtered text files with too many <>

nice_format = []
for paths in pathlist:
    print(paths)
    count = 0
    lines = decodee(paths[0])
    for line in lines:
        if "<" in line:
            for ele1 in line:
                if ele1 == "<":
                    count += 1
                    
    if count >= 100:
        continue
                    
    data, flag_all = extract_part(lines)
    #if count >= 100:
        #print(False)
    if flag_all ==1:
        print(True)
        #print(data)
        nice_format.append(paths)   
              


# In[ ]:


'''
Final Part: to combine everthing above
From the path in "nice_format", run extract_item to have everything ready to store in the csv.
For each text file, "Company", "Item#", "Title", "Content", "Doc_ID", "Item4", "CIK", "Date" are stored in the csv 
in a specific location that you like.
'''


# In[ ]:


'''
You will need to change the path "/Users/abcdefg/Downloads/item_info.csv" to the path that you want your
file to be in. 
'''


# In[65]:


## use filtered path to create csv  
import csv
with open('/Users/abcdefg/Downloads/item_info.csv', mode='w') as csv_file:
    fieldnames = ["Company", "Item#", "Title", "Content", "Doc_ID", "Item4", "CIK", "Date"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    id = 1
    for link in nice_format:
        print(link)
        name, date, data = extract_item(link[0])
        for i in range(len(data)):
            writer.writerow({"Company": name, "Item#": data[i][0], "Title": data[i][1], "Content": ' '.join(data[i][2]), "Doc_ID": id, "Item4": "4" in data[i][0], "CIK": link[1], "Date": date})
        id += 1


# In[ ]:




