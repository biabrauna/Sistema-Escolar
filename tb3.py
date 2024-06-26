import ast
import hashlib
import calendar
from datetime import datetime, timedelta
from termcolor import colored

# Dicionário global para armazenar as frequências
frequencias_globais = {}

def ler_arquivos():
    with open('alunos.txt','r') as file_alunos, open('professores.txt','r') as file_professores, open('turmas.txt','r') as file_turmas:
        alunos = file_alunos.readlines()
        professores = file_professores.readlines()
        turmas = file_turmas.readlines()
    return alunos, professores, turmas

def cadastroTurma(alunos, professores, turmas):
    op = 's'
    while op != 'n':
        codigoD = input("Digite o código da disciplina: ")
        nome = input("Digite o nome da disciplina: ")
        codigoT = input("Digite o código da turma: ")
        ano = input("Digite o ano em que a disciplina está sendo ofertada: ")
        dias = int(input("Número de aulas na semana: "))
        dias_aulas = []
        for i in range(dias):
            dia = input(f'Digite o {i+1} dia de aula (dd/mm/yyyy): ')
            dias_aulas.append(dia)
        semestre = input("Digite o semestre em que a disciplina está sendo ofertada: ")
        hora = input("Digite a hora em que a disciplina está sendo oferecida: ")
        num_avaliacoes = int(input("Quantas avaliações tem? "))
        
        avaliacoes = {}
        nota_soma = ""
        soma_pesos = 0
        for i in range(num_avaliacoes):
            peso = float(input(f"Digite o peso da avaliação {i+1}: "))
            nomeA = input(f"Digite o nome/tipo da avaliação {i+1}: ")
            avaliacoes[f'Avaliacao {i+1}'] = nomeA
            avaliacoes[f'Peso {i+1}'] = peso
            nota_soma += f'{peso}*{nomeA}'
            if i != num_avaliacoes - 1:
                nota_soma += ' + '
            soma_pesos += peso
        notaFinal = f'{nota_soma}/{soma_pesos}'
        
        infoTurma = {
            'Codigo da disciplina': codigoD,
            'Nome': nome,
            'Codigo da turma': codigoT,
            'Ano': ano,
            'Semestre': semestre,
            'Dias': dias_aulas,
            'Hora': hora,
            'Avaliacoes': avaliacoes,
            'Nota final': notaFinal
        }
        
        with open('turmas.txt', 'a') as turma_file:
            turma_file.write(f'{infoTurma}\n')
        
        op = input("Deseja cadastrar outra turma (s/n)? ")
    
    menuProfessor(alunos, professores, turmas)

def edicaoTurma(turmas):
    codigoT = input("Digite o código da turma que deseja editar: ")
    turmas_atualizados = []
    with open('turmas.txt', 'r') as turmas_file:
        for linha in turmas_file:
            informacoes = ast.literal_eval(linha.strip())
            if informacoes['Codigo da turma'] == codigoT:
                while True:
                    print("1 - Código da disciplina")
                    print("2 - Nome")
                    print("3 - Ano")
                    print("4 - Semestre")
                    print("5 - Hora")
                    print("6 - Avaliações")
                    print("7 - Sair")
                    op = input("Digite o que deseja editar: ")
                    if op == '1':
                        codigoD = input("Digite o novo código: ")
                        informacoes['Codigo da disciplina'] = codigoD
                    elif op == '2':
                        nome = input("Digite o nome da disciplina: ")
                        informacoes['Nome'] = nome
                    elif op == '3':
                        ano = input("Digite o ano: ")
                        informacoes['Ano'] = ano
                    elif op == '4':
                        semestre = input("Digite o semestre: ")
                        informacoes['Semestre'] = semestre
                    elif op == '5':
                        hora = input("Digite a hora: ")
                        informacoes['Hora'] = hora
                    elif op == '6':
                        avaliacoes = {}
                        nota_soma = ""
                        soma_pesos = 0
                        num_avaliacoes = int(input("Digite o número de avaliações: "))
                        for i in range(num_avaliacoes):
                            peso = float(input(f"Digite o peso da avaliação {i+1}: "))
                            nome = input(f"Digite o nome/tipo da avaliação {i+1}: ")
                            avaliacoes[f'Avaliacao {i+1}'] = nome
                            avaliacoes[f'Peso {i+1}'] = peso
                            nota_soma += f'{peso}*{nome}'
                            if i != num_avaliacoes - 1:
                                nota_soma += ' + '
                            soma_pesos += peso
                        informacoes['Avaliacoes'] = avaliacoes
                        informacoes['Nota final'] = f'{nota_soma}/{soma_pesos}'
                    elif op == '7':
                        break
                    else:
                        print("Opção inválida.")
                turmas_atualizados.append(informacoes)
            else:
                turmas_atualizados.append(informacoes)
    
    with open('turmas.txt', 'w') as turmas_file:
        for turma in turmas_atualizados:
            turmas_file.write(f'{turma}\n')
    
    menuProfessor(alunos, professores, turmas)

