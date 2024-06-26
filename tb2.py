import ast
import hashlib
import calendar
from datetime import datetime, timedelta
from termcolor import colored

# Dicionário global para armazenar as frequências
frequencias_globais = {}

def cadastroTurma():
    op = 's'
    while op != 'n':
        codigoD = input("Digite o código da disciplina: ")
        nome = input("Digite o nome da disciplina: ")
        codigoT = input("Digite o código da turma: ")
        ano = input("Digite o ano em que a disciplina está sendo ofertada: ")
        dias = int(input("Número de aulas na semana: "))
        dias_aulas = []
        for i in range(dias):
            dia = input(f'Digite o {i+1}º dia de aula (ex: segunda, terça): ')
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
            nota_soma += f' {peso}*{nomeA} '
            if i != num_avaliacoes - 1:
                nota_soma += '+'
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
        with open('turmas.txt', 'a') as turma:
            turma.write(f'{infoTurma}\n')
        op = input("Deseja cadastrar outra turma (s/n)? ")
    menuProfessor()

def edicaoTurma():
    b = True
    codigoT = input("Digite o código da turma que deseja editar: ")
    with open('turmas.txt', 'r') as turma:
        linhas = turma.readlines()
    with open('turmas.txt', 'w') as turma:
        for linha in linhas:
            informacoes = ast.literal_eval(linha.strip())
            if informacoes['Codigo da turma'] == codigoT:
                while b:
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
                    elif op == '4':
                        semestre = input("Digite o semestre: ")
                        informacoes['Semestre'] = semestre
                    elif op == '3':
                        ano = input("Digite o ano: ")
                        informacoes['Ano'] = ano
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
                            nomeA = input(f"Digite o nome/tipo da avaliação {i+1}: ")
                            avaliacoes[f'Avaliacao {i+1}'] = nomeA
                            avaliacoes[f'Peso {i+1}'] = peso
                            nota_soma += f' {peso}*{nomeA} '
                            if i != num_avaliacoes - 1:
                                nota_soma += '+'
                            soma_pesos += peso
                        notaFinal = f'{nota_soma}/{soma_pesos}'
                        informacoes['Nota final'] = notaFinal
                        informacoes['Avaliacoes'] = avaliacoes
                    else:
                        b = False
                        break
                turma.write(f'{informacoes}\n')
            else:
                turma.write(f'{informacoes}\n')
    menuProfessor()

def excTurma():
    codigoT = input("Digite o código da turma: ")
    with open('turmas.txt', 'r') as turma:
        linhas = turma.readlines()
    with open('turmas.txt', 'w') as turma:
        turma_encontrada = False
        for linha in linhas:
            informacoes = ast.literal_eval(linha.strip())
            if informacoes['Codigo da turma'] != codigoT:
                turma.write(f'{informacoes}\n')
            else:
                turma_encontrada = True
    if turma_encontrada:
        print("Turma excluída com sucesso.")
    else:
        print("Turma não encontrada.")
    menuProfessor()

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
    
    dias_indices = [dia_semana[dia] for dia in dias_aulas]
    
    data_atual = inicio
    while data_atual <= fim:
        if data_atual.weekday() in dias_indices:
            frequencias[data_atual.strftime('%d/%m/%Y')] = 2 # Presença não lançada
        data_atual += timedelta(days=1)

    return frequencias

