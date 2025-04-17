from flask import Flask, render_template, request, redirect, url_for
import os
import time  # Para gerar o timestamp
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Definindo a pasta para salvar as imagens
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuração para o tamanho máximo do arquivo (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB

# Verificar se a pasta existe, se não, cria
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta uploads caso não exista

@app.route('/')
def index():
    return redirect(url_for('inicio'))  # Redireciona para a página de boas-vindas (início)

@app.route('/inicio')
def inicio():
    return render_template('paginainicial.html')  # Página de boas-vindas com o botão de agendamento

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        # Coleta dos dados do formulário
        nome = request.form['nome']
        matricula = request.form['matricula']
        placa = request.form['placa']
        frota = request.form['frota']
        veiculo = request.form['veiculo']
        tipo_servico = request.form['tipo_servico']
        data_desejada = request.form['data_desejada']
        urgencia = request.form['urgencia']
        descricao_servico = request.form.get('descricao_servico', None)

        # Verificar se foi feito upload de uma imagem
        foto_path = None
        if 'foto_servico' in request.files:
            foto_servico = request.files['foto_servico']
            if foto_servico.filename != '':
                # Validar se a extensão do arquivo é permitida
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                file_extension = foto_servico.filename.rsplit('.', 1)[1].lower()
                
                if file_extension in allowed_extensions:
                    # Gerar um nome único para o arquivo usando nome, matrícula e timestamp
                    timestamp = str(int(time.time()))
                    filename = f"{nome}_{matricula}_{timestamp}.{file_extension}"
                    foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    foto_servico.save(foto_path)
                else:
                    return "Formato de arquivo inválido. Aceito apenas PNG, JPG, JPEG, GIF.", 400
            else:
                foto_path = None
        else:
            foto_path = None

        # Redirecionar para a página de sucesso com os dados coletados
        return render_template(
            'sucesso.html',
            nome=nome,
            matricula=matricula,
            placa=placa,
            frota=frota,
            veiculo=veiculo,
            tipo_servico=tipo_servico,
            descricao_servico=descricao_servico,
            urgencia=urgencia,
            data_desejada=data_desejada,
            foto_path=foto_path
        )

    return render_template('agendamento.html')  # Página com o formulário de agendamento

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)  # Desativar o modo debug para testar
