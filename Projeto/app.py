from flask import Flask, render_template, request, redirect, url_for
import os
import time  # Importar para gerar o timestamp

app = Flask(__name__)

# Definindo a pasta para salvar as imagens
UPLOAD_FOLDER = os.path.join('static', 'uploads')  # Caminho correto para a pasta 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Verificar se a pasta existe, se não, cria
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Cria a pasta uploads caso não exista

@app.route('/')
def index():
    return redirect(url_for('inicio'))  # Redireciona para a página inicial

@app.route('/inicio')
def inicio():
    return render_template('paginainicial.html')  # Página inicial de boas-vindas

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        # Coleta dos dados do formulário
        nome = request.form['nome']
        matricula = request.form['matricula']
        placa = request.form['placa']
        tipo_servico = request.form['tipo_servico']
        data_desejada = request.form['data_desejada']
        urgencia = request.form['urgencia']
        descricao_servico = request.form.get('descricao_servico', None)  # Para o campo 'Outro'

        # Verificar se foi feito upload de uma imagem
        if 'foto_servico' in request.files:
            foto_servico = request.files['foto_servico']
            if foto_servico.filename != '':
                # Obtém a extensão do arquivo (ex: .jpg, .png)
                file_extension = os.path.splitext(foto_servico.filename)[1]
                
                # Gerar um nome único para o arquivo usando nome, matrícula e timestamp
                timestamp = str(int(time.time()))  # Usando timestamp para garantir um nome único
                filename = f"{nome}_{matricula}_{timestamp}{file_extension}"
                
                # Caminho onde a imagem será salva
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Salvar a imagem
                foto_servico.save(foto_path)
            else:
                foto_path = None  # Caso não tenha foto
        else:
            foto_path = None  # Caso não tenha foto

        # Redirecionar para a página de sucesso com os dados coletados
        return render_template(
            'sucesso.html',
            nome=nome,
            matricula=matricula,
            placa=placa,
            tipo_servico=tipo_servico,
            descricao_servico=descricao_servico,
            urgencia=urgencia,
            data_desejada=data_desejada,
            foto_path=foto_path  # Enviar o caminho da foto
        )
    return render_template('agendamento.html')  # Página com o formulário de agendamento

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Configuração para rodar na porta 8080
