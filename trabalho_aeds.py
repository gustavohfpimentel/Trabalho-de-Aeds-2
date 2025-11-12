import random
import struct  # Para empacotar dados em bytes (int, float, etc.)
import math
from faker import Faker

# --- Configurações Iniciais ---
fake = Faker('pt_BR')
PADDING_CHAR = b'#' # Caractere de preenchimento
ENCODING = 'utf-8' # Codificação de caracteres para bytes

# --- Definição dos Tamanhos Fixos (baseado no PDF) ---
# Usamos 'struct' para definir tamanhos de tipos numéricos
# 'i' = 4 bytes (inteiro)
# 'd' = 8 bytes (double/float)
TAM_MATRICULA = 4  # Inteiro
TAM_NOME = 50      # String (50)
TAM_CPF = 11       # String (11)
TAM_CURSO = 30     # String (30)
TAM_MAE = 30       # String (30)
TAM_PAI = 30       # String (30)
TAM_ANO = 4        # Inteiro
TAM_CA = 8         # Float (double)

# O tamanho total de UM registro em modo fixo
TAM_REGISTRO_FIXO = (TAM_MATRICULA + TAM_NOME + TAM_CPF + TAM_CURSO +
                     TAM_MAE + TAM_PAI + TAM_ANO + TAM_CA)

# Formato para o 'struct.pack'. Define a ordem e o tipo de cada campo.
# 'i' (int), 's' (string/bytes), 'd' (double)
# Os números (50s) indicam o tamanho fixo da string
FORMATO_STRUCT_FIXO = f'i {TAM_NOME}s {TAM_CPF}s {TAM_CURSO}s {TAM_MAE}s {TAM_PAI}s i d'


# --- Passo 1: Geração de Dados ---

def gerar_aluno():
    """Gera um único registro de aluno fictício."""
    nome = fake.name()
    mae = fake.name_female()
    pai = fake.name_male()
    cpf = fake.cpf().replace('.', '').replace('-', '')
    cursos = ['Engenharia de Software', 'Ciência da Computação', 
              'Sistemas de Informação', 'Engenharia Elétrica', 'Medicina']
    
    # Garante que as strings não ultrapassem o limite máximo
    # (importante para a serialização)
    aluno = {
        'matricula': fake.random_int(min=100000000, max=999999999),
        'nome': nome[:TAM_NOME],
        'cpf': cpf,
        'curso': random.choice(cursos)[:TAM_CURSO],
        'mae': mae[:TAM_MAE],
        'pai': pai[:TAM_PAI],
        'ano_ingresso': fake.random_int(min=2018, max=2024),
        'ca': round(random.uniform(6.0, 9.9), 2)
    }
    return aluno

# --- Passo 3: Funções de Serialização ---

def serializar_registro_fixo(aluno):
    """
    Converte um dicionário de aluno em uma sequência de bytes de
    tamanho fixo (TAM_REGISTRO_FIXO).
    """
    # Converte strings para bytes e aplica o padding
    # .ljust() adiciona o PADDING_CHAR à direita até atingir o tamanho
    nome_bytes = aluno['nome'].encode(ENCODING).ljust(TAM_NOME, PADDING_CHAR)
    cpf_bytes = aluno['cpf'].encode(ENCODING).ljust(TAM_CPF, PADDING_CHAR)
    curso_bytes = aluno['curso'].encode(ENCODING).ljust(TAM_CURSO, PADDING_CHAR)
    mae_bytes = aluno['mae'].encode(ENCODING).ljust(TAM_MAE, PADDING_CHAR)
    pai_bytes = aluno['pai'].encode(ENCODING).ljust(TAM_PAI, PADDING_CHAR)

    # Empacota todos os campos em uma única sequência de bytes
    try:
        registro_bytes = struct.pack(
            FORMATO_STRUCT_FIXO,
            aluno['matricula'],
            nome_bytes,
            cpf_bytes,
            curso_bytes,
            mae_bytes,
            pai_bytes,
            aluno['ano_ingresso'],
            aluno['ca']
        )
        return registro_bytes
    except Exception as e:
        print(f"Erro ao empacotar registro: {e}")
        print(f"Aluno: {aluno}")
        return None

