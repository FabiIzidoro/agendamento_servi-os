from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Definindo pasta para salvar as imagens
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verificar se a pasta existe, se não, cria
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form['nome']
    matricula = request.form['matricula']
    placa = request.form['placa']
    tipo_servico = request.form['tipo_servico']
    data_desejada = request.form['data_desejada']

    # Verificar se foi feito upload de uma imagem
    if 'foto_servico' in request.files:
        foto_servico = request.files['foto_servico']
        if foto_servico.filename != '':
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_servico.filename)
            foto_servico.save(foto_path)
        else:
            foto_path = None
    else:
        foto_path = None

    return render_template(
        'sucesso.html',
        nome=nome,
        matricula=matricula,
        placa=placa,
        tipo_servico=tipo_servico,
        data_desejada=data_desejada,
        foto_path=foto_path  # Enviar o caminho da foto
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Configuração para rodar na porta 8080
