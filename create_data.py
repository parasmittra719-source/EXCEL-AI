import pandas as pd
data = {
    'Date': ['Jan', 'Feb', 'Mar'],
    'Revenue': [1000, 1200, 1500]
}
df = pd.DataFrame(data)
df.to_excel("data.xlsx", index=False)
print("Created data.xlsx")