def serializar_registro_variavel(aluno):
    """
    Converte um dicionário de aluno em uma sequência de bytes de
    tamanho VARIÁVEL. Os campos são separados por '|' e o 
    registro é terminado com '\n'.
    """
    # Converte todos os campos para string
    registro_str = (
        f"{aluno['matricula']}|"
        f"{aluno['nome']}|"
        f"{aluno['cpf']}|"
        f"{aluno['curso']}|"
        f"{aluno['mae']}|"
        f"{aluno['pai']}|"
        f"{aluno['ano_ingresso']}|"
        f"{aluno['ca']}\n"  # \n marca o fim do registro
    )
    # Converte a string inteira para bytes
    return registro_str.encode(ENCODING)

# --- Funções de Simulação de Escrita ---

def simular_tamanho_fixo(registros, tam_bloco):
    """
    Organiza os registros dentro dos blocos conforme a estratégia 
    de tamanho fixo.
    """
    if TAM_REGISTRO_FIXO > tam_bloco:
        print(f"Erro: O tamanho do registro ({TAM_REGISTRO_FIXO} bytes) "
              f"é maior que o tamanho do bloco ({tam_bloco} bytes).")
        return None, []

    dados_totais_bytes = b''
    ocupacao_por_bloco = [] # Lista para guardar quantos bytes foram usados em cada bloco
    
    bytes_no_bloco_atual = 0
    
    for aluno in registros:
        registro_bytes = serializar_registro_fixo(aluno)
        if registro_bytes is None:
            continue

        # Verifica se o registro cabe no bloco atual
        if bytes_no_bloco_atual + TAM_REGISTRO_FIXO > tam_bloco:
            # --- 1. Fechar o Bloco Anterior ---
            # Preenche o restante do bloco com padding
            bytes_padding_bloco = tam_bloco - bytes_no_bloco_atual
            dados_totais_bytes += (PADDING_CHAR * bytes_padding_bloco)
            
            # Salva a estatística de ocupação
            ocupacao_por_bloco.append(bytes_no_bloco_atual)
            
            # --- 2. Iniciar Novo Bloco ---
            bytes_no_bloco_atual = 0 # Reinicia a contagem
            
        # Adiciona o registro (bytes) ao bloco atual
        dados_totais_bytes += registro_bytes
        bytes_no_bloco_atual += TAM_REGISTRO_FIXO

    # --- Fechar o Último Bloco ---
    # Se o último bloco tiver dados, preenche o restante e salva
    if bytes_no_bloco_atual > 0:
        bytes_padding_bloco = tam_bloco - bytes_no_bloco_atual
        dados_totais_bytes += (PADDING_CHAR * bytes_padding_bloco)
        ocupacao_por_bloco.append(bytes_no_bloco_atual)
        
    return dados_totais_bytes, ocupacao_por_bloco

def simular_tamanho_variavel_contiguo(registros, tam_bloco):
    """
    Organiza os registros dentro dos blocos conforme a estratégia 
    de tamanho variável, sem espalhamento (contíguo).
    """
    dados_totais_bytes = b''
    ocupacao_por_bloco = [] # Guarda os bytes ÚTEIS em cada bloco
    
    bytes_no_bloco_atual = 0
    
    for aluno in registros:
        registro_bytes = serializar_registro_variavel(aluno)
        tamanho_registro = len(registro_bytes)

        # Validação: se um único registro for maior que o bloco, é impossível
        if tamanho_registro > tam_bloco:
            print(f"Aviso: Registro de {tamanho_registro} bytes "
                  f"é maior que o bloco ({tam_bloco} bytes) e será descartado.")
            continue
            
        # Verifica se o registro cabe no espaço restante do bloco atual
        if bytes_no_bloco_atual + tamanho_registro > tam_bloco:
            # --- 1. Fechar o Bloco Anterior (REGRA "SEM ESPALHAMENTO") ---
            # Preenche o restante do bloco com padding
            bytes_padding_bloco = tam_bloco - bytes_no_bloco_atual
            dados_totais_bytes += (PADDING_CHAR * bytes_padding_bloco)
            
            # Salva a estatística de ocupação (apenas dados úteis)
            ocupacao_por_bloco.append(bytes_no_bloco_atual)
            
            # --- 2. Iniciar Novo Bloco ---
            bytes_no_bloco_atual = 0 # Reinicia a contagem

        # Adiciona o registro (bytes) ao bloco atual
        dados_totais_bytes += registro_bytes
        bytes_no_bloco_atual += tamanho_registro

    # --- Fechar o Último Bloco ---
    if bytes_no_bloco_atual > 0:
        bytes_padding_bloco = tam_bloco - bytes_no_bloco_atual
        dados_totais_bytes += (PADDING_CHAR * bytes_padding_bloco)
        ocupacao_por_bloco.append(bytes_no_bloco_atual)
        
    return dados_totais_bytes, ocupacao_por_bloco

