# app_gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from modelos import (
    Usuario,
    DisciplinaObrigatoria,
    DisciplinaOptativa,
    Simulacao,
    ControleFaltas,
)


class AppMetricas:
    def __init__(self, root):
        self.root = root
        self.root.title("Métricas Acadêmicas")
        self.root.geometry("1100x550")  # Aumentado levemente para acomodar o novo campo
        self.root.configure(bg="#f5f6fa")

        self.root.withdraw()
        self.solicitar_dados_iniciais()

    def solicitar_dados_iniciais(self):
        janela_login = tk.Toplevel(self.root)
        janela_login.title("Boas-vindas ao App de Métricas")
        janela_login.geometry("350x300")
        janela_login.configure(bg="#ffffff")
        janela_login.protocol("WM_DELETE_WINDOW", self.root.quit)

        tk.Label(
            janela_login,
            text="Olá! Insira seus dados para começar:",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#2f3640",
        ).pack(pady=15)
        tk.Label(janela_login, text="Seu Nome:", bg="#ffffff").pack(anchor="w", padx=40)
        ent_nome_user = tk.Entry(janela_login, font=("Arial", 10), width=25)
        ent_nome_user.pack(pady=5, padx=40)
        ent_nome_user.insert(0, "Nome")

        tk.Label(
            janela_login, text="IRA Acumulado anterior (0 a 5):", bg="#ffffff"
        ).pack(anchor="w", padx=40)
        ent_ira_user = tk.Entry(janela_login, font=("Arial", 10), width=25)
        ent_ira_user.pack(pady=5, padx=40)
        ent_ira_user.insert(0, "0.0")

        tk.Label(janela_login, text="Total de créditos concluídos:", bg="#ffffff").pack(
            anchor="w", padx=40
        )
        ent_cred_user = tk.Entry(janela_login, font=("Arial", 10), width=25)
        ent_cred_user.pack(pady=5, padx=40)
        ent_cred_user.insert(0, "0")

        def confirmar_login():
            try:
                nome = ent_nome_user.get().strip()
                ira_ant = float(ent_ira_user.get())
                cred_ant = int(ent_cred_user.get())

                if not nome or not (0.0 <= ira_ant <= 5.0) or cred_ant < 0:
                    raise ValueError

                self.usuario = Usuario(
                    nome=nome, ira_anterior=ira_ant, creditos_anteriores=cred_ant
                )
                self.controle_faltas = ControleFaltas()
                self.simulador = Simulacao()

                janela_login.destroy()
                self.criar_widgets_app()
                self.criar_widgets_tutorial()
                self.atualizar_interface()
                self.root.deiconify()
            except ValueError:
                messagebox.showerror(
                    "Erro de Cadastro", "Preencha os dados corretamente."
                )

        tk.Button(
            janela_login,
            text="Entrar no Painel",
            command=confirmar_login,
            bg="#00a8ff",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5,
        ).pack(pady=15)

    def criar_widgets_app(self):
        self.frame_esquerdo = tk.Frame(self.root, bg="#f5f6fa")
        self.frame_esquerdo.pack(side="left", fill="both", expand=True, padx=10)

        lbl_titulo = tk.Label(
            self.frame_esquerdo,
            text=f"Painel Acadêmico - {self.usuario.nome}",
            font=("Arial", 16, "bold"),
            bg="#f5f6fa",
            fg="#2f3640",
        )
        lbl_titulo.pack(pady=15)

        frame_cadastro = tk.LabelFrame(
            self.frame_esquerdo,
            text=" Cadastrar Nova Disciplina ",
            font=("Arial", 10, "bold"),
            bg="#f5f6fa",
            fg="#718093",
        )
        frame_cadastro.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_cadastro, text="Nome:", bg="#f5f6fa").grid(
            row=0, column=0, padx=2, pady=10
        )
        self.ent_nome = tk.Entry(frame_cadastro, width=10, font=("Arial", 10))
        self.ent_nome.grid(row=0, column=1, padx=2, pady=10)

        tk.Label(frame_cadastro, text="Créd.", bg="#f5f6fa").grid(
            row=0, column=2, padx=2, pady=10
        )
        self.ent_creditos = tk.Entry(frame_cadastro, width=3, font=("Arial", 10))
        self.ent_creditos.grid(row=0, column=3, padx=2, pady=10)

        tk.Label(frame_cadastro, text="Carga:", bg="#f5f6fa").grid(
            row=0, column=4, padx=2, pady=10
        )
        self.ent_ch = tk.Entry(frame_cadastro, width=3, font=("Arial", 10))
        self.ent_ch.grid(row=0, column=5, padx=2, pady=10)

        tk.Label(frame_cadastro, text="Peso:", bg="#f5f6fa").grid(
            row=0, column=6, padx=2, pady=10
        )
        self.ent_nota = tk.Entry(frame_cadastro, width=3, font=("Arial", 10))
        self.ent_nota.grid(row=0, column=7, padx=2, pady=10)

        tk.Label(frame_cadastro, text="Tipo:", bg="#f5f6fa").grid(
            row=0, column=8, padx=2, pady=10
        )
        self.cb_tipo = ttk.Combobox(
            frame_cadastro,
            values=["Obrigatória", "Optativa"],
            width=10,
            state="readonly",
        )
        self.cb_tipo.current(0)
        self.cb_tipo.grid(row=0, column=9, padx=2, pady=10)

        btn_add = tk.Button(
            frame_cadastro,
            text="+",
            command=self.add_disciplina,
            bg="#4cd137",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            width=2,
        )
        btn_add.grid(row=0, column=10, padx=5, pady=10)

        self.tabela = ttk.Treeview(
            self.frame_esquerdo,
            columns=(
                "Nome",
                "Créditos",
                "Carga Horária",
                "Nota Atual",
                "Faltas",
                "Frequência",
                "Situação",
            ),
            show="headings",
            height=10,
        )
        colunas = [
            ("Nome", 110),
            ("Créditos", 60),
            ("Carga Horária", 100),
            ("Nota Atual", 80),
            ("Faltas", 60),
            ("Frequência", 85),
            ("Situação", 95),
        ]
        for col, larg in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=larg, anchor="center")
        self.tabela.pack(padx=10, pady=15, fill="both", expand=True)

        frame_rodape = tk.Frame(self.frame_esquerdo, bg="#f5f6fa")
        frame_rodape.pack(padx=10, pady=10, fill="x")

        self.lbl_ira = tk.Label(
            frame_rodape,
            text="IRA ATUAL: 0.00",
            font=("Arial", 13, "bold"),
            fg="#00a8ff",
            bg="#f5f6fa",
        )
        self.lbl_ira.pack(side="left", pady=5)

        btn_remover = tk.Button(
            frame_rodape,
            text="❌ Remover",
            command=self.deletar_disciplina,
            bg="#7f8c8d",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=8,
        )
        btn_remover.pack(side="right", padx=5)

        btn_falta = tk.Button(
            frame_rodape,
            text="+ Registrar Falta (2h)",
            command=self.add_falta,
            bg="#e84118",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=8,
        )
        btn_falta.pack(side="right", padx=5)

        btn_simular = tk.Button(
            frame_rodape,
            text="🔮 Simular Nota",
            command=self.janela_simulacao,
            bg="#9c88ff",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=8,
        )
        btn_simular.pack(side="right", padx=5)

    def criar_widgets_tutorial(self):
        self.frame_direito = tk.Frame(
            self.root, bg="#ffffff", bd=1, relief="solid", highlightthickness=0
        )
        self.frame_direito.pack(side="right", fill="y", padx=15, pady=15)

        lbl_inst_titulo = tk.Label(
            self.frame_direito,
            text="📖 Guia de Uso Rápido",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#2f3640",
        )
        lbl_inst_titulo.pack(pady=15, padx=15, anchor="w")

        texto_tutorial = (
            "1. CADASTRAR DISCIPLINAS\n"
            "Preencha os dados e escolha se ela é\n"
            "Obrigatória ou Optativa no seletor.\n\n"
            "2. TABELA DE CONVERSÃO DE NOTAS\n"
            "Insira a menção convertida em valor:\n"
            " • SS ➔ 5.0 | MS ➔ 4.0 | MM ➔ 3.0\n"
            " • MI ➔ 2.0 | II  ➔ 1.0 | SR ➔ 0.0\n\n"

        )

        lbl_corpo = tk.Label(
            self.frame_direito,
            text=texto_tutorial,
            font=("Arial", 9),
            bg="#ffffff",
            fg="#3d3d3d",
            justify="left",
            anchor="w",
        )
        lbl_corpo.pack(padx=15, pady=5, fill="both")

    def atualizar_interface(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for d in self.usuario.disciplinas:
            freq = d.calcular_percentual_frequencia()
            reprovado = self.controle_faltas.verificar_reprovacao(d)

            # POLIMORFISMO EM AÇÃO AQUI:
            situacao = d.obter_status_formatado(reprovado)

            self.tabela.insert(
                "",
                "end",
                values=(
                    d.nome,
                    d.creditos,
                    f"{d.carga_horaria}h",
                    f"{d.nota:.1f}",
                    f"{d.faltas}h",
                    f"{freq:.1f}%",
                    situacao,
                ),
            )

        self.lbl_ira.config(text=f"IRA ATUAL: {self.usuario.calcular_IRA():.2f}")

    def add_disciplina(self):
        try:
            nome = self.ent_nome.get().strip()
            creditos = int(self.ent_creditos.get())
            ch = int(self.ent_ch.get())
            nota = float(self.ent_nota.get())
            tipo = self.cb_tipo.get()

            if not nome or not (0.0 <= nota <= 5.0):
                raise ValueError

            # HERANÇA EM AÇÃO NA INSTANCIAÇÃO:
            if tipo == "Obrigatória":
                nova_disc = DisciplinaObrigatoria(nome, creditos, ch)
            else:
                nova_disc = DisciplinaOptativa(nome, creditos, ch)

            nova_disc.nota = nota
            self.usuario.adicionar_disciplina(nova_disc)
            self.atualizar_interface()

            self.ent_nome.delete(0, tk.END)
            self.ent_creditos.delete(0, tk.END)
            self.ent_ch.delete(0, tk.END)
            self.ent_nota.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro de Input", "Preencha os campos corretamente.")

    def add_falta(self):
        item_selecionado = self.tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma disciplina na tabela!")
            return

        indice = self.tabela.index(item_selecionado[0])
        disciplina_selecionada = self.usuario.disciplinas[indice]
        self.controle_faltas.registrar_falta(disciplina_selecionada, horas=2)
        self.atualizar_interface()

        restantes = disciplina_selecionada.calcular_faltas_restantes()
        if self.controle_faltas.verificar_reprovacao(disciplina_selecionada):
            messagebox.showerror(
                "Aviso", f"Reprovado por falta em {disciplina_selecionada.nome}!"
            )
        elif restantes <= 4:
            messagebox.showwarning(
                "Limite",
                f"Você só pode faltar mais {restantes}h em {disciplina_selecionada.nome}.",
            )

    def deletar_disciplina(self):
        item_selecionado = self.tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma disciplina!")
            return

        indice = self.tabela.index(item_selecionado[0])
        disciplina_alvo = self.usuario.disciplinas[indice]

        if messagebox.askyesno("Confirmar", f"Deseja remover {disciplina_alvo.nome}?"):
            self.usuario.remover_disciplina(disciplina_alvo)
            self.atualizar_interface()

    def janela_simulacao(self):
        item_selecionado = self.tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione a disciplina alvo!")
            return

        indice = self.tabela.index(item_selecionado[0])
        disciplina_alvo = self.usuario.disciplinas[indice]

        pop = tk.Toplevel(self.root)
        pop.title("Simulador de IRA")
        pop.geometry("300x180")
        pop.configure(bg="#f5f6fa")
        pop.grab_set()

        tk.Label(
            pop,
            text=f"Simulação para: {disciplina_alvo.nome}",
            font=("Arial", 11, "bold"),
            bg="#f5f6fa",
            fg="#2f3640",
        ).pack(pady=10)
        ent_ira_alvo = tk.Entry(pop, font=("Arial", 10), width=10, justify="center")
        ent_ira_alvo.pack(pady=5)
        ent_ira_alvo.insert(0, "4.0")

        def executar_calculo_reverso():
            try:
                ira_alvo = float(ent_ira_alvo.get())
                if not (0.0 <= ira_alvo <= 5.0):
                    raise ValueError

                peso_necessario = self.simulador.nota_necessaria(
                    self.usuario.disciplinas,
                    disciplina_alvo,
                    ira_alvo,
                    self.usuario.ira_anterior,
                    self.usuario.creditos_anteriores,
                )

                # Se o cálculo der maior que 5, significa que matemática é impossível atingir
                if peso_necessario > 5.0:
                    messagebox.showwarning(
                        "Meta Impossível",
                        f"Matematicamente não é possível atingir o IRA {ira_alvo:.2f} apenas com esta matéria, pois exigiria uma nota maior que SS.",
                    )
                    pop.destroy()
                    return

                # Traduz o peso para a menção (ex: 5.00 -> SS)
                mencao = self.simulador.converter_peso_para_mencao(peso_necessario)

                messagebox.showinfo(
                    "Previsão de Nota",
                    f"Para atingir o IRA global de {ira_alvo:.2f} no final do semestre:\n\n"
                    f"Você precisa tirar no mínimo a menção {mencao} (Peso correspondente: {max(0.0, peso_necessario):.2f}) na matéria {disciplina_alvo.nome}.",
                )
                pop.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Insira um valor válido para o IRA.")

        tk.Button(
            pop,
            text="Calcular Meta",
            command=executar_calculo_reverso,
            bg="#9c88ff",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
        ).pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppMetricas(root)
    root.mainloop()
