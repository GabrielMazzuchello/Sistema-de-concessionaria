import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Importação do ttk para o Treeview
import mysql.connector

# Conexão com o banco de dados
conexao_banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="concessionaria"
)

cursor = conexao_banco.cursor()

# Função para adicionar veículo
def cadastarVeiculo(placa, ano, marca, modelo, cor, categoria, preco, integridade):
    # Verifica se todos os campos foram preenchidos
    if placa and ano and marca and modelo and cor and categoria and preco and integridade:
        try:
            # Comando SQL de inserção
            comando = ("INSERT INTO veiculos (placa, ano, marca, modelo, cor, categoria, preco, integridade) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute(comando, (placa, ano, marca, modelo, cor, categoria, preco, integridade))
            conexao_banco.commit()
            # Exibe mensagem de sucesso
            messagebox.showinfo("Sucesso", "Carro cadastrado com sucesso!")
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro ao inserir o veículo: {erro}")
    else:
        # Se algum campo estiver em branco mostra a mensagem de erro
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos antes de adicionar o veículo.")

# Função para remover veículo
def removerVeiculo(placa) :
    print(type(placa))
    if placa :
        comando = ('SELECT * FROM veiculos WHERE placa = %s')
        cursor.execute(comando, (placa,))
        resultado = cursor.fetchone()

        if len(resultado) > 0:
            try:
                # Comando SQL para deletar
                comando = ("DELETE FROM veiculos WHERE placa = %s")
                cursor.execute(comando, (placa,))
                conexao_banco.commit()
                # Exibe mensagem de sucesso
                messagebox.showinfo("Sucesso", "Carro removido com sucesso!")
            except mysql.connector.Error as erro:
                messagebox.showerror("Erro", f"Erro ao remover o veículo: {erro}")
    else:
        # Se algum campo estiver em branco mostra a mensagem de erro
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos antes de remover o veículo.") 

# Função para remover veículo
def alterarVeiculo(placa, novo_preco=None, nova_cor=None, nova_integridade=None):
    if not placa:
        messagebox.showwarning("Atenção", "Por favor, informe a placa do veículo.")
        return
    
    try:
        # Verifique se o veículo existe
        cursor.execute("SELECT * FROM veiculos WHERE placa = %s", (placa,))
        if cursor.fetchone() is None:
            messagebox.showerror("Erro", "Veículo não encontrado.")
            return

        # Comando SQL para atualização parcial
        valores = []
        atualizacoes = []

        if novo_preco:
            atualizacoes.append("preco = %s")
            valores.append(novo_preco)
        if nova_cor:
            atualizacoes.append("cor = %s")
            valores.append(nova_cor)
        if nova_integridade:
            atualizacoes.append("integridade = %s")
            valores.append(nova_integridade)

        # Caso não haja nenhuma atualização, retorne
        if not atualizacoes:
            messagebox.showwarning("Atenção", "Nenhuma alteração foi especificada.")
            return

        # Monta o comando SQL dinâmico
        comando = f"UPDATE veiculos SET {', '.join(atualizacoes)} WHERE placa = %s"
        valores.append(placa)

        # Executa a atualização
        cursor.execute(comando, valores)
        conexao_banco.commit()
        messagebox.showinfo("Sucesso", "Veículo atualizado com sucesso!")
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro ao alterar o veículo: {erro}")

# Função para buscar o veículo pela placa e retornar os dados
def buscarVeiculo(placa):
    if not placa:
        messagebox.showwarning("Atenção", "Por favor, informe a placa do veículo.")
        return None

    try:
        # Busca o veículo pela placa
        cursor.execute("SELECT * FROM veiculos WHERE placa = %s", (placa,))
        veiculo = cursor.fetchone()

        if veiculo:
            return veiculo  # Retorna os dados do veículo como uma tupla
        else:
            messagebox.showerror("Erro", "Veículo não encontrado.")
            return None
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro ao buscar o veículo: {erro}")
        return None

def registrarVendaHistorico(placa, nome_cliente, cpf_cliente, vendedor):
    try:
        comando = ("INSERT INTO historico_vendas (placa, nome_cliente, cpf_cliente, vendedor, data_venda) "
                   "VALUES (%s, %s, %s, %s, NOW())")
        cursor.execute(comando, (placa, nome_cliente, cpf_cliente, vendedor))
        conexao_banco.commit()
        messagebox.showinfo("Sucesso", "Veículo vendido com sucesso e registrado no histórico!")
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro", f"Erro ao registrar a venda no histórico: {erro}")

def venderVeiculo(placa, nome_cliente, cpf_cliente, usuario):
    veiculo = buscarVeiculo(placa)
    
    if veiculo:
        # Exibe os dados do veículo para confirmação antes da venda
        tree.delete(*tree.get_children())
        tree.insert("", "end", values=veiculo)
        
        resposta = messagebox.askyesno("Confirmar Venda", "Deseja realmente vender este veículo?")
        if resposta:
            try:
                # Remove o veículo da tabela de veículos (simula a venda)
                cursor.execute("DELETE FROM veiculos WHERE placa = %s", (placa,))
                conexao_banco.commit()
                
                # Registra a venda no histórico de vendas
                registrarVendaHistorico(placa, nome_cliente, cpf_cliente, usuario)
                
            except mysql.connector.Error as erro:
                messagebox.showerror("Erro", f"Erro ao vender o veículo: {erro}")


def ocultar_todos_formularios():
    form_frame_add.pack_forget()
    form_frame_remove.pack_forget()
    form_frame_alterar.pack_forget()
    form_frame_venda.pack_forget()

def mostrar_formulario_add():
    ocultar_todos_formularios()
    form_frame_add.pack(side=tk.TOP, fill=tk.X) 

def mostar_formulario_remover():
    ocultar_todos_formularios()
    form_frame_remove.pack(side=tk.TOP, fill=tk.X)

def mostrar_formulario_alterar():
    ocultar_todos_formularios()
    form_frame_alterar.pack(side=tk.TOP, fill=tk.X)

def mostrar_formulario_venda():
    ocultar_todos_formularios()
    form_frame_venda.pack(side=tk.TOP, fill=tk.X)

# Função principal para a interface
def abrir_estoque():
    estoque_window = tk.Tk()
    estoque_window.title("Gerenciador de Estoque")
    estoque_window.geometry("800x500")
    login_window.destroy() #fecha a janela do login

    global form_frame_add, form_frame_remove, form_frame_alterar, form_frame_venda, tree

    # Botões de Ação
    button_frame = tk.Frame(estoque_window, pady=10)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    tk.Button(button_frame, text="Cadastrar", command=mostrar_formulario_add, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Alterar", command=mostrar_formulario_alterar, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Excluir", command=mostar_formulario_remover, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Vender", command=mostrar_formulario_venda, width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Histórico de vendas", width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Comissão", width=12).pack(side=tk.LEFT, padx=10)

    # Frame para Formulário de adicionar 

    form_frame_add = tk.Frame(estoque_window, padx=10, pady=10)
    form_frame_add.pack_forget()  # Oculta inicialmente

    # Placa
    tk.Label(form_frame_add, text="Placa:").grid(row=0, column=0, padx=5, pady=5)
    placa_entrada = tk.Entry(form_frame_add)
    placa_entrada.grid(row=0, column=1, padx=5, pady=5)

    # Ano
    tk.Label(form_frame_add, text="Ano:").grid(row=0, column=2, padx=5, pady=5)
    ano_entrada = tk.Entry(form_frame_add)
    ano_entrada.grid(row=0, column=3, padx=5, pady=5)

    # Marca
    tk.Label(form_frame_add, text="Marca:").grid(row=1, column=0, padx=5, pady=5)
    marca_entrada = tk.Entry(form_frame_add)
    marca_entrada.grid(row=1, column=1, padx=5, pady=5)

    # Modelo
    tk.Label(form_frame_add, text="Modelo:").grid(row=1, column=2, padx=5, pady=5)
    modelo_entrada = tk.Entry(form_frame_add)
    modelo_entrada.grid(row=1, column=3, padx=5, pady=5)

    # Cor
    tk.Label(form_frame_add, text="Cor:").grid(row=2, column=0, padx=5, pady=5)
    cor_entrada = tk.Entry(form_frame_add)
    cor_entrada.grid(row=2, column=1, padx=5, pady=5)

    # Categoria
    tk.Label(form_frame_add, text="Categoria:").grid(row=2, column=2, padx=5, pady=5)
    categoria_entrada = tk.Entry(form_frame_add)
    categoria_entrada.grid(row=2, column=3, padx=5, pady=5)

    # Preço
    tk.Label(form_frame_add, text="Preço:").grid(row=3, column=0, padx=5, pady=5)
    preco_entrada = tk.Entry(form_frame_add)
    preco_entrada.grid(row=3, column=1, padx=5, pady=5)

    # Integridade
    tk.Label(form_frame_add, text="Integridade:").grid(row=3, column=2, padx=5, pady=5)
    integridade_entrada = tk.Entry(form_frame_add)
    integridade_entrada.grid(row=3, column=3, padx=5, pady=5)

    # Botão de Cadastrar dentro do formulário
    tk.Button(form_frame_add, text="Cadastrar", command=lambda: cadastarVeiculo(
        placa_entrada.get(), ano_entrada.get(), marca_entrada.get(),
        modelo_entrada.get(), cor_entrada.get(), categoria_entrada.get(),
        preco_entrada.get(), integridade_entrada.get()
    ), width=12).grid(row=4, column=1, columnspan=2, pady=10)

    # frame de remover veiculo

    form_frame_remove = tk.Frame(estoque_window, padx=10, pady=10)
    tk.Label(form_frame_remove, text="Placa:").grid(row=0, column=0, padx=5, pady=5)
    placa_remover_entrada = tk.Entry(form_frame_remove)
    placa_remover_entrada.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(form_frame_remove, text="Remover", command=lambda: removerVeiculo(placa_remover_entrada.get())).grid(row=1, column=0, columnspan=2, pady=10)

    # frame para alterar

    # Função exibir os dados para edição subfunção da parte de alteração do veiculo
    def preencherCamposAlteracao():
        placa = placa_alterar_entrada.get()
        veiculo = buscarVeiculo(placa)
        
        if veiculo:
            # Exibe os dados do veículo na tabela
            tree.delete(*tree.get_children())
            tree.insert("", "end", values=veiculo)

            # Preenche os campos de edição com os dados do veículo
            preco_alterar_entrada.delete(0, tk.END)
            preco_alterar_entrada.insert(0, veiculo[6])  # Assume que o preço é o 7º campo

            cor_alterar_entrada.delete(0, tk.END)
            cor_alterar_entrada.insert(0, veiculo[4])  # Assume que a cor é o 5º campo

            integridade_alterar_entrada.delete(0, tk.END)
            integridade_alterar_entrada.insert(0, veiculo[7])  # Assume que a integridade é o 8º campo 

    # Frame para o formulário de alteração
    form_frame_alterar = tk.Frame(estoque_window, padx=10, pady=10)
    form_frame_alterar.pack_forget()  # Oculta inicialmente

    # Campo para inserir a placa do veículo a ser alterado
    tk.Label(form_frame_alterar, text="Placa:").grid(row=0, column=0, padx=5, pady=5)
    placa_alterar_entrada = tk.Entry(form_frame_alterar)
    placa_alterar_entrada.grid(row=0, column=1, padx=5, pady=5)

    # Botão para buscar o veículo
    tk.Button(form_frame_alterar, text="Buscar", command=preencherCamposAlteracao).grid(row=0, column=2, padx=5, pady=5)

    # Campo para atualizar o preço (opcional)
    tk.Label(form_frame_alterar, text="Novo Preço:").grid(row=1, column=0, padx=5, pady=5)
    preco_alterar_entrada = tk.Entry(form_frame_alterar)
    preco_alterar_entrada.grid(row=1, column=1, padx=5, pady=5)

    # Campo para atualizar a cor (opcional)
    tk.Label(form_frame_alterar, text="Nova Cor:").grid(row=2, column=0, padx=5, pady=5)
    cor_alterar_entrada = tk.Entry(form_frame_alterar)
    cor_alterar_entrada.grid(row=2, column=1, padx=5, pady=5)

    # Campo para atualizar a integridade (opcional)
    tk.Label(form_frame_alterar, text="Nova Integridade:").grid(row=3, column=0, padx=5, pady=5)
    integridade_alterar_entrada = tk.Entry(form_frame_alterar)
    integridade_alterar_entrada.grid(row=3, column=1, padx=5, pady=5)

    # Botão de Alterar
    tk.Button(form_frame_alterar, text="Alterar", command=lambda: alterarVeiculo(
        placa_alterar_entrada.get(),
        preco_alterar_entrada.get(),
        cor_alterar_entrada.get(),
        integridade_alterar_entrada.get()
    )).grid(row=4, column=0, columnspan=2, pady=10)

    # frame para a venda

    # Frame para o formulário de venda
    form_frame_venda = tk.Frame(estoque_window, padx=10, pady=10)
    form_frame_venda.pack_forget()  # Oculta inicialmente

    tk.Label(form_frame_venda, text="Placa:").grid(row=0, column=0, padx=5, pady=5)
    placa_venda_entrada = tk.Entry(form_frame_venda)
    placa_venda_entrada.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(form_frame_venda, text="Nome do Cliente:").grid(row=1, column=0, padx=5, pady=5)
    nomeCliente_venda_entrada = tk.Entry(form_frame_venda)
    nomeCliente_venda_entrada.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame_venda, text="CPF do Cliente:").grid(row=2, column=0, padx=5, pady=5)
    CPFcliente_venda_entrada = tk.Entry(form_frame_venda)
    CPFcliente_venda_entrada.grid(row=2, column=1, padx=5, pady=5)

    # botão de busca do veiculo
    tk.Button(form_frame_venda, text="Buscar", command=lambda: buscarVeiculo(placa_venda_entrada.get())).grid(row=0, column=2, padx=5, pady=5)

    #botão para realizar a venda
    tk.Button(form_frame_venda, text="Vender", command=lambda: venderVeiculo(
        placa_venda_entrada.get(),
        nomeCliente_venda_entrada.get(),
        CPFcliente_venda_entrada.get(),
        usuario
    )).grid(row=4, column=0, columnspan=2, pady=10)

    # frame para o histórico de venda 




    # Tabela de veiculos
    table_frame = tk.Frame(estoque_window, pady=10)
    table_frame.pack(fill=tk.BOTH, expand=True)

    columns = ("Placa", "Ano", "Marca", "Modelo", "Cor", "Categoria", "Preço", "Estado")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=100)

    tree.pack(fill=tk.BOTH, expand=True)

    # Execução da interface
    estoque_window.mainloop()

