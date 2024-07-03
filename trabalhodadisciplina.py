import ast
import hashlib
import calendar
from datetime import datetime, timedelta
from termcolor import colored

def ler_arquivos():
    with open('alunos.txt','r') as file_alunos, open('professores.txt','r') as file_professores, open('turmas.txt','r') as file_turmas:
        alunos = file_alunos.readlines()
        professores = file_professores.readlines()
        turmas = file_turmas.readlines()
    return alunos, professores, turmas

def salvarTurmas(filename, turmas):
    with open(filename, 'w') as f:
        f.writelines(turmas)

# Sessão dos professores

def cadastroTurma(alunos,professores,turmas):
    op = 's'
    while op != 'n':
        codigoD = input("Digite o código da disciplina: ")
        nome = input("Digite o nome da disciplina: ")
        codigoT = input("Digite o código da turma: ")
        ano = input("Digite o ano em que a disciplina está sendo ofertada: ")
        dias = int(input("Numero de dias na semana que terá aula: "))
        for i in range(dias):
            dia = input(f'Digite o {i+1} dia de aula (segunda, quarta,...): ')
            dia[f'{dia}'] = 'n'
        semestre = input("Digite o semestre em que a disciplina está sendo ofertada: ")
        hora = input("Digite a hora em que a disciplina está sendo oferecida: ")
        num_avaliacoes = int(input("Quantas avaliaçoes tem? "))
        i=0
        avaliacoes = {}
        nota_soma = " "
        soma_pesos = 0
        while i!=num_avaliacoes:
            peso = float(input("Digite o peso da avaliação: "))
            nomeA = input(f"Digite o nome/tipo da avaliaçao {i+1}: ")
            avaliacoes[f'Avaliacao {i+1}'] = nomeA
            avaliacoes[f'Peso {i+1}'] = peso
            i+=1
            nota_soma += f' {peso}*{nomeA} '
            if i != num_avaliacoes-1:
                nota_soma += '+'
            soma_pesos += peso
        notaFinal = f'{nota_soma}/{soma_pesos}'
        infoTurma = {}
        infoTurma['Codigo da disciplina'] = codigoD
        infoTurma['Nome'] = nome
        infoTurma['Codigo da turma'] = codigoT
        infoTurma['Ano'] = ano
        infoTurma['Semestre'] = semestre
        infoTurma['Dias'] = dias
        infoTurma['Hora'] = hora
        infoTurma['Avaliacoes'] = avaliacoes
        infoTurma['Nota final'] = notaFinal
        turma = open('turmas.txt','a')
        turma.write(f'{infoTurma}\n')
        turma.close()
        op = input("Deseja cadastrar outra turma(s/n)?")
    menuProfessor(alunos,professores,turmas)

