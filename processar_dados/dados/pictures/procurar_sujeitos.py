#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 14:59:53 2025

@author: tercio
"""

import os

# Defina o caminho da pasta onde estão os arquivos
pasta = 'trials/'  # Substitua pelo caminho real

# Gere a lista esperada de arquivos
sujeitos_esperados = [f'SUJ{n}_trial0.csv' for n in range(1, 582)]

# Liste os arquivos realmente presentes na pasta
arquivos_presentes = os.listdir(pasta)

# Filtrar apenas os arquivos que seguem o padrão
arquivos_presentes = [f for f in arquivos_presentes if f.endswith('_trial0.csv')]

# Obtenha os nomes esperados que estão faltando
faltando = sorted(set(sujeitos_esperados) - set(arquivos_presentes))

# Mostre os números dos sujeitos ausentes
sujeitos_faltando = [int(f.split('_')[0][3:]) for f in faltando]

print(f"Sujeitos ausentes ({len(sujeitos_faltando)}):", sujeitos_faltando)