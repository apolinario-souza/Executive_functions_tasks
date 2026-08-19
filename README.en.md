# Executive Functions Task Battery

🌐 [Ler em português](README.md)

A collection of computerized tasks (Python + Pygame) for assessing
executive functions: reaction time, inhibition, cognitive flexibility, and
Simon/flanker effects. Each task runs full-screen, records the
participant's responses to CSV, and — for the tasks already modernized —
automatically scores the session and lets you save a summary at the end.

## Installation (Windows)

1. Make sure the computer is connected to the internet.
2. Go to the `Instalar_Win` folder and double-click **`instalacao.bat`**.
3. Wait — the window shows progress on its own, no clicking needed. When
   you see **"Instalacao concluida com sucesso!"**, press any key to close
   it.

This installs (if not already present): Python 3.11 and the `numpy`,
`pygame`, and `pandas` libraries. Messages are in Portuguese (the target
audience for this installer), but the flow is fully automatic.

If something goes wrong, the script prints a plain-language message
explaining the problem and how to retry — see also
`Instalar_Win/Passo_a_passo_intalacao_requisitos.txt`.

> `Go-No-Go/tarefa_podal` records webcam video during data collection and
> also depends on `opencv-python` (`cv2`) — the installer already covers
> this.

## Opening the battery menu

The easiest way to run several tasks in a row with the same participant is
the **battery menu**: double-click `Tarefas/Battery/Executable.bat`. It
shows one button per already-modernized task (Abstract Shapes, Arrows,
Dots, Pictures); clicking a button closes the menu and opens that task
normally. Once the task finishes (or is closed), the menu comes back on
its own so you can pick the next one. Esc, or closing the menu window,
ends the battery session.

Next to each task button there's a small **"?"** button — click it to
watch that task's instructions video before opening it (videos live in
`instrucao/`). It opens in the computer's default video player without
closing the menu.

Flanker Test and Go-No-Go aren't in the menu yet — they'll be added once
they go through the same modernization as the other four.

## Running a task

Each task can also be opened on its own, without going through the menu:
every task/variant lives in its own folder under `Tarefas/`, with an
**`Executable.bat`** file — double-click it to open the task.

For the already-modernized tasks (see table below), the flow is:

1. **Settings screen** — fill in the subject code and session parameters
   (number of trials, presentation time, interstimulus interval, etc.) and
   click **Começar** (Start).
2. **Instructions screen** — shows the stimulus → key mapping; the
   participant presses **spacebar** to begin.
3. **Trials** — the task runs on its own until the end and then closes
   automatically.
4. **Results** — the task scores that subject's data and opens a "Save
   As" window so you can choose where to save the processed summary CSV
   (correct/incorrect/anticipatory/omitted counts, response time, and —
   where applicable — congruency/switch-cost breakdowns).

For tasks that haven't gone through this update yet, the subject code is
set by editing `constants.py` (open it via the folder's
`abrir_arquivo_constants.bat` shortcut) before double-clicking
`Executable.bat`.

## The tasks

| Task | Folders/variants | New front end? |
|---|---|:---:|
| Abstract Shapes | `two_shapes`, `six_shapes` | ✅ |
| Arrows | (single folder) | ✅ |
| Dots | `congruent`, `incongruent`, `mixed` | ✅ |
| Pictures | (single folder) | ✅ |
| Flanker Test | `Tarefa_1`, `Tarefa_2`, `Tarefa_3` | ⏳ not yet |
| Go-No-Go | `tarefa_manual`, `tarefa_podal` | ⏳ not yet |

### Abstract Shapes (`Tarefas/Abstract_Shapes`)

A two-alternative forced-choice task: an abstract shape appears on the
left or right side of the screen, and the participant responds with the
matching arrow key. Two variants: **two shapes** (one shape per side) and
**six shapes** (three distinct shapes per side), with pseudorandom
stimulus switches between trials.

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

### Pictures — Simon effect (`Tarefas/Pictures`)

A frog or a butterfly appears on the left or right. Butterfly = left key;
frog = right key, regardless of which side the image appears on
(congruent when the image appears on the side that matches the correct
key).

### Flanker Test (`Tarefas/Flanker_Test`)

A fish flanker task: a row of 5 fish appears on screen, and the
participant responds to the direction the **center** fish points,
ignoring the surrounding ones (congruent when all fish point the same
way, incongruent when the center one diverges). `Tarefa_1` is the blue
version, `Tarefa_2` the pink version, `Tarefa_3` mixes both.

### Go-No-Go (`Tarefas/Go-No-Go`)

An auditory task: numbers 1 through 9 are played as audio, and the
participant should only respond when hearing the number 6 (go), inhibiting
the response for every other number (no-go). `tarefa_manual` uses the
spacebar; `tarefa_podal` uses a foot response and records the session on
webcam.

## Where the data goes

Each task/variant writes raw per-trial data to its own `trials/` folder
(`SUJ<code>_trial<N>.csv` files), along with the session's stimulus
sequence (`sequence.csv`) and the stimulus/response code legend
(`legend.txt`). Each subject's processed summary (for the tasks with the
new front end) is saved wherever you choose, when the "Save processed
data" dialog appears.

Batch analysis scripts (processing all subjects at once) live in
`processar_dados/`.

## Contact

Tércio Apolinário-Souza — edf.tercio@gmail.com