def edicaoTurma(turmas):
    op = 'n'
    for turma in turmas:
        print(turma)
    codigoT = input("Digite o codigo da turma que deseja editar: ")
    for i, linha in enumerate(turmas):
        informacoes = ast.literal_eval(linha.strip())
        if informacoes['Codigo da turma'] == codigoT:
            while op != 's':
                print("1 - Codigo da disciplina")
                print("2 - Nome")
                print("3 - Ano")
                print("4 - Semestre")
                print("5 - Hora")
                print("6 - Avaliacoes")
                print("7 - Sair \n")
                op = input("Digite o que deseja editar e s para sair: ")
                if op == '1':
                    codigoD = input("Digite o novo codigo: ")
                    informacoes['Codigo da disciplina'] = codigoD
                    print("Alteração realizada com sucesso.")
                elif op == '2':
                    nomeD = input("Digite o nome da disciplina: ")
                    informacoes['Nome'] = nomeD
                    print("Alteração realizada com sucesso.")
                elif op == '4':
                    semestre = input("Digite o semestre: ")
                    informacoes['Semestre'] = semestre
                    print("Alteração realizada com sucesso.")
                elif op == '3':
                    ano = input("Digite o ano: ")
                    informacoes['Ano'] = ano
                    print("Alteração realizada com sucesso.")
                elif op == '5':
                    hora = input("Digite a hora: ")
                    informacoes['Hora'] = hora
                    print("Alteração realizada com sucesso.")
                elif op == '6':
                    avaliacoes = {}
                    nota_soma = ""
                    notaFinal = ""
                    num_avaliacoes = int(input("Digite o numero de avaliacoes: "))
                    while i!=num_avaliacoes:
                        peso = float(input("Digite o peso da avaliação: "))
                        nome = input(f"Digite o nome/tipo da avaliaçao {i+1}: ")
                        avaliacoes[f'Avaliacao {i+1}'] = nome
                        avaliacoes[f'Peso {i+1}'] = peso
                        i+=1
                        nota_soma += f' {peso}*{nome} ' 
                        if i != num_avaliacoes-1:
                            nota_soma += '+'
                        soma_pesos += peso
                    notaFinal += f'{nota_soma}/{soma_pesos}'
                    informacoes['Nota final'] = notaFinal
                    informacoes['Avaliacoes'] = avaliacoes
                    print("Alteração realizada com sucesso.")
                elif op == '7':
                    menuProfessor(alunos,professores,turmas)
                else:
                    print("Opção inválida.")

        turmas[i] = str(informacoes) + '\n'
    salvarTurmas('turmas.txt', turmas)
    menuProfessor(alunos,professores,turmas)

def excTurma(alunos,professores,turmas):
    codigoT = input("Digite o código da turma: ")
    t = False
    with open('turmas.txt', 'w') as turma:
        for linha in turmas:
            infoTurma = ast.literal_eval(linha.strip())
            if infoTurma['Codigo da turma'] == codigoT:
                t = True
                pass
            else:
                turma.write(linha)
    if t:
        print("Turma excluida com sucesso.")
    else:
        print("Turma não encontrada.")
    menuProfessor(alunos,professores,turmas)

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
        data_atual += timedelta(days=0)

    return frequencias

def Alunos(alunos,professores,turmas):
    op = 's'
    # Adicionar codigoD
    while op != 'n':
        # Adicionar dps pra mostrar só alunos da disciplina do professor
        print("1 - Para modificar as notas de um aluno.")
        print("2 - Para modificar as frequências de um aluno.")
        print("3 - Cadastrar um aluno.")
        op = input("Digite o número e 'n' para voltar ao menu inicial: ")
        if op == '1':
            b = 's'
            avaliacoes = {}
            for linha in alunos:
                print(linha)
            DRE = input("Digite o DRE do aluno:")

            for i, linha in enumerate(alunos):
                al = ast.literal_eval(linha.strip())
                while b != 'n':
                    if al['DRE'] == DRE:
                        if 'Notas' in al:
                            numero = int(input("Digite qual a avaliação que deseja alterar (1,2,3,...): "))
                            nota = float(input("Digite a nova nota: "))
                            avaliacoes[f'Avaliacao {numero}'] = nota
                            al['Notas'] = avaliacoes
                            print(al)
                            b = input("Digite s/n para continuar.")
                            
                        else:
                            print("O aluno ainda não tem notas lançadas.")
        elif op == '2': 
            b = 's'
            for linha in alunos:
                print(linha)
            DRE = input("Digite o DRE do aluno:")

            for i, linha in enumerate(alunos):
                al = ast.literal_eval(linha.strip())
                while b != 'n':
                    if al['DRE'] == DRE:
                        print(formatarCalendario(al['Frequencias']))
                        freq_data = input("Digite a data (dd/mm/yyyy): ")
                        freq_status = int(input("Digite a frequência (1 para presença e 0 para falta): "))
                        al['Frequencias'][f'{freq_data}'] = freq_status
                        alunos[i] = str(al) + '\n'  # Atualiza a lista de alunos com a nova frequência
                        print(formatarCalendario(al['Frequencias']))
                        b = input("Digite s/n para continuar ou não.")
                    else:
                        b = 'n'
        elif op == '3':
            codigoD = input("Digite o codigo da disciplina: ")
            codigoT = input("Digite o codigo da turma: ")
            nomeA = input("Digite o nome completo do aluno:")
            DRE = input("Digite o DRE do aluno:")
            for professor in professores:
                prof_dict = ast.literal_eval(professor.strip())
                if 'Disciplinas' in prof_dict:
                    disciplinas = prof_dict['Disciplinas']

                        # Verificar se a chave 'comp3' existe
                    if 'comp3' in disciplinas:
                        comp3 = disciplinas['comp3']

                            # Verificar se a chave '23' existe
                        if '23' in comp3:
                            datas = comp3['23']

                                # Agora, podemos acessar o dicionário de datas
                            print(datas)
                                
                                # Acessar um valor específico
                            if '10/06/2024' in datas:
                                valor = datas['10/06/2024']
                                print(valor)  # Isso imprimirá 2
           
            al = { 'Nome': nomeA, 
                        'DRE': DRE,
                        'Codigo da disciplina': codigoD,
                        'Codigo da turma': codigoT,
                        'Notas' : avaliacoes,
                        'Frequencias': datas
                }
            with open('alunos.txt', 'a') as alunos_cadastro:
                alunos_cadastro.write('\n')
                alunos_cadastro.write(f'{al}')
            print("Aluno cadastrado com sucesso.")

        else:
            op = input("Opção incorreta, pressione 'n' para sair.")
    # Escrevendo as alteraçoes para não interferir na leitura de nenhum arquivo
        if op != '3':
            with open('alunos.txt','w') as f:
                f.writelines(alunos)

    menuProfessor(alunos,professores,turmas)

