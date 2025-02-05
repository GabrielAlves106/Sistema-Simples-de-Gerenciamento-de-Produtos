import sqlite3
import tkinter as tk
from tkinter import messagebox, Toplevel
from datetime import datetime
import time

# Função para verificar login
def verificar_login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    banco_principal = sqlite3.connect("banco.db")
    cursor = banco_principal.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE NOMElogin = ? AND SENHAuser = ?", (usuario, senha))
    resultado = cursor.fetchone()
    banco_principal.close()

    if resultado:
        messagebox.showinfo("Login", "Login bem-sucedido!")
        janela_login.destroy()  # Fecha a janela de login
        abrir_menu_principal()  # Abre o menu principal
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# Função para abrir a interface principal
def abrir_menu_principal():
    root = tk.Tk()
    root.title("Sistema de Gerenciamento")
    root.geometry("500x300")

    # Criando o menu principal
    menu_principal = tk.Menu(root)

    # Menu "Produtos"
    menu_produtos = tk.Menu(menu_principal, tearoff=0)
    menu_produtos.add_command(label="Registrar Produto", command=registrar_produto)
    menu_produtos.add_separator()
    menu_produtos.add_command(label="Apagar Produtos", command=apagar_produto)
    menu_produtos.add_separator()
    menu_produtos.add_command(label="Visualizar Validades", command=visualizar_validades)
    menu_produtos.add_separator()
    menu_produtos.add_command(label="Visualizar Estoque", command=visualizar_estoque)
    menu_produtos.add_separator()
    menu_produtos.add_command(label="Produtos em Baixo Estoque", command=produtos_bx_estoque)
    menu_principal.add_cascade(label="Produtos", menu=menu_produtos)

    # Menu "Usuários"
    menu_usuarios = tk.Menu(menu_principal, tearoff=0)
    #menu_usuarios.add_command(label="Usuários", command=lambda: messagebox.showinfo("Usuários", "Gerenciar Usuários ainda não implementado"))
    menu_usuarios.add_command(label="Registrar Usuário",command=registrar_usuario)
    menu_usuarios.add_separator()
    menu_usuarios.add_command(label="Apagar Usuário", command=apagar_usuario)
    menu_usuarios.add_separator()
    #menu_usuarios.add_command(label="Sair", command=root.destroy)
    menu_principal.add_cascade(label="Usuários", menu=menu_usuarios)
    
    # Menu "Levantamentos"
    menu_levantamentos = tk.Menu(menu_principal,tearoff=0)   
    menu_levantamentos.add_command(label="Contagem de Estoque")
    menu_levantamentos.add_separator()
    menu_principal.add_cascade(label="Levantamentos", menu=menu_levantamentos)
    
    # Menu "Relatórios"
    menu_relatorios = tk.Menu(menu_principal,tearoff=0)
    menu_relatorios.add_command(label="Relatório de Estoque")
    menu_relatorios.add_separator()
    menu_relatorios.add_command(label="Relatório de Perdas")
    menu_relatorios.add_separator()
    menu_relatorios.add_command(label="Relatório Personalizado")
    menu_relatorios.add_separator()
    menu_relatorios.add_command(label="Produtos sem Movimentação")
    menu_relatorios.add_separator()
    menu_principal.add_cascade(label="Relatórios",menu=menu_relatorios)
    
    # Menu "Análises"
    menu_analises = tk.Menu(menu_principal,tearoff=0)
    menu_analises.add_command(label="Análise de Vendas")
    menu_analises.add_command(label="Taxa de Rotatividade")
    menu_analises.add_separator()
    menu_principal.add_cascade(label="Análises",menu=menu_analises)
    
    # Menu "Ajuda"
    menu_ajuda = tk.Menu(menu_principal, tearoff=0)
    menu_ajuda.add_command(label="Sobre", command=lambda: messagebox.showinfo("Sobre", "Sistema de Gerenciamento v1.0\nDesenvolvido por Gabriel Alves"))
    menu_principal.add_cascade(label="Ajuda", menu=menu_ajuda)
    

    # Configurando o menu na janela principal
    root.config(menu=menu_principal)
    root.mainloop()