def Alunos():
    op = 's'
    while op != 'n':
        print("1 - Para modificar as notas de um aluno.")
        print("2 - Para modificar as frequências de um aluno.")
        print("3 - Cadastrar um aluno.")
        op = input("Digite o número e 'n' para voltar ao menu inicial: ")
        with open('alunos.txt', 'r') as alunos:
            linhas = alunos.readlines()
        if op == '1':
            DRE = input("Digite o DRE do aluno: ")
            with open('alunos.txt', 'w') as alunos:
                for linha in linhas:
                    al = ast.literal_eval(linha.strip())
                    if al['DRE'] == DRE:
                        print(al)
                        if 'Notas' in al:
                            numero = int(input("Digite o número da avaliação que deseja alterar (1,2,3,...): "))
                            nota = float(input("Digite a nova nota: "))
                            if len(al['Notas']) >= numero:
                                al['Notas'][numero-1] = nota
                            else:
                                print("Número de avaliação inválido.")
                        else:
                            print("O aluno ainda não tem notas lançadas.")
                            al['Notas'] = []
                    alunos.write(f'{al}\n')
        elif op == '2':
            DRE = input("Digite o DRE do aluno: ")
            with open('alunos.txt', 'w') as alunos:
                for linha in linhas:
                    al = ast.literal_eval(linha.strip())
                    if al['DRE'] == DRE:
                        print(formatarCalendario(al['Frequencias']))
                        freq_data = input("Digite a data (dd/mm/yyyy): ")
                        freq_status = int(input("Digite a frequência (1 para presença e 0 para falta): "))
                        al['Frequencias'][f'{freq_data}'] = freq_status
                        print(formatarCalendario(al['Frequencias']))
                    alunos.write(f'{al}\n')
        elif op == '3':
            codigoD = input("Digite o código da disciplina: ")
            codigoT = input("Digite o código da turma: ")
            nome = input("Digite o nome completo do aluno: ")
            DRE = input("Digite o DRE do aluno: ")
            if codigoD in frequencias_globais:
                frequencias = frequencias_globais[codigoD]
            else:
                frequencias = gerar_frequencias(dias_aulas)
                frequencias_globais[codigoD] = frequencias
            al = {
                'Nome': nome,
                'DRE': DRE,
                'Codigo da disciplina': codigoD,
                'Codigo da turma': codigoT,
                'Frequencias': frequencias
            }
            with open('alunos.txt', 'a') as alunos:
                alunos.write(f'{al}\n')
            print("Aluno cadastrado.")
        else:
            op = input("Opção incorreta, pressione 'n' para sair.")

def lancarFrequencias():
    op = 's'
    while op != 'n':

        codigoD = input("Digite o codigo da disciplina que deseja lançar as frequências:")
        codigoT = input("Digite o codigo da turma:")
        
        freq_data = input("Digite a data (dd/mm/yyyy): ")
        freq_status = int(input("Digite a frequência (1 para presença e 0 para falta): "))

        # Ler todos os alunos
        with open('alunos.txt', 'r') as alunos:
            linhas = alunos.readlines()
            b = False
            with open('alunos.txt', 'w') as alunos:
                for linha in linhas:
                    al = ast.literal_eval(linha.strip())
                    if al['Codigo da disciplina'] == codigoD and al['Codigo da turma'] == codigoT:
                        DRE = input("Digite o DRE do aluno:")
                        if DRE == al['DRE']:
                            if 'Frequencias' in al:
                                print(formatarCalendario(al['Frequencias']))
                                al['Frequencias'][f'{freq_data}'] = freq_status
                                b = True
                                print(formatarCalendario(al['Frequencias']))
                                alunos.write(f'{al}\n')
                            else:
                                al['Frequencias'] = {}
                                al['Frequencias'][f'{freq_data}'] = freq_status
                                alunos.write(f'{al}\n')
                        else:
                            alunos.write(f'{al}\n')
                    else:
                        alunos.write(f'{al}\n')
        if b == False:
            print("Aluno não encontrado.")

        op = input("Pressione 'n' para sair, 's' para continuar: ")
    menuProfessor()

