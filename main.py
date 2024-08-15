import ast  # Módulo para analisar strings de literais em estruturas Python
import hashlib  # Módulo para hashes criptográficos seguros
from datetime import datetime, timedelta  # Módulos para manipulação de datas
from termcolor import colored # Módulo para adicionar cores
import calendar # Módulo para visualizar o calendário
import os # Módulo para manipular arquivos
import tkinter as tk
from tkinter import messagebox

frequencias_globais = {}

# Manipulação de arquivos

def ler_arquivos():
    # Função para ler os arquivos de alunos, professores e turmas e retornar seus conteúdos como listas
    try:
        with open('alunos.txt', 'r') as file_alunos:
            alunos = file_alunos.readlines()
    except FileNotFoundError:
        print(colored("Arquivo 'alunos.txt' não encontrado."),'red')
    
    try:
        with open('professores.txt', 'r') as file_professores:
            professores = file_professores.readlines()
    except FileNotFoundError:
        print(colored("Arquivo 'professores.txt' não encontrado."),'red')
    
    try:
        with open('turmas.txt', 'r') as file_turmas:
            turmas = file_turmas.readlines()
    except FileNotFoundError:
        print(colored("Arquivo 'turmas.txt' não encontrado."),'red')
    
    return alunos, professores, turmas

def salvarTurmas(filename, turmas):
    # Função para salvar as turmas de volta ao arquivo
    try:
        with open(filename, 'w') as f:
            f.writelines(turmas)
        return True
    except IOError:
        print(colored(f"Erro ao salvar no arquivo '{filename}'."),'red')
        return False

def verificar_ou_criar_arquivo(filename, dados_iniciais):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            for item in dados_iniciais:
                f.write(str(item) + '\n')

# Sessão dos professores

def cadastroTurma(alunos, professores, turmas):
    op = 's'
    while op != 'n':
        try:
            # Coleta das informações da nova turma
            codigoD = input("Digite o código da disciplina: ")
            if not codigoD.isdigit():
                raise ValueError(colored("O código da disciplina deve ser um número.",'red'))

            nome = input("Digite o nome da disciplina: ")

            codigoT = input("Digite o código da turma: ")
            if not codigoT.isdigit():
                raise ValueError(colored("O código da turma deve ser um número.",'red'))

            ano = int(input("Digite o ano em que a disciplina está sendo ofertada: "))
            if ano < datetime.now().year:
                raise ValueError(colored("O ano deve ser maior ou igual que o ano atual.",'red'))

            dias = int(input("Número de dias na semana que terá aula: "))
            if dias <= 0 or dias > 7:
                raise ValueError(colored("O número de dias deve estar entre 1 e 7.",'red'))
            dias_aulas = [0]*dias
            for i in range(dias):
                dia = input(f'Digite o {i+1} dia de aula (segunda, quarta,...): ')
                if dia.lower() not in ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']:
                    raise ValueError(colored(f"Dia inválido: {dia}. Utilize os nomes padrão dos dias da semana.",'red'))
                dias_aulas[i] = dia

            semestre = input("Digite o semestre em que a disciplina está sendo ofertada (1 ou 2): ")
            if semestre not in ['1', '2']:
                raise ValueError(colored("Semestre inválido. Digite apenas '1' ou '2'.",'red'))

            hora = input("Digite a hora em que a disciplina está sendo oferecida: ")

            num_avaliacoes = int(input("Quantas avaliações tem? "))
            if num_avaliacoes <= 0:
                raise ValueError("O número de avaliações deve ser maior que zero.")
            i = 0
            avaliacoes = {}
            nota_soma = " "
            soma_pesos = 0

            while i != num_avaliacoes:
                peso = float(input("Digite o peso da avaliação: "))
                if peso<0:
                    raise ValueError("O peso não pode ser negativo.")
                nomeA = input(f"Digite o nome/tipo da avaliação {i+1}: ")
                avaliacoes[f'Avaliacao {i+1}'] = nomeA
                avaliacoes[f'Peso {i+1}'] = peso
                
                nota_soma += f' {peso}*{nomeA} '
                if i != num_avaliacoes - 1:
                    nota_soma += '+'
                i += 1
                soma_pesos += peso
            datas = gerar_frequencias(dias_aulas)
            notaFinal = f'{nota_soma}/{soma_pesos}'  # Cálculo da nota final baseado nas avaliações

            # Construção do dicionário com as informações da turma
            infoTurma = {
                'Codigo da disciplina': codigoD,
                'Nome': nome,
                'Codigo da turma': codigoT,
                'Ano': ano,
                'Semestre': semestre,
                'Dias': dias,
                'Hora': hora,
                'Avaliacoes': avaliacoes,
                'Nota final': notaFinal,
                'Frequencias': datas
            }
            
            # Escrita das informações da turma no arquivo de turmas
            try:
                with open('turmas.txt', 'a') as turma_file:
                    turma_file.write(f'{infoTurma}\n')
            except IOError as e:
                print(f"Erro ao escrever no arquivo: {e}")

            op = input("Digite s/n para cadastrar mais uma turma: ")

        except ValueError as ve:
            print(f"Erro: {ve}")
            continue  # Continua o loop para tentar novamente

    menuProfessor(alunos, professores, turmas)  # Volta ao menu principal dos professores

