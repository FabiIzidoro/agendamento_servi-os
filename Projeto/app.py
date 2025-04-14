from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form['nome']
    placa = request.form['placa']
    tipo_servico = request.form['tipo_servico']
    data_desejada = request.form['data_desejada']

    return render_template('sucesso.html', nome=nome)

if __name__ == '__main__':
    app.run(debug=True)
