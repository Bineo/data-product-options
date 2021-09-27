import numpy as np
from src.utilities.tools import read_excel_table


the_tables = ["users", "products", "tags"]
table_cols = read_excel_table("refs/Sampling 360.xlsx.lnk", 
            sheet="Simulations", table="columns")

each_tbl = "products"
for each_tbl in the_tables:

    a_df = read_excel_table("refs/Sampling 360.xlsx.lnk", 
            sheet="Simulations", table=each_tbl)

    col_types = dict( (row.column, row.type) 
            for row in table_cols.query(f"table == '{each_tbl}'").itertuples())
    for each_col, each_type in col_types.items():
        if each_type == "datetime64[ns]": 
            a_df[each_col] = a_df[each_col].replace(False, np.nan)
        
        a_df[each_col] = a_df[each_col].astype(each_type)

    a_df.to_feather(f"data/sims/{each_tbl}.feather")
    a_df.to_csv(f"data/sims/{each_tbl}.csv", index=False)



