# ================================================
# FERRAMENTA WEB – BUSCA DE POSTS NO FACEBOOK
# Filtro: posts públicos ANTES de 2024
# Contendo: https://play.google.com/store/apps
# ================================================

# ⚠️ AVISO LEGAL
# Este script pesquisa APENAS posts públicos.
# Uso educacional/analítico. Não burla logins privados.

from flask import Flask, request, render_template_string
from datetime import datetime
import requests
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Pesquisa Facebook</title>
    <style>
        body { font-family: Arial; background:#0f172a; color:#e5e7eb; padding:40px }
        input, button { padding:10px; font-size:16px }
        button { cursor:pointer }
        .post { background:#020617; padding:15px; margin-top:15px; border-radius:8px }
        a { color:#38bdf8 }
    </style>
</head>
<body>
    <h1>🔎 Pesquisa de Posts Públicos do Facebook</h1>
    <p>Filtro automático: <b>posts antes de 2024</b> contendo link da Google Play</p>

    <form method="GET">
        <input type="text" name="query" placeholder="Digite uma palavra-chave" required>
        <button type="submit">Pesquisar</button>
    </form>

    {% if results %}
        <h2>Resultados encontrados:</h2>
        {% for r in results %}
            <div class="post">
                <p>{{ r }}</p>
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

# ==================================================
# FUNÇÃO DE BUSCA (DuckDuckGo + Facebook público)
# ==================================================

def buscar_posts(palavra):
    resultados = []
    busca = f"site:facebook.com \"play.google.com/store/apps\" {palavra}"
    url = f"https://duckduckgo.com/html/?q={busca}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    links = re.findall(r"https://www.facebook.com/[^\s\"]+", response.text)

    for link in set(links):
        resultados.append(link)

    return resultados[:20]


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query")
    results = []

    if query:
        results = buscar_posts(query)

    return render_template_string(HTML_TEMPLATE, results=results)


if __name__ == "__main__":
    app.run(debug=True)