def lancarFrequencias(alunos,professores,turmas):
    op = 's'
    while op != 'n':

        codigoD = input("Digite o codigo da disciplina que deseja lançar as frequências:")
        codigoT = input("Digite o codigo da turma:")
        b = False
        for aluno in alunos:
            al = ast.literal_eval(aluno.strip())
            if al['Codigo da disciplina'] == codigoD and al['Codigo da turma'] == codigoT:
                print(al)
        for i, aluno in enumerate(alunos):
            al = ast.literal_eval(aluno.strip())
            if al['Codigo da disciplina'] == codigoD and al['Codigo da turma'] == codigoT:
                DRE = input("Digite o DRE do aluno:")
                if DRE == al['DRE']:
                    if 'Frequencias' in al:
                        op2 = 's'
                        while op2 != 'n':
                            print(formatarCalendario(al['Frequencias']))
                            freq_data = input("Digite a data (dd/mm/yyyy): ")
                            freq_status = int(input("Digite a frequência (1 para presença e 0 para falta): "))
                            al['Frequencias'][f'{freq_data}'] = freq_status
                            b = True
                            alunos[i] = str(al) + '\n'  # Atualiza a lista de alunos com a nova frequência
                            print(formatarCalendario(al['Frequencias']))
                            op2 = input("Digite s/n para continuar ou não.")
        if b == False:
            print("Aluno não encontrado.")
        with open('alunos.txt','w') as f:
                f.writelines(alunos)
        op = input("Pressione s/n para continuar com outra disciplina/turma ou não: ")
    menuProfessor(alunos,professores,turmas)

def formatarCalendario(frequencias):
    
    # Organiza as frequências por mês
    meses = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}, 12: {}}
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

    ''' Exemplo de uso
    frequencias = {
        "01/01/2024": 1,       Presença não lançada no dia 1 de janeiro de 2024
        "02/01/2024": 2,       Presença no dia 2 de janeiro de 2024
        "15/02/2024": 3,       Falta no dia 15 de fevereiro de 2024
        "28/02/2024": 1        Presença não lançada no dia 28 de fevereiro d
    }
    '''