# Função para criar a interface de registro de produtos
def registrar_produto():
    def limpa_campos():
        for widget in janela_registro.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0,tk.END)
                
    def salvar_produto():
        id_produto = entrada_id.get()
        nome_produto = entrada_nome.get()
        quantidade = entrada_quantidade.get()
        data_vencimento = entrada_data.get()

        if not id_produto or not nome_produto or not quantidade or not data_vencimento:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            banco_principal = sqlite3.connect("banco.db")
            cursor = banco_principal.cursor()
            cursor.execute(
                "INSERT INTO estoque (IDproduto, NOMEproduto, QUANTIDADEproduto, DATAVENCIMENTOproduto) VALUES (?, ?, ?, ?)",
                (id_produto, nome_produto, quantidade, data_vencimento)
            )
            banco_principal.commit()
            banco_principal.close()
            messagebox.showinfo("Sucesso", "Produto registrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar produto: {e}")

    # Criando a janela de registro
    janela_registro = Toplevel()
    janela_registro.title("Registrar Produto")
    janela_registro.geometry("400x300")
    janela_registro.grab_set()

    tk.Label(janela_registro, text="ID do Produto:").grid(row=0, column=0, padx=10, pady=5)
    entrada_id = tk.Entry(janela_registro)
    entrada_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_registro, text="Nome do Produto:").grid(row=1, column=0, padx=10, pady=5)
    entrada_nome = tk.Entry(janela_registro)
    entrada_nome.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_registro, text="Quantidade:").grid(row=2, column=0, padx=10, pady=5)
    entrada_quantidade = tk.Entry(janela_registro)
    entrada_quantidade.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_registro, text="Data de Vencimento (AAAA-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
    entrada_data = tk.Entry(janela_registro)
    entrada_data.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Button(janela_registro, text="Salvar", command=salvar_produto).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(janela_registro, text="Limpar Campos", command=limpa_campos).grid(row=5, column=0, columnspan=2, pady=10)

def apagar_produto():
    def limpa_campos():
        for widget in janela_delete.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0,tk.END)
                
    def apaga_prod():
        id_produto = entrada_nome.get()
        
        try:
            banco_clientes = sqlite3.connect("banco.db")

            cursor = banco_clientes.cursor()

            cursor.execute("DELETE from estoque WHERE IDproduto = ?",(id_produto,))
            banco_clientes.commit()

            cursor.close()
            banco_clientes.close()
            messagebox.showinfo("Removendo", "Removido com Sucesso")
                    
        except sqlite3.Error as erro:
            messagebox.showerror("Erro ao Excluir Dados...",erro)
            janela_delete.destroy()
                    
    janela_delete = Toplevel()
    janela_delete.title("Apagar Produto")
    janela_delete.geometry("400x300")

    tk.Label(janela_delete, text="ID do Produto:").grid(row=0, column=0, padx=10, pady=5)
    entrada_nome = tk.Entry(janela_delete)
    entrada_nome.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(janela_delete, text="Apagar", command=apaga_prod).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(janela_delete, text="Limpar Campos", command=limpa_campos).grid(row=5, column=0, columnspan=2, pady=10)
    
            
# Função para visualizar validades 
def visualizar_validades():
    def verificar_validades():
        # Data de hoje no formato "YYYY-MM-DD"
        data_atual = datetime.now().strftime("%Y-%m-%d")
        texto = f"Data de Hoje: {data_atual}\n\n"

        # Conectando ao banco de dados
        banco_principal = sqlite3.connect("banco.db")
        cursor = banco_principal.cursor()

        try:
            # Executando a query para obter os nomes e datas de vencimento
            cursor.execute("SELECT NOMEproduto, DATAVENCIMENTOproduto FROM estoque")
            produtos = cursor.fetchall()

            # Verificando cada produto
            for nome, data_vencimento in produtos:
                data_vencimento_obj = datetime.strptime(data_vencimento, "%Y-%m-%d")
                data_atual_obj = datetime.strptime(data_atual, "%Y-%m-%d")

                # Verificar se o produto está vencido
                if data_atual_obj > data_vencimento_obj:
                    texto += f"Produto: {nome} | Data de Vencimento: {data_vencimento} | Status: VENCIDO\n"

            # Atualizando o rótulo com as informações
            label_mostrar.config(text=texto)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar produtos: {e}")

        finally:
            banco_principal.close()


    # Criando a janela de visualização
    janela_validades = Toplevel()
    janela_validades.title("Verificar Validades")
    janela_validades.geometry("600x400")

    tk.Button(janela_validades, text="Buscar Produtos Vencidos", command=verificar_validades).pack(pady=10)
    label_mostrar = tk.Label(janela_validades, text="", font=("Arial", 12), justify="left")
    label_mostrar.pack(padx=10, pady=10)
    
def produtos_bx_estoque():
    def visualiza_bxe():
        texto = ""
        
        banco_principal = sqlite3.connect("banco.db")
        cursor = banco_principal.cursor()
        
        try:
            # Executando a query para obter os nomes e datas de vencimento
            cursor.execute("SELECT NOMEproduto, QUANTIDADEproduto FROM estoque")
            produtos = cursor.fetchall()

            # Verificando cada produto
            for nome, quantidade in produtos:
                
                # Verificar se o produto está vencido
                if quantidade < 10:
                    texto += f"Produto: {nome} | Quantidade: {quantidade} | Produto a Ser Reposto!"
                
            # Atualizando o rótulo com as informações
            label_mostrar.config(text=texto)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar produtos: {e}")

        finally:
            banco_principal.close()


    # Criando a janela de visualização
    janela_validades = Toplevel()
    janela_validades.title("Produtos Em Baixo Estoque")
    janela_validades.geometry("600x400")

    tk.Button(janela_validades, text="Buscar Produtos em Baixa Quantidade", command=visualiza_bxe).pack(pady=10)
    label_mostrar = tk.Label(janela_validades, text="", font=("Arial", 12), justify="left")
    label_mostrar.pack(padx=10, pady=10)
        
