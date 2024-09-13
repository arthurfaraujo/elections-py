from pandas import DataFrame
from jinja2 import Template
import elections.elec_data as ed

def gen_statistics_html():
    qtd_por_cargo = ed.role_quantity_count()
    partidos_prefeito = ed.parties_with_mayor_candidates()
    qtd_por_faixa_etaria = ed.quantity_by_age_group()
    percentual_instrucao = {cargo: ed.percentage_by_category('DS_GRAU_INSTRUCAO', cargo) for cargo in ed.roles()}
    percentual_genero = {cargo: ed.percentage_by_category('DS_GENERO', cargo) for cargo in ed.roles()}
    percentual_estado_civil = {cargo: ed.percentage_by_category('DS_ESTADO_CIVIL', cargo) for cargo in ed.roles()}

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
    
    with open("html/stats.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print("Página HTML 'stats.html' gerada com sucesso.")
