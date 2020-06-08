from random import random
import  matplotlib.pyplot as plt
import pymysql #conda install pymysql

class Produto(): 
         #"classe produto"
 def __init__(self,nome,espaco,valor):
    self.nome = nome
    self.espaco = espaco   #Espaço que oculpa
    self.valor = valor     #valor do produto


         #"Classe individuo"
class Individuo():
  def __init__ (self,espacos,valores,limite_espacos,geracao=0):
     self.espacos = espacos
     self.valores = valores               #Valor dos produtos
     self.limite_espacos = limite_espacos #limite do espaco 
     self.nota_avaliacao = 0              #Somatória dos valores da carga
     self.espaco_usado = 0                #Soma total dos espaco usado
     self.geracao = geracao  
     self.cromossomo = []                 #Cadeia de cromossomo
     
            
     for i in range(len(espacos)):
        if random() < 0.5:                #"50 % de chance de levar um produto"
          self.cromossomo.append("0")
        else:
          self.cromossomo.append("1")
            
            #função avaliação do cromossomo (fitines)
  def avaliacao(self):
      nota =0
      soma_espacos =0
      for i in range(len(espacos)):
        if self.cromossomo[i] == '1':
            nota += self.valores[i];
            soma_espacos += self.espacos[i];
            
      if soma_espacos > self.limite_espacos:
            nota = 1 #nota de  avaliação
      self.nota_avaliacao = nota
      self.espaco_usado = soma_espacos
            
      
      
      #Crossover cruzamento de dois projenitores
  def crossover(self,individuo_dois):
      corte = round(random() * len(individuo_dois.cromossomo))
      
      filho1 = individuo_dois.cromossomo[0:corte] + self.cromossomo[corte::]
      filho2 = self.cromossomo[0:corte] + individuo_dois.cromossomo[corte::]
      
      filhos = [
      Individuo(self.espacos,self.valores,self.limite_espacos,self.geracao + 1),
      Individuo(self.espacos,self.valores,self.limite_espacos,self.geracao + 1)
      ]
       
      filhos[0].cromossomo = filho1
      filhos[1].cromossomo = filho2
      
      return filhos
  
    
       #Mutação no gens do cromossomo
  def mutacao (self,taxa_mutacao):
       # print("Taxa Mutacao-1: %s" % self.cromossomo)
        for i in range(len(self.cromossomo)):
          if(random() < taxa_mutacao):
            if self.cromossomo == '1':
               self.cromossomo[i] = '0'
            else:
               self.cromossomo[i] = '1'  
        #print("Taxa Mutacao-2: %s" % self.cromossomo)
        return self
         
    
     #Algoritmo Genetico
