import ttkbootstrap as ttkb
from ttkbootstrap.constants import SUCCESS, WARNING, CENTER, BOTH
from funcionalidades import carregar_tarefas, salvar_tarefas, adicionar_tarefa, atualizar_lista_tarefas


def main():
    tarefas = carregar_tarefas()  # Carregar tarefas salvas

    # Configuração da janela
    janela = ttkb.Window(themename="solar")
    janela.title('Sistema de Lista de Tarefas')
    janela.geometry('800x600')
    janela.minsize(600, 400)  # Definir tamanho mínimo da janela
    janela.resizable(True, True)  # Tornar a janela redimensionável

    # Configurar abas
    abas = ttkb.Notebook(janela)
    abas.pack(pady=10, expand=True, fill=BOTH)

    # Criar frame da aba
    frame_tarefas = ttkb.Frame(abas)
    frame_tarefas.pack(fill=BOTH, expand=True)
    abas.add(frame_tarefas, text='Lista de Tarefas')

    # Adicionar título para lista de tarefas
    ttkb.Label(frame_tarefas, text='Lista de Tarefas', font=('Arial', 14)).pack(pady=10)

    # Frame para os campos de entrada
    frame_entrada = ttkb.Frame(frame_tarefas)
    frame_entrada.pack(pady=10, fill=BOTH, padx=10)

    # Barra para o Assunto
    frame_assunto = ttkb.Frame(frame_entrada)
    frame_assunto.pack(fill=BOTH, pady=5)

    ttkb.Label(frame_assunto, text="Assunto:", font=('Arial', 12)).pack(side='left', padx=5)  # Alinha à esquerda
    entrada_tarefa = ttkb.Entry(frame_assunto, width=40, font=('Arial', 12))
    entrada_tarefa.pack(side='left', fill=BOTH)

    # Barra para a Descrição
    frame_descricao = ttkb.Frame(frame_entrada)
    frame_descricao.pack(fill=BOTH, pady=5)

    ttkb.Label(frame_descricao, text="Descrição:", font=('Arial', 12)).pack(side='left', padx=5)  # Alinha à esquerda
    entrada_data = ttkb.Entry(frame_descricao, width=40, font=('Arial', 12))
    entrada_data.pack(side='left', fill=BOTH)

    # Botão para criar tarefa
    botao_adicionar = ttkb.Button(
        frame_tarefas,
        text='Criar Tarefa',
        bootstyle=SUCCESS,
        command=lambda: adicionar_e_atualizar()
    )
    botao_adicionar.pack(pady=5, fill=BOTH, padx=10)

    # Adicionar canvas com barra de rolagem para a lista de tarefas
    canvas_frame = ttkb.Frame(frame_tarefas)
    canvas_frame.pack(fill=BOTH, expand=True, padx=10)

    # Canvas para tarefas
    canvas = ttkb.Canvas(canvas_frame)
    canvas.pack(side='left', fill=BOTH, expand=True)

    # Barra de rolagem
    scrollbar = ttkb.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    # Vincular scrollbar ao canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Frame interno do canvas
    lista_tarefas = ttkb.Frame(canvas)
    canvas.create_window((0, 0), window=lista_tarefas, anchor='nw')

    # Função para adicionar tarefa e atualizar a lista
    def adicionar_e_atualizar():
        # Chama a função para adicionar a tarefa e atualizar a lista
        adicionar_tarefa(lista_tarefas, entrada_tarefa, entrada_data, tarefas)
        # Atualiza a lista com as novas tarefas
        atualizar_lista_tarefas_com_rolagem(lista_tarefas, tarefas)

    # Função para adicionar as tarefas ao layout e criar botões de editar/excluir
    def atualizar_lista_tarefas_com_rolagem(lista_tarefas, tarefas):
        # Limpar lista de tarefas atual para evitar duplicações
        for widget in lista_tarefas.winfo_children():
            widget.destroy()

        # Exibir tarefas, limitando a 3 por linha
        for i, tarefa in enumerate(tarefas):
            tarefa_frame = ttkb.Frame(lista_tarefas, padding=10, relief='solid', width=250, height=150)
            tarefa_frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)  # Coloca em 3 colunas

            titulo_tarefa = ttkb.Label(tarefa_frame, text=tarefa['tarefa'], font=('Arial', 12, 'bold'))
            titulo_tarefa.pack(side='top', padx=10, pady=5)

            descricao_tarefa = ttkb.Label(tarefa_frame, text=f"Data: {tarefa['data_criacao']}", font=('Arial', 10))
            descricao_tarefa.pack(side='top', anchor='w', padx=10, pady=5)

            # Botões de Editar e Excluir
            botao_editar = ttkb.Button(
                tarefa_frame,
                text='Editar',
                bootstyle=SUCCESS,
                command=lambda t=tarefa: editar_tarefa(t)
            )
            botao_editar.pack(side='left', padx=5, pady=5)

            botao_excluir = ttkb.Button(
                tarefa_frame,
                text='Excluir',
                bootstyle=WARNING,
                command=lambda t=tarefa: excluir_tarefa(t)
            )
            botao_excluir.pack(side='right', padx=5, pady=5)

    # Função de editar tarefa
    def editar_tarefa(tarefa):
        # Implemente a lógica de edição
        print(f"Editar tarefa: {tarefa['tarefa']}")

    # Função de excluir tarefa
    def excluir_tarefa(tarefa):
        # Implemente a lógica de exclusão
        tarefas.remove(tarefa)
        salvar_tarefas(tarefas)
        atualizar_lista_tarefas_com_rolagem(lista_tarefas, tarefas)

    # Exibir tarefas salvas ao iniciar
    atualizar_lista_tarefas_com_rolagem(lista_tarefas, tarefas)

    # Iniciar o loop
    janela.mainloop()


if __name__ == "__main__":
    main()
