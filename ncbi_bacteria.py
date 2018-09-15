"""

All Organism name and ID's of Bacteria  

requirement : Bio package python

"""


import pandas as pd
from Bio import Entrez
Entrez.email = "your email-id"
search_term= "bacteria[Organism]"
handle=Entrez.esearch(db="genome", retmax=10000000, term=search_term)
result = Entrez.read(handle)
id_list = result['IdList']
first_list = " ".join(str(x) for x in id_list[0:10000])
second_list = " ".join(str(x) for x in id_list[10000:20000])
third_list = " ".join(str(x) for x in id_list[20000:22463])
handle.close()
handle1 = Entrez.esummary(db="genome", id=first_list)
handle2 = Entrez.esummary(db="genome", id=second_list)
handle3 = Entrez.esummary(db="genome", id=third_list)

resultfirst = Entrez.read(handle1)
resultsecond = Entrez.read(handle2)
resultthird = Entrez.read(handle3)
Organisms = []
for i in range(0,10000):
    Organisms.append(resultfirst[i]['Organism_Name'])
for j in range(0,10000):
    Organisms.append(resultsecond[j]['Organism_Name'])
for k in range(0,2463):
    Organisms.append(resultthird[k]['Organism_Name'])
organism_list = pd.DataFrame({'idlist':id_list,'Organism': Organisms})
writer = pd.ExcelWriter('organismlist_ids.xlsx')
organism_list.to_excel(writer,'Sheet1')
writer.save()





