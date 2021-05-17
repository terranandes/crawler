import pandas as pd
import re

#USER modifiable CFG
lasting_yrs = 3
std_grd = 14
df = pd.read_csv('stock_list_s2006e2021_unfiltered.csv')

#drop column bah and bal
drop_roi_type = ['bah', 'bal']
drop_roi_cl = ['s'+'2006'+'e'+str(ey)+ roit for ey in range(2007, 2022) for roit in drop_roi_type]
df2 = df.drop(drop_roi_cl, axis=1)

#drop column unused yrs
drop_yrs_cl = ['s'+'2006'+'e'+str(ey)+'yrs' for ey in range(2007, 2021)]
df3 = df2.drop(drop_yrs_cl, axis=1)

#Filter stock with lasting years > lasting_yrs
df4 = df3[df3.s2006e2021yrs > lasting_yrs]


#sorted by 's2006e2021bao' , TBD with variable
df5=df4.sort_values(by='s2006e2021bao', ascending=False)

#filter valid stock info only
vslist = []
for stk in df5.index:
    tmp2 = int(df5.loc[stk][-1])
    if tmp2 >= 15 :
        vs = True
    else :
        vs = pd.isnull(df5.loc[stk][-1-tmp2-1])
    vslist.append(vs)
df6 = df5[vslist]

#filter stock with std less than std_grd
vslist_2 = []
for stk2 in df6.index:
    tmp2 = int(df6.loc[stk2][-1])
    if tmp2 >= 15 :
        ser_s = df6.loc[stk2][4:-1]
    else :
        ser_s = df6.loc[stk2][-1-tmp2:-1]
    if ser_s.std() <= std_grd : 
        vs_2 = True
    else :
        vs_2 = False
    vslist_2.append(vs_2)
df7 = df6[vslist_2]

#filter special ETF with id 'L'
vslist_3 = []
for stk3 in df7.index:
    id = df7.loc[stk3][0]
    if re.search("L", id) :
        vs_3 = False
    else :
        vs_3 = True
    vslist_3.append(vs_3)

df8 = df7[vslist_3]

df8.to_csv('stock_list_s2006e2021_filtered.csv')

