#Função para calcular os impostos pertencentes a cada contribuinte
def calcular(faixas, pessoas, saida_arq):
    resultados = []

    for pessoa in pessoas:
        nome = pessoa["nome"]  
        salario = pessoa["salario"]
        imposto_devido = 0

        for faixa in faixas:
            if salario > faixa["max"]:
                imposto_devido += (faixa["max"] - faixa["min"]) * (faixa["valor"] / 100) 
            else:
                imposto_devido += (salario - faixa["min"]) * (faixa["valor"] / 100)
                break
            
        resultados.append((nome, imposto_devido))

    try:
        with open(saida_arq, 'a') as arquivo_saida:
            for resultado in resultados:
                arquivo_saida.write(f"Nome: {resultado[0]}   Imposto: R${resultado[1]:.2f}\n")
    except IOError:
        raise ValueError("Erro ao criar arquivo")
    
    print("Verifique na pasta o arquivo de saida!")
    
#Função que le os arquivos passados pelo usuario
def ler_arquivos(arquivos):
    aliquotas_arq = arquivos[0]
    contribuintes_arq = arquivos[1]
    arquivo_saida = arquivos[2]
    
    if not aliquotas_arq.strip() or not contribuintes_arq.strip() or not arquivo_saida.strip():    
        raise FileNotFoundError("Erro ao procurar arquivo")
    
    # Abre e lê os arquivos de aliquotas e contribuintes
    with open(aliquotas_arq, 'r') as arquivo1:
        linhas_aliquotas = arquivo1.readlines()
                
    with open(contribuintes_arq, 'r') as arquivo2:
        linhas_contribuintes = arquivo2.readlines()
      
    #Cria um dicionario com os valores de cada faixa e adiciona em uma lista
    lista_faixas = []
    for i in range(len(linhas_aliquotas)):
        if linhas_aliquotas[i].startswith('Faixa'):
            faixa = {
                "min": float(linhas_aliquotas[i + 1].strip().replace(',', '.')),
                "max": float(linhas_aliquotas[i + 2].strip().replace(',', '.')),
                "valor": float(linhas_aliquotas[i + 3].strip().replace(',', '.'))
            }
            lista_faixas.append(faixa)
                
    #Cria um dicionario com os valores de cada pessoa e adiciona em uma lista
    lista_pessoas = []
    for i in range(0, len(linhas_contribuintes), 2):
        if i + 1 < len(linhas_contribuintes):
            pessoa = {
                "nome": linhas_contribuintes[i].strip(),
                "salario": float(linhas_contribuintes[i + 1].strip().replace(',', '.'))
            }
            lista_pessoas.append(pessoa)         
    calcular(lista_faixas, lista_pessoas, arquivo_saida)
   
#Inicio do programa
try:
    aliquotas = input("Digite o nome do arquivo que contém as aliquotas: ")
    contribuintes = input("Digite o nome do arquivo dos contribuintes: ")
    saida = input("Digite o nome do arquivo de saida: ")

    nome_arquivos = [aliquotas, contribuintes, saida]
    ler_arquivos(nome_arquivos)
except FileNotFoundError as e:
    print(f'Erro ao procurar arquivo: {e}')
except ValueError:
    print("Verifique se os valores nos arquivos de entrada estão corretos!")