def formatarCalendario(frequencias):
    
    # Organiza as frequências por mês
    meses = {i: {} for i in range(1, 13)}
    for data, freq in frequencias.items():
        dia, mes, ano = map(int, data.split('/'))
        meses[mes][dia] = freq

    # Lista de cores para os status
    cores = {
        2: 'yellow',  # Dia com aula (presença não lançada)
        1: 'green',   # Presença lançada
        0: 'red'      # Falta
    }

    # String para armazenar o calendário colorido
    cal = ""

    # Percorre todos os meses do ano
    for mes in range(1, 13):  # Meses de 1 a 12
        if meses[mes]:  # Verifica se há dias registrados para o mês atual
            cal += f"{calendar.month_name[mes]}:\n"
            cal += "Dom Seg Ter Qua Qui Sex Sáb\n"
            
            # Obtém a matriz de dias do mês e seus status de frequência
            matriz_mes = calendar.monthcalendar(2024, mes)  # Assumindo o ano 2024
            
            for semana in matriz_mes:
                for dia in semana:
                    if dia == 0:
                        cal += "    "  # Dia vazio para dias que não pertencem ao mês
                    elif dia in meses[mes]:
                        freq = meses[mes][dia]
                        status = colored(f"{dia:2d}", cores.get(freq, 'yellow'))  # Colore o dia de acordo com o status
                        cal += f" {status}"
                    else:
                        cal += f" {dia:2d}"  # Dia comum (sem aula)
                cal += "\n"
            cal += "\n"
    
    return cal

def Verfrequencia():
    op = 's'
    b = False
    while op != 'n':
        codigoD = input("Digite o código da disciplina para exibir a frequencia: ")
        DRE = input("Digite o seu DRE: ")
        with open('alunos.txt', 'r') as turma:
            linhas = turma.readlines()
            for linha in linhas:
                al = ast.literal_eval(linha.strip())
                if al['Codigo da disciplina'] == codigoD and al['DRE'] == DRE: 
                    freq = al.get('Frequencias', {})
                    print(formatarCalendario(freq))   
                    b = True  
            op = input("Pressione 'n' para sair, 's' para continuar.")
    if b == False : print("Disciplina não encontrada.") 
    menuAluno()

def lancarNotas():
    op = 's'
    while op != 'n':
        codigoD = input("Digite o codigo da disciplina que deseja lançar notas:")
        codigoT = input("Digite o codigo da turma:")
        avaliacoes = {}
        with open('alunos.txt', 'r') as alunos:
            linhas = alunos.readlines()
        with open('alunos.txt', 'w') as alunos:
            for linha in linhas:
                al = ast.literal_eval(linha.strip())
                if al['Codigo da disciplina'] == codigoD and al['Codigo da turma'] == codigoT:
                    print(al)
                    i = 0
                    op2 = 's'
                    while op2 != 'n':
                        nota = input("Digite o valor da nota: ")
                        op2 = input("Digite s/n para finalizar ou continuar adicionando notas.")
                        avaliacoes[f'Avaliacao {i+1}'] = nota
                        i += 1
                    al['Avaliacoes'] = avaliacoes
                alunos.write(f'{al}\n')
        op = input("Pressione 'n' para sair, 's' para continuar.")
    menuProfessor()

def Vernotas():
    nome = input("Digite o seu nome completo:")
    DRE = input("Digite o seu DRE:")
    with open('alunos.txt', 'r') as alunos:
        for aluno in alunos:
            al = ast.literal_eval(aluno.strip())
            if al['Nome'].lower() == nome.lower() and al['DRE'].lower() == DRE.lower():
                print(al['Avaliacoes'])
    menuAluno()

def VercalculoNotas():
    op = 's'
    while op != 'n':
        codigoD = input("Digite o código da disciplina para exibir o cálculo da nota final: ")
        with open('turmas.txt', 'r') as turma:
            linhas = turma.readlines()
            for linha in linhas:
                infoTurma = ast.literal_eval(linha.strip())
                if infoTurma['Codigo da disciplina'] == codigoD:
                    print(f"Nota Final da disciplina {infoTurma['Nome']}: {infoTurma['Nota final']}")
            op = input("Pressione 'n' para sair, 's' para continuar.")
    if op == 'n':
        print("Disciplina não encontrada.")
    menuAluno()

