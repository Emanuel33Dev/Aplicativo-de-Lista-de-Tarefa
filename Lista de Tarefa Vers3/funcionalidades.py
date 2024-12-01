import sqlite3
import ttkbootstrap as ttkb
from ttkbootstrap.dialogs import Messagebox, Querybox


# Função para conectar ao banco de dados SQLite
def conectar_banco():
    return sqlite3.connect('tarefas.db')


# Função para criar a tabela de tarefas (caso não exista)
def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarefa TEXT,
        data_criacao TEXT,
        concluida BOOLEAN
    )
    ''')
    conn.commit()
    conn.close()


# Função para carregar tarefas do banco de dados
def carregar_tarefas():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    conn.close()

    # Formatar tarefas no formato desejado
    return [{'id': t[0], 'tarefa': t[1], 'data_criacao': t[2], 'concluida': t[3]} for t in tarefas]


# Função para salvar tarefas no banco de dados
def salvar_tarefas(tarefas):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Apagar todas as tarefas e reinserir
    cursor.execute("DELETE FROM tarefas")
    for tarefa in tarefas:
        cursor.execute("INSERT INTO tarefas (tarefa, data_criacao, concluida) VALUES (?, ?, ?)",
                       (tarefa['tarefa'], tarefa['data_criacao'], tarefa['concluida']))

    conn.commit()
    conn.close()


# Função para adicionar tarefa
def adicionar_tarefa(lista_tarefas, entrada_tarefa, entrada_data, tarefas):
    tarefa = entrada_tarefa.get()
    data_criacao = entrada_data.get()
    if tarefa and data_criacao:
        tarefa_obj = {'tarefa': tarefa, 'data_criacao': data_criacao, 'concluida': False}
        tarefas.append(tarefa_obj)
        salvar_tarefas(tarefas)
        atualizar_lista_tarefas(lista_tarefas, tarefas)
        entrada_tarefa.delete(0, 'end')
        entrada_data.delete(0, 'end')
    else:
        Messagebox.show_error("Por favor, preencha todos os campos.", "Erro")


# Função para excluir tarefa
def excluir_tarefa(tarefa_obj, tarefas, atualizar_lista, lista_tarefas):
    tarefas.remove(tarefa_obj)
    salvar_tarefas(tarefas)
    atualizar_lista(lista_tarefas, tarefas)


# Função para editar tarefa
def editar_tarefa(tarefa_obj, tarefas, atualizar_lista, lista_tarefas, entrada_tarefa, entrada_data, botao_adicionar):
    # Carregar a tarefa nos campos de entrada
    entrada_tarefa.delete(0, 'end')
    entrada_data.delete(0, 'end')

    entrada_tarefa.insert(0, tarefa_obj['tarefa'])
    entrada_data.insert(0, tarefa_obj['data_criacao'])

    # Alterar o comportamento do botão "Criar Tarefa" para "Salvar Alterações"
    botao_adicionar.config(
        text='Salvar Alterações',
        bootstyle="success",
        command=lambda: salvar_alteracoes(tarefa_obj, tarefas, lista_tarefas, botao_adicionar, entrada_tarefa,
                                          entrada_data)
    )


# Função para salvar as alterações feitas na tarefa
def salvar_alteracoes(tarefa_obj, tarefas, lista_tarefas, botao_adicionar, entrada_tarefa, entrada_data):
    tarefa_obj['tarefa'] = entrada_tarefa.get()
    tarefa_obj['data_criacao'] = entrada_data.get()
    salvar_tarefas(tarefas)
    atualizar_lista_tarefas(lista_tarefas, tarefas)

    # Reverter o botão "Salvar Alterações" para "Criar Tarefa"
    botao_adicionar.config(
        text='Criar Tarefa',
        bootstyle="success",
        command=lambda: adicionar_tarefa(lista_tarefas, entrada_tarefa, entrada_data, tarefas)
    )


# Função para atualizar lista de tarefas
def atualizar_lista_tarefas(lista_tarefas, tarefas):
    for widget in lista_tarefas.winfo_children():
        widget.destroy()

    for tarefa in tarefas:
        tarefa_frame = ttkb.Frame(lista_tarefas, padding=10, relief='solid')
        tarefa_frame.pack(fill='x', pady=5)

        ttkb.Label(tarefa_frame, text=f"Tarefa: {tarefa['tarefa']}", font=('Arial', 12, 'bold')).pack(anchor='w')
        ttkb.Label(tarefa_frame, text=f"Data: {tarefa['data_criacao']}", font=('Arial', 10)).pack(anchor='w')

        btn_frame = ttkb.Frame(tarefa_frame)
        btn_frame.pack(anchor='e', pady=5)

        ttkb.Button(btn_frame, text='Editar', bootstyle="success",
                    command=lambda t=tarefa: editar_tarefa(t, tarefas, atualizar_lista_tarefas, lista_tarefas,
                                                           entrada_tarefa, entrada_data, botao_adicionar)).pack(
            side='left', padx=5)
        ttkb.Button(btn_frame, text='Excluir', bootstyle="danger",
                    command=lambda t=tarefa: excluir_tarefa(t, tarefas, atualizar_lista_tarefas, lista_tarefas)).pack(
            side='right', padx=5)


# Inicialização do banco de dados
criar_tabela()
