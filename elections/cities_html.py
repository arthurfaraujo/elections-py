import logging
from flask import Flask, render_template_string, request
from elections.elec_data import cities, roles_by_city

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
            prefeitos += f"<li><a href='/candidato?nome={prefeito}&cargo=Prefeito&municipio={municipio}'>{prefeito}</a></li>"
        
        vice_prefeitos = ""
        for vice_prefeito in candidates_city['vice_prefeitos']:
            vice_prefeitos += f"<li><a href='/candidato?nome={vice_prefeito}&cargo=Vice-Prefeito&municipio={municipio}'>{vice_prefeito}</a></li>"
        
        
        vereadores = ""
        for vereador in candidates_city['vereadores']:
            vereadores += f"<li><a href='/candidato?nome={vereador}&cargo=Vereador&municipio={municipio}'>{vereador}</a></li>"
        
        
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
    nome_candidato = request.args.get('nome')
    cargo = request.args.get('cargo')
    municipio = request.args.get('municipio')
    
    return render_template_string("""
    <html>
    <head><title>{{ nome_candidato }} - {{ cargo }}</title></head>
    <body>
        <h1>{{ nome_candidato }} - {{ cargo }}</h1>
        <p>Candidato a {{ cargo }} no município de {{ municipio }}.</p>
        <a href="/municipio?municipio={{ municipio }}">Voltar para o município</a>
    </body>
    </html>
    """, nome_candidato=nome_candidato, cargo=cargo, municipio=municipio)


def start_flask():
    app.run(debug=False, use_reloader=False)
