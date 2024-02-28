import pandas as pd
import numpy as np

def fix_data_format():
    df = pd.read_csv("utils/datasets/Charging/hl_2023_hourly.csv")
    grouped_df = df.groupby('date').agg({'std_scaled': list, 'weekend': lambda x: 1  if np.any(x) else 0})
    print(grouped_df.columns)
    print(grouped_df)


    grouped_df.reset_index(inplace=True)
    print(grouped_df)
    grouped_df = grouped_df.drop("date", axis=1)
    print(grouped_df)
    grouped_df['std_scaled'] = grouped_df.apply(lambda row: [row['weekend']] + row['std_scaled'], axis=1)

    grouped_df = grouped_df.drop("weekend", axis=1)
    print(grouped_df)


    # Create a new DataFrame with only the "std_scaled" values
    values_df = pd.DataFrame(grouped_df['std_scaled'].tolist())

    # Save the values to a CSV file
    values_df.to_csv('utils/datasets/Charging/Charging_BOTH.csv', index=False, header=False)
