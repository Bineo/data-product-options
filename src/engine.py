# Diego Villamil, EPIC
# CDMX, 24 de septiembre de 2021

import os
from datetime import datetime as dt
from pathlib import Path

import pandas as pd
from flask import jsonify

SITE = Path(__file__).parents[1] if "__file__" in globals() else Path(os.getcwd())

# ['1499', '2225', '3560', '9124', '7714', '2872', '4084', '4357',
#  '6541', '5532', '1812', '6428', '1896', '6054', '3778']

# user_id = users_df.loc[5, "id"]
def process_request(an_input):
    try: 
        a_request    = an_input.get("user360Request")
        user_id      = a_request.get("userId")
        response_360 = get_user_360(user_id, source="tidy")
        return (jsonify(response_360), 200)
    except Exception as err:
        an_error = {
            "code"          : "0002",
            "status_code"   : "500",
            "type"          : "internal-error",
            "instance"      : "input/messagess_strategy/internal-error",
            "timestamp"     : str(dt.now()),
            "detail"        : str(err)}
    return (jsonify(an_error), 500)


def get_user_360(user_id, source="tidy"):
    if source not in ["tidy", "xls"]:
        raise "SOURCE argument not valid."

    users_df_1 = pd.read_feather(SITE/f"data/sims/users_{source}.feather")
    users_df   = users_df_1.assign(id = users_df_1.id.astype(str))

    if user_id not in users_df["id"].values:
        raise "User ID not found"
        
    user_row = users_df.loc[users_df["id"] == user_id]

    products_1    = pd.read_feather(SITE/f"data/sims/products_{source}.feather")
    products      = products_1.loc[products_1.userId.astype(str) == user_id, :]
    
    prod_offers   = dataframe_to_list("product-offers", 
            products.loc[~(products.accepted), :])

    lifecycles    = dataframe_to_list("lifecycles", 
            products.loc[products.accepted, :])

    tags_df = pd.read_feather(SITE/f"data/sims/tags_{source}.feather")
    tags_ls = list(tags_df
        .loc[tags_df.userId.astype(str) == user_id]["contextTag"])

    past_interactions = []

    a_response = {
        "userContext" : {
            "userId"          : user_id, 
            "userName"        : user_row.iloc[0]["name"],
            "userProfile"     : user_row.iloc[0]["persona"],
            "situationContext": {
                "overallScore": int(user_row.iloc[0]["context"]),
                "tags"        : tags_ls },
            "lifecycleContext": lifecycles }, 
        "productOffers"       : prod_offers,
        "pastInteractions"    : past_interactions}
    return a_response 



def dataframe_to_list(df_class, a_df): 
    df_classes = ["product-offers", "lifecycles"]

    if df_class not in df_classes: 
        raise f"DF_CLASS must be one of {str(df_classes)}."

    base_keys = ["id", "date", "class"]
    non_base  = ["annualRate", "amount", "tenor", "payments"]

    if df_class == "product-offers":
        base_keys += ["expiry"]
    elif df_class == "lifecycles":
        base_keys += ["lifecycle"]
    
    a_dict_ls = [ { k: str(val) for (k, val) in zip(list(a_df.columns), df_tuple[1:])  
                if (k in base_keys) or (k in non_base and not pd.isna(val)) }
                for df_tuple in a_df.itertuples() ]

    return a_dict_ls


    

