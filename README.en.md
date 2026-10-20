# Executive Functions Task Battery

🌐 [Ler em português](README.md)

A collection of computerized tasks (Python + Pygame) for assessing
executive functions: reaction time, inhibition, cognitive flexibility, and
Simon/flanker effects. Each task runs full-screen, records the
participant's responses and automatically scores the session at the end.
A menu with a **guided mode** walks through the session step by step for
people with little computer experience.

## Installation (Windows)

### 1. Download the program

1. On this GitHub page, click the green **Code** button, then
   **Download ZIP**.
2. Open the **Downloads** folder, right-click the `.zip` file and choose
   **Extract All...** → **Extract**.
   **Don't run the program from inside the `.zip`**: always use the
   extracted folder.

### 2. Install

1. Make sure the computer is connected to the internet.
2. In the program folder, open `Instalar_Win` and double-click
   **`instalacao.bat`**. (If Windows says "Windows protected your PC",
   click **More info** → **Run anyway**.)
3. Wait — the window shows the progress on its own, no clicking needed.
   When **"Instalação concluída com sucesso!"** appears, press any key:
   the program opens by itself.

This installs (if not already installed) Python 3.11 and the `numpy`,
`pygame`, `pandas` and `openpyxl` libraries, and creates the
**Bateria de Funções Executivas** icon on the desktop and in the Start
menu. From then on, just double-click that icon (or
`INICIAR_BATERIA.bat`, in the program folder).

If something goes wrong, the script shows a message in Portuguese
explaining the problem and how to retry — see also
`Instalar_Win/Passo_a_passo_intalacao_requisitos.txt`.

## Using the program

### Guided mode

The program opens in **guided mode**, made for people with little
computer experience: one thing per screen, large text and buttons, and
**Voltar** (Back) / **Continuar** (Continue) always in the same place.

1. **Participant** — type the participant code (only once for the whole
   session).

   ![Participant code](docs/img/guiado_participante.png)

2. **Choose the task** — one card per task/condition, with a picture from
   the task itself. Tasks already done in the session are marked
   **FEITA** (done).

   ![Choosing a task](docs/img/guiado_tarefas.png)

