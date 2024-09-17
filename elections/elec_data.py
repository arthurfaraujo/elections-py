import pandas as pd

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

# separar em várias funções que chamam as infos pelo código e depois juntar num candidate_info
def goods_by_code(candidateCode: int):
  return goods_df[goods_df["Código Sequencial"] == candidateCode][["Tipo do bem", "Bem", "Valor do bem"]]
  
def social_medias_by_code(candidateCode: int):
  return social_media_df[social_media_df["Código Sequencial"] == candidateCode][["Link da rede social"]]

def candidate_by_code(candidateCode: int) -> pd.DataFrame:
  return candidates_df.loc[(candidates_df["Código Sequencial"] == candidateCode), ["Nome", "Nome na urna", "Número", "Partido"]]

def role_quantity_count() -> dict:
    return candidates_df['DS_CARGO'].value_counts().to_dict()

def parties_with_mayor_candidates() -> list:
    partidos = candidates_df[candidates_df['DS_CARGO'] == 'PREFEITO']['SG_PARTIDO'].unique()
    return partidos.tolist()

def quantity_by_age_group() -> dict:
    candidates_df['IDADE'] = pd.to_datetime('2024-01-01') - pd.to_datetime(candidates_df['DT_NASCIMENTO'], format='%d/%m/%Y', errors='coerce')
    candidates_df['IDADE'] = candidates_df['IDADE'].dt.days // 365
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