def lancarNotas(alunos,professores,turmas):
    op = 's'
    a = False
    b = False
    c = False
    op2 = 's'
    while op != 'n':
        avaliacoes = {}
        codigoD = input("Digite o codigo da disciplina que deseja lançar notas:")
        codigoT = input("Digite o codigo da turma:")
        for turma in turmas:
            infoTurma = ast.literal_eval(turma.strip())
            if infoTurma['Codigo da disciplina'] == codigoD:
                a = True
                if infoTurma['Codigo da turma'] == codigoT:
                    b = True
                    avaliacoes = infoTurma['Avaliacoes']
                    tamanho = len(avaliacoes)
                    limite = tamanho/2
        if not b: print("Turma não encontrada.")
        if not a: print("Disciplina não encontrada")
        b = False
        a = False
        for i,aluno in enumerate(alunos):
            al = ast.literal_eval(aluno.strip())
            if al['Codigo da disciplina'] == codigoD:
                a = True
                if al['Codigo da turma'] == codigoT:
                    b = True
                    print(aluno)
                    j = 0
                    DRE = input("Digite o DRE do aluno: ")
                    if al['DRE'] == DRE:
                        c = True
                        
                        while op2 != 'n' and j<=limite:
                            nota = input(f"Digite o valor da nota {j+1}: ")
                            op2 = input("Digite s/n para finalizar ou continuar adicionando notas.")
                            al['Notas'][f'Avaliacao {j+1}'] = nota
                            j+=1
                        alunos[i] = str(al) + '\n'
        if not c: print("Aluno não encontrado.")
        if not b: print("Turma não encontrada.")
        if not a: print("Disciplina não encontrada")
        op = input("Pressione 'n' para sair, 's' para continuar.")
    with open('alunos.txt','w') as f:
        f.writelines(alunos)
    menuProfessor(alunos,professores,turmas)

# Sessão dos alunos

def Verfrequencia(cal):
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

def Vernotas(alunos):
    DRE = input("Digite o seu DRE:")
    op = 's'
    a = False
    b = False
    for aluno in alunos:
            al = ast.literal_eval(aluno.strip())
            if al['DRE'] == DRE:
                print(al)
    while op != 'n':
        codigoD = input("Digite o codigo da disciplina que deseja ver a nota: ")
        for aluno in alunos:
            al = ast.literal_eval(aluno.strip())
            if al['DRE'] == DRE:
                a = True
                if al['Codigo da disciplina'] == codigoD:
                    print(al['Notas'])
                b = True
        if not a: print("DRE não encontrado.")
        if not b: print("Disciplina não encontrada")
        op = input("Pressione 'n' para sair, 's' para continuar.")
    menuAluno(alunos,professores,turmas)

def VercalculoNotas(alunos,professores,turmas):
    op = 's'
    b = False
    c = False
    while op != 'n':
        codigoD = input("Digite o código da disciplina para exibir o cálculo da nota final: ")
        codigoT = input("Digite o código da turma: ")
        for turma in turmas:
            infoTurma = ast.literal_eval(turma.strip())
            if infoTurma['Codigo da disciplina'] == codigoD:
                c = True
                if infoTurma['Codigo da turma'] == codigoT:
                    print(f"Nota Final da disciplina {infoTurma['Nome']}: {infoTurma['Nota final']}")
                    b = True
        if not c:   print("Disciplina não encontrada.")
        if not b:   print("Turma não encontrada.")
        op = input("Pressione 'n' para sair, 's' para continuar.")
   
    menuAluno(alunos,professores,turmas)

