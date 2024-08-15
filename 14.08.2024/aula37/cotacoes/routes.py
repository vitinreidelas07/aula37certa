from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
import requests

def get_currency_rates():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    response = requests.get(url)
    data = response.json()

    rates = {
            "USD_BRL": f'{float(data["USDBRL"]["bid"]):.2f}',
            "EUR_BRL": f'{float(data["EURBRL"]["bid"]):.2f}',
            "BTC_BRL": f'{float(data["BTCBRL"]["bid"]):.2f}',
        }
    print(rates)
    return rates
# Criando o Blueprint para o clima
cotacoes_bp = Blueprint('cotacoes', __name__, template_folder='templates/cotacoes')

# Rota para renderizar a página de cotações
@cotacoes_bp.route('/cotacoes')
def cotacoes():
    return render_template('cotacoes/cotacoes.html')

# Rota para fornecer as cotações em formato JSON
@cotacoes_bp.route('/rates')
def rates():
    return jsonify(get_currency_rates())