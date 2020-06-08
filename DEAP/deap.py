# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:14:31 2020
@author: Allan
"""

from deap import base
from deap import creator
from deap import algorithms
from deap import tools
import matplotlib.pyplot as plt

import random
import numpy

class Produto(): 
         #"classe produto"
 def __init__(self,nome,espaco,valor):
    self.nome = nome
    self.espaco = espaco   #Espaço que oculpa
    self.valor = valor     #valor do produto


lista = []
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


espacos = []
valores = []
nomes   = []
    
for produto in lista:
   espacos.append(produto.espaco)
   valores.append(produto.valor)
   nomes.append(produto.nome)
   
limite = 3   
   
toolbox = base.Toolbox()#Carregarfução  do deap
creator.create("FitnessMax",base.Fitness,weights=(1.0,))#Função avaliação 
creator.create("individual",list,fitness=creator.FitnessMax)#Parametros FitnessMax
toolbox.register("attr_bool",random.randint,0,1)#criterio de operação
toolbox.register("individual",tools.initRepeat,creator.individual,
                 toolbox.attr_bool,n=len(espacos))#Atribuindo parametros para o individuo 
toolbox.register("population",tools.initRepeat,list,toolbox.individual)#Gerar população

   
def avaliacao(individual):
    nota = 0
    soma_espacos = 0
    for i in range(len(individual)):
        nota += valores[i]
        soma_espacos += espacos[i]
    if soma_espacos > limite:
       nota = 1
    return nota / 100000,


if __name__ == "__main__":
    #random.seed(1)
    populacao = toolbox.population(n=20)
    probabilidade_crossover = 1.0
    probabilidade_mutacao = 0.01
    numero_geracoes = 100
    
    
    estatisticas = tools.Statistics(key=lambda individuo:individuo.fitness.values)
    estatisticas.register("max",numpy.max)
    estatisticas.register("min",numpy.min)
    estatisticas.register("med",numpy.mean) 
    estatisticas.register("std",numpy.std)
    
    
    
    populacao,info = algorithms.eaSimple(populacao,
                                         toolbox,probabilidade_crossover,
                                         probabilidade_mutacao,
                                         numero_geracoes)
    


    