def simular_tamanho_variavel_espalhado(registros, tam_bloco):
    """
    Organiza os registros dentro dos blocos conforme a estratégia 
    de tamanho variável, COM espalhamento (fragmentação).
    """
    dados_totais_bytes = b''
    ocupacao_por_bloco = [] # Guarda os bytes ÚTEIS em cada bloco
    
    bytes_no_bloco_atual = 0
    
    for aluno in registros:
        registro_bytes = serializar_registro_variavel(aluno)
        tamanho_registro = len(registro_bytes)
        
        ponteiro_registro = 0 # Qual parte do registro já foi escrita

        # Loop 'while' para garantir que o registro seja escrito,
        # mesmo que em vários blocos
        while ponteiro_registro < tamanho_registro:
            espaco_restante_bloco = tam_bloco - bytes_no_bloco_atual
            bytes_a_escrever_do_registro = tamanho_registro - ponteiro_registro

            # --- CASO 1: O restante do registro CABE no bloco atual ---
            if bytes_a_escrever_do_registro <= espaco_restante_bloco:
                # Escreve o restante do registro
                dados_totais_bytes += registro_bytes[ponteiro_registro:]
                bytes_no_bloco_atual += bytes_a_escrever_do_registro
                ponteiro_registro = tamanho_registro # Termina o loop 'while'
            
            # --- CASO 2: O restante do registro NÃO CABE (fragmenta) ---
            else:
                # Escreve a parte que cabe
                parte_que_cabe = registro_bytes[ponteiro_registro : ponteiro_registro + espaco_restante_bloco]
                dados_totais_bytes += parte_que_cabe
                
                # Atualiza o ponteiro
                ponteiro_registro += espaco_restante_bloco
                
                # --- Fechar o Bloco (que agora está 100% cheio) ---
                bytes_no_bloco_atual += espaco_restante_bloco # Agora == tam_bloco
                ocupacao_por_bloco.append(bytes_no_bloco_atual)
                
                # --- Iniciar Novo Bloco ---
                bytes_no_bloco_atual = 0
                # O loop 'while' continua para escrever o resto do registro

    # --- Fechar o Último Bloco (se não estiver vazio) ---
    if bytes_no_bloco_atual > 0:
        bytes_padding_bloco = tam_bloco - bytes_no_bloco_atual
        dados_totais_bytes += (PADDING_CHAR * bytes_padding_bloco)
        ocupacao_por_bloco.append(bytes_no_bloco_atual)
        
    return dados_totais_bytes, ocupacao_por_bloco

def exibir_estatisticas(ocupacao_blocos, tam_bloco, tam_total_dados, modo): # <-- MUDANÇA (adicionado 'modo')
    """
    Calcula e exibe as estatísticas de armazenamento.
    """
    if not ocupacao_blocos:
        print("Nenhum bloco foi utilizado.")
        return

    num_total_blocos = len(ocupacao_blocos)
    print("\n--- Estatísticas de Armazenamento ---")
    
    # <-- MUDANÇA LÓGICA
    if modo == '1':
        print(f"Tamanho do Registro Fixo: {TAM_REGISTRO_FIXO} bytes")
    else:
        print("Modo de Armazenamento: Tamanho Variável")
        
    print(f"Tamanho do Bloco: {tam_bloco} bytes")
    print(f"Número total de blocos utilizados: {num_total_blocos}")

    # Cálculo da ocupação
    percentuais = [(ocupado / tam_bloco) * 100 for ocupado in ocupacao_blocos]
    media_ocupacao = sum(percentuais) / num_total_blocos
    print(f"Percentual médio de ocupação dos blocos: {media_ocupacao:.2f}%")

    # Blocos parcialmente utilizados
    num_parcial = sum(1 for p in percentuais if p < 100)
    print(f"Número de blocos parcialmente utilizados: {num_parcial}")

    # Eficiência
    # (Bytes úteis / bytes totais alocados)
    total_bytes_uteis = sum(ocupacao_blocos)
    total_bytes_alocados = num_total_blocos * tam_bloco
    eficiencia = (total_bytes_uteis / total_bytes_alocados) * 100
    print(f"Eficiência de armazenamento (dados úteis / total): {eficiencia:.2f}%")

    # Mapa de ocupação
    print("\n--- Mapa de Ocupação dos Blocos ---")
    for i, ocupado in enumerate(ocupacao_blocos):
        percent = percentuais[i]
        print(f"Bloco {i+1}: {ocupado} bytes ({percent:.2f}% cheio)")
    print(f"Total de blocos: {num_total_blocos}")
    print(f"Eficiência total: {eficiencia:.2f}%")