def excTurma(alunos, professores, turmas):
    codigoT = input("Digite o código da turma que deseja excluir: ")
    turmas_atualizados = []
    with open('turmas.txt', 'r') as turmas_file:
        for linha in turmas_file:
            informacoes = ast.literal_eval(linha.strip())
            if informacoes['Codigo da turma'] != codigoT:
                turmas_atualizados.append(informacoes)
    
    with open('turmas.txt', 'w') as turmas_file:
        for turma in turmas_atualizados:
            turmas_file.write(f'{turma}\n')
    
    print("Turma excluída com sucesso.")
    menuProfessor(alunos, professores, turmas)

def gerar_frequencias(dias_aulas):
    frequencias = {}
    hoje = datetime.now().date()
    inicio = hoje - timedelta(days=15)
    fim = hoje + timedelta(days=30)
    dia_semana = {
        'domingo': 6,
        'segunda': 0,
        'terça': 1,
        'quarta': 2,
        'quinta': 3,
        'sexta': 4,
        'sábado': 5
    }
    
    dias_indices = [dia_semana[dia.lower()] for dia in dias_aulas]
    
    data_atual = inicio
    while data_atual <= fim:
        if data_atual.weekday() in dias_indices:
            frequencias[data_atual.strftime('%d/%m/%Y')] = 2  # Presença não lançada
        data_atual += timedelta(days=1)

    return frequencias

def Alunos(alunos, professores, turmas):
    op = 's'
    while op != 'n':
        print("1 - Modificar as notas de um aluno.")
        print("2 - Modificar as frequências de um aluno.")
        print("3 - Cadastrar um aluno.")
        print("4 - Sair")
        op = input("Digite o número ou 'n' para voltar ao menu inicial: ")
        
        if op == '1':
            DRE = input("Digite o DRE do aluno: ")
            with open('alunos.txt', 'r') as alunos_file:
                linhas = alunos_file.readlines()
            with open('alunos.txt', 'w') as alunos_file:
                for linha in linhas:
                    al = ast.literal_eval(linha.strip())
                    if al['DRE'] == DRE:
                        print(al)
                        if 'Notas' in al:
                            numero = int(input("Digite o número da avaliação que deseja alterar: "))
                            nota = float(input("Digite a nova nota: "))
                            al['Notas'][numero - 1] = nota
                        else:
                            print("O aluno ainda não tem notas lançadas.")
                            al['Notas'] = []
                    alunos_file.write(f'{al}\n')
        
        elif op == '2':
            DRE = input("Digite o DRE do aluno: ")
            with open('alunos.txt', 'r') as alunos_file:
                linhas = alunos_file.readlines()
            with open('alunos.txt', 'w') as alunos_file:
                for linha in linhas:
                    al = ast.literal_eval(linha.strip())
                    if al['DRE'] == DRE:
                        while True:
                            print(formatarCalendario(al['Frequencias']))
                            freq_data = input("Digite a data (dd/mm/yyyy): ")
                            freq_status = int(input("Digite a frequência (1 para presença e 0 para falta): "))
                            al
