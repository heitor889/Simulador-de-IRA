# modelos.py
from abc import ABC, abstractmethod


class Disciplina(ABC):
    def __init__(self, nome: str, creditos: int, carga_horaria: int):
        self.nome = nome
        self.creditos = creditos
        self.carga_horaria = carga_horaria
        self.nota = 0.0  # Peso da menção (0.0 a 5.0)
        self.faltas = 0  # Horas de falta acumuladas

    def calcular_faltas_restantes(self) -> int:
        limite_faltas = self.carga_horaria * 0.25
        return max(0, int(limite_faltas - self.faltas))

    def calcular_percentual_frequencia(self) -> float:
        if self.carga_horaria == 0:
            return 100.0
        presencas = self.carga_horaria - self.faltas
        return (presencas / self.carga_horaria) * 100

    @abstractmethod
    def obter_status_formatado(self, reprovado_por_falta: bool) -> str:
        """Método polimórfico implementado pelas subclasses"""
        pass


class DisciplinaObrigatoria(Disciplina):
    def obter_status_formatado(self, reprovado_por_falta: bool) -> str:
        if reprovado_por_falta:
            return "RF (Obrig.)"
        return "Regular"


class DisciplinaOptativa(Disciplina):
    def obter_status_formatado(self, reprovado_por_falta: bool) -> str:
        if reprovado_por_falta:
            return "RF (Optat.)"
        return "Regular (Opt)"


class CalculadoraIRA:
    def calcular_IRA(
        self,
        disciplinas: list[Disciplina],
        ira_anterior: float,
        creditos_anteriores: int,
    ) -> float:
        if not disciplinas:
            return round(ira_anterior, 2)

        soma_ponderada_semestre = 0.0
        creditos_semestre = 0

        for d in disciplinas:
            # Criamos uma instância temporária para checar a assiduidade
            # Se o aluno tiver menos de 75% de presença, a nota vira 0.0 obrigatoriamente
            frequencia = d.calcular_percentual_frequencia()
            reprovado_por_falta = frequencia < 75.0

            if reprovado_por_falta:
                nota_efetiva = 0.0  # Consequência do RF: Nota vira zero
            else:
                nota_efetiva = d.nota

            soma_ponderada_semestre += nota_efetiva * d.creditos
            creditos_semestre += (
                d.creditos
            )  # O crédito CONTINUA contando aqui, penalizando o IRA

        pontos_anteriores = ira_anterior * creditos_anteriores
        pontos_totais = pontos_anteriores + soma_ponderada_semestre
        creditos_totais = creditos_anteriores + creditos_semestre

        return round(pontos_totais / creditos_totais, 2) if creditos_totais > 0 else 0.0


class ControleFaltas:
    def registrar_falta(self, d: Disciplina, horas: int = 2):
        d.faltas += horas

    def verificar_reprovacao(self, d: Disciplina) -> bool:
        return d.calcular_percentual_frequencia() < 75.0


class Simulacao:
    def nota_necessaria(
        self,
        disciplinas: list[Disciplina],
        disciplina_alvo: Disciplina,
        ira_desejado: float,
        ira_anterior: float,
        creditos_anteriores: int,
    ) -> float:
        creditos_semestre = sum(d.creditos for d in disciplinas)
        total_creditos_geral = creditos_anteriores + creditos_semestre

        pontos_totais_necessarios = ira_desejado * total_creditos_geral
        pontos_historico = ira_anterior * creditos_anteriores
        pontos_outras_semestre = sum(
            d.nota * d.creditos for d in disciplinas if d != disciplina_alvo
        )

        pontos_ja_adquiridos = pontos_historico + pontos_outras_semestre
        pontos_na_alvo_necessarios = pontos_totais_necessarios - pontos_ja_adquiridos

        return pontos_na_alvo_necessarios / disciplina_alvo.creditos

    def converter_peso_para_mencao(self, peso: float) -> str:
        """Converte o peso numérico de volta para a menção oficial da UnB"""
        if peso > 4.5:
            return "SS"
        if peso > 3.5:
            return "MS"
        if peso > 2.5:
            return "MM"
        if peso > 1.5:
            return "MI"
        if peso > 0.5:
            return "II"
        return "SR"


class Usuario:
    def __init__(self, nome: str, ira_anterior: float = 0.0, creditos_anteriores: int = 0):
        self.nome = nome
        self.ira_anterior = ira_anterior
        self.creditos_anteriores = creditos_anteriores
        self.disciplinas: list[Disciplina] = []
        self.calculadora = CalculadoraIRA()

    def adicionar_disciplina(self, disciplina: Disciplina):
        self.disciplinas.append(disciplina)

    def remover_disciplina(self, disciplina: Disciplina):
        if disciplina in self.disciplinas:
            self.disciplinas.remove(disciplina)

    def calcular_IRA(self) -> float:
        # A calculadora agora analisa o estado de faltas de cada disciplina internamente
        return self.calculadora.calcular_IRA(self.disciplinas, self.ira_anterior, self.creditos_anteriores)