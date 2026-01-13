from flask import Flask, request, render_template_string
import requests
import re
import os

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
                <a href="{{ r }}" target="_blank">{{ r }}</a>
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

def buscar_posts(palavra):
    busca = f'site:facebook.com "
