import pandas as pd

df = pd.read_csv("data/consulta_cand_2024_PB.csv", encoding="latin1", sep=";", encoding_errors='replace')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def candidates_by_city_and_role(cityCode: int, roleCode: int):
  return df[(df["SG_UE"] == cityCode) & (df["CD_CARGO"] == roleCode)][["SQ_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "NR_CANDIDATO", "NM_PARTIDO"]]

def candidate_by_code(code: int):
  return df.loc[df["SQ_CANDIDATO"] == code, ["NM_CANDIDATO", "NM_URNA_CANDIDATO", "NR_CANDIDATO", "NM_PARTIDO"]]

def role_quantity_count():
    return df['DS_CARGO'].value_counts().to_dict()

def parties_with_mayor_candidates():
    partidos = df[df['DS_CARGO'] == 'Prefeito']['SG_PARTIDO'].unique()
    return partidos.tolist()

def quantity_by_age_group():
    df['IDADE'] = pd.to_datetime('2024-01-01') - pd.to_datetime(df['DT_NASCIMENTO'], format='%d/%m/%Y', errors='coerce')
    df['IDADE'] = df['IDADE'].dt.days // 365
    faixa_ate_21 = df[df['IDADE'] <= 21].shape[0]
    faixa_22_40 = df[(df['IDADE'] > 21) & (df['IDADE'] <= 40)].shape[0]
    faixa_41_60 = df[(df['IDADE'] > 40) & (df['IDADE'] <= 60)].shape[0]
    faixa_acima_60 = df[df['IDADE'] > 60].shape[0]
    return {'Até 21 anos': faixa_ate_21, '22 a 40 anos': faixa_22_40, '41 a 60 anos': faixa_41_60, 'Acima de 60 anos': faixa_acima_60}

def percentage_by_category(coluna, cargo):
    # total_cargo = df[df['DS_CARGO'] == cargo].shape[0]
    percentuais = df[df['DS_CARGO'] == cargo][coluna].value_counts(normalize=True) * 100
    return percentuais.to_dict()
  
def roles():
  return df['DS_CARGO'].unique()