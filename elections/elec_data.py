import pandas as pd
from datetime import datetime

candidates_df = pd.read_csv("data/consulta_cand_2024_PB.csv", encoding="latin1", sep=";")
social_media_df = pd.read_csv("data/rede_social_candidato_2024_PB.csv", encoding="latin1", sep=";") 
goods_df = pd.read_csv("data/bem_candidato_2024_PB.csv", encoding="latin1", sep=";")


candidates_df.rename(columns={"SQ_CANDIDATO": "Código Sequencial", "NM_CANDIDATO": "Nome", "NM_URNA_CANDIDATO": "Nome na urna", "NR_CANDIDATO": "Número","NM_PARTIDO": "Partido"}, inplace=True)
social_media_df.rename(columns={"SQ_CANDIDATO": "Código Sequencial", "DS_URL": "Link da rede social"}, inplace=True)
goods_df.rename(columns={"SQ_CANDIDATO": "Código Sequencial", "DS_TIPO_BEM_CANDIDATO": "Tipo do bem", "DS_BEM_CANDIDATO": "Bem", "VR_BEM_CANDIDATO": "Valor do bem"}, inplace=True)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def candidates_by_city_and_role(cityCode: int, roleCode: int) -> pd.DataFrame:
  return candidates_df[(candidates_df["SG_UE"] == cityCode) & (candidates_df["CD_CARGO"] == roleCode)][["Código Sequencial", "Nome", "Nome na urna", "Número", "Partido"]]

def goods_by_code(candidateCode: int):
  return goods_df[goods_df["Código Sequencial"] == candidateCode][["Tipo do bem", "Bem", "Valor do bem"]]
  
def social_medias_by_code(candidateCode: int):
  return social_media_df[social_media_df["Código Sequencial"] == candidateCode][["Link da rede social"]]

def candidate_by_code(candidateCode: int) -> pd.DataFrame:
  return candidates_df.loc[(candidates_df["Código Sequencial"] == candidateCode), ["Nome", "Nome na urna", "Número", "Partido", "SG_PARTIDO"]]

def role_quantity_count() -> dict:
    return candidates_df['DS_CARGO'].value_counts().to_dict()

def parties_with_mayor_candidates() -> list:
    partidos = candidates_df[candidates_df['DS_CARGO'] == 'PREFEITO']['SG_PARTIDO'].unique()
    return sorted(partidos.tolist())

def quantity_by_age_group() -> dict:
    now = datetime.now()
    candidates_df_nascimento = pd.to_datetime(candidates_df['DT_NASCIMENTO'], format='%d/%m/%Y', errors='coerce')
    candidates_df['IDADE'] = now.year - candidates_df_nascimento.dt.year
    candidates_df['IDADE'] -= (
        (candidates_df_nascimento.dt.month > now.month) | 
        ((candidates_df_nascimento.dt.month == now.month) & (candidates_df_nascimento.dt.day > now.day))
    )
    faixa_ate_21 = candidates_df[candidates_df['IDADE'] <= 21].shape[0]
    faixa_22_40 = candidates_df[(candidates_df['IDADE'] > 21) & (candidates_df['IDADE'] <= 40)].shape[0]
    faixa_41_60 = candidates_df[(candidates_df['IDADE'] > 40) & (candidates_df['IDADE'] <= 60)].shape[0]
    faixa_acima_60 = candidates_df[candidates_df['IDADE'] > 60].shape[0]
    return {'Até 21 anos': faixa_ate_21, '22 a 40 anos': faixa_22_40, '41 a 60 anos': faixa_41_60, 'Acima de 60 anos': faixa_acima_60}

def percentage_by_category(coluna: str, cargo: str) -> dict:
    # total_cargo = df[df['DS_CARGO'] == cargo].shape[0]
    percentuais = candidates_df[candidates_df['DS_CARGO'] == cargo][coluna].value_counts(normalize=True) * 100
    return percentuais.to_dict()
  
def roles() -> pd.DataFrame:
  return candidates_df['DS_CARGO'].unique()

def cities() -> list:
  return candidates_df['NM_UE'].unique().tolist()

def roles_by_city(cityName: str) -> dict:
  prefeitos = list(candidates_df[(candidates_df["NM_UE"] == cityName) & (candidates_df["DS_CARGO"] == "PREFEITO")][["Nome", "Código Sequencial"]].itertuples(index=False, name=None))
  vice_prefeitos = list(candidates_df[(candidates_df["NM_UE"] == cityName) & (candidates_df["DS_CARGO"] == "VICE-PREFEITO")][["Nome", "Código Sequencial"]].itertuples(index=False, name=None))
  vereadores = list(candidates_df[(candidates_df["NM_UE"] == cityName) & (candidates_df["DS_CARGO"] == "VEREADOR")][["Nome", "Código Sequencial"]].itertuples(index=False, name=None))
  
  
  dicionario = {
    'prefeitos': [x for x in prefeitos],
    'vice_prefeitos': [x for x in vice_prefeitos],
    'vereadores': [x for x in vereadores]
  }
  return dicionario 

# quantity_by_age_group()