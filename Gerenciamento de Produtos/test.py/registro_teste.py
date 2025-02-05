import sqlite3
import time
import sys
import datetime

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def registrar_produto():
    def limpa_campos():
        for widget in frame_campos.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
                
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
            limpa_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar produto: {e}")

    # Criando a janela de registro
    janela_registro = tk.Toplevel()
    janela_registro.title("Registrar Produto")
    janela_registro.geometry("450x400")
    janela_registro.configure(bg="#f5f5f5")
    janela_registro.grab_set()

    # Título da Janela
    ttk.Label(
        janela_registro, 
        text="Registro de Produtos", 
        font=("Arial", 18, "bold"), 
        background="#f5f5f5"
    ).pack(pady=10)

    # Frame para os campos
    frame_campos = ttk.Frame(janela_registro, padding=20)
    frame_campos.pack(fill="x", pady=10)

    # Campos de entrada
    ttk.Label(frame_campos, text="ID do Produto:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entrada_id = ttk.Entry(frame_campos, width=30)
    entrada_id.grid(row=0, column=1, pady=5)

    ttk.Label(frame_campos, text="Nome do Produto:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entrada_nome = ttk.Entry(frame_campos, width=30)
    entrada_nome.grid(row=1, column=1, pady=5)

    ttk.Label(frame_campos, text="Quantidade:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entrada_quantidade = ttk.Entry(frame_campos, width=30)
    entrada_quantidade.grid(row=2, column=1, pady=5)

    ttk.Label(frame_campos, text="Data de Vencimento (AAAA-MM-DD):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entrada_data = ttk.Entry(frame_campos, width=30)
    entrada_data.grid(row=3, column=1, pady=5)

    # Botões
    frame_botoes = ttk.Frame(janela_registro, padding=20)
    frame_botoes.pack(fill="x", pady=10)

    ttk.Button(frame_botoes, text="Salvar", command=salvar_produto).grid(row=0, column=0, padx=10)
    ttk.Button(frame_botoes, text="Limpar Campos", command=limpa_campos).grid(row=0, column=1, padx=10)


    # Ícone da Janela (opcional, adicione seu caminho para um arquivo .ico)
    # janela_registro.iconbitmap("icone.ico")

                

