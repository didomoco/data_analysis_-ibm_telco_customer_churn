import pandas as pd

try:
    df = pd.read_csv("data/churn.csv")
except:
    url = "https://raw.githubusercontent.com/blastchar/telco-customer-churn/master/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    df = pd.read_csv(url)

print(df.head())
        