# --- Função Principal (main) ---
# --- Função Principal (main) ---

def main():
    print("--- Trabalho Prático 01: AEDs II ---")

    # --- Passo 1: Geração de Dados ---
    try:
        num_registros = int(input("Digite o número total de registros a serem gerados: "))
        if num_registros <= 0:
            print("Por favor, digite um número positivo.")
            return
        
        registros = [gerar_aluno() for _ in range(num_registros)]
        print(f"\n[Sucesso] {len(registros)} registros gerados.")
        
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")
        return

    # --- Passo 2: Definição dos Parâmetros ---
    try:
        tam_bloco = int(input("Digite o tamanho máximo do bloco (em bytes): "))
        if tam_bloco <= 0:
            print("O tamanho do bloco deve ser positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")
        return

    print("Escolha o modo de armazenamento:")
    print(" (1) Registros de tamanho fixo")
    print(" (2) Registros de tamanho variável")
    modo = input("Modo: ")

    # --- Passos 3, 4, 5 (Tamanho Fixo) ---
    if modo == '1':
        print("\nSimulando armazenamento de TAMANHO FIXO...")
        
        # Passo 3: Simulação
        dados_binarios, ocupacao = simular_tamanho_fixo(registros, tam_bloco)
        
        if dados_binarios:
            # Passo 4 e 5: Estatísticas e Exibição
            exibir_estatisticas(ocupacao, tam_bloco, len(dados_binarios), modo)
            
            # Gravar o arquivo .DAT
            try:
                with open("alunos_fixo.dat", "wb") as f:
                    f.write(dados_binarios)
                print("\n[Sucesso] Arquivo 'alunos_fixo.dat' gerado.")
            except IOError as e:
                print(f"Erro ao escrever arquivo: {e}")
                
    elif modo == '2':
        print("Escolha o modo de tamanho variável:")
        print("  (a) Registros contíguos (sem espalhamento)")
        print("  (b) Registros espalhados (com fragmentação)")
        sub_modo = input("Sub-modo: ").lower().strip()
        
        if sub_modo == 'a':
            print("\nSimulando T. VARIÁVEL (Contíguos)...")
            
            # Passo 3: Simulação
            dados_binarios, ocupacao = simular_tamanho_variavel_contiguo(registros, tam_bloco)
            
            if dados_binarios:
                # Passo 4 e 5: Estatísticas e Exibição
                exibir_estatisticas(ocupacao, tam_bloco, len(dados_binarios), modo)
                
                # Gravar o arquivo .DAT
                try:
                    with open("alunos_var_contiguo.dat", "wb") as f:
                        f.write(dados_binarios)
                    print("\n[Sucesso] Arquivo 'alunos_var_contiguo.dat' gerado.")
                except IOError as e:
                    print(f"Erro ao escrever arquivo: {e}")

        elif sub_modo == 'b':
            print("\nSimulando T. VARIÁVEL (Espalhado/Fragmentado)...")
            
            # Passo 3: Simulação
            dados_binarios, ocupacao = simular_tamanho_variavel_espalhado(registros, tam_bloco)
            
            if dados_binarios:
                # Passo 4 e 5: Estatísticas e Exibição
                exibir_estatisticas(ocupacao, tam_bloco, len(dados_binarios), modo)
                
                # Gravar o arquivo .DAT
                try:
                    with open("alunos_var_espalhado.dat", "wb") as f:
                        f.write(dados_binarios)
                    print("\n[Sucesso] Arquivo 'alunos_var_espalhado.dat' gerado.")
                except IOError as e:
                    print(f"Erro ao escrever arquivo: {e}")
            
        else:
            print("Opção inválida.") # <-- Else para o sub_modo
    
    
    else:
        print("Opção inválida.") # <-- Else para o modo


if __name__ == "__main__":
    main() # <-- O 'main()' deve ter um recuo