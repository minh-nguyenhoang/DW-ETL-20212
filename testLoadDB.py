import pandas as pd
import pyodbc

DB = {'servername': 'MSI',
      'source': 'AdventureWorks2019',
      'destination':'DW',
      'user':'user1',
      'pass':'123456'}
# create the connection
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + DB['servername'] + ';DATABASE=' + DB['source'] +';UID='+ DB['user']+';PWD='+DB['pass']+ ';Trusted_Connection=yes')
df = pd.read_sql('SELECT * FROM Purchasing.[PurchaseOrderHeader]',conn)
df['ModifiedDate'] =pd.to_datetime(df['ModifiedDate']).dt.date
#df['ModifiedDate'] = pd.to_datetime(df['ModifiedDate']).dt.strftime('%m/%d/%Y')
#print(df['ModifiedDate'].drop_duplicates())
date=pd.DataFrame(df['ModifiedDate'].drop_duplicates())
#print(date)
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + DB['servername'] + ';DATABASE='+DB['destination'] +';UID='+ DB['user']+';PWD='+DB['pass']+ ';Trusted_Connection=yes')
cursor=cnxn.cursor()
# datedim = pd.read_sql('SELECT * FROM dbo.DateDim',cnxn)
# print(datedim)
for index, row in date.iterrows():
      cursor.execute('''INSERT INTO dbo.DateDim (date) values(?)''', row.ModifiedDate)
      cursor.commit()
datedim2 = pd.read_sql('SELECT * FROM dbo.DateDim',cnxn)
print(datedim2)
