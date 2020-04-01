#!/usr/bin/env python3
# coding: utf-8

# Código para leitura do arquivo de saída do PHonon do Quantum Espresso e 
# criação do arquivo BORN utilizado pelos códigos Phonopy e Phono3py.

# Autor: Guilherme Lorenset
# Data: 2 mar 2020
# Versão: 0.20

import numpy as np
from datetime import datetime 
import os 

def existeBorn():
    try:
        with open('BORN') as f_obj:
            datahora=datetime.now()
            dh=datahora.strftime('%Y%m%d_%H%M')
        
            msg = "Renomeando arquivo existente para BORN"+dh+"."
            print(msg)
            os.rename('BORN', 'BORN'+dh)
    except FileNotFoundError:
        print("Criando arquivo!")
        
        
def existePH(filename="out.ph"):
    try: 
        with open(filename) as f_obf:
            msg="Encontrado arquivo de saída de ph.x"
            print(msg)
            return(filename)
    except FileNotFoundError:
        newname=input("Arquivo com nome padrão não encontrado, insira o nome do arquivo para leitura: ")
        filename=newname
        existePH(filename=newname)
        return(filename)    

#Checando se os arquivos se encontram na pasta
existeBorn()
filename=existePH()

print(filename)

#Variáveis a serem lidas
deleccons=[]
effcharges=[]
a=b=i=j=0
with open(filename) as file_obj:
       
    for line in file_obj:
        if "number of atomic types" in line:
            number_atoms=int(line.split()[5])
            
        elif "Dielectric constant in cartesian axis" in line:
            a=5
                                            
        elif "Effective charges (d Force / dE) in cartesian axis" in line:
            b=2+4*number_atoms
        
        else:
            a-=1
            b-=1
        
                
        if a>0 and a<4:
            if line.rstrip() in deleccons:
                pass
            else:
                deleccons.append(line.rstrip())
            
        if b>0 and b<(2+4*number_atoms):
            if line.rstrip() in effcharges:
                pass
            else:
                effcharges.append(line.rstrip())



#Escrevendo o arquivo BORN para leitura no Phonopy e Phono3py

f=open('BORN', 'a')
#Valor padrão para leitura como estilo PWSCF
f.write("2\n")

#Escrevendo as constantes dielétricas
for i in range(3):
    delec=deleccons[i].rstrip()
    #print(d.split())
    f.write(" %s %s %s " % (delec.split()[1],delec.split()[2],delec.split()[3]))

#Escrevendo as cargas efetivas
j=0
for i in range(1+4*number_atoms):
    if i==1+4*j:
        f.write("\n")
        #print(i ,"A")
        j+=1
    elif i>1 and j%3!=0:
        charges=effcharges[i].strip()
        #print(i, j, charges.split())
        #print(charges.split()[2], charges.split()[3], charges.split()[4])
        f.write(" %s %s %s " % (charges.split()[2], charges.split()[3], charges.split()[4]))
    
#Fechando o arquivo BORN
f.close()