# Funções para verificar o usuario e a senha e abrir o sistema (algusto fazer)
def entrar():
    global usuario
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    comando = 'SELECT usuario, senha FROM usuarios WHERE usuario = %s AND senha = %s';
    cursor.execute(comando, (usuario, senha));
    resultado = cursor.fetchone();
    
    if len(resultado) > 0:
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        abrir_estoque()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def registrar_novo_usuario(usuario, senha):
    if usuario and senha:
        # Verifica se o usuário já existe no banco
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = %s", (usuario,))
        if cursor.fetchone()[0] > 0:
            messagebox.showwarning("Erro", "Usuário já existe.")
            return
        
        try:
            comando = ("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)")
            cursor.execute(comando, (usuario, senha))
            conexao_banco.commit()
            messagebox.showinfo("Registro", "Usuário registrado com sucesso!")
            cadastro_window.destroy()  # Fecha a janela de cadastro
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao registrar usuário: {err}")
    else:
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

def abrir_janela_cadastro():
    global cadastro_window
    cadastro_window = tk.Toplevel(login_window)
    cadastro_window.title("Registrar Novo Usuário")
    cadastro_window.geometry("300x200")
    
    # Label e Campo para Nome de Usuário
    tk.Label(cadastro_window, text="Nome de Usuário").pack(pady=5)
    novo_usuario_entrada = tk.Entry(cadastro_window, width=30)
    novo_usuario_entrada.pack(pady=5)
    
    # Label e Campo para Senha
    tk.Label(cadastro_window, text="Senha").pack(pady=5)
    nova_senha_entrada = tk.Entry(cadastro_window, width=30, show="*")
    nova_senha_entrada.pack(pady=5)
    
    # Botão para Registrar
    tk.Button(cadastro_window, text="Registrar", command=lambda: registrar_novo_usuario(novo_usuario_entrada.get(), nova_senha_entrada.get())).pack(pady=10)

# Janela principal
login_window = tk.Tk()
login_window.title("Login")

# Definindo tamanho fixo e centralizado
window_width, window_height = 300, 200
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
login_window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
login_window.resizable(False, False)

# Frame centralizado para o conteúdo de login
login_frame = tk.Frame(login_window, padx=20, pady=20)
login_frame.pack(expand=True)

# Labels e Entradas para Usuário e Senha
tk.Label(login_frame, text="Usuário").pack(anchor="w")
entrada_usuario = tk.Entry(login_frame, width=30)
entrada_usuario.pack(pady=5)

tk.Label(login_frame, text="Senha").pack(anchor="w")
entrada_senha = tk.Entry(login_frame, show="*", width=30)
entrada_senha.pack(pady=5)

# Botões Registrar e Entrar
btn_frame = tk.Frame(login_frame)
btn_frame.pack(pady=10)
btn_registrar = tk.Button(btn_frame, text="Registrar", command=abrir_janela_cadastro)
btn_registrar.pack(side="left", padx=5)
btn_entrar = tk.Button(btn_frame, text="Entrar", command=entrar)
btn_entrar.pack(side="right", padx=5)

# Executar a interface
login_window.mainloop()
