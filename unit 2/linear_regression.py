from scipy import stats
import collections
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
# Drop null rows
loansData.dropna(inplace=True)

a=loansData['FICO.Range']
g = lambda x: str.replace(x,'-',' '); 
loansData['FICO.Score'] = map(g,a)

b = loansData['Loan.Length']
g = lambda x: str.replace(x,'months',''); 
loansData['Loan.Length'] = map(g,b)

c = loansData['Interest.Rate']
g = lambda x: str.replace(x,'%',''); 
loansData['Interest.Rate']= map(g,c)

intrate = loansData['Interest.Rate'].apply(float)
fico = loansData['FICO.Score']
fico = fico.str.split(' ').apply(min).apply(float)
loanamt = loansData['Amount.Funded.By.Investors']

y = np.matrix(intrate).transpose()
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()

x = np.column_stack([x1,x2])

X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

print 'Coefficients: ', f.params[0:2]
print 'Intercept: ', f.params[2]
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared