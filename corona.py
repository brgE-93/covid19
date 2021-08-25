import pandas as pd
import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##objective :detecter si qqulun a le corona a 90 pourcent

#ANALYSE DE FORME
d=pd.read_excel('dataset2.xlsx', engine='openpyxl')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 200)
#print(d.head())
#print(d.shape,d.columns,d.describe())
df=d.copy()
print("les types variables",df.dtypes.value_counts())
#sns.heatmap(df.isna())
#plt.show()
print((df.isna().sum()/df.shape[0]).sort_values())
print("yo",df.isna().sum())
print("=========================")
#ANALYSE DE FOND

df=df[df.columns[(df.isna().sum()/df.shape[0]) < 0.90]]
print(df.shape)
df=df.drop('Patient ID', axis=1) #car inutile
#sns.heatmap(df.isna())
#plt.show()
print(df['SARS-Cov-2 exam result'].value_counts())

#variable continu les floats
#for d in df.select_dtypes('float'):
    #plt.figure()
    #sns.displot(df[d])
#plt.show()

#variable age du patient un int
#sns.displot(df['Patient age quantile'])
#plt.show()

#var categorielle qualitative
for j in df.select_dtypes('object'):
   print(j, df[j].unique())

'''for j in df.select_dtypes('object'):
   df[j].value_counts().plot.pie()
   #plt.show()'''

#relation target/variable
#target : creer 2 sous ensemble positive/negative donc 2 dataframe
positive_df = df[df['SARS-Cov-2 exam result'] =='positive']
negative_df = df[df['SARS-Cov-2 exam result'] =='negative']
#Les 2 categories de var observer les 76% et 89% qui represente testsanguin et virus
blood_df=df.columns[((df.isna().sum()/df.shape[0])<0.9) & ((df.isna().sum()/df.shape[0])>0.88)]#renvoie liste colomne
viral_df=df.columns[((df.isna().sum()/df.shape[0])<0.88) & ((df.isna().sum()/df.shape[0])>0.75)]
print(blood_df)
plt.figure()
'''for col in blood_df:
   #(sns.displot(positive_df[col],label='positive'))
   #(sns.displot(negative_df[col], label='negative'))
   plt.legend()'''
#plt.show()
#relation target/age
#sns.countplot(x='Patient age quantile',hue='SARS-Cov-2 exam result',data=df)
#plt.show()
#target/tauxsanguins
'''for col in viral_df:
   plt.figure()
   #sns.heatmap(pd.crosstab(df['SARS-Cov-2 exam result'],df[col]),annot=True,fmt='d')'''

#analyse plus detaille
##var/var
#sns.heatmap(df[blood_df].corr())#renvoi matrice de corelation avec dependance des var blood(plus c claire)
#age/varblood
'''for col in blood_df:
   plt.figure()
   #sns.lmplot(x='Patient age quantile',y=col,hue='SARS-Cov-2 exam result',data=df)'''
print(df.corr()['Patient age quantile'])#car c que var quantitave tfacon donc par defaut yaura pas viral..
#plt.show()

#viral/viral
#analyser influenza avec leru test rapide
print(pd.crosstab(df['Influenza A'],df['Influenza A, rapid test']))
print(pd.crosstab(df['Influenza B'],df['Influenza B, rapid test']))

#estmalade/blood
#creer varaible estmalade
df['estmalade'] = (np.sum(df[viral_df[:-2]]=="detected",axis=1)>=1) #creer new colonmne qui dit si on plus de 1 maladie
malade_df=df[df['estmalade']==True]
nonmalade_df=df[df['estmalade']==False]
'''for col in blood_df:
   plt.figure()
   #(sns.displot(malade_df[col],label='malade'))
   #(sns.displot(nonmalade_df[col], label='nonmalade'))
   #plt.legend()'''
#estmalade/hospitalisation
def hospitalisation(df):
   if df['Patient addmited to regular ward (1=yes, 0=no)'] == 1:
      return 'surveillance'
   elif df['Patient addmited to semi-intensive unit (1=yes, 0=no)'] == 1:
      return 'soins semi intensive'
   elif df['Patient addmited to intensive care unit (1=yes, 0=no)']==1:
      return'intensive'
   else:
      return 'inconnu'
df['statut']=df.apply(hospitalisation,axis=1)

#hospitalisation/blood
for col in blood_df:
   plt.figure()
   for cat in df['statut'].unique():
      sns.displot(df[df['statut']==cat][col],label=cat)
      plt.legend()
plt.show()