"""
from liznerski_explainable_2021
Liznerski, P., Ruff, L., Vandermeulen, R.A., Franks, B.J., Kloft, M., Muller, K.R., 2021. Explainable Deep One-Class Classification, in: International Conference on Learning Representations. Presented at the International Conference on Learning Representations.
Table 3
"""

from pathlib import Path
import pandas as pd


txt_fifle = Path(__file__).parent / "fcdd_2021_table2.txt"  # contains the data part of the table above

str_data = txt_fifle.read_text()
nlines_per_group = 11

# this is in the order of the lines inside each group of 11 lines
METHODS_NAMES = [
    "AE-SS", "AE-L2", "Ano-GAN", "CNNFD",
    "VEVAE", "SMAI", "GDR", "P-NET",
    "FCDD-unsupervised", "FCDD-semi-supervised",
]

lines = str_data.strip().split("\n")
line_groups = [
    lines[(i * nlines_per_group):((i + 1) * nlines_per_group)] 
    for i in range(len(lines) // nlines_per_group)
]

line_groups = [
    {
        "class": g[0].lower().replace(" ", "-"),
        **{
            col: float(val)
            for col, val in zip(METHODS_NAMES, g[1:])
        },
    }
    for g in line_groups
]

df = pd.DataFrame.from_records(data=line_groups).set_index("class")


def get_aess():
    return df[["AE-SS"]].rename(columns={"AE-SS": "score"})


def get_ael2():
    return df[["AE-L2"]].rename(columns={"AE-L2": "score"})


def get_ano_gan():
    return df[["Ano-GAN"]].rename(columns={"Ano-GAN": "score"})


def get_cnnfd():
    return df[["CNNFD"]].rename(columns={"CNNFD": "score"})   


def get_vevae():
    return df[["VEVAE"]].rename(columns={"VEVAE": "score"})


def get_smai():
    return df[["SMAI"]].rename(columns={"SMAI": "score"})


def get_gdr():
    return df[["GDR"]].rename(columns={"GDR": "score"})


def get_pnet():
    return df[["P-NET"]].rename(columns={"P-NET": "score"})


def get_fcdd_unsupervised():
    return df[["FCDD-unsupervised"]].rename(columns={"FCDD-unsupervised": "score"})


def get_fcdd_semi_supervised():
    return df[["FCDD-semi-supervised"]].rename(columns={"FCDD-semi-supervised": "score"})