def registrar_usuario():
    def salvar_usuario():
        id_usuario = entrada_id.get()
        senha_usuario = entrada_nome.get()
        nome_usuario= entrada_quantidade.get()
        login_usuario = entrada_data.get()

        if not id_usuario or not nome_usuario or not nome_usuario or not login_usuario:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            banco_principal = sqlite3.connect("banco.db")
            cursor = banco_principal.cursor()
            cursor.execute(
                "INSERT INTO usuarios (IDuser, SENHAuser, NOMEuser, NOMElogin) VALUES (?, ?, ?, ?)",
                (id_usuario, senha_usuario, nome_usuario, login_usuario)
            )
            banco_principal.commit()
            banco_principal.close()
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            janela_registro.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar Usuário: {e}")

    # Criando a janela de registro
    janela_registro = Toplevel()
    janela_registro.title("Registrar Usuario")
    janela_registro.geometry("400x300")

    tk.Label(janela_registro, text="ID do Usuário:").grid(row=0, column=0, padx=10, pady=5)
    entrada_id = tk.Entry(janela_registro)
    entrada_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(janela_registro, text="Senha do Usuário:").grid(row=1, column=0, padx=10, pady=5)
    entrada_nome = tk.Entry(janela_registro, show="*")
    entrada_nome.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(janela_registro, text="Nome do Usuário:").grid(row=2, column=0, padx=10, pady=5)
    entrada_quantidade = tk.Entry(janela_registro)
    entrada_quantidade.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(janela_registro, text="Login do Usuário:").grid(row=3, column=0, padx=10, pady=5)
    entrada_data = tk.Entry(janela_registro)
    entrada_data.grid(row=3, column=1, padx=10, pady=5)

    tk.Button(janela_registro, text="Salvar", command=salvar_usuario).grid(row=4, column=0, columnspan=2, pady=10)
    
def apagar_usuario():
    def apagauser():
        nome_user = entrada_nome.get()
        
        try:
            banco_clientes = sqlite3.connect("banco.db")

            cursor = banco_clientes.cursor()

            cursor.execute("DELETE from usuarios WHERE IDuser = ?",(nome_user,))
            banco_clientes.commit()

            cursor.close()
            banco_clientes.close()
            messagebox.showinfo("Removendo", "Removido com Sucesso")
            janela_delete.destroy()
                    
        except sqlite3.Error as erro:
            messagebox.showerror("Erro ao Excluir Dados...",erro)
            janela_delete.destroy()
                    
    janela_delete = Toplevel()
    janela_delete.title("Apagar Usuário")
    janela_delete.geometry("400x300")

    tk.Label(janela_delete, text="ID do Usuário:").grid(row=0, column=0, padx=10, pady=5)
    entrada_nome = tk.Entry(janela_delete)
    entrada_nome.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(janela_delete, text="Apagar", command=apagauser).grid(row=4, column=0, columnspan=2, pady=10)

def visualizar_estoque():
    def visualizar():
        data_atual = datetime.now().strftime("%Y-%m-%d")
        texto = f"Data de Hoje: {data_atual}\n\n"
        banco_principal = sqlite3.connect("banco.db")
        cursor = banco_principal.cursor()

        try:
            # Executando a query para obter os nomes e datas de vencimento
            cursor.execute("SELECT IDproduto, NOMEproduto, QUANTIDADEproduto, DATAVENCIMENTOproduto FROM estoque")
            produtos = cursor.fetchall()

            # Verificando cada produto
            for id, nome, quantidade, data_vencimento in produtos:
                texto += f"ID: {id} | Produto: {nome} | Quantidade {quantidade} | Data de Vencimento: {data_vencimento} |\n"
            # Atualizando o rótulo com as informações
            label_mostrar.config(text=texto)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar produtos: {e}")

        finally:
            banco_principal.close()


    # Criando a janela de visualização
    janela_validades = Toplevel()
    janela_validades.title("Verificar Validades")
    janela_validades.geometry("600x400")

    tk.Button(janela_validades, text="Acessar Estoque", command=visualizar).pack(pady=10)
    label_mostrar = tk.Label(janela_validades, text="", font=("Arial", 12), justify="left")
    label_mostrar.pack(padx=10, pady=10)
    

# Criando a janela de login
janela_login = tk.Tk()
janela_login.title("Login do Sistema")
janela_login.geometry("300x200")

tk.Label(janela_login, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
entrada_usuario = tk.Entry(janela_login)
entrada_usuario.grid(row=0, column=1, padx=10, pady=10)

tk.Label(janela_login, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
entrada_senha = tk.Entry(janela_login, show="*")
entrada_senha.grid(row=1, column=1, padx=10, pady=10)

tk.Button(janela_login, text="Login", command=verificar_login).grid(row=2, column=0, columnspan=2, pady=20)

janela_login.mainloop()
