"""Correção aproximada do tempo nos dados coletados antes de 20/10/2026.

Até essa data, as tarefas gravavam a coluna Time dos arquivos
trials/SUJ<código>_trial<N>.csv como 0, 5, 10, 15... (supondo que cada
quadro durava exatamente 5 ms), e não o tempo real. Os quadros na verdade
duram mais (5,8 ms em média, variando de tentativa para tentativa, no
computador onde medimos), então o tempo de reação calculado ficava menor
que o real.

O que este script faz, para cada tarefa/condição:
  1. Lê os arquivos de tentativa de cada participante.
  2. Se o arquivo é do formato antigo (Time sempre de 5 em 5), reescala o
     tempo para que a última linha caia na duração real conhecida da
     tentativa: interstímulo + apresentação (+ feedback no Flanker) + 51 ms.
     Isso supõe que os quadros tiveram a mesma duração ao longo da
     tentativa, por isso a correção é APROXIMADA. Arquivos já gravados com
     o tempo real são usados como estão.
  3. Grava os arquivos corrigidos em outra pasta (os originais não são
     alterados) e calcula o resumo de cada participante com a mesma
     pontuação das tarefas (medidas de Davidson et al., 2006; veja o README).
  4. Salva uma planilha com uma aba por tarefa/condição.

Os parâmetros (interstímulo, apresentação, feedback) não ficam gravados nos
arquivos de tentativa. Use os mesmos da coleta; se eles mudaram entre
participantes, rode o script separado para cada grupo (opção --participantes).

Uso (na pasta do programa):
    python processar_dados/corrigir_tempo_dados_antigos.py
    python processar_dados/corrigir_tempo_dados_antigos.py --apresentacao 2500 --participantes 3 7 12
    python processar_dados/corrigir_tempo_dados_antigos.py --tarefas "Dots mixed" Arrows --saida C:/dados_corrigidos
"""
import argparse
import importlib
import importlib.util
import os
import re
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")  # the Flanker scoring imports pygame settings

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "Tarefas"

# (name, task folder, trials folder, session fields, presentation ms, feedback ms)
VARIANTS = [
    ("Arrows", "Arrows", "Arrows/trials", {}, 750, 0),
    ("Dots congruent", "Dots", "Dots/congruent/trials", {"condition": "congruent"}, 750, 0),
    ("Dots incongruent", "Dots", "Dots/incongruent/trials", {"condition": "incongruent"}, 750, 0),
    ("Dots mixed", "Dots", "Dots/mixed/trials", {"condition": "mixed"}, 750, 0),
    ("Abstract Shapes 2", "Abstract_Shapes", "Abstract_Shapes/two_shapes/trials", {"n_shapes": 2}, 750, 0),
    ("Abstract Shapes 6", "Abstract_Shapes", "Abstract_Shapes/six_shapes/trials", {"n_shapes": 6}, 750, 0),
    ("Pictures", "Pictures", "Pictures/trials", {}, 750, 0),
    ("Flanker azul", "Flanker_Test", "Flanker_Test/azul/trials", {"condition": "azul"}, 2500, 1500),
    ("Flanker rosa", "Flanker_Test", "Flanker_Test/rosa/trials", {"condition": "rosa"}, 2500, 1500),
    ("Flanker mixed", "Flanker_Test", "Flanker_Test/mixed/trials", {"condition": "mixed"}, 2500, 1500),
]

TRIAL_FILE = re.compile(r"^SUJ(.+)_trial(\d+)\.csv$")


def load_results_module(task_folder):
    """The task's contents/results.py, loaded under its own package name
    (every task calls its package "contents")."""
    alias = f"tarefa_{task_folder.lower()}"
    if alias + ".results" in sys.modules:
        return sys.modules[alias + ".results"]
    contents = TASKS_DIR / task_folder / "contents"
    spec = importlib.util.spec_from_file_location(alias, contents / "__init__.py",
                                                  submodule_search_locations=[str(contents)])
    package = importlib.util.module_from_spec(spec)
    sys.modules[alias] = package
    spec.loader.exec_module(package)
    return importlib.import_module(alias + ".results")


def correct_file(source, target, trial_ms):
    """Copies one trial file, rescaling Time if it is in the old format.
    Returns True when it was rescaled."""
    data = np.loadtxt(source, delimiter=",", skiprows=1, ndmin=2)
    time = data[:, 0]
    old = len(time) > 1 and np.all(np.diff(time) == 5)
    if old:
        data[:, 0] = time * (trial_ms / time[-1])
        np.savetxt(target, data, header="Time,Key_press,Stimulus", delimiter=",")
    else:
        shutil.copyfile(source, target)
    return old


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--interestimulo", type=int, default=500, help="ms (padrão 500)")
    parser.add_argument("--apresentacao", type=int, default=None,
                        help="ms (padrão: 750; no Flanker, 2500)")
    parser.add_argument("--feedback", type=int, default=None, help="ms, só no Flanker (padrão 1500)")
    parser.add_argument("--tarefas", nargs="*", default=None, help="nomes como em VARIANTS (padrão: todas)")
    parser.add_argument("--participantes", nargs="*", default=None, help="códigos (padrão: todos)")
    parser.add_argument("--origem", default=str(TASKS_DIR), help="pasta Tarefas com os dados (padrão: a do programa)")
    parser.add_argument("--saida", default=str(ROOT / "dados_corrigidos"), help="pasta onde salvar (padrão: dados_corrigidos)")
    args = parser.parse_args()

    origin, output = Path(args.origem), Path(args.saida)
    sheets = {}
    for name, task_folder, trials_rel, fields, presentation, feedback in VARIANTS:
        if args.tarefas and name not in args.tarefas:
            continue
        source_dir = origin / trials_rel
        if not source_dir.exists():
            continue

        files = {}
        for f in source_dir.iterdir():
            m = TRIAL_FILE.match(f.name)
            if m:
                files.setdefault(m.group(1), {})[int(m.group(2))] = f
        subjects = [s for s in sorted(files) if not args.participantes or s in args.participantes]
        if not subjects:
            continue

        presentation = args.apresentacao if args.apresentacao is not None else presentation
        feedback = (args.feedback if args.feedback is not None else feedback) if feedback else 0
        trial_ms = args.interestimulo + presentation + feedback + 51
        results = load_results_module(task_folder)
        target_dir = output / trials_rel
        target_dir.mkdir(parents=True, exist_ok=True)

        rows = []
        for suj in subjects:
            n_trials = len(files[suj])
            if sorted(files[suj]) != list(range(n_trials)):
                print(f"  {name}, participante {suj}: faltam tentativas, pulando.")
                continue
            rescaled = [correct_file(files[suj][i], target_dir / files[suj][i].name, trial_ms)
                        for i in range(n_trials)]
            session = SimpleNamespace(suj=suj, n_trials=n_trials, interstimulus=args.interestimulo,
                                      trials_dir=target_dir, **fields)
            summary = results.summarize_subject(session)
            summary["tempo"] = "corrigido (aproximado)" if all(rescaled) else (
                "real" if not any(rescaled) else "misto")
            rows.append(summary)
        if rows:
            sheets[name] = pd.DataFrame(rows)
            print(f"{name}: {len(rows)} participante(s)")

    if not sheets:
        print("Nenhum arquivo de tentativa encontrado.")
        return
    output.mkdir(parents=True, exist_ok=True)
    path = output / "resumo_dados_corrigidos.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name, index=False)
    print(f"\nPlanilha salva em: {path}\nArquivos de tentativa corrigidos em: {output}")


if __name__ == "__main__":
    main()
