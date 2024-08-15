#configuração pasica até a linha 13

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
from datetime import datetime
from cotacoes.routes import cotacoes_bp  # Importando o Blueprint
from flask import Flask, render_template, jsonify # Importe o modulo jsonify
from weather.routes import weather_bp  # Importando o Blueprint

app = Flask(__name__)
app.config["SECRET_KEY"] = "sua_chave_secreta"  # Substitua por uma chave secreta segura
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///livros.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

#definir modelo de dados ---> criar a classe livros até a linha 35

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    editora = db.Column(db.String(200), default="Sem Editora")
    ativo = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, autor, categoria, ano, editora="Sem Editora", ativo=False):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.ano = ano
        self.editora = editora
        self.ativo = ativo

    def __repr__(self):
        return f"<Livro {self.titulo}>"
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

# ### **Adicionar o Modelo `Reservation`** No arquivo `app.py`, crie o modelo `Reservation`
# para reservar livros

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    date_reserved = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id    
    #criar tabela e inserir dados iniciais 

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(150), nullable=False, unique=True)
    biografia = db.Column(db.String(150), nullable=False)
    def __init__(self, autor, biografia):
        self.autor = autor
        self.biografia = biografia  

with app.app_context():
    db.create_all()

    # Ler o arquivo CSV para um DataFrame
    df = pd.read_csv("tabela - livros.csv")

    # Adicionar cada livro à base de dados, se ainda não estiverem presentes até a linha 57

    for index, row in df.iterrows():
        if not Livro.query.filter_by(titulo=row["Titulo do Livro"]).first():
            livro = Livro(
                titulo=row["Titulo do Livro"],
                autor=row["Autor"],
                categoria=row["Categoria"],
                ano=row["Ano de Publicação"],
                ativo=row["Ativo"] == "TRUE",
            )
            db.session.add(livro)
    db.session.commit()

#### Criar as Rotas para o Site ----> 1. **Rota `/inicio`:** 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/tempo')
def home():
    return render_template('weather.html')

@app.route('/dashboard')
def victor():
    return render_template('dashboard.html')


# 2. **Rota `/curriculo`:** -----> Crie uma rota para a página de currículo:   





@app.route("/curriculo")
def curriculo():
    return render_template("curriculo.html")

# 3. **Rota `/novo`:** ---> Crie uma rota para a página de adicionar novos livros:



# 4. **Rota `/criar`:**-----> Crie uma rota para processar o formulário e salvar o novo livro:



# 2. **Adicionar a Rota para Deletar Livros:** -----> Adicione o seguinte código no `app.py` para criar a rota de deleção:



#  Adicionar uma Rota para Exibir o Formulário de Edição para atualizar livros 



### 3. **Adicionar a Rota para Processar a Atualização** 1. **Adicionar a Rota `/atualizar/<int:id>` no `app.py`:**


# 1. **Importações Necessárias e Configurações:** ------> No `app.py`, importe as bibliotecas necessárias e configure o Flask-Login.
       # estão nas linhas 8 a 16

#2. **Criação do Modelo de Usuário:**
    # Adicione um modelo de usuário para armazenar informações de login.



# 3. **Carregar Usuário:**
    # Adicione a função para carregar um usuário por ID.



### 3. **Criação da Tela de Login**

# 1. **Rota de Login:**
    # Crie uma rota para exibir o formulário de login e processar o login.

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("inicio"))
        else:
            flash("Login ou senha incorretos. Tente novamente.")
    return render_template("login.html")




@app.route("/inicio")
@login_required
def inicio():
    livros = Livro.query.all()
    return render_template("lista.html", lista_de_livros=livros)

@app.route("/novo")
@login_required
def novo():
    return render_template("novo.html", titulo="Novo Livro")


@app.route("/autor", methods=["GET", "POST"])
@login_required
def autor():
    if request.method == "POST":
        autor = request.form["nome"]
        biografia = request.form["biografia"]
        autor = Autor(autor=autor, biografia=biografia)
        db.session.add(autor)
        db.session.commit()
        flash("Autor cadastrado com sucesso!")
        return redirect(url_for("inicio"))  # Redireciona para uma página de sua escolha

    return render_template("autor.html")

