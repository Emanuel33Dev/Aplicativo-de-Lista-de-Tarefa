import tkinter as tk
from tkinter import ttk, simpledialog
import json
import os


# Função para carregar tarefas de um arquivo JSON
def carregar_tarefas():
    if os.path.exists("tarefas.json"):
        with open("tarefas.json", "r") as file:
            return json.load(file)
    return []


# Função para salvar tarefas no arquivo JSON
def salvar_tarefas():
    with open("tarefas.json", "w") as file:
        json.dump(tarefas, file)


# Lista de tarefas (armazenamento em arquivo JSON)
tarefas = carregar_tarefas()


# Função para adicionar tarefa
def adicionar_tarefa(lista_tarefas, entrada_tarefa, entrada_data):
    tarefa = entrada_tarefa.get()
    data_criacao = entrada_data.get()
    if tarefa and data_criacao:
        # Armazenar a tarefa na lista de tarefas
        tarefas.append({'tarefa': tarefa, 'data_criacao': data_criacao, 'concluida': False})
        salvar_tarefas()  # Salvar tarefas no arquivo

        # Criar frame para a tarefa
        tarefa_frame = tk.Frame(lista_tarefas, bg="lightyellow", bd=2, relief="groove")

        check_var = tk.BooleanVar()
        check_button = tk.Checkbutton(tarefa_frame, text=f'{tarefa} ({data_criacao})', variable=check_var,
                                      anchor="w", width=40, bg="lightyellow")
        check_button.pack(side="left", padx=5)

        botao_excluir_tarefa = tk.Button(tarefa_frame, text="Excluir", command=lambda: excluir_tarefa(tarefa_frame),
                                         bg="red", fg="white")
        botao_excluir_tarefa.pack(side="left", padx=5)

        botao_editar_tarefa = tk.Button(tarefa_frame, text="Editar",
                                        command=lambda: editar_tarefa(tarefa_frame, check_button, tarefa), bg="blue",
                                        fg="white")
        botao_editar_tarefa.pack(side="left", padx=5)

        tarefa_frame.pack(fill="x", pady=5)

        # Limpar campos de entrada
        entrada_tarefa.delete(0, tk.END)
        entrada_data.delete(0, tk.END)


# Função para excluir tarefa
def excluir_tarefa(tarefa_frame):
    tarefa_frame.destroy()
    salvar_tarefas()  # Salvar após exclusão


# Função para editar tarefa
def editar_tarefa(tarefa_frame, check_button, tarefa_antiga):
    nova_tarefa = simpledialog.askstring("Editar Tarefa", "Digite o novo texto para a tarefa:",
                                         initialvalue=tarefa_antiga)
    if nova_tarefa:
        check_button.config(text=nova_tarefa)
        salvar_tarefas()  # Salvar após edição


# Configuração da janela principal
janela = tk.Tk()
janela.title('Sistema de Lista de Tarefas')

# Criar notebook (abas)
notebook = ttk.Notebook(janela)
notebook.pack(pady=10, expand=True)

# Criar frame da aba
frame_tarefas = ttk.Frame(notebook, width=600, height=400)
frame_tarefas.pack(fill='both', expand=True)
notebook.add(frame_tarefas, text='Lista de Tarefas')

# Adicionar título para lista de tarefas
tk.Label(frame_tarefas, text="Lista de Tarefas", font=("Arial", 14)).pack(pady=10)

# Campos de entrada e botão para criar tarefa
entrada_tarefa = tk.Entry(frame_tarefas, width=50)
entrada_tarefa.pack(pady=10)
entrada_data = tk.Entry(frame_tarefas, width=50)
entrada_data.insert(0, "Coloque a informação")
entrada_data.pack(pady=5)

botao_adicionar = tk.Button(frame_tarefas, text='Criar Tarefa',
                            command=lambda: adicionar_tarefa(lista_tarefas, entrada_tarefa, entrada_data), bg="green",
                            fg="white")
botao_adicionar.pack(pady=5)

# Frame para a lista de tarefas
lista_tarefas = tk.Frame(frame_tarefas)
lista_tarefas.pack(pady=10, fill="both", expand=True)

# Iniciar o loop
janela.mainloop()
