import sqlite3


# CONFIGURAÇÃO INICIAL DO BANCO

# Cria (ou conecta) ao banco local
conexao = sqlite3.connect("materias.db")
cursor = conexao.cursor()

# Cria tabela de matérias
cursor.execute("""
CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
)
""")

# Cria tabela de temas (relacionada à matéria)
cursor.execute("""
CREATE TABLE IF NOT EXISTS temas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_materia INTEGER,
    nome TEXT,
    FOREIGN KEY (id_materia) REFERENCES materias(id)
)
""")

conexao.commit()


# FUNÇÕES DO PROGRAMA
def adicionar_materia():
    print(" ADICIONANDO MATÉRIA NOVA  \n")
    materia_nova = input('DIGITE O NOME DA MATÉRIA: ')
    qtd_temas = int(
        input(f"QUANTOS TEMAS PRETENDE ADICIONAR PARA {materia_nova}: "))

    temas = []
    for i in range(qtd_temas):
        tema = input(f'DIGITE O {i + 1}° TEMA: ')
        temas.append(tema)

    # Inserir matéria
    cursor.execute("INSERT INTO materias (nome) VALUES (?)", (materia_nova,))
    id_materia = cursor.lastrowid  # pega o ID da matéria recém-criada

    # Inserir temas
    for tema in temas:
        cursor.execute(
            "INSERT INTO temas (id_materia, nome) VALUES (?, ?)", (id_materia, tema))

    conexao.commit()
    print(f'A MATÉRIA {materia_nova} FOI ADICIONADA COM SUCESSO!!\n')


def listar_materias():
    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()

    if len(materias) == 0:
        print('NENHUMA MATÉRIA CADASTRADA\n')
    else:
        for cont, materia in enumerate(materias, start=1):
            print(f"{cont}. {materia[1]}")
            cursor.execute(
            "SELECT nome FROM temas WHERE id_materia = ?", (materia[0],))
            temas = cursor.fetchall()
            for tema in temas:
                print(f'  - {tema[0]}')
        print()


def remover_materia():
    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()

    if len(materias) == 0:
        print('NÃO EXISTE MATÉRIAS CADASTRADAS.\n')
        return

    listar_materias()
    remover = int(input('DIGITE QUAL NÚMERO DESEJA REMOVER: '))
    print()

    cursor.execute("SELECT * FROM materias WHERE id = ?", (remover,))
    materia = cursor.fetchone()

    if materia:
        cursor.execute("DELETE FROM temas WHERE id_materia = ?", (remover,))
        cursor.execute("DELETE FROM materias WHERE id = ?", (remover,))
        conexao.commit()
        print(f'A MATÉRIA "{materia[1]}" FOI REMOVIDA.\n')
    else:
        print('MATÉRIA INFORMADA NÃO EXISTE.\n')


def editar_materia():
    listar_materias()
    print()
    select = int(input('QUAL MATÉRIA QUER EDITAR? '))
    print()

    cursor.execute("SELECT * FROM materias WHERE id = ?", (select,))
    materia = cursor.fetchone()

    if not materia:
        print('OPÇÃO INCORRETA.\n')
        return

    print(f"{materia[0]}. {materia[1]}\n")
    cursor.execute("SELECT * FROM temas WHERE id_materia = ?", (materia[0],))
    temas = cursor.fetchall()

    for t in temas:
        print(f'   - {t[2]}')
    print()

    print(' 1. EDITAR NOME DA MATÉRIA\n')
    print(' 2. REMOVER OU ADICIONAR TEMA\n')
    print()
    opcao = int(input("QUAL OPÇÃO DESEJA: "))
    print()

    if opcao == 1:
        novo_nome = input("NOVO NOME DA MATÉRIA: ")
        cursor.execute("UPDATE materias SET nome = ? WHERE id = ?",
                       (novo_nome, materia[0]))
        conexao.commit()
        print('Nome da matéria atualizado com sucesso.\n')

    elif opcao == 2:
        print('1. ADICIONAR TEMA')
        print('2. REMOVER TEMA\n')
        opcao_2 = int(input('ESCOLHA QUAL OPÇÃO DESEJA: '))

        if opcao_2 == 1:
            novo_tema = input('NOVO TEMA: ')
            cursor.execute(
                "INSERT INTO temas (id_materia, nome) VALUES (?, ?)", (materia[0], novo_tema))
            conexao.commit()
            print(f'Tema "{novo_tema}" adicionado com sucesso.\n')

        elif opcao_2 == 2:
            cursor.execute(
                "SELECT * FROM temas WHERE id_materia = ?", (materia[0],))
            temas = cursor.fetchall()
            for i, t in enumerate(temas, start=1):
                print(f"  {i} - {t[2]}")

            print()
            excluir = int(
                input(f"QUAL NÚMERO DESEJA EXCLUIR DE {materia[1]}? "))
            if 1 <= excluir <= len(temas):
                id_tema = temas[excluir - 1][0]
                nome_tema = temas[excluir - 1][2]
                cursor.execute("DELETE FROM temas WHERE id = ?", (id_tema,))
                conexao.commit()
                print(f'Tema "{nome_tema}" removido com sucesso.\n')
            else:
                print('Número inválido.\n')
        else:
            print('OPÇÃO INCORRETA.\n')
    else:
        print('OPÇÃO INCORRETA.\n')


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


# LOOP PRINCIPAL
while True:
    escolha = menu()

    if escolha == 1:
        adicionar_materia()
    elif escolha == 2:
        listar_materias()
    elif escolha == 3:
        remover_materia()
    elif escolha == 4:
        editar_materia()
    elif escolha == 5:
        print('ENCERRANDO SESSÃO... \n')
        break
    else:
        print('OPÇÃO INVÁLIDA.\n')

# Fecha conexão ao sair
conexao.close()
