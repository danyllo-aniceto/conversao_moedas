from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def obter_taxa(moeda):
    url = "https://api.exchangerate-api.com/v4/latest/BRL"  # API para obter taxas em relação ao Real
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        if moeda == 1:  # Real
            return 1.00, "Real(ais)"
        elif moeda == 2:  # Dólar
            return dados['rates']['USD'], "Dólar(es)"
        elif moeda == 3:  # Euro
            return dados['rates']['EUR'], "Euro(s)"
    return None, None

def conversao_moeda(moeda_base, moeda_alvo, valor):
    taxa_base, nome_base = obter_taxa(moeda_base)
    taxa_alvo, nome_alvo = obter_taxa(moeda_alvo)

    if taxa_alvo is None or taxa_base is None:
        return None, None, None
    # Ajuste na fórmula de conversão
    resultado = valor * (taxa_alvo / taxa_base)
    return resultado, nome_base, nome_alvo

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = ""
    if request.method == 'POST':
        moeda_base = int(request.form['moeda_base'])
        moeda_alvo = int(request.form['moeda_alvo'])
        valor = float(request.form['valor'])

        resultado_conversao, nome_base, nome_alvo = conversao_moeda(moeda_base, moeda_alvo, valor)

        if resultado_conversao is not None:
            resultado = f"{valor} {nome_base} equivale a {resultado_conversao:.2f} {nome_alvo}."
        else:
            resultado = "Erro ao obter taxas de câmbio."

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
