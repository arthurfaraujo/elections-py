import pandas as pd

df = pd.read_csv("data/consulta_cand_2024_PB.csv", encoding="latin1", sep=";", encoding_errors='replace')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def getCandidatesByCityAndRole(cityCode: int, roleCode: int):
  print(df[(df["SG_UE"] == cityCode) & (df["CD_CARGO"] == roleCode)][["SQ_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "NR_CANDIDATO", "NM_PARTIDO"]].to_string(index=False))

def getCandidateByCode(code: int):
  print(df.loc[df["SQ_CANDIDATO"] == code, ["NM_CANDIDATO", "NM_URNA_CANDIDATO", "NR_CANDIDATO", "NM_PARTIDO"]].to_string(index=False))