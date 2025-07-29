from flask import render_template, url_for, redirect, session, request, flash
from ecommerce import app, databse, bcrypt
from ecommerce.models import Usuario, Produto
from flask_login import login_required, login_user, logout_user, current_user
from ecommerce.forms import FormLogin, FormCriarConta, FormProduto


@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", usuario=usuario.username))

    return render_template("homepage.html", form=formlogin)

    # PAGINA DE CADASTRO


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    formcriarConta = FormCriarConta()
    if formcriarConta.validate_on_submit():
        senha = bcrypt.generate_password_hash(
            formcriarConta.senha.data).decode('utf-8')
        usuario = Usuario(
            username=formcriarConta.username.data,
            password=senha,
            email=formcriarConta.email.data
        )
        databse.session.add(usuario)
        databse.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", usuario=usuario.username))
    return render_template("pagecadastro.html", form=formcriarConta)


@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
    return render_template("perfil.html", usuario=usuario)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/vitrine")
@login_required
def vitrine():
    produtos = Produto.query.all()
    return render_template("vitrine.html", produtos=produtos)


@app.route('/adicionar_carrinho/<int:produto_id>')
@login_required
def adicionar_carrinho(produto_id):
    carrinho = session.get('carrinho', {})
    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        carrinho[produto_id_str] += 1
    else:
        carrinho[produto_id_str] = 1

    session['carrinho'] = carrinho
    flash("Produto adicionado ao carrinho!", "success")
    return redirect(url_for('vitrine'))


@app.route("/carrinho")
@login_required
def ver_carrinho():
    carrinho = session.get('carrinho', {})
    produtos_carrinho = []

    for produto_id_str, quantidade in carrinho.items():
        produto = Produto.query.get(int(produto_id_str))
        if produto:
            produtos_carrinho.append({
                'produto': produto,  #  Adiciona o produto ao dicionário
                'quantidade': quantidade,
                'total': produto.valor * quantidade
            })

    total_geral = sum(item['total'] for item in produtos_carrinho)
    return render_template('carrinho.html', produtos_carrinho=produtos_carrinho, total_geral=total_geral)


@app.route('/remover_carrinho/<int:produto_id>')
@login_required
def remover_carrinho(produto_id):
    carrinho = session.get('carrinho', {})
    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        del carrinho[produto_id_str]
        session['carrinho'] = carrinho
        flash("Produto removido do carrinho.", "info")
    return redirect(url_for('ver_carrinho'))


@app.route("/adicionar-produto", methods=["GET", "POST"])
@login_required
def adicionar_produto():
    form = FormProduto()
    if form.validate_on_submit():
        novo_produto = Produto(
            nome=form.nome.data,
            valor=form.valor.data,
            usuario=current_user
        )
        databse.session.add(novo_produto)
        databse.session.commit()
        flash("Produto adicionado com sucesso!", "success")
        return redirect(url_for("vitrine"))
    return render_template("adicionar_produto.html", form=form)


@app.route('/finalizar_compra', methods=['POST'])
@login_required
def processar_finalizacao():
    rua = request.form.get('rua')
    numero = request.form.get('numero')
    cep = request.form.get('cep')
    bairro = request.form.get('bairro')
    complemento = request.form.get('complemento')

    session.pop('carrinho', None)

    return render_template("pedido_confirmado.html",
                           rua=rua,
                           numero=numero,
                           cep=cep,
                           bairro=bairro,
                           complemento=complemento)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        endereco = request.form.get('endereco')
        session.pop('carrinho', None)
        return render_template("pedido_confirmado.html", endereco=endereco)
    return render_template("finalizar_compra.html")
