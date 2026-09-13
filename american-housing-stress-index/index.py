import pandas as pd
import numpy as np
from pathlib import Path
p = Path(".")

df = pd.read_csv( p / "Texas_data_tracts.csv")
#try:
#    assert p.exists(), "This is a directory."
#except:
#    print("Not asserted!")

#weighting formulas
renter_weights = {
    "B25070_002E(Estimate!!Total:!!Less than 10.0 percent - Gross Rent as a Percentage of Household Income in the Past 12 Months)": -4.0,
    "B25070_003E(Estimate!!Total:!!10.0 to 14.9 percent - Gross Rent as a Percentage of Household Income in the Past 12 Months)": -3.0,
    "B25070_004E(Estimate!!Total:!!15.0 to 19.9 percent - Gross Rent as a Percentage of Household Income in the Past 12 Months)": -2.0,
    "B25070_005E(Estimate!!Total:!!20.0 to 24.9 percent - Gross Rent as a Percentage of Household Income in the Past 12 Months)": -1.0,
    "B25070_006E(Estimate!!Total:!!25.0 to 29.9 percent - Gross Rent as a Percentage of Household Income in the Past 12 Months)": -0.5,
    "B25070_007E(Estimate!!Total:!!30.0 to 34.9 percent - Gross Rent as a Percentage of Household Income in the Past 12 Months)":  0.5,
    "B25070_008E(Estimate!!Total:!!35.0 to 39.9 percent - Gross Rent as a Percentage of Household Income in the Past 12 Months)":  1.0,
    "B25070_009E(Estimate!!Total:!!40.0 to 49.9 percent - Gross Rent as a Percentage of Household Income in the Past 12 Months)":  2.0,
    "B25070_010E(Estimate!!Total:!!50.0 percent or more - Gross Rent as a Percentage of Household Income in the Past 12 Months)":  3.0,
}

mortgaged_weights = {
    "B25091_003E(Estimate!!Total:!!Housing units with a mortgage:!!Less than 10.0 percent)": -4.0,
    "B25091_004E(Estimate!!Total:!!Housing units with a mortgage:!!10.0 to 14.9 percent)": -3.0,
    "B25091_005E(Estimate!!Total:!!Housing units with a mortgage:!!15.0 to 19.9 percent)": -2.0,
    "B25091_006E(Estimate!!Total:!!Housing units with a mortgage:!!20.0 to 24.9 percent)": -1.0,
    "B25091_007E(Estimate!!Total:!!Housing units with a mortgage:!!25.0 to 29.9 percent)": -0.5,
    "B25091_008E(Estimate!!Total:!!Housing units with a mortgage:!!30.0 to 34.9 percent)":  0.5,
    "B25091_009E(Estimate!!Total:!!Housing units with a mortgage:!!35.0 to 39.9 percent)":  1.0,
    "B25091_010E(Estimate!!Total:!!Housing units with a mortgage:!!40.0 to 49.9 percent)":  2.0,
    "B25091_011E(Estimate!!Total:!!Housing units with a mortgage:!!50.0 percent or more)":  3.0,
}

unmortgaged_weights = {
    "B25091_014E(Estimate!!Total:!!Housing units without a mortgage:!!Less than 10.0 percent)": -4.0,
    "B25091_015E(Estimate!!Total:!!Housing units without a mortgage:!!10.0 to 14.9 percent)": -3.0,
    "B25091_016E(Estimate!!Total:!!Housing units without a mortgage:!!15.0 to 19.9 percent)": -2.0,
    "B25091_017E(Estimate!!Total:!!Housing units without a mortgage:!!20.0 to 24.9 percent)": -1.0,
    "B25091_018E(Estimate!!Total:!!Housing units without a mortgage:!!25.0 to 29.9 percent)": -0.5,
    "B25091_019E(Estimate!!Total:!!Housing units without a mortgage:!!30.0 to 34.9 percent)":  0.5,
    "B25091_020E(Estimate!!Total:!!Housing units without a mortgage:!!35.0 to 39.9 percent)":  1.0,
    "B25091_021E(Estimate!!Total:!!Housing units without a mortgage:!!40.0 to 49.9 percent)":  2.0,
    "B25091_022E(Estimate!!Total:!!Housing units without a mortgage:!!50.0 percent or more)":  3.0,
}

computable_renters = (
    df["B25070_001E(Estimate!!Total: - Gross Rent as a Percentage of Household Income in the Past 12 Months)"] - 
    df["B25070_011E(Estimate!!Total:!!Not computed - Gross Rent as a Percentage of Household Income in the Past 12 Months)"]
)

computable_mortgaged = (
    df["B25091_002E(Estimate!!Total:!!Housing units with a mortgage:)"] - 
    df["B25091_012E(Estimate!!Total:!!Housing units with a mortgage:!!Not computed)"]
)

computable_unmortgaged = (
    df["B25091_013E(Estimate!!Total:!!Housing units without a mortgage:)"] - 
    df["B25091_023E(Estimate!!Total:!!Housing units without a mortgage:!!Not computed)"]
)

df["computable_renters"] = computable_renters
df["computable_mortgaged"] = computable_mortgaged
df["computable_unmortgaged"] = computable_unmortgaged

#calculate renter, mortgaged, and unmortgaged scores series type
renter_score = np.where(
    df["computable_renters"] > 0,
    sum(df[var] / df["computable_renters"] * weight 
        for var, weight in renter_weights.items()),
    0
)

mortgaged_score = np.where(
    df["computable_mortgaged"] > 0,
    sum(df[var] / df["computable_mortgaged"] * weight 
        for var, weight in mortgaged_weights.items()),
    0
)

unmortgaged_score = np.where(
    df["computable_unmortgaged"] > 0,
    sum(df[var] / df["computable_unmortgaged"] * weight 
        for var, weight in unmortgaged_weights.items()),
    0
)

#append calculated series to columns in loaded df 
df["renter_score"] = renter_score
df["renter_score"] = df["renter_score"].fillna(0)

df["mortgaged_score"] = mortgaged_score
df["mortgaged_score"] = df["mortgaged_score"].fillna(0)

df["unmortgaged_score"] = unmortgaged_score
df["unmortgaged_score"] = df["unmortgaged_score"].fillna(0)

#calculate housing stress index as series
housing_stress_index = (
    (renter_score * computable_renters) +
    (mortgaged_score * computable_mortgaged) +
    (unmortgaged_score * computable_unmortgaged)
) / (computable_renters + computable_mortgaged + computable_unmortgaged)

#append calculated hsi series to column in loaded df
df["housing_stress_index"] = housing_stress_index

#add 'GEOID' column for GIS table join w/census tracts
df["GEOID"] = (
    df["state"].astype(str).str.zfill(2) +
    df["county"].astype(str).str.zfill(3) +
    df["tract"].astype(str).str.zfill(6)
)

#export df as csv
df.to_csv(p / "Texas_data_tracts_renters.csv")

