#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 09:41:19 2022

@author: tercio
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math


voluntarios = np.arange(1, 176)

n_suj = len(voluntarios)

time_for_stimulus = 500
n_tt = 48


stimulus_A = [1]
stimulus_B = [2]
correct_A = 0
correct_B = 1






# Variáveis
resp_corretas, n_corretas,n_erradas,n_antecipadas, n_omissas = np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj)
congruente, incogruente, n_congruente, n_incogruente =  np.zeros(n_suj), np.zeros(n_suj),np.zeros(n_suj), np.zeros(n_suj)
com_mudanca_cong, sem_mudanca_cong, com_mudanca_inc, sem_mudanca_inc =  np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj)


cont = 0




############ Corretas ###########

for suj in voluntarios:
    
    #set variables
   
    anticipatory = []
    missing = []
    correct_responses = []
    errada_responses = []
    index_cong = []
    index_unc = []
    

    for i in range (n_tt):
    
        df=pd.read_csv('dados/abstract_shapes_six/trials/SUJ'+str(suj)+'_trial'+str(i)+'.csv', sep=',',header=0)
        
        df = np.array(df)
    
        time = df[:,0]
        key_press = df[:,1]
        for k in range(len(key_press)-100):
            #Check response
            if key_press[k+100] == 0 or key_press[k+100] == 1: 
                rt = time[k+100]-time_for_stimulus
                #check antecipatory        
                if rt > 200:
                    #check correct
                    if df[0,2] == stimulus_A [0]:
                        if key_press[k+100] == correct_A:
                            correct_responses.append(rt)                       
                            
                        else:
                            errada_responses.append(rt)
                            
                    if df[0,2] == stimulus_B [0]:
                        if key_press[k+100] == correct_B:
                            correct_responses.append(rt)                       
                            
                        else:
                            errada_responses.append(rt)
                            
                    
                
                
                else:
                    anticipatory.append(rt)                        
                break 
       
            
        
    
    
    resp_corretas[cont] = np.mean(correct_responses)
    n_corretas[cont], n_erradas[cont], n_antecipadas[cont], n_omissas[cont] = len(correct_responses), len(errada_responses), len(anticipatory), n_tt-(len(errada_responses)+len(correct_responses)+len(anticipatory))
    
    
    cont +=1
    
nomes_coluna = ['resp_corretas','n_corretas', 'n_erradas', 'n_antecipadas', 'n_omissas']

np.savetxt('resultados/Abstract_two.csv', np.column_stack([resp_corretas,n_corretas, n_erradas, n_antecipadas, n_omissas] ), header = ','.join(nomes_coluna), delimiter=',')





'''    
 

######################    Plot graphic     ######################


fig, ax = plt.subplots()

labels = ['Corretas', 'Erradas','Antecipadas','Omissas']
counts = [len(correct_responses), len(errada_responses), len(anticipatory), n_tt -(len(errada_responses)+len(correct_responses)+len(anticipatory))]

bar_colors = ['k', 'r', 'b', 'g']

ax.bar(labels, counts, color=bar_colors)
ax.text(0, counts[0], str(format(counts[0],'.0f')), ha="center")
ax.text(1, counts[1], str(format(counts[1],'.0f')), ha="center")
ax.text(2, counts[2], str(format(counts[2],'.0f')), ha="center")
ax.text(3, counts[3], str(format(counts[3],'.0f')), ha="center")



plt.show()

######################

fig, ax = plt.subplots()

labels = ['Congruente', 'Incogruente']
counts = [np.mean(rt_Cong), np.mean(rt_Unc)]
bar_colors = ['m', 'y']

ax.bar(labels , counts, color=bar_colors)
ax.text(0, counts[0], str(format(counts[0],'.2f')), ha="center")
ax.text(1, counts[1], str(format(counts[1],'.2f')), ha="center")

plt.title("Tempo de resposta corretas")

plt.show()

###########################

fig, ax = plt.subplots()

labels = ['Congruente', 'Incogruente']
counts = [len(rt_Cong), len(rt_Unc)]

bar_colors = ['k', 'r', 'b', 'g']

ax.bar(labels, counts, color=bar_colors)
ax.text(0, counts[0], str(format(counts[0],'.0f')), ha="center")
ax.text(1, counts[1], str(format(counts[1],'.0f')), ha="center")


plt.title("N. acertos Corretas")

plt.show()


#####################3
fig, ax = plt.subplots()

labels = ['Congruente', 'Incogruente']
counts = [np.mean(rt_Cong_inc), np.mean(rt_Unc_inc)]
bar_colors = ['m', 'y']

ax.bar(labels , counts, color=bar_colors)
ax.text(0, counts[0], str(format(counts[0],'.2f')), ha="center")
ax.text(1, counts[1], str(format(counts[1],'.2f')), ha="center")

plt.title("Tempo de resposta incorretas")

plt.show()


########################
fig, ax = plt.subplots()

labels = ['Cong. mudança', 'Cong. sem', 'Inco. mudança', 'Inco. sem']
counts = [np.mean(switch_cost_cong), np.mean(no_switch_cost_cong), np.mean(switch_cost_unc), np.mean(no_switch_cost_unc)]
bar_colors = ['k', 'r', 'b', 'g']

ax.bar(labels , counts, color=bar_colors)
ax.text(0, counts[0], str(format(counts[0],'.2f')), ha="center")
ax.text(1, counts[1], str(format(counts[1],'.2f')), ha="center")
ax.text(2, counts[2], str(format(counts[2],'.2f')), ha="center")
ax.text(3, counts[3], str(format(counts[3],'.2f')), ha="center")

plt.title("Custo da mudança")

plt.show()


'''

