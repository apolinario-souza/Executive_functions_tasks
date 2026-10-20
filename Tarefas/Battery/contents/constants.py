from collections import namedtuple
from pathlib import Path

# Tarefas/ (this launcher's parent folder) — each task lives in its own
# sibling folder there, with its own main.py handling settings/instructions/
# trials/results on its own.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INSTRUCTIONS_DIR = BASE_DIR.parent / "instrucao"
ICON_FILE = BASE_DIR / "Battery" / "icone.ico"

TITLE = "Bateria de Funções Executivas"
FOOTER_TEXT = "Desenvolvido por Tércio Apolinário-Souza — edf.tercio@gmail.com"

# One entry per task/variant the experimenter can run:
#   key       — unique id (also the sheet name in the results spreadsheet)
#   name      — task name (kept in English, as in the papers)
#   variant   — condition shown under the name, or None
#   main      — that task's main.py
#   args      — extra arguments that pick the variant
#   icon      — image(s) from the task's img/ folder for the menu card, or
#               "text:<chars>" when the task has no picture
#   video     — instructions video (instrucao/), or None
#   rule      — how the task works, in plain words, for the guided mode
Task = namedtuple("Task", "key name variant main args icon video rule")

ARROWS_RULE = ("Uma seta aparece ao lado da cruz, apontando para baixo (reta ou na diagonal). "
               "O participante aperta a tecla de seta (esquerda ou direita) do lado para onde a seta aponta.")
DOTS_RULE = ("Um círculo aparece à esquerda ou à direita da tela. "
             "Círculo listrado: apertar a tecla de seta do MESMO lado. "
             "Círculo cinza: apertar a tecla de seta do lado OPOSTO.")
ABSTRACT_RULE = ("Uma forma aparece na tela. Cada forma tem a sua tecla de seta (esquerda ou direita), "
                 "como mostra a tela de instruções antes de começar.")
PICTURES_RULE = ("Um sapo ou uma borboleta aparece à esquerda ou à direita. "
                 "Borboleta: tecla de seta para a esquerda. Sapo: tecla de seta para a direita. "
                 "Não importa o lado em que a figura aparece.")
FLANKER_RULE = ("Aparece uma fileira de 5 peixes. O participante aperta a tecla de seta (esquerda ou direita) "
                "para onde aponta o peixe do MEIO, sem ligar para os outros. "
                "Depois de cada resposta aparece um rosto feliz ou triste.")
GONOGO_RULE = ("Números de 1 a 9 aparecem na tela e são falados em voz alta (ligue o som do computador). "
               "O participante aperta a BARRA DE ESPAÇO só quando for o número 6. "
               "Nos outros números, não aperta nada.")