def VerpontosNecessarios():
    # Função para ver pontos necessários para aprovação
    menuAluno()

def menuProfessor():
    op = 's'
    while op != 'n':
        print("1 - Cadastro de turma")
        print("2 - Edição de turma")
        print("3 - Exclusão de turma")
        print("4 - Alunos")
        print("5 - Lançar notas")
        print("6 - Lançar frequências")
        tarefa = input("Digite o número ou 'sair' para sair: ")
        if tarefa == '1':
            cadastroTurma()
        elif tarefa == '2':
            edicaoTurma()
        elif tarefa == '3':
            excTurma()
        elif tarefa == '4':
            Alunos()
        elif tarefa == '5':
            lancarNotas()
        elif tarefa == '6':
            lancarFrequencias()
        elif tarefa == 'sair':
            return 0
        else:
            print("Opção errada.")
        op = input("Digite s/n se deseja continuar.")
    identificacao()

def menuAluno():
    op = 's'
    while op != 'n':
        print("1 - Notas")
        print("2 - Ver as médias das notas das turmas, cálculo da média final e etc.")
        print("3 - Frequência")
        print("4 - Quantos pontos são necessários para a aprovação")
        tarefa = input("Digite uma opção: ")
        if tarefa == '1':
            Vernotas()
        elif tarefa == '2':
            VercalculoNotas()
        elif tarefa == '3':
            Verfrequencia()
        elif tarefa == '4':
            VerpontosNecessarios()
        else:
            print("Opção errada.")
        op = input("Digite s/n se deseja continuar.")

def identificacao():
    tipo = input("Informe aluno, professor ou sair se desejar encerrar o programa: ")
    if tipo.lower() == 'sair':
        return 0
    
    if tipo.lower() == 'aluno':
        while True:
            nome = input("Digite o seu nome completo: ")
            DRE = input("Digite o seu DRE: ")
            c = False
            for linha in linhas:
                al = ast.literal_eval(linha.strip())
                if al['Nome'].lower() == nome.lower() and al['DRE'].lower() == DRE.lower():
                    c = True
                    print("Login bem-sucedido.")
                    menuAluno()
                    return
            if not c:
                print("Nome ou/e DRE incorretos, digite novamente.")
    
    elif tipo.lower() == 'professor':
        while True:
            r = input("Deseja se cadastrar(s/n)? ").lower()
            
            if r == 's':
                login = input("Digite o nome de usuário: ")
                senha = input("Digite a senha: ")
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                disciplinas = {}
                numero = int(input("Quantas disciplinas você ministra: "))
                for i in range(numero):
                    chave = input("Digite o nome da disciplina: ")
                    codigoD = input("Digite o codigo da disciplina: ")
                    dias_aulas = input("Digite os dias da semana que tem aula (ex: segunda, quarta): ").split(', ')
                    frequencias = gerar_frequencias(dias_aulas)
                    disciplinas[chave] = codigoD
                professor = {
                    'Nome': login,
                    'Senha': senha_hash,
                    'Disciplinas': disciplinas
                }
                with open('professores.txt', 'a') as cadastro:
                    cadastro.write(f'{professor}\n')
                print("Usuário cadastrado com sucesso. Agora faça o login.")
            
            while True:
                login = input("Digite o nome de usuário: ")
                senha = input("Digite a senha: ")
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                c = False
                with open('professores.txt', 'r') as cadastro:
                    linhas = cadastro.readlines()
                    for linha in linhas:
                        informacoes = ast.literal_eval(linha.strip())
                        if informacoes['Nome'].lower() == login.lower() and informacoes['Senha'] == senha_hash:
                            c = True
                            print("Login bem-sucedido.")
                            menuProfessor()
                            return
                if not c:
                    print("Usuário ou/e senha incorretos, digite novamente.")
                    break
        
    else:
        print("Opção não identificada, digite se você é aluno ou professor.")
        identificacao()

identificacao()