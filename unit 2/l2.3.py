from scipy import stats
import collections
import matplotlib.pyplot as plt
import pandas as pd

# Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
# Drop null rows
loansData.dropna(inplace=True)

a=loansData['FICO.Range']
g = lambda x: str.replace(x,'-',' '); 
print(map(g,a))
