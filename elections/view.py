import pandas as pd
from jinja2 import Template

file_path = 'consulta_cand_2024_PB.csv'
df = pd.read_csv(file_path, delimiter=';', encoding='latin1', quotechar='"')

def calcular_quantidade_por_cargo(df):
    return df['DS_CARGO'].value_counts().to_dict()

def partidos_com_candidatos_prefeito(df):
    partidos = df[df['DS_CARGO'] == 'Prefeito']['SG_PARTIDO'].unique()
    return partidos.tolist()

def calcular_quantidade_por_faixa_etaria(df):
    df['IDADE'] = pd.to_datetime('2024-01-01') - pd.to_datetime(df['DT_NASCIMENTO'], format='%d/%m/%Y', errors='coerce')
    df['IDADE'] = df['IDADE'].dt.days // 365
    faixa_ate_21 = df[df['IDADE'] <= 21].shape[0]
    faixa_22_40 = df[(df['IDADE'] > 21) & (df['IDADE'] <= 40)].shape[0]
    faixa_41_60 = df[(df['IDADE'] > 40) & (df['IDADE'] <= 60)].shape[0]
    faixa_acima_60 = df[df['IDADE'] > 60].shape[0]
    return {'Até 21 anos': faixa_ate_21, '22 a 40 anos': faixa_22_40, '41 a 60 anos': faixa_41_60, 'Acima de 60 anos': faixa_acima_60}

def calcular_percentual_por_categoria(df, coluna, cargo):
    total_cargo = df[df['DS_CARGO'] == cargo].shape[0]
    percentuais = df[df['DS_CARGO'] == cargo][coluna].value_counts(normalize=True) * 100
    return percentuais.to_dict()

def gerar_html_estatisticas(df):
    qtd_por_cargo = calcular_quantidade_por_cargo(df)
    partidos_prefeito = partidos_com_candidatos_prefeito(df)
    qtd_por_faixa_etaria = calcular_quantidade_por_faixa_etaria(df)
    percentual_instrucao = {cargo: calcular_percentual_por_categoria(df, 'DS_GRAU_INSTRUCAO', cargo) for cargo in df['DS_CARGO'].unique()}
    percentual_genero = {cargo: calcular_percentual_por_categoria(df, 'DS_GENERO', cargo) for cargo in df['DS_CARGO'].unique()}
    percentual_estado_civil = {cargo: calcular_percentual_por_categoria(df, 'DS_ESTADO_CIVIL', cargo) for cargo in df['DS_CARGO'].unique()}

    template = Template("""
    <html>
    <head><title>Estatísticas Eleitorais - Eleições 2024</title></head>
    <body>
    <h1>Estatísticas de Candidatos - Eleições 2024</h1>
    <h2>Quantidade de Candidatos por Cargo</h2>
    <ul>
        {% for cargo, qtd in qtd_por_cargo.items() %}
        <li>{{ cargo }}: {{ qtd }}</li>
        {% endfor %}
    </ul>
    
    <h2>Partidos com Candidatos ao Cargo de Prefeito</h2>
    <ul>
        {% for partido in partidos_prefeito %}
        <li>{{ partido }}</li>
        {% endfor %}
    </ul>

    <h2>Quantidade de Candidatos por Faixa Etária</h2>
    <ul>
        {% for faixa, qtd in qtd_por_faixa_etaria.items() %}
        <li>{{ faixa }}: {{ qtd }}</li>
        {% endfor %}
    </ul>

    <h2>Percentual de Candidatos por Cargo e Grau de Instrução</h2>
    {% for cargo, percentuais in percentual_instrucao.items() %}
        <h3>{{ cargo }}</h3>
        <ul>
        {% for categoria, percentual in percentuais.items() %}
            <li>{{ categoria }}: {{ "%.2f" % percentual }}%</li>
        {% endfor %}
        </ul>
    {% endfor %}

    <h2>Percentual de Candidatos por Cargo e Gênero</h2>
    {% for cargo, percentuais in percentual_genero.items() %}
        <h3>{{ cargo }}</h3>
        <ul>
        {% for categoria, percentual in percentuais.items() %}
            <li>{{ categoria }}: {{ "%.2f" % percentual }}%</li>
        {% endfor %}
        </ul>
    {% endfor %}

    <h2>Percentual de Candidatos por Cargo e Estado Civil</h2>
    {% for cargo, percentuais in percentual_estado_civil.items() %}
        <h3>{{ cargo }}</h3>
        <ul>
        {% for categoria, percentual in percentuais.items() %}
            <li>{{ categoria }}: {{ "%.2f" % percentual }}%</li>
        {% endfor %}
        </ul>
    {% endfor %}
    
    </body>
    </html>
    """)

    html_content = template.render(
        qtd_por_cargo=qtd_por_cargo,
        partidos_prefeito=partidos_prefeito,
        qtd_por_faixa_etaria=qtd_por_faixa_etaria,
        percentual_instrucao=percentual_instrucao,
        percentual_genero=percentual_genero,
        percentual_estado_civil=percentual_estado_civil
    )
    
    with open("estatisticas_completas.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print("Página HTML 'estatisticas_completas.html' gerada com sucesso.")

gerar_html_estatisticas(df)