def VerpontosNecessarios(alunos,turmas,DRE):
    op = 's'
    while op != 'n':
        codigoD = input("Digite o codigo da disciplina: ")
        codigoT = input("Digite o codigo da turma: ")
        soma_pesos = 0
        soma_notas = 0
        for i, turma in enumerate(turmas):
            informacoes = ast.literal_eval(turma.strip())
            if informacoes['Codigo da disciplina'] == codigoD:
                c = True
                if informacoes['Codigo da turma'] == codigoT:
                    b = True
                    disciplina = informacoes['Nome']
                    for aluno in alunos:
                        al = ast.literal_eval(aluno.strip())
                        if al['DRE'] == DRE:
                            for i in len(al['Notas']):
                                soma_notas += float(al['Notas'][i])*float(informacoes['Avaliacoes'][f'Peso {i+1}'])
                                soma_pesos += float(informacoes['Avaliacoes'][f'Peso {i+1}'])
                                notaFinal = soma_notas/soma_pesos
        if not c:   print("Disciplina não encontrada.")
        if not b:   print("Turma não encontrada.")
        op = input("Pressione 'n' para sair, 's' para continuar.")
    if notaFinal < 5:
            pontos_necessarios = 5 - notaFinal 
            print(f"Você precisa de {pontos_necessarios} para ser aprovada em {disciplina}")
    else:
            print(f"Você não precisa de pontos, sua nota final é {notaFinal}")

    menuAluno(alunos,turmas)

# Menus e identificação

def menuProfessor(alunos,professores,turmas):
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
            cadastroTurma(alunos,professores,turmas)
        elif tarefa == '2':
            edicaoTurma(turmas)
        elif tarefa == '3':
            excTurma(alunos,professores,turmas)
        elif tarefa == '4':
            Alunos(alunos,professores,turmas)
        elif tarefa == '5':
            lancarNotas(alunos,professores,turmas)
        elif tarefa == '6':
            lancarFrequencias(alunos,professores,turmas)
        elif tarefa == 'sair':
            return 0
        else:
            print("Opção errada.")
            op = input("Digite s/n se deseja continuar.")

def menuAluno(alunos,professores,turmas, DRE):
    op = 's'
    while op != 'n':
        print("1 - Notas")
        print("2 - Ver as médias das notas das turmas, cálculo da média final e etc.")
        print("3 - Frequência")
        print("4 - Quantos pontos são necessários para a aprovação")
        tarefa = input("Digite uma opção ou 's' para sair: ")
        if tarefa == '1':
            Vernotas(alunos)
        elif tarefa == '2':
            VercalculoNotas(alunos, turmas)
        elif tarefa == '3':
            Verfrequencia(alunos, professores, turmas)
        elif tarefa == '4':
            VerpontosNecessarios(alunos, turmas, DRE)
        elif tareta == 's':
            return 0
        else:
            print("Opção errada.")
    identificacao(alunos,professores,turmas)

def identificacao(alunos,professores,turmas):

    tipo = input("Informe aluno, professor ou sair se desejar encerrar o programa: ")
    if tipo.lower() == 'sair':
        return alunos, professores, turmas
    
    if tipo.lower() == 'aluno':
        while True:
            DRE = input("Digite o seu DRE: ")
            c = False
            for linha in alunos:
                al = ast.literal_eval(linha.strip())
                if al['DRE'] == DRE:
                    c = True
                    print("Login bem-sucedido.")
                    menuAluno(alunos,professores,turmas, DRE)
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
                    frequencias_globais[f'{codigoD}'] = frequencias
                    disciplinas[chave] = frequencias_globais
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
                for linha in professores:
                    informacoes = ast.literal_eval(linha.strip())
                    if informacoes['Nome'].lower() == login.lower() and informacoes['Senha'] == senha_hash:
                        c = True
                        print("Login bem-sucedido.")
                        menuProfessor(alunos,professores,turmas)
                if not c:
                        print("Usuário ou/e senha incorretos, digite novamente.")
                else:
                    break
            if c:
                break
        
    else:
        print("Opção não identificada, digite se você é aluno ou professor.")
        identificacao(alunos,professores,turmas)
    return alunos,professores,turmas

alunos, professores, turmas = ler_arquivos()
alunos, professores, turmas = identificacao(alunos, professores, turmas)






