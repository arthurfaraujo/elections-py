from jinja2 import Template
import elections.elec_data as ed
import os
from webbrowser import open_new as op

def gen_statistics_html() -> str:
    qtd_por_cargo = ed.role_quantity_count()
    partidos_prefeito = ed.parties_with_mayor_candidates()
    qtd_por_faixa_etaria = ed.quantity_by_age_group()
    percentual_instrucao = {cargo: ed.percentage_by_category('DS_GRAU_INSTRUCAO', cargo) for cargo in ed.roles()}
    percentual_genero = {cargo: ed.percentage_by_category('DS_GENERO', cargo) for cargo in ed.roles()}
    percentual_estado_civil = {cargo: ed.percentage_by_category('DS_ESTADO_CIVIL', cargo) for cargo in ed.roles()}

    template = Template("""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Estatísticas Eleitorais - Eleições 2024</title>
</head>

<body class="container mx-auto">
    <h1 class="py-4 font-bold text-gray-700 text-2xl text-center border-b">Estatísticas de Candidatos - Eleições 2024</h1>
    <div class="mt-8 flex flex-col mx-auto max-w-[800px]">
        
        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Quantidade de Candidatos por Cargo</h2>
            <ul>
                {% for cargo, qtd in qtd_por_cargo.items() %}
                <li class="flex justify-between"><span class="font-semibold text-gray-600">{{ cargo }}:</span> <span>{{ qtd }}</span></li>
                {% endfor %}
            </ul>
        </div>

        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Partidos com Candidatos ao Cargo de Prefeito</h2>
            <ul class="flex flex-wrap">
                {% for partido in partidos_prefeito %}
                <li class="hover:scale-105 cursor-default duration-300 border p-4 rounded m-2 grow">{{ partido }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Quantidade de Candidatos por Faixa Etária</h2>
            <ul>
                {% for faixa, qtd in qtd_por_faixa_etaria.items() %}
                <li class="flex justify-between"><span class="font-semibold text-gray-600">{{ faixa }}:</span> <span>{{ qtd }}</span></li>
                {% endfor %}
            </ul>
        </div>

        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Percentual de Candidatos por Cargo e Grau de Instrução</h2>
            {% for cargo, percentuais in percentual_instrucao.items() %}
            <h3 class="text-gray-600 font-bold mt-8 text-lg">{{ cargo }}</h3>
            <ul>
                {% for categoria, percentual in percentuais.items() %}
                <li class="flex justify-between"><span class="font-semibold text-gray-600">{{ categoria }}:</span> <span>{{ "%.2f" % percentual }}%</span></li>
                {% endfor %}
            </ul>
            {% endfor %}
        </div>
    
        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Percentual de Candidatos por Cargo e Gênero</h2>
            {% for cargo, percentuais in percentual_genero.items() %}
            <h3 class="text-gray-600 font-bold mt-8 text-lg">{{ cargo }}</h3>
            <ul>
                {% for categoria, percentual in percentuais.items() %}
                <li class="flex justify-between"><span class="font-semibold text-gray-600">{{ categoria }}:</span> <span>{{ "%.2f" % percentual }}%</span></li>
                {% endfor %}
            </ul>
            {% endfor %}
        </div>

        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Percentual de Candidatos por Cargo e Estado Civil</h2>
            {% for cargo, percentuais in percentual_estado_civil.items() %}
            <h3 class="text-gray-600 font-bold mt-8 text-lg">{{ cargo }}</h3>
            <ul>
                {% for categoria, percentual in percentuais.items() %}
                <li class="flex justify-between"><span class="font-semibold text-gray-600">{{ categoria }}:</span> <span>{{ "%.2f" % percentual }}%</span></li>
                {% endfor %}
            </ul>
            {%endfor %}
        </div>
    </div>
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
    
    return "html/stats.html"

def open_file(relPath: str):
  op(os.path.abspath(relPath))

def open_url(url: str):
  op(url)
  
def create_html_dir():
    if not os.path.exists("html"):
      os.makedirs("html")
      