class algoritimoGenetico():
    def __init__(self,tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        #MatpLotlib#
        self.listas_solucoes = []
        
        
    def inicializa_populacao(self,espacos,valores,limite_espacos):
      for i in range(tamanho_populacao):
        self.populacao.append(Individuo(espacos, valores, limite_espacos))
      self.melhor_solucao = self.populacao[0]
    
    
    def ordenar_populacao(self):
        self.populacao = sorted(
        self.populacao,key= lambda populacao:populacao.nota_avaliacao,reverse = True)
       
        
        #melhor individuo
    def melhor_individuo(self,individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
        
        
        #soma da avaliacao de cada individuo, para selecionar o melhor 
    def soma_avaliacoes(self):
     soma = 0
     for individuo in self.populacao:
         soma += individuo.nota_avaliacao
     return soma    
        
 
    
       #Metodo da roleta viciada
    def selecionar_pai(self,soma_avaliacoes):
        pai = -1
        valor_sorteado = random() * soma_avaliacoes
        soma=0
        i=0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai +=1
            i +=1
        return pai
    
    
    def visualiza_geracao(self):
        melhor =  self.populacao[0]
        print("G:%s -> valor: %s Espaço: %s cromossomo: %s" % (self.populacao[0].geracao,
              melhor.nota_avaliacao,
              melhor.espaco_usado,
              melhor.cromossomo))
    
    
    
    #resolver o problema
    def resolver(self,taxa_mutacao,numero_geracoes,espacos,valores,limite_espaco):
      self.inicializa_populacao(espacos,valores,limite_espaco)
      
      for individuo in self.populacao:
          individuo.avaliacao()
          
      self.ordenar_populacao()
      self.visualiza_geracao()
      #-----------------PLOT----------------------------------------------------
      melhor = self.populacao[0]
      self.listas_solucoes.append(self.melhor_solucao.nota_avaliacao)
      #-------------------------------------------------------------------------
      for geracao in range(numero_geracoes):
          soma_avaliacoes = self.soma_avaliacoes()
          nova_populacao = []
          
          for individuos_gerados in range(0,self.tamanho_populacao,2):
              pai1 = self.selecionar_pai(soma_avaliacoes)
              pai2 = self.selecionar_pai(soma_avaliacoes)
              
              filhos = self.populacao[pai1].crossover(self.populacao[pai2])
              
              nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
              nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
              
          self.populacao = list(nova_populacao)
        
        
          for individuo in self.populacao:
            individuo.avaliacao()


          self.ordenar_populacao()
        
          self.visualiza_geracao()
        
          melhor = self.populacao[0]  
          #--------PLOT---------------------------------------------------
          self.listas_solucoes.append(melhor.nota_avaliacao)
          #-------------------------------------------------------------------
          self.melhor_individuo(melhor)
        
      print("\nMelhor solução -> G: %s valor: %s Espaço: %s Cromossomo: %s" % 
          (
           self.melhor_solucao.geracao,
           self.melhor_solucao.nota_avaliacao,
           self.melhor_solucao.espaco_usado,
           self.melhor_solucao.cromossomo
           ))
      
      
    
     
      return  self.melhor_solucao.cromossomo;
              
          
      
          
if __name__ == '__main__':
    lista = []
    #Conexao com banco de dados mysql 
    conexao = pymysql.connect(host='localhost',user="root",passwd='root',db='produtos')
    cursor = conexao.cursor()
    cursor.execute('select nome,espaco,valor,quantidade from produtos')
    for produto in cursor:
        for i in range(produto[3]):
          lista.append(Produto(produto[0],produto[1],produto[2]))
    cursor.close()
    conexao.close() 
    #-------------------------------------------------------------------------------   
    '''
    lista.append(Produto("Iphone 6",0.0751,999.90))
    lista.append(Produto("Geladeira Dako",0.0000899,2199.12))
    lista.append(Produto("TV 55",0.400,4346.99))
    lista.append(Produto("TV 50 ",0.290,3999.00))
    lista.append(Produto("TV 42",0.200,2999.00))
    lista.append(Produto("Notebook Dell",0.003500,2499.90)) 
    lista.append(Produto("Ventilador Panasonic",0.496,199.90))
    lista.append(Produto("Microondas Electrolux",0.424,308.66))
    lista.append(Produto("Microondas LG",0.0544,429.90))
    lista.append(Produto("Microondas Panasonic",0.0319,299.29))
    lista.append(Produto("Geladeira Brastemp",0.635,849.00))
    lista.append(Produto("Geladeira Consul",0.870,1999.89))
    lista.append(Produto("Notebook Lenovo",0.498,1999.90))
    lista.append(Produto("Notebook Asus",0.527,3999.00))
    #for item in lista:
       # print(item.nome + ": " + str(item.espaco))
    '''
    
    espacos = []
    valores = []
    nomes   = []
    
    
    for produto in lista:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
        
    limite = 10 #3 metros cubicos
    tamanho_populacao = 20;
    taxa_mutacao = 0.01;
    numero_geracoes = 100;
    
    #Trabalhando e iniciando o algoritmo genetico
    tamanho_populacao = 20
    ag = algoritimoGenetico(tamanho_populacao)
    resultado = ag.resolver(taxa_mutacao,numero_geracoes,espacos,valores,limite)
    
    for i in range(len(lista)):
      if resultado[i] == '1':
        print("Nome: %s R$: %s" % (lista[i].nome,
                                     lista[i].valor))
                                          
    plt.plot(ag.listas_solucoes)
    plt.title("Acompanhamento dos Valores")
    plt.show()
        