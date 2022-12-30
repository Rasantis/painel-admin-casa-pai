from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
import datetime
import magic



app = Flask(__name__)
# caminho da pasta na hospedagem
#UPLOAD_FOLDER = '/home/Rasantis/mysite/repositorio'
#UPLOAD_FOLDER = 'repositorio' #Caminho máquina local
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'repositorio')
UPLOAD_FOLDER = 'repositorio'


# Definindo a lista de usuarios e senhas validos
users = [
    {"username": "admin", "password": "1234"},
    {"username": "user1", "password": "abcd"},
    {"username": "user2", "password": "efgh"},
]

# Rota para exibir o formulario de login


@app.route("/login", methods=["GET"])
def login_form():
    return render_template("index.html")

# Rota para processar o login do usuario


@app.route("/login", methods=["POST"])
def login_submit():
    # Obtendo os valores do formulario de login
    input_username = request.form["username"]
    input_password = request.form["password"]

    # Verificando se o usuario e senha digitados sao validos
    for user in users:
        if input_username == user["username"] and input_password == user["password"]:
            # return "Voce foi autorizado"

            return render_template("repositorio.html")

        if input_username != user["username"] and input_password != user["password"]:
            return render_template("error.html")


@app.route('/repositorio', methods=['POST'])
def upload():
    file = request.files['imagem']
    save_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(save_path)
    Nome = request.form.get("Nome")
    Email = request.form.get("email")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # with open('/home/Rasantis/mysite/submissions.txt', 'a+') as f:
    with open('submissions.txt', 'a+') as f:

        f.write('{} - {} - {} - {}\n'.format(Nome, Email, file.filename, time))
    return render_template("repositorio.html")


@app.route('/get-file/<filename>')
def get_file(filename):
    file = os.path.join(UPLOAD_FOLDER, filename)
    file_type = magic.from_file(file)
    return send_file(file, mimetype=file_type) 
# return send_file(file, mimetype="image/png|image/jpeg|text/csv|application/vnd.ms-excel|text/plain|application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") 

# @app.route('/arquivos')
# def show_repository():
#     files = os.listdir(UPLOAD_FOLDER)
#     return render_template('arquivos.html', files=files, os=os, UPLOAD_FOLDER=UPLOAD_FOLDER)

@app.route('/arquivos', methods=['GET', 'POST'])
def show_repository():
    print("UPLOAD_FOLDER:", UPLOAD_FOLDER)  # Imprime o valor de UPLOAD_FOLDER
    if request.method == 'GET':
        files = os.listdir(UPLOAD_FOLDER)
        return render_template('arquivos.html', files=files, os=os, UPLOAD_FOLDER=UPLOAD_FOLDER)
    elif request.method == 'POST':
        # Obter o nome do arquivo e o novo conteúdo do formulário
        file_name = request.form['file_name']
        print("file_name:", file_name)  # Imprime o valor de file_name
        new_content = request.form['new_content']

        # Lê o conteúdo atual do arquivo
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, 'r') as f:
            old_content = f.read()

        # Sobrescreve o conteúdo do arquivo com o novo conteúdo
        with open(file_path, 'w') as f:
            f.write(new_content)

        # Salva o arquivo
        f.save()

        return 'Arquivo editado com sucesso!'



if __name__ == "__main__":
    app.run(debug=True)
