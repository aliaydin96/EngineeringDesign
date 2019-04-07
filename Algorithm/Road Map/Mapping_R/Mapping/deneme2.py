
clear 
#%%
import csv

#%%


#%%

def Self_Localization(Self_Localization):
    with open(self_localization, 'w') as myfile:
        writer= csv.writer(myfile)
        writer.writerows(Self_Localization)
        
    
 #%%