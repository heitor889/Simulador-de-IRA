# modelos.py

class Disciplina:
    def __init__(self, nome: str, creditos: int, carga_horaria: int):
        self.nome = nome
        self.creditos = creditos
        self.carga_horaria = carga_horaria
        self.nota = 0.0  
        self.faltas = 0  

    def calcular_faltas_restantes(self) -> int:
        limite_faltas = self.carga_horaria * 0.25
        restantes = int(limite_faltas - self.faltas)
        return max(0, restantes)

    def calcular_percentual_frequencia(self) -> float:
        if self.carga_horaria == 0:
            return 100.0
        presencas = self.carga_horaria - self.faltas
        return (presencas / self.carga_horaria) * 100


class CalculadoraIRA:
    def calcular_IRA(self, disciplinas: list[Disciplina], ira_anterior: float, creditos_anteriores: int) -> float:
        if not disciplinas:
            return round(ira_anterior, 2)
        
        soma_ponderada_semestre = sum(d.nota * d.creditos for d in disciplinas)
        creditos_semestre = sum(d.creditos for d in disciplinas)
        
        pontos_anteriores = ira_anterior * creditos_anteriores
        pontos_totais = pontos_anteriores + soma_ponderada_semestre
        creditos_totais = creditos_anteriores + creditos_semestre
        
        return round(pontos_totais / creditos_totais, 2) if creditos_totais > 0 else 0.0


class ControleFaltas:
    def registrar_falta(self, disciplina: Disciplina, horas: int = 2):
        disciplina.faltas += horas

    def verificar_reprovacao(self, disciplina: Disciplina) -> bool:
        return disciplina.calcular_percentual_frequencia() < 75.0


class Simulacao:
    def nota_necessaria(self, disciplinas: list[Disciplina], disciplina_alvo: Disciplina, ira_desejado: float, ira_anterior: float, creditos_anteriores: int) -> float:
        creditos_semestre = sum(d.creditos for d in disciplinas)
        total_creditos_geral = creditos_anteriores + creditos_semestre
        
        pontos_totais_necessarios = ira_desejado * total_creditos_geral
        
        pontos_historico = ira_anterior * creditos_anteriores
        pontos_outras_semestre = sum(d.nota * d.creditos for d in disciplinas if d != disciplina_alvo)
        
        pontos_ja_adquiridos = pontos_historico + pontos_outras_semestre
        pontos_na_alvo_necessarios = pontos_totais_necessarios - pontos_ja_adquiridos
        nota_precisa = pontos_na_alvo_necessarios / disciplina_alvo.creditos
        
        return round(max(0.0, min(5.0, nota_precisa)), 2)


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
        return self.calculadora.calcular_IRA(self.disciplinas, self.ira_anterior, self.creditos_anteriores)