3. **Do the task** — the screen explains the task in plain words and has
   **Ver o vídeo** (instructions video), **Treinar** (a few practice
   trials that don't count) and **COMEÇAR A TAREFA** (start). On the task
   screen, Space starts and **Esc** stops.

   ![Before starting a task](docs/img/guiado_tarefa.png)

4. When it ends, the hits and errors are shown, with a button to go to the
   **next task** on the list.

   ![End of a task](docs/img/guiado_resultado.png)

5. **End the session** — all results go to **one spreadsheet** (`.xlsx`),
   saved wherever you choose: the **Sessão** sheet has one row per task
   (hits, errors, no response) and each task has its own sheet with the
   full summary. Closing the program without saving shows a warning.

   ![Saving the results](docs/img/guiado_fim.png)

The program also warns before redoing a task the participant has already
done (in this session or an earlier one), since the new data replaces the
old.

### Advanced mode

The **Modo avançado** button, at the top right, shows every task on one
screen. Each task opens its own **settings screen** (number of trials,
presentation time, interstimulus, etc.), pre-filled with the participant
code, and at the end asks where to save that task's summary CSV. The
**?** buttons open the instructions video. **Modo guiado** goes back to
the step-by-step mode.

![Advanced mode](docs/img/modo_avancado.png)

## Running a single task

Each task can also be opened without the menu: every task/variant lives
in its own folder under `Tarefas/`, with an **`Executable.bat`** file —
double-click it to open the task. The flow is the same as in advanced
mode:

1. **Settings screen** — fill in the subject code and the session
   parameters. Two buttons: **Começar** (Start) runs the data collection
   with those parameters, and **Familiarização** (Practice) runs a short
   practice block (no CSV saved) — when it ends, the settings screen comes
   back so you can click Começar.
2. **Instructions screen** — shows the stimulus → key mapping; the
   participant presses **Space** to start (Esc quits).
3. **Trials** — the task runs on its own to the end and closes
   automatically (Esc stops it).
4. **Results** — the task scores this subject's data and opens a window
   to choose where to save the summary CSV (correct, incorrect,
   anticipatory and omitted responses, response time, and — where
   applicable — congruency/switch costs).

## The tasks

| Task | Folders/variants |
|---|---|
| Arrows | (single folder) |
| Dots | `congruent`, `incongruent`, `mixed` |
| Abstract Shapes | `two_shapes`, `six_shapes` |
| Pictures | (single folder) |
| Flanker Test | `azul`, `rosa`, `mixed` |
| Go-No-Go | `tarefa_manual` |

### Arrows (`Tarefas/Arrows`)

An arrow appears on one side of the central cross, pointing straight down
or diagonally. The correct response depends on which side of the screen
the arrow appears on (Simon effect), with half the trials congruent and
half incongruent.

### Dots (`Tarefas/Dots`)

Circles of dots (striped or solid/gray) appear on the left or right. Rule:
**striped = same side, solid = opposite side**. Three conditions:
- **congruent** — striped stimuli only (rule is always "same side");
- **incongruent** — solid stimuli only (rule is always "opposite side");
- **mixed** — striped and solid interleaved, requiring the rule to switch
  from trial to trial.

### Abstract Shapes (`Tarefas/Abstract_Shapes`)

A two-alternative forced-choice task: an abstract shape appears on the
left or right side of the screen, and the participant responds with the
matching arrow key. Two variants: **two shapes** (one shape per side) and
**six shapes** (three distinct shapes per side), with pseudorandom
stimulus switches between trials. For this task, Familiarização runs 6
practice trials (instead of 4) when the "six shapes" variant is selected,
so every shape appears at least once during practice.

### Pictures — Simon effect (`Tarefas/Pictures`)

A frog or a butterfly appears on the left or right. Butterfly = left key;
frog = right key, regardless of which side the image appears on
(congruent when the image appears on the side that matches the correct
key).

### Flanker Test (`Tarefas/Flanker_Test`)

A fish flanker task: a row of 5 fish appears on screen, and the
participant responds to the direction the **center** fish points,
ignoring the surrounding ones (congruent when all fish point the same
way, incongruent when the center one diverges). Three conditions:
`azul` (blue only), `rosa` (pink only) and `mixed` (alternates between
both, trial by trial). There's an extra feedback screen (happy/sad face)
after each response, with a configurable duration on the settings screen
(can be set to zero).

### Go-No-Go (`Tarefas/Go-No-Go/tarefa_manual`)

An auditory task: the numbers 1 to 9 appear on screen and are played as
audio, and the participant presses **Space** only for the number 6 (go),
withholding responses to the others (no-go). The summary has hits on 6,
omissions, false alarms (pressed on a number other than 6), correct
rejections and the mean reaction time on 6; the trial-by-trial
spreadsheet is saved as `tarefa_manual/<code>_resultados.xlsx`.

## Where the data goes

Each task/variant writes its raw per-trial data to its own `trials/`
folder (`SUJ<code>_trial<N>.csv` files), along with that session's
stimulus sequence (`sequence.csv`) and the stimulus/response code legend
(`legend.txt`). Go-No-Go writes `<code>_resultados.xlsx` in the
`tarefa_manual` folder. The processed summary is saved wherever you
choose: one spreadsheet per session in guided mode, or one CSV per task
in advanced mode and when running a single task.

Participant data **is not pushed to GitHub**: `.gitignore` leaves out the
`trials/SUJ*.csv` files, `Arrows/sujeitos/` and the Go-No-Go results.
They stay only on the data-collection computer — back them up.

Batch analysis scripts (all subjects at once) live in `processar_dados/`.

## Contact

Tércio Apolinário-Souza — edf.tercio@gmail.com