def edicaoTurma(turmas):
    # Função para editar uma turma existente
    op = 'n'
    for turma in turmas:
        print(turma)
    codigoT = input("Digite o código da turma que deseja editar: ")
    for i, linha in enumerate(turmas):
        informacoes = ast.literal_eval(linha.strip())
        if informacoes['Codigo da turma'] == codigoT:
            while op != 's':
                # Opções de edição da turma
                print("1 - Código da disciplina")
                print("2 - Nome")
                print("3 - Ano")
                print("4 - Semestre")
                print("5 - Hora")
                print("6 - Avaliações")
                print("7 - Sair \n")
                op = input("Digite o número do campo que deseja editar ou 's' para sair: ")
                try:
                    if op == '1':
                        codigoD = input("Digite o novo código da disciplina: ")
                        if not codigoD.isdigit():
                            raise ValueError("O código deve ser um número.")
                        informacoes['Codigo da disciplina'] = codigoD
                        print("Alteração realizada com sucesso.")
                    elif op == '2':
                        nomeD = input("Digite o novo nome da disciplina: ")
                        informacoes['Nome'] = nomeD
                        print("Alteração realizada com sucesso.")
                    elif op == '3':
                        ano = input("Digite o novo ano: ")
                        if not ano.isdigit():
                            raise ValueError("O ano deve ser um número.")
                        informacoes['Ano'] = ano
                        print("Alteração realizada com sucesso.")
                    elif op == '4':
                        semestre = input("Digite o novo semestre (1 ou 2): ")
                        if not semestre.isdigit():
                            raise ValueError("O semestre deve ser um número '1' ou '2'.")
                        informacoes['Semestre'] = semestre
                        print("Alteração realizada com sucesso.")
                    elif op == '5':
                        hora = input("Digite a nova hora: ")
                        informacoes['Hora'] = hora
                        print("Alteração realizada com sucesso.")
                    elif op == '6':
                        avaliacoes = {}
                        nota_soma = ""
                        notaFinal = ""
                        num_avaliacoes = int(input("Digite o número de avaliações: "))
                        for j in range(num_avaliacoes):
                            peso = float(input("Digite o peso da avaliação: "))
                            nome = input(f"Digite o nome/tipo da avaliação {j+1}: ")
                            avaliacoes[f'Avaliacao {j+1}'] = nome
                            avaliacoes[f'Peso {j+1}'] = peso
                            nota_soma += f' {peso}*{nome} '
                            if j != num_avaliacoes - 1:
                                nota_soma += '+'
                            soma_pesos += peso
                        notaFinal += f'{nota_soma}/{soma_pesos}'
                        informacoes['Nota final'] = notaFinal
                        informacoes['Avaliacoes'] = avaliacoes
                        print("Alteração realizada com sucesso.")
                    elif op == '7':
                        menuProfessor(alunos, professores, turmas)
                    elif op == 's':
                        break
                    else:
                        print("Opção inválida.")
                except ValueError as e:
                    print(f"Erro: {e}")
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")

        turmas[i] = str(informacoes) + '\n'  # Atualiza a lista de turmas com as informações editadas

    salvarTurmas('turmas.txt', turmas)  # Salva as alterações no arquivo de turmas
    menuProfessor(alunos, professores, turmas)  # Volta ao menu principal dos professores