TASKS = [
    Task("Arrows", "Arrows", None, BASE_DIR / "Arrows" / "main.py", [],
         [BASE_DIR / "Arrows" / "img" / "downRight.png"], INSTRUCTIONS_DIR / "Arrows.mp4", ARROWS_RULE),
    Task("Dots congruent", "Dots", "Congruente", BASE_DIR / "Dots" / "main.py", ["--condition", "congruent"],
         [BASE_DIR / "Dots" / "congruent" / "img" / "dots_stripes.png"], INSTRUCTIONS_DIR / "Dots.mp4",
         DOTS_RULE + " Nesta condição só aparecem círculos listrados."),
    Task("Dots incongruent", "Dots", "Incongruente", BASE_DIR / "Dots" / "main.py", ["--condition", "incongruent"],
         [BASE_DIR / "Dots" / "incongruent" / "img" / "dots_solid.png"], INSTRUCTIONS_DIR / "Dots.mp4",
         DOTS_RULE + " Nesta condição só aparecem círculos cinzas."),
    Task("Dots mixed", "Dots", "Mista", BASE_DIR / "Dots" / "main.py", ["--condition", "mixed"],
         [BASE_DIR / "Dots" / "mixed" / "img" / "dots_stripes.png",
          BASE_DIR / "Dots" / "mixed" / "img" / "dots_solid.png"], INSTRUCTIONS_DIR / "Dots.mp4",
         DOTS_RULE + " Nesta condição os dois tipos de círculo se misturam."),
    Task("Abstract Shapes 2", "Abstract Shapes", "2 formas", BASE_DIR / "Abstract_Shapes" / "main.py",
         ["--variant", "2"], [BASE_DIR / "Abstract_Shapes" / "two_shapes" / "img" / "left1.png"],
         INSTRUCTIONS_DIR / "Abstract_2.mp4", ABSTRACT_RULE),
    Task("Abstract Shapes 6", "Abstract Shapes", "6 formas", BASE_DIR / "Abstract_Shapes" / "main.py",
         ["--variant", "6"], [BASE_DIR / "Abstract_Shapes" / "six_shapes" / "img" / "left2.png"],
         INSTRUCTIONS_DIR / "Abstract_6.mp4", ABSTRACT_RULE),
    Task("Pictures", "Pictures", None, BASE_DIR / "Pictures" / "main.py", [],
         [BASE_DIR / "Pictures" / "img" / "frog.png"], INSTRUCTIONS_DIR / "Pictures.mp4", PICTURES_RULE),
    Task("Flanker azul", "Flanker Test", "Azul", BASE_DIR / "Flanker_Test" / "main.py", ["--condition", "azul"],
         [BASE_DIR / "Flanker_Test" / "azul" / "img" / "azulD.jpg"], INSTRUCTIONS_DIR / "Flaker_azul.mp4",
         FLANKER_RULE),
    Task("Flanker rosa", "Flanker Test", "Rosa", BASE_DIR / "Flanker_Test" / "main.py", ["--condition", "rosa"],
         [BASE_DIR / "Flanker_Test" / "rosa" / "img" / "rosaD.jpg"], INSTRUCTIONS_DIR / "Flaker_rosa.mp4",
         FLANKER_RULE),
    Task("Flanker mixed", "Flanker Test", "Misto", BASE_DIR / "Flanker_Test" / "main.py", ["--condition", "mixed"],
         [BASE_DIR / "Flanker_Test" / "azul" / "img" / "azulD.jpg",
          BASE_DIR / "Flanker_Test" / "rosa" / "img" / "rosaD.jpg"], INSTRUCTIONS_DIR / "gerais_flaker.mp4",
         FLANKER_RULE + " Nesta condição os peixes azuis e rosas se misturam."),
    Task("Go-No-Go", "Go-No-Go", None, BASE_DIR / "Go-No-Go" / "tarefa_manual" / "main.py", [],
         "text:6", None, GONOGO_RULE),
]

# Raw data file each task writes for a participant ({suj} = code), used
# to warn before a new run replaces data from an earlier session
RAW_FILES = {
    "Arrows": BASE_DIR / "Arrows" / "trials" / "SUJ{suj}_trial0.csv",
    "Dots congruent": BASE_DIR / "Dots" / "congruent" / "trials" / "SUJ{suj}_trial0.csv",
    "Dots incongruent": BASE_DIR / "Dots" / "incongruent" / "trials" / "SUJ{suj}_trial0.csv",
    "Dots mixed": BASE_DIR / "Dots" / "mixed" / "trials" / "SUJ{suj}_trial0.csv",
    "Abstract Shapes 2": BASE_DIR / "Abstract_Shapes" / "two_shapes" / "trials" / "SUJ{suj}_trial0.csv",
    "Abstract Shapes 6": BASE_DIR / "Abstract_Shapes" / "six_shapes" / "trials" / "SUJ{suj}_trial0.csv",
    "Pictures": BASE_DIR / "Pictures" / "trials" / "SUJ{suj}_trial0.csv",
    "Flanker azul": BASE_DIR / "Flanker_Test" / "azul" / "trials" / "SUJ{suj}_trial0.csv",
    "Flanker rosa": BASE_DIR / "Flanker_Test" / "rosa" / "trials" / "SUJ{suj}_trial0.csv",
    "Flanker mixed": BASE_DIR / "Flanker_Test" / "mixed" / "trials" / "SUJ{suj}_trial0.csv",
    "Go-No-Go": BASE_DIR / "Go-No-Go" / "tarefa_manual" / "{suj}_resultados.xlsx",
}

# Result columns worth showing right after a task, with friendly names
RESULT_NAMES = {
    "pct_corretas": "% de acerto",
    "tr_mediana": "Tempo de reação (ms)",
    "n_corretas": "Acertos",
    "n_erradas": "Erros",
    "n_antecipadas": "Antecipadas",
    "n_omissas": "Sem resposta",
    "acertos_go": "Acertos no 6",
    "falsos_alarmes": "Apertou sem ser 6",
    "omissoes_go": "Não apertou no 6",
    "tr_mediana_go": "Tempo de reação no 6 (ms)",
}

# Colors (same dark look as the tasks)
BG = "#000000"
PANEL = "#141414"
FG = "#ffffff"
MUTED = "#b4b4b4"
FOOTER = "#6e6e6e"
ACCENT = "#2f6fd6"
OK = "#4caf50"
WARN = "#e6a23c"
ERROR = "#e65a5a"
GREY = "#333333"
