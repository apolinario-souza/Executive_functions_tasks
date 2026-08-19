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

voluntarios = np.concatenate((np.arange(1, 159), np.arange(160, 500), np.arange(550, 582)))

n_suj = len(voluntarios)


time_for_stimulus = 500
n_tt = 20



stimulus_A = [2, 3]
stimulus_B = [1, 4]
correct_A = 1
correct_B = 0
condition_cong = [1,3]






# Variáveis
resp_corretas, n_corretas,n_erradas,n_antecipadas, n_omissas = np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj)
congruente, incogruente, n_congruente, n_incogruente =  np.zeros(n_suj), np.zeros(n_suj),np.zeros(n_suj), np.zeros(n_suj)
com_mudanca_cong, sem_mudanca_cong, com_mudanca_inc, sem_mudanca_inc =  np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj), np.zeros(n_suj)


cont = 0




############ Corretas ###########

for suj in voluntarios:
    
    #set variables
    rt_Cong = []
    rt_Unc = []
    rt_Cong_inc = []
    rt_Unc_inc = []
    anticipatory = []
    missing = []
    correct_responses = []
    errada_responses = []
    index_cong = []
    index_unc = []
    

    for i in range (n_tt):
        
        
        df=pd.read_csv('dados/arrows/trials/SUJ'+str(suj)+'_trial'+str(i)+'.csv', sep=',',header=0)
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
                    if df[0,2] == stimulus_A [0] or df[0,2] == stimulus_A [1]:
                        if key_press[k+100] == correct_A:
                            correct_responses.append(rt)
                            #split into congruent and uncogrunet correct response
                            if df[0,2] == condition_cong [0] or df[0,2] == condition_cong [1]:
                                index_cong.append(i)
                                
                                for k in range(len(key_press)-100):
                                    if key_press[k+100] == 0 or key_press[k+100] == 1:
                                        rt_Cong.append(time[k+100]-time_for_stimulus)
                                        break            
                            else: 
                                index_unc.append(i)
                                for k in range(len(key_press)-100):
                                    if key_press[k+100] == 0 or key_press[k+100] == 1:
                                        rt_Unc.append(time[k+100]-time_for_stimulus)
                                        break
                            
                        else:
                            errada_responses.append(rt)
                            #split into congruent and uncogrunet incorrect response
                            
                            if df[0,2] == condition_cong [0] or df[0,2] == condition_cong [1]: 
                                
                                for k in range(len(key_press)-100):
                                    if key_press[k+100] == 0 or key_press[k+100] == 1:
                                        rt_Cong_inc.append(time[k+100]-time_for_stimulus)
                                        break            
                            else: 
                                
                                for k in range(len(key_press)-100):
                                    if key_press[k+100] == 0 or key_press[k+100] == 1:
                                        rt_Unc_inc.append(time[k+100]-time_for_stimulus)
                                        break
                    #check correct        
                    if df[0,2] == stimulus_B [0] or df[0,2] == stimulus_B [1]:
                        if key_press[k+100] == correct_B:
                            correct_responses.append(rt)
                            #split into congruent and uncogrunet
                            if df[0,2] == condition_cong [0] or df[0,2] == condition_cong [1]:
                                index_cong.append(i)                            
                                for k in range(len(key_press)-100):
                                    if key_press[k+100] == 0 or key_press[k+100] == 1:
                                        rt_Cong.append(time[k+100]-time_for_stimulus)
                                        break            
                            else: 
                                index_unc.append(i)
                                for k in range(len(key_press)-100):
                                    if key_press[k+100] == 0 or key_press[k+100] == 1:
                                        rt_Unc.append(time[k+100]-time_for_stimulus)
                                        break
                            
                        else:
                            errada_responses.append(rt)
                            #split into congruent and uncogrunet incorrect response
                            
                            if df[0,2] == condition_cong [0] or df[0,2] == condition_cong [1]: 
                                
                                for k in range(len(key_press)-100):
                                    if key_press[k+100] == 0 or key_press[k+100] == 1:
                                        rt_Cong_inc.append(time[k+100]-time_for_stimulus)
                                        break            
                            else: 
                                
                                for k in range(len(key_press)-100):
                                    if key_press[k+100] == 0 or key_press[k+100] == 1:
                                        rt_Unc_inc.append(time[k+100]-time_for_stimulus)
                                        break
                           
                            
                    
                
                
                else:
                    anticipatory.append(rt)                        
                break
            
       
    
    
    
    switch_cost_unc = []
    no_switch_cost_unc = []
    
    for i in range (len(index_unc)-1):
        if abs(index_unc[i]-index_unc[i+1]) == 1:
            no_switch_cost_unc.append(rt_Unc[i+1])
        else:
            switch_cost_unc.append(rt_Unc[i+1])
            
            
    switch_cost_cong = []
    no_switch_cost_cong = []
    
    for i in range (len(index_cong)-1):
        if abs(index_cong[i]-index_cong[i+1]) == 1:
            no_switch_cost_cong.append(rt_Cong[i+1])
        else:
            switch_cost_cong.append(rt_Cong[i+1])    
       
            
        
    
    
    resp_corretas[cont] = np.mean(correct_responses)
    n_corretas[cont], n_erradas[cont], n_antecipadas[cont], n_omissas[cont] = len(correct_responses), len(errada_responses), len(anticipatory), n_tt-(len(errada_responses)+len(correct_responses)+len(anticipatory))
    
    congruente[cont], incogruente[cont]  = np.mean(rt_Cong), np.mean(rt_Unc)
    n_congruente[cont], n_incogruente[cont]  = len(rt_Cong), len(rt_Unc)
    
    com_mudanca_cong[cont], sem_mudanca_cong[cont], com_mudanca_inc[cont], sem_mudanca_inc[cont] = np.mean(switch_cost_cong), np.mean(no_switch_cost_cong), np.mean(switch_cost_unc), np.mean(no_switch_cost_unc)
    cont +=1
    
nomes_coluna = ['cod_suj','resp_corretas','n_corretas', 'n_erradas', 'n_antecipadas', 'n_omissas','congruente', 'incogruente','n_congruente', 'n_incogruente','com_mudanca_cong', 'sem_mudanca_cong', 'com_mudanca_inc', 'sem_mudanca_inc']

np.savetxt('resultados/Arrows.csv', np.column_stack([voluntarios, resp_corretas,n_corretas, n_erradas, n_antecipadas, n_omissas,congruente, incogruente,n_congruente, n_incogruente,com_mudanca_cong, sem_mudanca_cong, com_mudanca_inc, sem_mudanca_inc ] ), header = ','.join(nomes_coluna), delimiter=',')





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