@app.route("/criar", methods=["POST"])
@login_required
def criar():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    categoria = request.form["categoria"]
    ano = request.form["ano"]
    editora = request.form["editora"]
    livro = Livro(titulo=titulo, autor=autor, categoria=categoria, ano=ano, editora=editora)
    db.session.add(livro)
    db.session.commit()
    return redirect(url_for("inicio"))

@app.route("/editar/<int:id>")
@login_required
def editar(id):
    livro = Livro.query.get(id)
    if livro:
        return render_template("editar.html", livro=livro)
    return redirect(url_for("inicio"))

@app.route("/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar(id):
    livro = Livro.query.get(id)
    if livro:
        livro.titulo = request.form["titulo"]
        livro.autor = request.form["autor"]
        livro.categoria = request.form["categoria"]
        livro.ano = request.form["ano"]
        livro.editora = request.form["editora"]
        db.session.commit()
    return redirect(url_for("inicio"))

@app.route("/deletar/<int:id>")
@login_required
def deletar(id):
    livro = Livro.query.get(id)
    if livro:
        db.session.delete(livro)
        db.session.commit()
    return redirect(url_for("inicio"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

#2. **Adicionar Link de Logout:**
    # Adicione um link de logout em uma área visível da aplicação, como em um menu de navegação.





#### 4.5 Iniciar o Servidor Flask ---> 1. **Adicionar o Código para Rodar o Servidor:**
    # No final do `app.py`, adicione o seguinte código para iniciar o servidor Flask:





### 2. **Criar a Rota e Página de Listagem de Livros para Reserva** Crie uma nova rota para exibir os livros disponíveis para reserva:

@app.route("/reservar", methods=["GET"])
@login_required
def reservar():
    livros = Livro.query.all()  # Pega todos os livros
    return render_template("reservar.html", livros=livros)


# criando a rota para processar a reserva

@app.route("/fazer_reserva/<int:book_id>")
@login_required
def fazer_reserva(book_id):
    # Verifica se o livro já foi reservado pelo usuário
    reserva_existente = Reservation.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if reserva_existente:
        flash("Você já reservou este livro.")
        return redirect(url_for("reservar"))

    # Criação de uma nova reserva
    nova_reserva = Reservation(user_id=current_user.id, book_id=book_id)
    db.session.add(nova_reserva)
    db.session.commit()
    flash("Reserva realizada com sucesso!")
    return redirect(url_for("reservar"))


# - **Verificações:**     - Antes de criar uma nova reserva, o sistema verifica se o usuário já reservou o livro para evitar duplicatas.

### 4. **Visualizar Reservas** Adicione uma rota para visualizar as reservas de um usuário:

@app.route("/minhas_reservas")
@login_required
def minhas_reservas():
    reservas = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template("minhas_reservas.html", reservas=reservas)


#  Criando Rota para DashBoard

@app.route("/dashboard")
@login_required
#@admin_required
def dashboard():
    # Totalizadores
    total_livros = Livro.query.count()
    total_usuarios = User.query.count()
    total_reservas = Reservation.query.count()

    # Dados para os gráficos
    livros_por_autor = db.session.query(Livro.autor, db.func.count(Livro.id)).group_by(Livro.autor).all()
    livros_por_ano = db.session.query(Livro.ano, db.func.count(Livro.id)).group_by(Livro.ano).all()
    livros_por_editora = db.session.query(Livro.editora, db.func.count(Livro.id)).group_by(Livro.editora).all()

    return render_template("dashboard.html",
                           total_livros=total_livros,
                           total_usuarios=total_usuarios,
                           total_reservas=total_reservas,
                           livros_por_autor=livros_por_autor,
                           livros_por_ano=livros_por_ano,
                           livros_por_editora=livros_por_editora)

# Registrando o Blueprint
app.register_blueprint(cotacoes_bp)
app.register_blueprint(weather_bp)

if __name__ == "__main__":
    app.run(debug=True)