def excTurma(alunos, professores, turmas):
    # Função para excluir uma turma
    try:
        for turma in turmas:
            print(turma)
        codigoT = input("Digite o código da turma que deseja excluir: ")
        if not codigoT.isdigit():
            raise ValueError("O código da turma deve ser um número.")
        
        t = False
        with open('turmas.txt', 'w') as turma:
            for linha in turmas:
                try:
                    infoTurma = ast.literal_eval(linha.strip())
                    if infoTurma['Codigo da turma'] == codigoT:
                        t = True  # Indica que a turma foi encontrada
                    else:
                        turma.write(linha + '\n')  # Escreve todas as turmas, exceto a que foi excluída
                except (ValueError, SyntaxError) as e:
                    print(f"Erro ao processar a linha: {linha}. Erro: {e}")
                    turma.write(linha)  # Mantém a linha no arquivo, apesar do erro

        if t:
            print("Turma excluída com sucesso.")
        else:
            print("Turma não encontrada.")
    except ValueError as e:
        print(f"Erro: {e}")
    except IOError as e:
        print(f"Ocorreu um erro ao acessar o arquivo: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    menuProfessor(alunos, professores, turmas)  # Volta ao menu principal dos professores

def gerar_frequencias(dias_aulas):
    """
    Gera um dicionário de frequências para uma disciplina com base nos dias de aula.

    Args:
    dias_aulas (list): Lista de dias da semana em que ocorrem as aulas, ex: ['segunda', 'quarta'].

    Returns:
    dict: Dicionário com as datas como chaves (formato 'dd/mm/yyyy') e valores padrão de frequência (2 para presença não lançada).
    """
    try:
        frequencias = {}  # Dicionário para armazenar as frequências
        hoje = datetime.now().date()  # Obtém a data atual
        inicio = hoje - timedelta(days=15)  # Data de início das aulas (15 dias antes da data atual)
        fim = hoje + timedelta(days=30)  # Data de término das aulas (30 dias após a data atual)

        # Mapeia os dias da semana para seus índices correspondentes
        dia_semana = {
            'domingo': 6,
            'segunda': 0,
            'terça': 1,
            'quarta': 2,
            'quinta': 3,
            'sexta': 4,
            'sábado': 5
        }

        # Obtém os índices dos dias de aula especificados
        dias_indices = [dia_semana[dia] for dia in dias_aulas]

        data_atual = inicio
        # Itera sobre todos os dias entre inicio e fim para definir as frequências
        while data_atual <= fim:
            # Verifica se o dia atual da semana está entre os dias de aula especificados
            if data_atual.weekday() in dias_indices:
                frequencias[data_atual.strftime('%d/%m/%Y')] = 2  # Presença não lançada

            data_atual += timedelta(days=1)  # Avança para o próximo dia

        return frequencias

    except KeyError as e:
        print(f"Erro: Dia da semana inválido fornecido - {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
 
def Alunos(alunos, professores, turmas):
    op = 's'
    # Loop principal para as opções de menu
    while op != 'n':
        print("1 - Para modificar as notas de um aluno.")
        print("2 - Para modificar as frequências de um aluno.")
        print("3 - Cadastrar um aluno.")
        op = input("Digite o número e 'n' para voltar ao menu inicial: ")
        try:
            if op == '1':
                b = 's'
                avaliacoes = {}
                for linha in alunos:
                    print(linha)
                
                c = False # Inserindo uma variável para ver se encontrou o DRE
                while b != 'n':
                    DRE = input("Digite o DRE do aluno:")
                    if not DRE.isdigit():
                        raise ValueError("DRE incorreto, digite apenas números.")
                    for i, linha in enumerate(alunos):
                            al = ast.literal_eval(linha.strip())
                            if al['DRE'] == DRE:
                                c = True
                                if 'Notas' in al:
                                    numero = input("Digite qual a avaliação que deseja alterar (1,2,3,...): ")
                                    nota = input("Digite a nova nota: ")
                                    if not (numero.isdigit() and nota.replace('.', '', 1).isdigit()):
                                        raise ValueError("Valor incorreto, digite apenas números.")
                                    numero = int(numero)
                                    nota = float(nota)
                                    avaliacoes = al['Notas']
                                    avaliacoes[f'Avaliacao {numero}'] = nota
                                    al['Notas'] = avaliacoes
                                    print(al)
                                    b = input("Digite s/n para continuar.")
                                else:
                                    print("O aluno ainda não tem notas lançadas.")
                    if not c:
                        b = input("DRE não encontrado. Digite s/n para continuar.")
                alunos[i] = str(al) + '\n'
            
            elif op == '2':
                b = 's'
                for linha in alunos:
                    print(linha)
                
                c = False # Variavel para certificar que encontrou o DRE do aluno
                while b != 'n':
                    DRE = input("Digite o DRE do aluno:")
                    if not DRE.isdigit():
                        raise ValueError("DRE incorreto, digite apenas números.")
                    for i, linha in enumerate(alunos):
                        al = ast.literal_eval(linha.strip())
                        if al['DRE'] == DRE:
                            c = True
                            print(formatarCalendario(al['Frequencias']))
                            freq_data = input("Digite a data (dd/mm/yyyy): ")
                            freq_status = input("Digite a frequência (1 para presença e 0 para falta): ")
                            if not (freq_status == '1' or freq_status == '0'):
                                raise ValueError("Valor de frequência incorreto. Digite 1 para presença e 0 para falta.")
                            freq_status = int(freq_status)
                            al['Frequencias'][f'{freq_data}'] = freq_status
                            alunos[i] = str(al) + '\n'  # Atualiza a lista de alunos com a nova frequência
                            print(formatarCalendario(al['Frequencias']))
                            b = input("Digite s/n para continuar ou não.")
                    if not c:
                        b = 'n'
            
            elif op == '3':
                # Coleta informações para cadastrar um novo aluno
                codigoD = input("Digite o código da disciplina: ")
                DRE = input("Digite o DRE do aluno:")
                if not DRE.isdigit():
                    raise ValueError(colored("DRE incorreto, digite apenas números.",'red'))
                codigoT = input("Digite o código da turma: ")
                if not codigoD.isdigit() or not codigoT.isdigit():
                    raise ValueError(colored("O codigo deve ser um conjunto de numeros.",'red'))
                nomeA = input("Digite o nome completo do aluno:")
                
                
                avaliacoes = {}  # Inicializa as avaliações vazias
                datas = {} # Inicializa as frequencias vazias
                c = False # Verifica se achou a disciplina

                # Pega as frequencias dessa disciplina e turma especifica e adiciona aos dados do aluno
                for turma in turmas:
                    infoTurma = ast.literal_eval(turma.strip())
                    if infoTurma['Codigo da disciplina'] == codigoD:
                        if infoTurma['Codigo da turma'] == codigoT:
                            datas = infoTurma['Frequencias']
                            c = True
                            break
                if not c:
                    print("Disciplina ou turma não encontrada.")

                al = {
                    'Nome': nomeA,
                    'DRE': DRE,
                    'Codigo da disciplina': codigoD,
                    'Codigo da turma': codigoT,
                    'Notas': avaliacoes,
                    'Frequencias': datas
                }

                # Escreve o novo aluno no arquivo
                with open('alunos.txt', 'a') as alunos_cadastro:
                    alunos_cadastro.write(f'{al}\n')
                print("Aluno cadastrado com sucesso.")

            elif op == 'n':
                break
            else:
                print("Opção incorreta.")
                op = input("Digite s/n para continuar.")
            
            # Escreve as alterações no arquivo para garantir que nenhum dado seja perdido
            if op != '3':
                with open('alunos.txt', 'w') as f:
                    f.writelines(alunos)
        except IOError:
            print(colored(f"Erro ao salvar no arquivo 'alunos.txt'."),'red')
        
        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    # Volta ao menu principal dos professores
    menuProfessor(alunos, professores, turmas)

def lancarFrequencias(alunos, professores, turmas):
    op = 's'
    while op != 'n':
        try:
            # Pede os códigos da disciplina e da turma
            codigoD = input("Digite o código da disciplina que deseja lançar as frequências: ")
            codigoT = input("Digite o código da turma: ")
            if not codigoD.isdigit() or not codigoT.isdigit():
                    raise ValueError(colored("Os codigos devem ser um conjunto de numeros.",'red'))

            # Variaveis auxiliares para verificar se os codigos e o aluno existem
            a = False
            b = False

            # Exibe os alunos que pertencem à disciplina e turma especificadas
            for aluno in alunos:
                al = ast.literal_eval(aluno.strip())
                if al['Codigo da disciplina'] == codigoD and al['Codigo da turma'] == codigoT:
                    print(al)

            DRE = input("Digite o DRE do aluno: ")
            if not DRE.isdigit():
                raise ValueError(colored("DRE incorreto, digite apenas números.",'red'))

            # Lança as frequências para o aluno especificado
            for i, aluno in enumerate(alunos):
                # Transforma a linha em dicionario de novo
                al = ast.literal_eval(aluno.strip())
                if al['Codigo da disciplina'] == codigoD and al['Codigo da turma'] == codigoT:
                    a = True
                    if DRE == al['DRE']:
                        if 'Frequencias' in al:
                            op2 = 's'
                            while op2 != 'n':
                                # Mostra o calendario ja passando as frequencias atuais do aluno pra funçao formatarCalendario
                                print(formatarCalendario(al['Frequencias']))
                                freq_data = input("Digite a data (dd/mm/yyyy): ")
                                freq_status = input("Digite a frequência (1 para presença e 0 para falta): ")
                                if not (freq_status == '1' or freq_status == '0'):
                                    raise ValueError("Valor de frequência incorreto. Digite 1 para presença e 0 para falta.")
                                freq_status = int(freq_status)
                                # Altera a frequencia
                                al['Frequencias'][f'{freq_data}'] = freq_status
                                alunos[i] = str(al) + '\n'  # Atualiza a lista de alunos com a nova frequência
                                print(formatarCalendario(al['Frequencias']))
                                b = True
                                op2 = input("Digite s/n para continuar ou não.")
            if not a:
                print("Turma e/ou disciplina não encontrada(s).")
            if not b:
                print("Aluno não encontrado.")

            # Escreve as alterações no arquivo de alunos
            with open('alunos.txt', 'w') as f:
                f.writelines(alunos)

            op = input("Pressione s/n para continuar com outra disciplina/turma ou não: ")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    # Volta ao menu principal dos professores
    menuProfessor(alunos, professores, turmas)

def lancarNotas(alunos, professores, turmas):
    op = 's'
    op2 = 's'

    # Variaveis auxiliares para verificar se o programa achou os codigos
    a = False
    b = False
    c = False

    while op != 'n':
        try:
            avaliacoes = {}
            codigoD = input("Digite o código da disciplina que deseja lançar notas: ")
            codigoT = input("Digite o código da turma: ")
            if not codigoD.isdigit() or not codigoT.isdigit():
                    raise ValueError(colored("O codigo deve ser um conjunto de numeros.",'red'))

            # Verifica se a disciplina e a turma existem
            for turma in turmas:
                infoTurma = ast.literal_eval(turma.strip())
                if infoTurma['Codigo da disciplina'] == codigoD:
                    a = True
                    if infoTurma['Codigo da turma'] == codigoT:
                        b = True
                        avaliacoes = infoTurma['Avaliacoes']
                        tamanho = len(avaliacoes)
                        limite = tamanho // 2  # Calcula o limite de avaliações

            if not b:
                print("Turma não encontrada.")
            if not a:
                print("Disciplina não encontrada")

            # Redefinindo para usa-las de novo para verificar se o programa achou os codigos
            b = False
            a = False

            # Lança as notas para os alunos da turma especificada
            for i, aluno in enumerate(alunos):
                al = ast.literal_eval(aluno.strip())
                if al['Codigo da disciplina'] == codigoD:
                    a = True
                    if al['Codigo da turma'] == codigoT:
                        b = True
                        print(aluno)
            DRE = input("Digite o DRE do aluno: ")
            if not DRE.isdigit():
                raise ValueError(colored("O DRE deve ser composto apenas por numeros.",'red'))
            for i, aluno in enumerate(alunos):
                        al = ast.literal_eval(aluno.strip())
                        if al['DRE'] == DRE:
                            c = True
                            j = 0
                            while j != limite:
                                nota = input(f"Digite o valor da nota {j + 1}: ")
                                if not nota.replace('.', '', 1).isdigit():
                                        raise ValueError(colored("Valor incorreto, digite apenas números.",'red'))
                                al['Notas'][f'Avaliacao {j + 1}'] = nota
                                j += 1
                            alunos[i] = str(al) + '\n'

            if not c:
                print("Aluno não encontrado.")
            if not b:
                print("Turma não encontrada.")
            if not a:
                print("Disciplina não encontrada")
            op = input("Pressione 'n' para sair, 's' para continuar.")

            # Escreve as alterações no arquivo de alunos
            with open('alunos.txt', 'w') as f:
                f.writelines(alunos)

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    # Volta ao menu principal dos professores
    menuProfessor(alunos, professores, turmas)

def formatarCalendario(frequencias):
    total_dias = len(frequencias)
    presencas = sum(freq == 1 for freq in frequencias.values())
    faltas = sum(freq == 0 or freq == 2 for freq in frequencias.values())
    porcentagem_presenca = (presencas / total_dias) * 100 if total_dias > 0 else 0

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
    for mes in range(1, 12 + 1):  # Meses de 1 a 12
        if meses[mes]:  # Verifica se há dias registrados para o mês atual
            cal += f"{calendar.month_name[mes]}:\n"
            cal += "Seg Ter Qua Qui Sex Sáb Dom\n"
            
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
                        cal += f" {dia:2d} "  # Dia comum (sem aula)
                cal += "\n"
            cal += "\n"

    # Adiciona a porcentagem de presença ao final da linha
    cal += f"\nPorcentagem de presença: {porcentagem_presenca:.2f}%\n"

    return cal

def VerificarAprovacao(alunos, turmas):
    try:
        codigoD = input("Digite o código da disciplina: ")
        codigoT = input("Digite o código da turma: ")
        if not codigoD.isdigit() or not codigoT.isdigit():
            raise ValueError(colored("Códigos incorretos, digite apenas um conjunto de números.", 'red'))

        aprovados = 0
        reprovados = 0
        disciplina_encontrada = False
        turma_encontrada = False

        # Percorre as turmas para encontrar a disciplina e turma especificadas
        for turma in turmas:
            informacoes = ast.literal_eval(turma.strip())
            if informacoes['Codigo da disciplina'] == codigoD:
                disciplina_encontrada = True
                if informacoes['Codigo da turma'] == codigoT:
                    turma_encontrada = True
                    disciplina = informacoes['Nome']

                    # Calcula a média final de cada aluno e conta os aprovados e reprovados
                    for aluno in alunos:
                        al = ast.literal_eval(aluno.strip())
                        if al['Codigo da disciplina'] == codigoD and al['Codigo da turma'] == codigoT:
                            soma_notas = 0
                            soma_pesos = 0

                            # Calcula a soma das notas ponderadas e dos pesos
                            for i in range(len(al['Notas'])):
                                soma_notas += float(al['Notas'][f'Avaliacao {i + 1}']) * float(
                                    informacoes['Avaliacoes'][f'Peso {i + 1}'])
                                soma_pesos += float(informacoes['Avaliacoes'][f'Peso {i + 1}'])

                            if soma_pesos > 0:
                                nota_final = soma_notas / soma_pesos
                                if nota_final >= 5:
                                    aprovados += 1
                                else:
                                    reprovados += 1

        if not disciplina_encontrada:
            print("Disciplina não encontrada.")
        if not turma_encontrada:
            print("Turma não encontrada.")

        # Exibe o resultado
        print(f"Alunos aprovados em {disciplina}: {aprovados}")
        print(f"Alunos reprovados em {disciplina}: {reprovados}")

    except ValueError as ve:
        print(f"Erro de valor: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    # Volta ao menu principal do aluno
    menuProfessor(alunos, professores, turmas)

# Sessão dos alunos

def Verfrequencia(alunos, DRE):
    op = 's'
    b = False
    while op != 'n':
        try:
            # Pede o código da disciplina e o DRE do aluno
            codigoD = input("Digite o código da disciplina para exibir a frequência: ")
            if not codigoD.isdigit():
                raise ValueError(colored("Codigo da disciplina incorreto, digite apenas numeros.",'red'))
            # DRE = input("Digite o seu DRE: ")
            # if not DRE.isdigit():
                # raise ValueError(colored("DRE incorreto, digite apenas números.",'red'))

            for aluno in alunos:
                    al = ast.literal_eval(aluno.strip())
                    # Verifica se a disciplina e o DRE correspondem
                    if al['Codigo da disciplina'] == codigoD and al['DRE'] == DRE:
                        # Exibe o calendário formatado das frequências
                        print(formatarCalendario(al['Frequencias']))
                        b = True

            op = input("Pressione 'n' para sair, 's' para continuar.")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    if not b:
        print("Disciplina não encontrada.")

    # Volta ao menu principal do aluno
    menuAluno(alunos, DRE)

def Vernotas(alunos, DRE):
    # DRE = input("Digite o seu DRE:")
    # if not DRE.isdigit():
        # raise ValueError(colored("DRE incorreto, digite apenas números.",'red'))
    op = 's'
    a = False
    b = False

    # Exibe os detalhes do aluno com o DRE especificado
    for aluno in alunos:
        al = ast.literal_eval(aluno.strip())
        if al['DRE'] == DRE:
            print(al)

    while op != 'n':
        try:
            codigoD = input("Digite o código da disciplina que deseja ver a nota: ")
            if not codigoD.isdigit():
                raise ValueError(colored("Codigo da disciplina incorreto, digite apenas numeros.",'red'))
            # Verifica e exibe as notas da disciplina especificada para o aluno
            for aluno in alunos:
                al = ast.literal_eval(aluno.strip())
                if al['DRE'] == DRE:
                    a = True
                    if al['Codigo da disciplina'] == codigoD:
                        print(al['Notas'])
                    b = True

            if not a:
                print("DRE não encontrado.")
            if not b:
                print("Disciplina não encontrada.")

            op = input("Pressione 'n' para sair, 's' para continuar.")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    # Volta ao menu principal do aluno
    menuAluno(alunos, professores, turmas, DRE)

def VercalculoNotas(alunos, turmas, DRE):
    op = 's'
    b = False
    c = False

    while op != 'n':
        try:
            codigoD = input("Digite o código da disciplina para exibir o cálculo da nota final: ")
            codigoT = input("Digite o código da turma: ")
            if not codigoD.isdigit() or not codigoT.isdigit():
                raise ValueError(colored("Codigos incorretos, digite apenas um conjunto de numeros.",'red'))

            # Verifica a disciplina e a turma, e exibe a nota final
            for turma in turmas:
                infoTurma = ast.literal_eval(turma.strip())
                if infoTurma['Codigo da disciplina'] == codigoD:
                    c = True
                    if infoTurma['Codigo da turma'] == codigoT:
                        print(f"Nota Final da disciplina {infoTurma['Nome']}: {infoTurma['Nota final']}")
                        b = True

            if not c:
                print("Disciplina não encontrada.")
            if not b:
                print("Turma não encontrada.")

            op = input("Pressione 'n' para sair, 's' para continuar.")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    # Volta ao menu principal do aluno
    menuAluno(alunos, professores, turmas, DRE)

def VerpontosNecessarios(alunos, turmas, DRE):
    op = 's'

    while op != 'n':
        try:
            codigoD = input("Digite o código da disciplina: ")
            codigoT = input("Digite o código da turma: ")
            if not codigoD.isdigit() or not codigoT.isdigit():
                raise ValueError(colored("Codigos incorretos, digite apenas um conjunto de numeros.",'red'))
            soma_pesos = 0
            soma_notas = 0
            b = False
            c = False

            # Verifica a disciplina e a turma, e calcula os pontos necessários
            for i, turma in enumerate(turmas):
                informacoes = ast.literal_eval(turma.strip())
                if informacoes['Codigo da disciplina'] == codigoD:
                    c = True
                    if informacoes['Codigo da turma'] == codigoT:
                        b = True
                        disciplina = informacoes['Nome']

                        # Calcula a soma das notas ponderadas e dos pesos
                        for aluno in alunos:
                            al = ast.literal_eval(aluno.strip())
                            if al['DRE'] == DRE:
                                for i in range(len(al['Notas'])):
                                    soma_notas += float(al['Notas'][f'Avaliacao {i + 1}']) * float(
                                        informacoes['Avaliacoes'][f'Peso {i + 1}'])
                                    soma_pesos += float(informacoes['Avaliacoes'][f'Peso {i + 1}'])

                        notaFinal = soma_notas / soma_pesos

            if not c:
                print("Disciplina não encontrada.")
            if not b:
                print("Turma não encontrada.")

            op = input("Pressione 'n' para sair, 's' para continuar.")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    # Exibe os pontos necessários para aprovação
    if notaFinal < 5:
        pontos_necessarios = 5 - notaFinal
        print(f"Você precisa de {pontos_necessarios} para ser aprovado em {disciplina}")
    else:
        print(f"Você não precisa de pontos, sua nota final é {notaFinal}")

    # Volta ao menu principal do aluno
    menuAluno(alunos, professores, turmas, DRE)

# Menus e identificação

def menuProfessor(alunos, professores, turmas):
        try:
            print("\n### Menu do Professor ###")
            print("===========================")
            print("1 - Cadastro de turma")
            print("2 - Edição de turma")
            print("3 - Exclusão de turma")
            print("4 - Alunos")
            print("5 - Lançar notas")
            print("6 - Lançar frequências")
            print("7 - Verificar número de aprovados")
            print("===========================")
            tarefa = input("Digite o número desejado ou 's' para sair: ")
            # Chamando a função apropriada com base na entrada do usuário
            if tarefa == '1':
                cadastroTurma(alunos, professores, turmas)
            elif tarefa == '2':
                edicaoTurma(turmas)
            elif tarefa == '3':
                excTurma(alunos, professores, turmas)
            elif tarefa == '4':
                Alunos(alunos, professores, turmas)
            elif tarefa == '5':
                lancarNotas(alunos, professores, turmas)
            elif tarefa == '6':
                lancarFrequencias(alunos, professores, turmas)
            elif tarefa == '7':
                VerificarAprovacao(alunos, turmas)
            elif tarefa == 's':
                return 0
            else:
                print("Opção errada.")
        
        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

def menuAluno(alunos, professores, turmas, DRE):
    op = 's'
    while op != 'n':
        try:
            print("\n### Menu do Aluno ###")
            print("===========================")
            print("1 - Notas")
            print("2 - Ver cálculo da média final")
            print("3 - Frequência")
            print("4 - Quantos pontos são necessários para a aprovação")
            print("===========================")
            tarefa = input("Digite uma opção ou 's' para sair: ")
            
            # Chamando a função apropriada com base na entrada do usuário
            if tarefa == '1':
                Vernotas(alunos, DRE)
            elif tarefa == '2':
                VercalculoNotas(alunos, turmas, DRE)
            elif tarefa == '3':
                Verfrequencia(alunos, DRE)
            elif tarefa == '4':
                VerpontosNecessarios(alunos, turmas, DRE)
            elif tarefa == 's':
                break
            else:
                print("Opção errada.")
        
        except ValueError as ve:
            print(f"Erro de valor: {ve}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    identificacao(alunos, professores, turmas)

def identificacao(alunos, professores, turmas):
    try:
        while True:
            print("\n### Identificação ###")
            print("===========================")
            print("Você é:")
            print("1 - Aluno")
            print("2 - Professor")
            print("3 - Sair do Programa")
            print("===========================")
            tipo = input("Escolha o número da sua identificação: ")
            
            if tipo == '1':
                    try:
                        DRE = input("Digite o seu DRE: ")
                        c = False
                        # Verifica se o DRE está cadastrado
                        for linha in alunos:
                            al = ast.literal_eval(linha.strip())
                            if al['DRE'] == DRE:
                                c = True
                                print("Login bem-sucedido.")
                                menuAluno(alunos, professores, turmas, DRE)
                        if not c:
                            print("Nome ou DRE incorretos, digite novamente.")
                    
                    except ValueError as ve:
                        print(f"Erro de valor: {ve}")
                    except Exception as e:
                        print(f"Ocorreu um erro inesperado: {e}")
            
            elif tipo == '2':
                    try:
                        r = input("Deseja se cadastrar (s/n)? ").lower()
                        
                        if r == 's':
                            login = input("Digite o nome de usuário: ")
                            senha = input("Digite a senha: ")
                            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                            disciplinas = {}
                            numero = int(input("Quantas disciplinas você ministra: "))
                            for i in range(numero):
                                chave = input("Digite o nome da disciplina: ")
                                codigoD = input("Digite o código da disciplina: ")
                                dias_aulas = input("Digite os dias da semana que tem aula (ex: segunda, quarta): ").split(', ')
                                frequencias = gerar_frequencias(dias_aulas)
                                frequencias_globais[f'{codigoD}'] = frequencias
                                disciplinas[chave] = frequencias_globais
                            professor = {
                                'Nome': login,
                                'Senha': senha_hash,
                                'Disciplinas': disciplinas
                            }
                            # Salva o novo cadastro de professor
                            with open('professores.txt', 'a') as cadastro:
                                cadastro.write(f'{professor}\n')
                            print("Usuário cadastrado com sucesso. Faça login agora.")
                        
                        while True:
                            login = input("Digite o nome de usuário: ")
                            senha = input("Digite a senha: ")
                            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                            c = False
                            # Verifica as credenciais de login do professor
                            for linha in professores:
                                informacoes = ast.literal_eval(linha.strip())
                                if informacoes['Nome'].lower() == login.lower() and informacoes['Senha'] == senha_hash:
                                    c = True
                                    print("Login bem-sucedido.")
                                    menuProfessor(alunos, professores, turmas)
                            if not c:
                                print("Usuário ou senha incorretos, digite novamente.")
                            
                            if c:
                                break
                    except ValueError as ve:
                        print(f"Erro de valor: {ve}")
                    except Exception as e:
                        print(f"Ocorreu um erro inesperado: {e}")
            elif tipo == '3':

                break     
            else:
                print("Opção não identificada, digite se você é aluno ou professor.")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    
    return alunos, professores, turmas

def menuProfessor(alunos, professores, turmas):
    professor_window = tk.Tk()
    professor_window.title("Menu do Professor")

    def execute_task(task):
        if task == 1:
            cadastroTurma(alunos, professores, turmas)
        elif task == 2:
            edicaoTurma(turmas)
        elif task == 3:
            excTurma(alunos, professores, turmas)
        elif task == 4:
            Alunos(alunos, professores, turmas)
        elif task == 5:
            lancarNotas(alunos, professores, turmas)
        elif task == 6:
            lancarFrequencias(alunos, professores, turmas)
        elif task == 7:
            VerificarAprovacao(alunos, turmas)
        professor_window.destroy()

    tk.Label(professor_window, text="### Menu do Professor ###").pack()
    tasks = [
        ("Cadastro de turma", 1),
        ("Edição de turma", 2),
        ("Exclusão de turma", 3),
        ("Alunos", 4),
        ("Lançar notas", 5),
        ("Lançar frequências", 6),
        ("Verificar número de aprovados", 7),
    ]

    for task, value in tasks:
        tk.Button(professor_window, text=task, command=lambda v=value: execute_task(v)).pack()

    tk.Button(professor_window, text="Sair", command=professor_window.destroy).pack()
    professor_window.mainloop()

def menuAluno(alunos, professores, turmas, DRE):
    aluno_window = tk.Tk()
    aluno_window.title("Menu do Aluno")

    def execute_task(task):
        if task == 1:
            Vernotas(alunos, DRE)
        elif task == 2:
            VercalculoNotas(alunos, turmas, DRE)
        elif task == 3:
            Verfrequencia(alunos, DRE)
        elif task == 4:
            VerpontosNecessarios(alunos, turmas, DRE)
        aluno_window.destroy()

    tk.Label(aluno_window, text="### Menu do Aluno ###").pack()
    tasks = [
        ("Notas", 1),
        ("Ver cálculo da média final", 2),
        ("Frequência", 3),
        ("Quantos pontos são necessários para a aprovação", 4),
    ]

    for task, value in tasks:
        tk.Button(aluno_window, text=task, command=lambda v=value: execute_task(v)).pack()

    tk.Button(aluno_window, text="Sair", command=aluno_window.destroy).pack()
    aluno_window.mainloop()

def identificacao(alunos, professores, turmas):
    main_window = tk.Tk()
    main_window.title("Identificação")

    def aluno_login():
        login_window = tk.Toplevel(main_window)
        login_window.title("Login Aluno")

        tk.Label(login_window, text="Digite o seu DRE:").pack()
        dre_entry = tk.Entry(login_window)
        dre_entry.pack()

        def verify_aluno():
            DRE = dre_entry.get()
            for linha in alunos:
                al = ast.literal_eval(linha.strip())
                if al['DRE'] == DRE:
                    messagebox.showinfo("Login", "Login bem-sucedido.")
                    login_window.destroy()
                    menuAluno(alunos, professores, turmas, DRE)
                    return
            messagebox.showerror("Erro", "DRE incorreto, tente novamente.")

        tk.Button(login_window, text="Entrar", command=verify_aluno).pack()

    def professor_login():
        login_window = tk.Toplevel(main_window)
        login_window.title("Login Professor")

        tk.Label(login_window, text="Nome de usuário:").pack()
        username_entry = tk.Entry(login_window)
        username_entry.pack()

        tk.Label(login_window, text="Senha:").pack()
        password_entry = tk.Entry(login_window, show='*')
        password_entry.pack()

        def verify_professor():
            login = username_entry.get()
            senha = password_entry.get()
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            for linha in professores:
                informacoes = ast.literal_eval(linha.strip())
                if informacoes['Nome'].lower() == login.lower() and informacoes['Senha'] == senha_hash:
                    messagebox.showinfo("Login", "Login bem-sucedido.")
                    login_window.destroy()
                    menuProfessor(alunos, professores, turmas)
                    return
            messagebox.showerror("Erro", "Usuário ou senha incorretos, tente novamente.")

        tk.Button(login_window, text="Entrar", command=verify_professor).pack()

    tk.Label(main_window, text="### Identificação ###").pack()
    tk.Button(main_window, text="Aluno", command=aluno_login).pack()
    tk.Button(main_window, text="Professor", command=professor_login).pack()
    tk.Button(main_window, text="Sair do Programa", command=main_window.destroy).pack()

    main_window.mainloop()

if __name__ == '__main__':
    # Arquivos
    alunos_file = 'alunos.txt'
    professores_file = 'professores.txt'
    turmas_file = 'turmas.txt'

    # Dados iniciais
    dados_iniciais_professores = [
        {'Nome': 'rafael', 'Senha': 'fa36c2bb7ffde432fa4e8149423d3c451fc625965d9d3dc25dd56e70d7cca393', 'Disciplinas': {'comp1': '3', 'comp2': '4'}},
        {'Nome': 'luciana', 'Senha': 'fa36c2bb7ffde432fa4e8149423d3c451fc625965d9d3dc25dd56e70d7cca393', 'Disciplinas': {'portugues': '1', 'ingles': '2'}},
        {'Nome': 'bia', 'Senha': 'fa36c2bb7ffde432fa4e8149423d3c451fc625965d9d3dc25dd56e70d7cca393', 'Disciplinas': {'frances': '5', 'espanhol': '7'}},
        {'Nome': 'samuel', 'Senha': 'fa36c2bb7ffde432fa4e8149423d3c451fc625965d9d3dc25dd56e70d7cca393', 'Disciplinas': {'matematica': '6', 'ciencias': '9'}},
        {'Nome': 'jane', 'Senha': 'fa36c2bb7ffde432fa4e8149423d3c451fc625965d9d3dc25dd56e70d7cca393', 'Disciplinas': {'comp3': {'23': {'10/06/2024': 2, '17/06/2024': 2, '24/06/2024': 2, '01/07/2024': 2, '08/07/2024': 2, '15/07/2024': 2, '22/07/2024': 2}}}}
    ]

    dados_iniciais_turmas = [
        {'Codigo da disciplina': '22', 'Nome': 'fisica', 'Codigo da turma': '45', 'Ano': 2024, 'Semestre': '1', 'Dias': 2, 'Hora': '13', 'Avaliacoes': {'Avaliacao 1': 'p1', 'Peso 1': 10.0}, 'Nota final': '10.0*p1/10.0', 'Frequencias': {'17/06/2024': 2, '20/06/2024': 2, '24/06/2024': 2, '27/06/2024': 2, '01/07/2024': 2, '04/07/2024': 2, '08/07/2024': 2, '11/07/2024': 2, '15/07/2024': 2, '18/07/2024': 2, '22/07/2024': 2, '25/07/2024': 2, '29/07/2024': 2, '01/08/2024': 2}},
        {'Codigo da disciplina': '23', 'Nome': 'fisica', 'Codigo da turma': '23', 'Ano': 2025, 'Semestre': '2', 'Dias': 2, 'Hora': '8', 'Avaliacoes': {'Avaliacao 1': 'p1', 'Peso 1': 0.4, 'Avaliacao 2': 'p2', 'Peso 2': 0.7}, 'Nota final': '0.4*p1 + 0.7*p2/1.1', 'Frequencias': {'19/06/2024': 2, '20/06/2024': 2, '26/06/2024': 2, '27/06/2024': 2, '03/07/2024': 2, '04/07/2024': 2, '10/07/2024': 2, '11/07/2024': 2, '17/07/2024': 2, '18/07/2024': 2, '24/07/2024': 2, '25/07/2024': 2, '31/07/2024': 2, '01/08/2024': 2}},
        {'Codigo da disciplina': '23', 'Nome': 'algebra', 'Codigo da turma': '43', 'Ano': 2025, 'Semestre': '2', 'Dias': 2, 'Hora': '8', 'Avaliacoes': {'Avaliacao 1': 'p1', 'Peso 1': 0.4, 'Avaliacao 2': 'p2', 'Peso 2': 0.7}, 'Nota final': '0.4*p1 + 0.7*p2/1.1', 'Frequencias': {'19/06/2024': 2, '20/06/2024': 2, '26/06/2024': 2, '27/06/2024': 2, '03/07/2024': 2, '04/07/2024': 2, '10/07/2024': 2, '11/07/2024': 2, '17/07/2024': 2, '18/07/2024': 2, '24/07/2024': 2, '25/07/2024': 2, '31/07/2024': 2, '01/08/2024': 2}}
    ]

    dados_iniciais_alunos = [
        {'Nome': 'bia brauna', 'DRE': '122342', 'Codigo da disciplina': '23', 'Codigo da turma': '2', 'Notas': {}, 'Frequencias': {'10/06/2024': 2, '17/06/2024': 2, '24/06/2024': 2, '01/07/2024': 2, '08/07/2024': 1, '15/07/2024': 2, '22/07/2024': 1}},
        {'Nome': 'rafael', 'DRE': '233232', 'Codigo da disciplina': '23', 'Codigo da turma': '3', 'Notas': {}, 'Frequencias': {'10/06/2024': 2, '17/06/2024': 2, '24/06/2024': 2, '01/07/2024': 2, '08/07/2024': 2, '15/07/2024': 2, '22/07/2024': 2}},
        {'Nome': 'daniella', 'DRE': '2335566', 'Codigo da disciplina': '23', 'Codigo da turma': '1', 'Notas': {'Avaliacao 1': 10.0, 'Avaliacao 2': 9.0}, 'Frequencias': {'10/06/2024': 0, '17/06/2024': 2, '24/06/2024': 2, '01/07/2024': 0, '08/07/2024': 1, '15/07/2024': 2, '22/07/2024': 1}},
        {'Nome': 'Andre botelho', 'DRE': '2334421', 'Codigo da disciplina': '22', 'Codigo da turma': '45', 'Notas': {'Avaliacao 1': '10'}, 'Frequencias': {'10/06/2024': 2, '17/06/2024': 2, '24/06/2024': 2, '01/07/2024': 2, '08/07/2024': 2, '15/07/2024': 2, '22/07/2024': 2}}
    ]
    # Verificar e criar arquivos se não existirem
    verificar_ou_criar_arquivo(alunos_file, dados_iniciais_alunos)
    verificar_ou_criar_arquivo(professores_file, dados_iniciais_professores)
    verificar_ou_criar_arquivo(turmas_file, dados_iniciais_turmas)

    # Ler arquivos
    alunos, professores, turmas = ler_arquivos()
    alunos, professores, turmas = identificacao(alunos, professores, turmas)
