import sys, os
import pandas as pd
import numpy as np
import glob
from functools import reduce
from collections import Counter

#os.system('mkdir Downloads')
input_file = sys.argv[1]

input_txt = pd.read_csv('%s'%input_file, comment='#', sep=';')

tissue = [x for x in input_txt['tissue']]

for x in set(tissue):
    m = input_txt['tissue'] == x
    treatment = [x.split(',')[0].split('_')[0] for x in input_txt[m]['treatment']]
    print(x,'>>' ,Counter(treatment))

selected_tissue = input('pick tissue!! : ')
m_tissue        = input_txt['tissue'] == selected_tissue
treatment       = [x.split(',')[0].split('_')[0] for x in input_txt[m_tissue]['treatment']]
print(selected_tissue,'>>' ,Counter(treatment))
selected_treatment=[]
while(1):
    input_treatment = input('pick treatment: ')
    if input_treatment in set(treatment):
        selected_treatment.append(input_treatment)
    else:
        break
print(selected_treatment)

select_mat =pd.DataFrame()
for x in selected_treatment:
    select = np.array([x.split(',')[0].split('_')[0] for x in input_txt[m_tissue]['treatment']]) == x
    select_mat = select_mat.append(input_txt[m_tissue][select])
    
def convert_files(x):
    SRR_ID = x['SRR_id']
    H1     = SRR_ID[0:3]
    H2     = SRR_ID[0:6]
    os.system('~/.aspera/connect/bin/ascp  -i ~/.aspera/connect/etc/asperaweb_id_dsa.openssh -k 1 -T -l60m anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra ./'%(H1,H2,SRR_ID,SRR_ID))
    
    if x['Layout'] == 'S':
        os.system('fastq-dump -F --origfmt %s.sra'%SRR_ID)
        os.system('kallisto quant -i Araport11_genes.201606.cdna.idx -o output --single -l 200 -s 20 %s.fastq'%(SRR_ID,SRR_ID))
        os.system('mv ./output/abundance.tsv ./Downloads/%s.tsv'%SRR_ID)
        os.system('rm -rf ./output/')
        os.system('rm %s.sra'%SRR_ID)
        os.system('rm %s*.fastq'%SRR_ID)
    
    else:
        os.system('fastq-dump --split-files %s.sra'%SRR_ID)
        os.system('kallisto quant -i Araport11_genes.201606.cdna.idx -o output %s_1.fastq %s_2.fastq'%(SRR_ID,SRR_ID))
        os.system('mv ./output/abundance.tsv ./Downloads/%s.tsv'%SRR_ID)
        os.system('rm -rf ./output/')
        os.system('rm %s.sra'%SRR_ID)
        os.system('rm %s*.fastq'%SRR_ID)
        
select_mat.apply(lambda x : convert_files(x), axis=1)

def columns_cg(x):
    for i in df_mat.columns[1:]:
        if x['SRR_id'] == i:
            return x['SRR_id'] + ';' + x['treatment'].split(',')[0].split('_')[0] + ';' + x['tissue'] 


file_list      = glob.glob('./Downloads/*.tsv')
df_list        = [pd.read_csv(x,sep='\t')[['target_id','tpm']] for x in file_list]
df_mat         = reduce(lambda a,b : pd.merge(a,b, on='target_id', how = 'outer'), df_list)
df_mat.columns = ['target_id']+[x.split('/')[2].split('.')[0] for x in file_list]
columns_fix    = select_mat.apply(columns_cg, axis=1)
df_mat.columns = ['target_id']+ list(columns_fix)

def num(x):
    global i
    try:
        return dic[x]
    except KeyError:
        dic[x] = i
        i+=1
        return dic[x]
i   = 0
dic = {}    

treat_list = [x.split(';')[1].split(',')[0] for x in df_mat.columns[1:]]
Y          = [num(x) for x in treat_list]
X = df_mat[df_mat.columns[1:]].T.values


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from multiprocessing import Pool, Manager
def skrun(fis,i):
    rf = RandomForestClassifier(n_estimators=2000,n_jobs=1)
    rf.fit(X,Y)
    fi =rf.feature_importances_
    fis.append(fi)
l   = Manager()
fis = l.list()
p   = Pool(10)

for i in range(0, 1000):
    p.apply_async(skrun, args=(fis,i))
p.close()
p.join()


fis_sum = np.sum(fis, axis = 0)
cut     = np.percentile(fis_sum,99.5)
m       = fis_sum > cut


df_ix   = df_mat[m].set_index('target_id')
a,b = df_ix.shape
db_list = []
for x in range(a):
    for y in range(b):
            db_list.append(df_ix.columns[y]+';'+ df_ix.index[x] + ';'+ str(df_ix.iloc[x,y]))
            
data= [np.stack(x.split(';')) for x in db_list]
output_mat = pd.DataFrame(data, columns=['Run_id','Treatment','Tissue','Gene_id','Tpm'])
output_mat.index.names = ['id']
output_mat.to_csv('./test_test/mysite/csv_exp.csv')

os.sys('python3 ./test_test/mysite/db.py')