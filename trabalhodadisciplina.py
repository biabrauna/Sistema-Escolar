import ast
import hashlib

def cadastroTurma():
    op = 's'
    while op != 'n':
        codigoD = input("Digite o código da disciplina: ")
        nome = input("Digite o nome da disciplina: ")
        codigoT = input("Digite o código da turma: ")
        ano = input("Digite o ano em que a disciplina está sendo ofertada: ")
        semestre = input("Digite o semestre em que a disciplina está sendo ofertada: ")
        hora = input("Digite a hora em que a disciplina está sendo oferecida: ")
        num_avaliacoes = int(input("Quantas avaliaçoes tem? "))
        i=0
        avaliacoes = {}
        nota_soma = " "
        soma_pesos = 0
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
        notaFinal = f'{nota_soma}/{soma_pesos}'
        infoTurma = {}
        infoTurma['Codigo da disciplina'] = codigoD
        infoTurma['nome'] = nome
        infoTurma['Codigo da turma'] = codigoT
        infoTurma['Ano'] = ano
        infoTurma['Semestre'] = semestre
        infoTurma['Hora'] = hora
        infoTurma['Avaliacoes'] = avaliacoes
        infoTurma['Nota Final'] = notaFinal
        turma = open('turmas.txt','a')
        turma.write(f'{infoTurma}')
        turma.write(f"\n")
        turma.write(codigoT)
        turma.write(f"\n")
        turma.close()
        op = input("Deseja cadastrar outra turma(s/n)?")
    menuProfessor()

def edicaoTurma():
    b=True
    codigoT = input("Digite o codigo da turma que deseja editar: ")
    turma = open('turmas.txt','r+')
    linhas = turma.readlines()
    for linha in linhas:
        if linha[2] == codigoT:
            while b:
                print("1 - Codigo da disciplina")
                print("2 - Nome")
                print("3 - Ano")
                print("4 - Semestre")
                print("5 - Hora")
                print("6 - Avaliacoes")
                print("7 - Sair")
                op = input("Digite o que deseja editar: ")
                if op == '1':
                    codigo = input("Digite o novo codigo: ")
                    linha[0] = codigo
                elif op == '2':
                    nome = input("Digite o nome da disciplina: ")
                    linha[1] = nome
                elif op == '4':
                    semestre = input("Digite o semestre: ")
                    linha[4] = semestre
                elif op == '3':
                    ano = input("Digite o ano: ")
                    linha[3] = ano
                elif op == '5':
                    hora = input("Digite a hora: ")
                    linha[5] = hora
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
                    linha[7] = notaFinal
                    linha[6] = avaliacoes
                else:
                    turma.close()
                    return 0

def excTurma():
    codigoT = input("Digite o código da turma: ")
    with open('turmas.txt', 'r') as turma:
        linhas = turma.readlines()
    t=False
    with open('turmas.txt', 'w') as turma:
        for i in range(len(linhas)):
            if linhas[i] == '{':
                if linhas[i+1]!=codigoT:
                    turma.write(linhas[i])
                    turma.write(linhas[i+1])
                if linhas[i+1]==codigoT:
                    t=True
    if t:
        print("Turma excluida com sucesso.")
    else:
        print("Turma não encontrada.")
    menuProfessor()

def cadastrarAlunos():
    op = 's'
    while op != 'n':
        print("1 - Para modificar as notas de um aluno.")
        print("2 - Para modificar as frequências de um aluno.")
        print("3 - Cadastrar outro aluno.")
        op = input("Digite o número e 'n' para voltar ao menu inicial: ")
        if op =='1':
            nome = input("Digite o nome completo do aluno:")
            DRE = input("Digite o DRE do aluno:")
            with open('alunos.txt', 'r') as alunos:
                for aluno in alunos:
                    al = aluno.split(',')
                    if al[0].lower() == nome.lower() and al[1].lower == DRE.lower():
                        print(aluno)
                        numero = float(input("Digite qual o numero da avaliação que deseja alterar (1,2,3,...): "))
                        nota = float(input("Digite a nova nota: "))
                        al[1+numero] = nota
                    else:
                        with open('alunos.txt', 'w') as alunos:
                            alunos.write(aluno)
                    alunos.write(al)
        elif op =='2':
            nome = input("Digite o nome completo do aluno:")
            DRE = input("Digite o DRE do aluno:")
            with open('alunos.txt', 'r') as alunos:
                for aluno in alunos:
                    al = aluno.split(',')
                    if al[0].lower() == nome.lower() and al[1].lower == DRE.lower():
                        print(aluno)
                        numero = float(input("Digite qual o numero da frequência que deseja alterar (1,2,3,...)(DE TRÁS PARA FRENTE): "))
                        freq = float(input("Digite a nova frequência (0/1): "))
                        al[len(al)-numero] = freq
                    else:
                        with open('alunos.txt', 'w') as alunos:
                            alunos.write(aluno) 
                    alunos.write(al)
                        
        elif op == '3':
            nome = input("Digite o nome completo do aluno:")
            DRE = input("Digite o DRE do aluno:")
            notas = input("Digite as notas, e 'n' caso não queira adicionar nenhuma: ")
            freq = input("Digite as frequências, e 'n' caso não queira adicionar nenhuma: ") 
            al = [nome, DRE]
            with open('alunos.txt', 'w') as alunos:
                if notas != 'n':
                    notas = notas.split('')
                    al += [notas]
                    if freq != 'n':
                        freq = freq.split('')
                        al += [freq]
                alunos.write(al)
        else:
            op = input("Opção incorreta, pressione 'n' para sair.")
    menuProfessor()

