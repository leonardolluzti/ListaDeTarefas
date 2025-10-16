# Aplicativo de lista de tarefas
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os

class ListaDeTarefasApp:
    def __init__(self, root):
        """
        Inicializa o aplicativo de lista de tarefas.
        """
        self.root = root
        self.root.title("Lista de Tarefas")
        self.root.geometry("650x700")
        self.root.resizable(True, True)

        # Configuração de estilo
        self.root.configure(bg="#f0f0f0")
        fonte_titulo = ("Arial", 20, "bold")
        fonte_geral = ("Arial", 12)
        cor_principal = "#2c3e50"
        cor_secundaria = "#ecf0f1"
        bg_botao_adicionar = "#27ae60"  # Verde
        bg_botao_remover = "#c0392b"    # Vermelho
        bg_botao_editar = "#2980b9"     # Azul
        bg_botao_concluir = "#f39c12"  # Laranja
        fg_botao = "white"

        # --- Widgets da Interface ---

        # Título
        self.label_titulo = tk.Label(root, text="Minhas Tarefas", font=fonte_titulo, bg="#f0f0f0", fg=cor_principal)
        self.label_titulo.pack(pady=15)

        # Frame para entrada de texto e botão Adicionar
        self.frame_entrada = tk.Frame(root, bg="#f0f0f0")
        self.frame_entrada.pack(pady=5)

        # Campo de entrada de texto
        self.entrada_tarefa = tk.Entry(self.frame_entrada, width=35, font=fonte_geral, relief="flat", bd=2, bg=cor_secundaria)
        self.entrada_tarefa.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        self.entrada_tarefa.bind("<Return>", self.adicionar_tarefa_event)  # Adiciona tarefa com a tecla Enter

        # Botão para adicionar tarefa
        self.botao_adicionar = tk.Button(self.frame_entrada, text="Adicionar", font=fonte_geral, command=self.adicionar_tarefa,
                                         bg=bg_botao_adicionar, fg=fg_botao, relief="flat", bd=0, activebackground="#2ecc71")
        self.botao_adicionar.pack(side=tk.RIGHT, ipadx=10, ipady=5)

        # Lista de tarefas
        self.lista_tarefas = tk.Listbox(root, width=50, height=15, font=fonte_geral,
                                        selectmode=tk.SINGLE, bg="white", relief="flat", bd=2)
        self.lista_tarefas.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Frame para os botões de controle
        self.frame_botoes = tk.Frame(root, bg="#f0f0f0")
        self.frame_botoes.pack(pady=10)

        # Botão para remover tarefa
        self.botao_remover = tk.Button(self.frame_botoes, text="Remover", font=fonte_geral, command=self.remover_tarefa,
                                       bg=bg_botao_remover, fg=fg_botao, relief="flat", bd=0, activebackground="#e74c3c")
        self.botao_remover.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

        # Botão para editar tarefa
        self.botao_editar = tk.Button(self.frame_botoes, text="Editar", font=fonte_geral, command=self.editar_tarefa,
                                      bg=bg_botao_editar, fg=fg_botao, relief="flat", bd=0, activebackground="#3498db")
        self.botao_editar.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Botão para marcar como concluída/reabrir
        self.botao_concluir = tk.Button(self.frame_botoes, text="Marcar/Reabrir", font=fonte_geral, command=self.alternar_status,
                                        bg=bg_botao_concluir, fg=fg_botao, relief="flat", bd=0, activebackground="#f1c40f")
        self.botao_concluir.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Botões de salvar e carregar
        self.botao_salvar = tk.Button(self.frame_botoes, text="Salvar Lista", font=fonte_geral, command=self.salvar_tarefas,
                                      bg="#16a085", fg=fg_botao, relief="flat", bd=0, activebackground="#1abc9c")
        self.botao_salvar.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        self.botao_carregar = tk.Button(self.frame_botoes, text="Carregar Lista", font=fonte_geral, command=self.carregar_tarefas,
                                        bg="#34495e", fg=fg_botao, relief="flat", bd=0, activebackground="#3e5975")
        self.botao_carregar.pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)

    def adicionar_tarefa_event(self, event):
        """
        Função para adicionar uma tarefa a partir do evento de tecla Enter.
        """
        self.adicionar_tarefa()

    def adicionar_tarefa(self):
        """
        Adiciona a tarefa do campo de entrada à lista.
        """
        tarefa = self.entrada_tarefa.get().strip()
        if tarefa:
            self.lista_tarefas.insert(tk.END, tarefa)
            self.entrada_tarefa.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Por favor, digite uma tarefa.")

    def remover_tarefa(self):
        """
        Remove a tarefa selecionada da lista.
        """
        try:
            indice_selecionado = self.lista_tarefas.curselection()[0]
            self.lista_tarefas.delete(indice_selecionado)
        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para remover.")

    def editar_tarefa(self):
        """
        Permite editar a tarefa selecionada.
        """
        try:
            indice_selecionado = self.lista_tarefas.curselection()[0]
            tarefa_original = self.lista_tarefas.get(indice_selecionado)

            # Cria uma nova janela de edição
            janela_edicao = tk.Toplevel(self.root)
            janela_edicao.title("Editar Tarefa")
            janela_edicao.geometry("300x100")
            janela_edicao.resizable(False, False)
            janela_edicao.configure(bg="#f0f0f0")

            tk.Label(janela_edicao, text="Nova tarefa:", bg="#f0f0f0").pack(pady=5)
            nova_tarefa_entrada = tk.Entry(janela_edicao, width=30, relief="flat", bd=2)
            nova_tarefa_entrada.insert(0, tarefa_original.replace("✓ ", ""))  # Preenche com o texto original
            nova_tarefa_entrada.pack(padx=10)

            def salvar_edicao():
                nova_tarefa = nova_tarefa_entrada.get().strip()
                if nova_tarefa:
                    self.lista_tarefas.delete(indice_selecionado)
                    # Mantém o status de concluída se a tarefa original tinha
                    if tarefa_original.startswith("✓ "):
                        nova_tarefa = "✓ " + nova_tarefa
                    self.lista_tarefas.insert(indice_selecionado, nova_tarefa)
                    janela_edicao.destroy()
                else:
                    messagebox.showwarning("Aviso", "A tarefa não pode estar vazia.", parent=janela_edicao)

            tk.Button(janela_edicao, text="Salvar", command=salvar_edicao, bg="#27ae60", fg="white", relief="flat").pack(pady=10)

        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para editar.")

    def alternar_status(self):
        """
        Marca ou desmarca a tarefa selecionada como concluída.
        """
        try:
            indice_selecionado = self.lista_tarefas.curselection()[0]
            tarefa = self.lista_tarefas.get(indice_selecionado)

            if tarefa.startswith("✓ "):
                # Desmarca a tarefa
                nova_tarefa = tarefa[2:]
            else:
                # Marca a tarefa
                nova_tarefa = "✓ " + tarefa
            
            self.lista_tarefas.delete(indice_selecionado)
            self.lista_tarefas.insert(indice_selecionado, nova_tarefa)

        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa para marcar/desmarcar.")
            
    def salvar_tarefas(self):
        """
        Salva todas as tarefas da lista em um arquivo de texto, permitindo ao usuário escolher o nome e local.
        """
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
                                                initialfile="tarefas.txt")
        if filename:
            try:
                with open(filename, "w") as f:
                    tarefas = self.lista_tarefas.get(0, tk.END)
                    for tarefa in tarefas:
                        f.write(tarefa + "\n")
                messagebox.showinfo("Sucesso", "Tarefas salvas com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

    def carregar_tarefas(self):
        """
        Carrega tarefas de um arquivo de texto, permitindo ao usuário escolher o arquivo.
        """
        filename = filedialog.askopenfilename(defaultextension=".txt",
                                              filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
        if filename:
            try:
                with open(filename, "r") as f:
                    tarefas = [line.strip() for line in f]
                    self.lista_tarefas.delete(0, tk.END)
                    for tarefa in tarefas:
                        self.lista_tarefas.insert(tk.END, tarefa)
                messagebox.showinfo("Sucesso", "Tarefas carregadas com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar o arquivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ListaDeTarefasApp(root)
    root.mainloop()
