# Bateria de Testes de Funções Executivas

🌐 [Read this in English](README.en.md)

Coleção de tarefas computadorizadas (Python + Pygame) para avaliação de
funções executivas: tempo de reação, inibição, flexibilidade cognitiva e
efeito Simon/flanker. Cada tarefa roda em tela cheia, grava as respostas do
participante em CSV e (nas tarefas já modernizadas) processa e salva um
resumo automaticamente ao final.

## Instalação (Windows)

1. Verifique se o computador está conectado à internet.
2. Vá até a pasta `Instalar_Win` e dê dois cliques em **`instalacao.bat`**.
3. Aguarde — a janela mostra o andamento sozinha, não precisa clicar em
   nada. Quando aparecer **"Instalação concluída com sucesso!"**, aperte
   qualquer tecla para fechar.

Isso instala (se ainda não estiverem instalados): Python 3.11 e as
bibliotecas `numpy`, `pygame` e `pandas`.

Se algo der errado, o script mostra uma mensagem em português explicando o
problema e como tentar de novo — veja também
`Instalar_Win/Passo_a_passo_intalacao_requisitos.txt`.

> A tarefa `Go-No-Go/tarefa_podal` grava vídeo da webcam durante a coleta e
> depende também de `opencv-python` (`cv2`) — o instalador já cobre isso.

## Abrir o menu da bateria

A forma mais prática de rodar várias tarefas seguidas com o mesmo
participante é pelo **menu da bateria**: dê dois cliques em
`Tarefas/Battery/Executable.bat`. Aparece uma tela com um botão para cada
tarefa já modernizada, nesta ordem: Arrows, Dots, Abstract Shapes,
Pictures e Flanker Test; ao clicar em um botão, o menu se fecha e aquela tarefa abre
normalmente. Quando a tarefa termina (ou é fechada), o menu volta sozinho
para você escolher a próxima. Esc ou fechar a janela do menu encerra a
bateria.

Ao lado de cada botão de tarefa tem um botãozinho **"?"** — clique nele
para assistir, antes de abrir a tarefa, ao vídeo de instruções daquela
tarefa (os vídeos ficam em `instrucao/`). Ele abre no player de vídeo
padrão do computador, sem fechar o menu.

Go-No-Go ainda não aparece no menu — só entra quando passar pela mesma
modernização das outras cinco.

## Como rodar uma tarefa

Também é possível abrir cada tarefa avulsa, sem passar pelo menu: cada
tarefa/variante fica em sua própria pasta dentro de `Tarefas/`, com um
arquivo **`Executable.bat`** — dê dois cliques nele para abrir a tarefa.

Nas tarefas já modernizadas (veja tabela abaixo) o fluxo é:

1. **Tela de configuração** — preencha o código do sujeito e os parâmetros
   da sessão (número de tentativas, tempo de apresentação, interstímulo
   etc.). Há dois botões: **Começar**, que roda a coleta com esses
   parâmetros, e **Familiarização**, que roda só um bloco curto de 4
   tentativas de treino (sem salvar CSV) para o participante praticar
   antes da coleta valendo — ao terminar, a tela de configuração volta
   para você clicar em Começar.
2. **Tela de instruções** — mostra o mapeamento estímulo → tecla; o
   participante aperta a **barra de espaço** para iniciar.
3. **Tentativas** — a tarefa roda sozinha até o fim e fecha automaticamente.
4. **Resultados** — a tarefa processa os dados desse sujeito e abre uma
   janela para você escolher onde salvar o CSV com o resumo (acertos,
   erros, antecipações, omissões, tempo de resposta, e — quando aplicável —
   custo de congruência/mudança).

Nas tarefas que ainda não passaram por essa atualização, o código do
sujeito é definido editando `constants.py` (abra pelo atalho
`abrir_arquivo_constants.bat` da pasta) antes de clicar em
`Executable.bat`.

## As tarefas

