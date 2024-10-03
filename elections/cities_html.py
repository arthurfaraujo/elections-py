import logging
from flask import Flask, render_template_string, request
from elections.elec_data import cities, roles_by_city, social_medias_by_code, candidate_by_code
import unicodedata

app = Flask(__name__)

# Desativa os logs no terminal
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

cities_df = cities()

@app.route('/')
def index():
    lista_municipios = "<ul class='flex flex-wrap gap-2'>"
    for municipio in cities_df:
        lista_municipios += f"<li class='flex grow'><a class='justify-center p-2 gap-0 hover:scale-105 rounded border duration-300 text-center flex w-full h-full' href='/municipio?municipio={municipio}'>{municipio.title()}</a></li>"
    lista_municipios += "</ul>"
    return render_template_string("""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="UTF-8">
    <title>Municípios</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="container mx-auto">
    <h1 class="py-4 font-bold text-gray-700 text-2xl text-center border-b">Lista de Municípios</h1>
    <div class="flex mx-auto justify-center max-w-[700px] mt-4">{{ lista_municipios | safe }}</div>
</body>
</html>
    """, lista_municipios=lista_municipios)


def remover_acentos(tuple):
    # Removendo acentos para ordenar alfabeticamente sem interferir na ordem
    # Usando tupla porque estou pegando uma tupla com o nome e o numero do candidato
    return ''.join(
        c for c in unicodedata.normalize('NFD', tuple[0])
        if unicodedata.category(c) != 'Mn'
    )

@app.route('/municipio')
def municipio():
    municipio = request.args.get('municipio')
    if municipio not in cities_df:
        return "Município não encontrado", 404
    else:
        candidates_city = roles_by_city(municipio)
        
        prefeitos = ""
        for prefeito, numero in sorted(candidates_city['prefeitos'], key=remover_acentos):
            prefeitos += f"<li><a class='flex w-full p-1 px-2 hover:bg-gray-200 border duration-300 text-center' href='/candidato?id={numero}&cargo=Prefeito&municipio={municipio}'>{prefeito.title()}</a></li>"
        
        vice_prefeitos = ""
        for vice_prefeito, numero in sorted(candidates_city['vice_prefeitos'], key=remover_acentos):
            vice_prefeitos += f"<li><a class='flex w-full p-1 px-2 hover:bg-gray-200 border duration-300 text-center' href='/candidato?id={numero}&cargo=Vice-Prefeito&municipio={municipio}'>{vice_prefeito.title()}</a></li>"
        
        
        vereadores = ""
        for vereador, numero in sorted(candidates_city['vereadores'], key=remover_acentos):
            vereadores += f"<li><a class='flex w-full p-1 px-2 hover:bg-gray-200 border duration-300 text-center' href='/candidato?id={numero}&cargo=Vereador&municipio={municipio}'>{vereador.title()}</a></li>"
        
        
        return render_template_string("""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>Estatísticas Eleitorais - Eleições 2024</title>
</head>

<body class="container mx-auto flex flex-col">
    <div class='flex flex-col items-center sticky py-4 top-0 backdrop-blur border-b'>
        <h1 class="font-bold text-gray-700 text-2xl text-center">{{ nome_municipio }}</h1>
        <a class="bg-white hover:bg-gray-200 duration-300 mt-4 mx-auto w-fit px-8 py-1 text-gray-700 text-center rounded border" href="/">Voltar para página inicial</a>
    </div>
    <div class="mt-4 flex flex-col mx-auto">
        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Prefeito:</h2>
            <ul>{{ prefeito | safe }}</ul>
        </div>

        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Vice-Prefeito:</h2>
            <ul>{{ vice_prefeito | safe }}</ul>
        </div>

        <div class="border p-4 rounded m-4">
            <h2 class="text-gray-600 text-center text-xl font-bold mb-4 pb-4 border-b">Vereadores:</h2>
            <ul>{{ vereadores | safe }}</ul>
        </div>
    </div>
</body>
</html>
        """, nome_municipio=municipio.title(), prefeito=prefeitos, vice_prefeito=vice_prefeitos, vereadores=vereadores)


@app.route('/candidato')
def candidato():
    id_candidato = request.args.get('id')
    cargo = request.args.get('cargo')
    municipio = request.args.get('municipio')
    imagem = f"https://raw.githubusercontent.com/davicesarmorais/fotos-candidatos-pb/main/fotos-candidatos-pb/FPB{id_candidato}_div.jpg"    
    link_redes = social_medias_by_code(int(id_candidato))
    candidato_df = candidate_by_code (int(id_candidato))
    NomeCandidato = candidato_df['Nome'].values[0]
    NomeUrna = candidato_df['Nome na urna'].values[0]
    NumeroCandidato = candidato_df['Número'].values[0]
    Partido = candidato_df['Partido'].values[0]
    SiglaPartido = candidato_df['SG_PARTIDO'].values[0]
    redes = ""
    
    # arthur nao apaga <-------------------------
    # variavel redes terá varias <li> com links
    for index, row in link_redes.iterrows():
        # index, row para iterar por cada indice e linha
        redes += f"<li><a class='flex w-full p-1 px-2 hover:bg-gray-200 border duration-300' href='{row['Link da rede social']}'>{row['Link da rede social']}</a></li>"
        #row['Link da rede social'] para percorrer justamente por essa coluna

    return render_template_string("""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>{{ NomeCandidato }}</title>
</head>
<body class="container mx-auto flex flex-col">
    <div class='flex flex-col items-center sticky py-4 top-0 backdrop-blur border-b'>
        <h1 class="font-bold text-gray-700 text-2xl text-center">({{ NumeroCandidato }}) {{ NomeCandidato }} - {{ cargo }}</h1>
        <a class="bg-white hover:bg-gray-200 duration-300 mt-4 mx-auto w-fit px-8 py-1 text-gray-700 text-center rounded border" href="/municipio?municipio={{ municipio }}">Voltar para o município</a>
    </div>
    
    
    <div class="flex gap-12 justify-center mt-8">
        <img class="hidden sm:block rounded w-48 h-48 object-cover" src="{{ imagem }}">
        <div class="text-center sm:text-left">
            <h2 class="font-bold text-gray-600 text-xl">{{ NomeUrna }} | {{ Partido }} ({{ SiglaPartido }})</h2>
            <p class="font-semibold text-gray-500 mt-2 mb-4">Candidato a {{ cargo }} no município de {{ municipio }}.</p>
            <ul class="flex flex-col border p-4 rounded">
                <h3 class="text-gray-600 font-bold text-lg border-b pb-2 mb-4">Redes sociais</h3>
                {{ link_redes | safe }}
            </ul>
        </div>
    </div>
</body>
</html>
    """, link_redes=redes, imagem=imagem, id_candidato=id_candidato, cargo=cargo, municipio=municipio, NomeCandidato=NomeCandidato.title(), NomeUrna=NomeUrna.title(), NumeroCandidato=NumeroCandidato, Partido=Partido.title(), SiglaPartido=SiglaPartido)


def start_flask():
    app.run(debug=False, use_reloader=False)