def lancarNotas():
    op = 's'
    with open('alunos.txt', 'r') as alunos:
        while op != 'n':
            codigoT = input("Digite o codigo da turma que deseja lançar notas:")
            for aluno in alunos:
                al = aluno.split(',')
                if al[1][0] == codigoT:
                    print(aluno)
                    notas = float(input("Digite as notas: "))
                    notas = notas.split('')
                    for i in range(len(al)):
                        alu += [al[i]]
                    alu += [notas]
                else:
                    with open('alunos.txt', 'r') as alunos:
                        alunos.write(aluno)
                alunos.write(alu)
            op = input("Pressione 'n' para sair, 's' para continuar.")
    menuProfessor()

def lancarFrequencias():
    op = 's'
    with open('alunos.txt', 'r') as alunos:
        while op != 'n':
            # Adicionar porcentagem de frequência
            codigoT = input("Digite o codigo da turma que deseja lançar as frequências:")
            for aluno in alunos:
                al = aluno.split(',')
                if al[1][0] == codigoT:
                    print(aluno)
                    freq = float(input("Digite as frequências (0/1): "))
                    freq = freq.split('')
                    for i in range(len(al)):
                        alu += [al[i]]
                    alu += [freq]
                else:
                    with open('alunos.txt', 'w') as alunos:
                        alunos.write(aluno)
                alunos.write(alu)
            op = input("Pressione 'n' para sair, 's' para continuar.")
    menuProfessor()

def notas():
    nome = input("Digite o seu nome completo:")
    DRE = input("Digite o seu DRE:")
    with open('alunos.txt', 'r') as alunos:
        for aluno in alunos:
            al = aluno.split(',')
            if al[0].lower() == nome.lower() and al[1].lower == DRE.lower():
                print(aluno)
    menuAluno()

def calculoNotas():
    op = 's'
    while op != 'n':
        codigoD = input("Digite o código da disciplina para exibir a nota final: ")
        with open('turmas.txt', 'r') as turma:
            linhas = turma.readlines()
            for linha in linhas:
                infoTurma = ast.literal_eval(linha.strip())
                if infoTurma['Codigo da disciplina'] == codigoD:
                    print(f"Nota Final da disciplina {codigoD}: {infoTurma['Nota Final']}")
            op = input("Pressione 'n' para sair, 's' para continuar.")
            print("Disciplina não encontrada.")
    menuAluno()

def frequencia():
    op = 's'
    while op != 'n':
        codigoD = input("Digite o código da disciplina para exibir a frequencia: ")
        DRE = input("Digite o seu DRE: ")
        with open('turmas.txt', 'r') as turma:
            linhas = turma.readlines()
            for linha in linhas:
                infoTurma = ast.literal_eval(linha.strip())
                if infoTurma['Codigo da disciplina'] == codigoD:
                    print(f"Nota Final da disciplina {codigoD}: {infoTurma['Nota Final']}")
            op = input("Pressione 'n' para sair, 's' para continuar.")
            print("Disciplina não encontrada.")
    menuAluno()

def pontosNecessarios():
    # Função para ver pontos necessários para aprovação
    menuAluno()

def menuProfessor():
    op = 's'
    while op != 'n':
        print("1 - Cadastro de turma")
        print("2 - Edição de turma")
        print("3 - Exclusão de turma")
        print("4 - Cadastrar alunos")
        print("5 - Lançar notas")
        print("6 - Lançar frequências")
        tarefa = input("Digite o número: ")
        if tarefa == '1':
            cadastroTurma()
        elif tarefa == '2':
            edicaoTurma()
        elif tarefa == '3':
            excTurma()
        elif tarefa == '4':
            cadastrarAlunos()
        elif tarefa == '5':
            lancarNotas()
        elif tarefa == '6':
            lancarFrequencias()
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
            notas()
        elif tarefa == '2':
            calculoNotas()
        elif tarefa == '3':
            frequencia()
        elif tarefa == '4':
            pontosNecessarios()
        else:
            print("Opção errada.")
        op = input("Digite s/n se deseja continuar.")

def identificacao():
    tipo = input("Informe aluno, professor ou sair se desejar encerrar o programa: ")
    if tipo.lower() == 'sair':
        return 0
    if tipo.lower() == 'aluno':
        b=True
        while b:
            login = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")
            # Adicionar segurança hashlib
            #senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            c=False
            avaliacoes = {}
            with open('alunos.txt', 'r') as cadastro:
                linhas = cadastro.readlines()
                for linha in linhas:
                    if linha[0].lower() == login.lower() and linha[1].lower() == senha.lower():
                        c = True
                        print("Login bem-sucedido.")
                        b = False
                        cadastro.close()
                        break
                if not c:
                    print("Usuário ou/e senha incorretos, digite novamente.")
            menuAluno()
    elif tipo.lower() == 'professor':
        b=True
        #Adicionar opcao de cadastrar aluno
        r = input("Deseja se cadastrar(s/n)? ").lower()
        while b:
            login = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")
            # A dicionar segurança hashlib
            # senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            c=False
            if r=='n':
                    with open('professores.txt', 'r') as cadastro:
                        for linha in cadastro:
                            informacoes = linha.strip().split(',')
                            if informacoes[0].lower() == login and informacoes[1].lower() == senha.lower():
                                c = True
                                print("Login bem-sucedido.")
                                b = False
                                cadastro.close()
                                break
                        if not c:
                            print("Usuário ou/e senha incorretos, digite novamente.")
            else:
                cadastro = open('professores.txt','a')
                cadastro.write(f'{login},{senha}\n')
                print("Usuário cadastrado com sucesso. Agora faça o login.")
                r = 'n'
        menuProfessor()
    elif tipo.lower() == 'sair':
        return 0
    else:
        tipo = input("Opção não identificada, digite se você é aluno ou professor: ")
        identificacao()

identificacao()