| Tarefa | Pastas/variantes | Front end novo? |
|---|---|:---:|
| Arrows | (pasta única) | ✅ |
| Dots | `congruent`, `incongruent`, `mixed` | ✅ |
| Abstract Shapes | `two_shapes`, `six_shapes` | ✅ |
| Pictures | (pasta única) | ✅ |
| Flanker Test | `azul`, `rosa`, `mixed` | ✅ |
| Go-No-Go | `tarefa_manual`, `tarefa_podal` | ⏳ ainda não |

### Arrows (`Tarefas/Arrows`)

Uma seta aparece de um dos lados da cruz central, apontando para baixo em
linha reta ou na diagonal. A resposta correta depende do lado da tela em
que a seta aparece (efeito Simon), com metade das tentativas congruentes e
metade incongruentes.

### Dots (`Tarefas/Dots`)

Círculos de pontos (listrados ou sólidos/cinza) aparecem à esquerda ou à
direita. Regra: **listrado = mesmo lado, sólido = lado oposto**. Três
condições:
- **congruent** — só estímulos listrados (regra sempre "mesmo lado");
- **incongruent** — só estímulos sólidos (regra sempre "lado oposto");
- **mixed** — listrado e sólido intercalados, exigindo alternar a regra a
  cada tentativa.

### Abstract Shapes (`Tarefas/Abstract_Shapes`)

Tarefa de escolha forçada de duas alternativas: uma forma abstrata aparece
à esquerda ou à direita da tela e o participante responde com a tecla
correspondente (seta esquerda/direita). Existem duas variantes: **2
formas** (uma forma por lado) e **6 formas** (três formas distintas por
lado), com trocas pseudoaleatórias de estímulo entre tentativas. Nesta
tarefa, a Familiarização roda 6 tentativas (em vez de 4) quando a variante
"6 formas" está selecionada, para garantir que toda forma apareça ao menos
uma vez no treino.

### Pictures — efeito Simon (`Tarefas/Pictures`)

Um sapo ou uma borboleta aparece à esquerda ou à direita. Borboleta = tecla
esquerda; sapo = tecla direita, independente do lado em que a imagem
aparece (congruente quando a imagem aparece do lado que "combina" com a
tecla certa).

### Flanker Test (`Tarefas/Flanker_Test`)

Tarefa de flanker com peixinhos: uma fileira de 5 peixes aparece na tela e
o participante responde à direção para onde aponta o peixe **central**,
ignorando os peixes ao redor (congruentes quando todos apontam para o
mesmo lado, incongruentes quando o central diverge). Três condições:
`azul` (só a versão azul), `rosa` (só a versão rosa) e `mixed` (mistura
as duas, alternando entre elas de tentativa em tentativa). Tem uma tela
extra de feedback (rosto feliz/triste) depois de cada resposta, com
duração configurável na tela de configuração (pode zerar).

### Go-No-Go (`Tarefas/Go-No-Go`)

Tarefa auditiva: números de 1 a 9 são reproduzidos em áudio e o
participante deve responder somente ao ouvir o número 6 (go), inibindo a
resposta para os demais (no-go). `tarefa_manual` usa a barra de espaço;
`tarefa_podal` usa resposta podal e grava vídeo da execução pela webcam.

## Onde ficam os dados

Cada tarefa/variante grava os dados brutos por tentativa em sua própria
pasta `trials/` (arquivos `SUJ<código>_trial<N>.csv`), junto com a
sequência de estímulos da sessão (`sequence.csv`) e a legenda dos códigos
de estímulo/resposta (`legend.txt`). O resumo processado de cada sujeito
(nas tarefas com o front end novo) é salvo onde você escolher, no momento
em que a caixa de diálogo "Salvar dados processados" aparecer.

Scripts de análise em lote (todos os sujeitos de uma vez) ficam em
`processar_dados/`.

## Contato

Tércio Apolinário-Souza — edf.tercio@gmail.com
