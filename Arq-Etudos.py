import json

#função para salvar os dados
def salvar_dados():
    with open("materias.json", "w", encoding="utf-8") as arquivo:
        json.dump(materias, arquivo, indent=4, ensure_ascii= False)
  

# função para carregar matérias ja salvas      
def carregar_dados():
        try:
            with open("materias.json", "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return [] 
        except Exception as erro:
            print("Erro ao carregar JSON:", erro)
            return []

# função para chamar a função MENU
def menu(): 

    print('    GERADOR INTELIGENTE DE ESTUDOS     \n')
    print('      M E N U  DE  E S T U D O S       \n')
    print('\n')
    print(' [1]  ADICIONAR UMA MATÉRIA \n')
    print(' [2]  LISTAR MATÉRIAS CADASTRADAS \n')
    print(' [3]  REMOVER MÁTERIA        \n')
    print(' [4]  S A I R  \n')
    resposta = int(input('DIGITE OQUE DESEJA: \n'))
    return resposta

# Iniciando e carregando os dados
materias = carregar_dados()
#print("Matérias carregadas ao iniciar:", materias)


# loop para o programa principal
while True:
    escolha = menu()

    if escolha == 1:
        print(" ADICIONANDO MATÉRIA NOVA  \n")
        
        materia_nova = str(input(' DIGITE O NOME DA MATÉRIA: '))
        qtd_temas = int(input(f"QUANTOS TEMAS PRETENDE ADICIONAR PARA {materia_nova}: "))
    
        temas = []
        for i in range(qtd_temas):
            tema = input(f'DIGITE O {i + 1}° TEMA: ')
            temas.append(tema)
            
        materia = {
            "nome" : materia_nova,
            "temas" : temas
        }
        
        materias.append(materia)
        salvar_dados()
        print(f'A MATÉRIA {materia_nova} FOI ADICIONADA COM SUCESSO!!\n')


    elif escolha == 2:
        if len(materias) == 0:
            print("\nNENHUMA MATÉRIA CADASTRADA. \n")
        else:
            print(' LISTAR MATÉRIAS CADASTRADAS  \n')
            for i, materia in enumerate(materias, start=1):
                print(f'{i}. {materia["nome"].upper()}')
                for tema in materia['temas']:
                    print(f'   - {tema}')
        print()

    elif escolha == 3:
        if len(materias) == 0:
            print('NÃO EXISTE MATERIAS CADASTRADAS.')
        else:
            for indic, mat in enumerate(materias, start= 1):
                print(f' {indic}. {mat["nome"]}')
                for cont in mat["temas"]:
                    print(f'     -{cont}')
            print()
            remover = int(input('DIGITE QUAL NÚMERO DESEJA REMOVER: '))
            print()
            if 1 <= remover <= len(materias):
                removida = materias.pop(remover-1)
                salvar_dados()
                print(f'A MÁTERIA {removida["nome"]} FOI REMOVIDA.\n')
            else:
                print('MATÉRIA INFORMADA NÃO EXISTE.\n')
                print(len(materias), remover)
        
    elif escolha == 4:
        print('ENCERRANDO SESSÃO... \n')
        break
    else:
        print('OPÇÃO INVÁLIDA.\n')