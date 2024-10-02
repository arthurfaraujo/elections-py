import logging
from flask import Flask, render_template_string, request
from elections.elec_data import cities, roles_by_city, social_medias_by_code, candidate_by_code

app = Flask(__name__)

# Desativa os logs no terminal
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True


cities_df = cities()

@app.route('/')
def index():
    lista_municipios = "<ul>"
    for municipio in cities_df:
        lista_municipios += f"<li><a href='/municipio?municipio={municipio}'>{municipio}</a></li>"
    lista_municipios += "</ul>"
    return render_template_string("""
    <html>
    <head><title>Municípios</title></head>
    <body>
        <h1>Lista de Municípios</h1>
        {{ lista_municipios | safe }}
    </body>
    </html>
    """, lista_municipios=lista_municipios)


@app.route('/municipio')
def municipio():
    municipio = request.args.get('municipio')
    if municipio not in cities_df:
        return "Município não encontrado", 404
    else:
        candidates_city = roles_by_city(municipio)
        
        prefeitos = ""
        for prefeito in candidates_city['prefeitos']:
            prefeitos += f"<li><a href='/candidato?id={prefeito[1]}&cargo=Prefeito&municipio={municipio}'>{prefeito[0]}</a></li>"
        
        vice_prefeitos = ""
        for vice_prefeito in candidates_city['vice_prefeitos']:
            vice_prefeitos += f"<li><a href='/candidato?id={vice_prefeito[1]}&cargo=Vice-Prefeito&municipio={municipio}'>{vice_prefeito[0]}</a></li>"
        
        
        vereadores = ""
        for vereador in candidates_city['vereadores']:
            vereadores += f"<li><a href='/candidato?id={vereador[1]}&cargo=Vereador&municipio={municipio}'>{vereador[0]}</a></li>"
        
        
        return render_template_string("""
        <html>
        <head><title>{{ nome_municipio }}</title></head>
        <body>
            <h1>{{ nome_municipio }}</h1>
            <a href="/">Voltar</a>
            <h2>Prefeito:</h2>
            <ul>{{ prefeito | safe }}</ul>
            <h2>Vice-Prefeito:</h2>
            <ul>{{ vice_prefeito | safe }}</ul>
            <h2>Vereadores:</h2>
            <ul>{{ vereadores | safe }}</ul>
        </body>
        </html>
        """, nome_municipio=municipio, prefeito=prefeitos, vice_prefeito=vice_prefeitos, vereadores=vereadores)


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
    SiglaPartido = candidato_df['Sigla do Partido'].values[0]
    redes = ""
    # arthur nao apaga <-------------------------
    # variavel redes terá varias <li> com links
    for index, row in link_redes.iterrows():
        # index, row para iterar por cada indice e linha
        redes += f"<li><a href='{row['Link da rede social']}'>{row['Link da rede social']}</a></li>"
        #row['Link da rede social'] para percorrer justamente por essa coluna

    return render_template_string("""
    <html>
    <head><title>{{ NomeCandidato }}</title></head>
    <body>
        <h1> ({{ NumeroCandidato }}) {{ NomeCandidato }} - {{ cargo }}</h1>
        <p>Candidato a {{ cargo }} no município de {{ municipio }}.</p>
        <p>{{ NomeUrna }} | {{ Partido }} ({{ SiglaPartido }})</p>
        <img src="{{ imagem }}"> <br>
        <ul>{{ link_redes | safe }}</ul>
        <a href="/municipio?municipio={{ municipio }}">Voltar para o município</a>
    </body>
    </html>
    """, link_redes=redes, imagem=imagem, id_candidato=id_candidato, cargo=cargo, municipio=municipio, NomeCandidato=NomeCandidato, NomeUrna=NomeUrna, NumeroCandidato=NumeroCandidato, Partido=Partido, SiglaPartido=SiglaPartido)


def start_flask():
    app.run(debug=False, use_reloader=False)
