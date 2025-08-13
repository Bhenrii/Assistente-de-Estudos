import json

# função para salvar os dados
def salvar_dados():
    with open("materias.json", "w", encoding="utf-8") as arquivo:
        json.dump(materias, arquivo, indent=4, ensure_ascii=False)

# função para carregar matérias já salvas
def carregar_dados():
    try:
        with open("materias.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    except Exception as erro:
        print("Erro ao carregar JSON:", erro)
        return []

# função para mostrar o menu
def menu():
    print('    GERADOR INTELIGENTE DE ESTUDOS     \n')
    print('      M E N U  DE  E S T U D O S       \n')
    print('\n')
    print(' [1]  ADICIONAR UMA MATÉRIA \n')
    print(' [2]  LISTAR MATÉRIAS CADASTRADAS \n')
    print(' [3]  REMOVER MÁTERIA        \n')
    print(' [4]  EDITAR MÁTERIA / TEMA        \n')
    print(' [5]  S A I R  \n')
    resposta = int(input('DIGITE O QUE DESEJA: \n'))
    return resposta

# Função para listar matérias
def listar_materias():
    if len(materias) == 0:
        print('NENHUMA MATÉRIA CADASTRADA\n')
    else:
        for indice, materia in enumerate(materias, start=1):
            print(f"{indice}. {materia['nome']}")
            for tema in materia['temas']:
                print(f'  - {tema}')
        print()

# Carregar dados ao iniciar
materias = carregar_dados()

# Loop principal do programa
while True:
    escolha = menu()

    if escolha == 1:
        print(" ADICIONANDO MATÉRIA NOVA  \n")
        materia_nova = input('DIGITE O NOME DA MATÉRIA: ')
        qtd_temas = int(input(f"QUANTOS TEMAS PRETENDE ADICIONAR PARA {materia_nova}: "))

        temas = []
        for i in range(qtd_temas):
            tema = input(f'DIGITE O {i + 1}° TEMA: ')
            temas.append(tema)

        materia = {
            "nome": materia_nova,
            "temas": temas
        }

        materias.append(materia)
        salvar_dados()
        print(f'A MATÉRIA {materia_nova} FOI ADICIONADA COM SUCESSO!!\n')

    elif escolha == 2:
        listar_materias()

    elif escolha == 3:
        if len(materias) == 0:
            print('NÃO EXISTE MATÉRIAS CADASTRADAS.\n')
        else:
            listar_materias()
            remover = int(input('DIGITE QUAL NÚMERO DESEJA REMOVER: '))
            print()
            if 1 <= remover <= len(materias):
                removida = materias.pop(remover - 1)
                salvar_dados()
                print(f'A MATÉRIA {removida["nome"]} FOI REMOVIDA.\n')
            else:
                print('MATÉRIA INFORMADA NÃO EXISTE.\n')

    elif escolha == 4:
        listar_materias()
        print()
        select = int(input('QUAL MATÉRIA QUER EDITAR? '))
        print()
        if 1 <= select <= len(materias):
            materia_edit = materias[select - 1]
            print(f" {select}. {materia_edit['nome']}\n")
            for cont in materia_edit['temas']:
                print(f'   - {cont}')
            print()
            print(' 1. EDITAR NOME MATÉRIA\n')
            print(' 2. REMOVER OU ADICIONAR TEMA\n')
            print()
            opcao = int(input("QUAL OPÇÃO DESEJA: "))
            print()
            if opcao == 1:
                novo_nome = input("NOVO NOME DA MATÉRIA: ")
                materia_edit['nome'] = novo_nome
                salvar_dados()
                print('Nome da matéria atualizado com sucesso.\n')
            elif opcao == 2:
                print('1. ADICIONAR TEMA')
                print('2. REMOVER TEMA\n')
                opcao_2 = int(input('ESCOLHA QUAL OPÇÃO DESEJA: '))
                if opcao_2 < 1 or opcao_2 > 2:
                    print('OPÇÃO INCORRETA.\n')
                elif opcao_2 == 1:
                    novo_tema = input('NOVO TEMA: ')
                    materia_edit['temas'].append(novo_tema)
                    salvar_dados()
                    print(f'Tema "{novo_tema}" adicionado com sucesso.\n')
                elif opcao_2 == 2:
                    print(f"{select}. {materia_edit['nome']}")
                    for i, tema in enumerate(materia_edit['temas'], start=1):
                        print(f'  {i} - {tema}')
                    print()
                    excluir = int(input(f"QUAL NÚMERO DESEJA EXCLUIR DE {materia_edit['nome']}? "))
                    if 1 <= excluir <= len(materia_edit['temas']):
                        excluida = materia_edit['temas'].pop(excluir - 1)
                        salvar_dados()
                        print(f'Tema "{excluida}" removido com sucesso.\n')
                    else:
                        print('Número inválido.\n')
            else:
                print('OPÇÃO INCORRETA.\n')
        else:
            print('OPÇÃO INCORRETA.\n')

    elif escolha == 5:
        print('ENCERRANDO SESSÃO... \n')
        break
    else:
        print('OPÇÃO INVÁLIDA.\n')
