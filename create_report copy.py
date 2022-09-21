from datetime import datetime
#from pandas import DataFrame
import pandas as pd

df_original = pd.DataFrame(
            {
                "Name": "Maria Maria Maria Maria Jane Carlos".split(),
                "Sample": [25, 9, 4, 3, 2, 8],
                "Date": [
                    datetime(2019, 9, 1, 13, 0),
                    datetime(2019, 9, 1, 13, 5),
                    datetime(2019, 10, 1, 20, 0),
                    datetime(2019, 10, 3, 10, 0),
                    datetime(2019, 12, 2, 12, 0),
                    datetime(2019, 9, 2, 14, 0),
                ],
            }
        )
#df_original.set_index('Date',inplace=True)

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(df_original)

print(df_original.to_string())

text = df_original.groupby(pd.Grouper(key='Date',freq='D')).sum().to_string()
print(text)