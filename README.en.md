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

4. When it ends, the % correct, reaction time, correct, incorrect,
   anticipatory and missing responses are shown, with a button to go to
   the **next task** on the list.

   ![End of a task](docs/img/guiado_resultado.png)

5. **End the session** — all results go to **one spreadsheet** (`.xlsx`),
   saved wherever you choose: the **Sessão** sheet has one row per task,
   the **Comparações** sheet combines measures from two tasks, and each
   task has its own sheet with the full summary (see "Results", below). Closing the program without saving shows a warning.

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
   applicable — congruency effect and switch costs; every column is
   explained in "Results", below).

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

A two-alternative forced-choice task: an abstract shape appears at the
**center** of the screen, and the participant responds with the arrow key
taught for that shape (left or right). Two variants: **two shapes** (one
per key) and **six shapes** (three per key), with pseudorandom
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

## Results: what each column means

The measures follow **Davidson, Amso, Anderson & Diamond (2006)**,
*Neuropsychologia*, 44, 2037–2078 (folder `referencias/`). The paper has
neither the Flanker Test nor Go-No-Go: Flanker uses the same measures as
the other tasks, and Go-No-Go has its own (see further below).

### How each trial is classified

Each trial has two screens: the **interstimulus** (just the rectangle and
cross, 500 ms by default) and the stimulus **presentation** (750 ms by
default). What counts is the **first key** (left or right arrow) pressed
after the stimulus appears:

| Classification | When | Counts for % correct? | Counts for RT? |
|---|---|:---:|:---:|
| **Correct** | The first key was the right one and came **more than 200 ms** after the stimulus | yes | yes |
| **Incorrect** | The first key was the wrong one and came more than 200 ms after the stimulus | yes | no |
| **Anticipatory** | The first key came **within 200 ms** of the stimulus, too fast to be a response to it. Includes a key still held down from the previous trial. | no | no |
| **Omission** | No key until the end of the trial | no | no |

**Reaction time (RT)** is counted from the moment the stimulus appears, in
milliseconds (ms). A response counts until the end of the trial: end of
the presentation + about 50 ms. In Flanker it also counts during the
feedback screen (happy/sad face).

Three measures appear for every group of trials:

- **% correct** = correct ÷ (correct + incorrect) × 100. As in Davidson,
  anticipatory responses and omissions are left out: if the participant
  left many trials unanswered, that shows in `n_omissas`, not in the %.
- **Median RT** = median RT of the **correct** responses. Davidson uses the
  median because it is less affected by one very slow response. The mean
  is also given (`tr_media`), for comparison with older data.
- **% anticipatory** = anticipatory ÷ all trials × 100. Indicates
  impulsivity, i.e. failing to wait for the stimulus.

### Terms used in the column names

**Congruent (`cong`) vs incongruent (`inc`)**: a congruent trial is one
whose correct response is **on the same side** where the stimulus
appears. An incongruent trial has it on the **opposite side**, so it
requires inhibiting the pull to respond on the stimulus side.

| Task | Congruent | Incongruent |
|---|---|---|
| Arrows | Arrow pointing straight down (respond on the same side) | Diagonal arrow (respond on the opposite side) |
| Dots | Striped circle (same side) | Gray circle (opposite side) |
| Pictures | Butterfly on the left or frog on the right | Butterfly on the right or frog on the left |
| Flanker | All 5 fish point the same way | The middle fish points the other way |
| Abstract Shapes | — (the shape appears at the center of the screen) | — |

**Nonswitch (`sem_troca`) vs switch (`com_troca`)**: each trial is
compared with the previous one, using the sequence that was shown
(whether or not the previous one was answered correctly). **Nonswitch** =
same type (congruent/incongruent) as the previous trial. **Switch** = the
type changed: in Arrows and Dots-Mixed this means **the rule changed**.
The first trial of the block has no previous trial and is left out of
these columns. `com_troca_cong` = switched **to** a congruent trial;
`com_troca_inc` = switched **to** an incongruent one.

**Same side (`mesmo_lado`) vs opposite side (`lado_oposto`)**: the correct
response of this trial is on the **same key** as the previous trial's, or
on the other key.

### Columns of each task's summary (Arrows, Dots, Abstract Shapes, Pictures, Flanker)

This is what appears in each task's sheet of the session spreadsheet
(guided mode) and in the CSV saved in advanced mode and when running a
single task. Times in ms, percentages from 0 to 100. An **empty cell**
(`nan` in the CSV) means there was no trial of that type, or no correct
response to compute the RT from.

**Identification**

| Column | Meaning |
|---|---|
| `cod_suj` | Participant code |
| `condicao` | Only Dots (`congruent`, `incongruent`, `mixed`) and Flanker (`azul`, `rosa`, `mixed`) |
| `n_formas` | Only Abstract Shapes: 2 or 6 |

**Overall (all trials of the block)**

| Column | Meaning |
|---|---|
| `n_tentativas` | Number of trials in the block |
| `n_corretas`, `n_erradas`, `n_antecipadas`, `n_omissas` | Number of correct / incorrect / anticipatory / omitted trials (they add up to `n_tentativas`) |
| `pct_corretas` | % correct |
| `pct_antecipadas` | % anticipatory |
| `tr_mediana` | Median RT of correct responses |
| `tr_media` | Mean RT of correct responses |

**Abstract Shapes** has only these columns, as in Davidson: the shape
appears at the center, so there are no congruent/incongruent trials. The
task measures **working memory**: with 6 shapes there are 6 rules to
remember instead of 2. Compare the two versions in the **Comparações**
sheet.

**By trial type** (Arrows, Dots, Pictures, Flanker)

| Column | Meaning |
|---|---|
| `n_tentativas_cong`, `n_tentativas_inc` | Number of congruent / incongruent trials |
| `pct_corretas_cong`, `pct_corretas_inc` | % correct for each type |
| `pct_antecipadas_cong`, `pct_antecipadas_inc` | % anticipatory for each type |
| `tr_mediana_cong`, `tr_mediana_inc` | Median RT for each type |
| `tr_media_cong`, `tr_media_inc` | Mean RT for each type |

**Congruency effect** (Simon / spatial incompatibility effect; in Flanker,
interference from the neighboring fish)

| Column | Formula | How to read it |
|---|---|---|
| `efeito_congruencia_pct` | `pct_corretas_cong` − `pct_corretas_inc` | Percentage points of accuracy lost on incongruent trials. **Larger = harder to inhibit** responding on the stimulus side. |
| `efeito_congruencia_tr` | `tr_mediana_inc` − `tr_mediana_cong` | How many ms slower on incongruent trials. Larger = higher inhibition cost. |
| `efeito_congruencia_tr_rel` | (`tr_mediana_inc` − `tr_mediana_cong`) ÷ `tr_mediana_cong` × 100 | The same effect as a % of the congruent RT. Useful to compare faster and slower people (Davidson, Fig. 3C). |

**Local context: rule switching** (Arrows, Dots, Pictures, Flanker)

Each group below has three columns: `n_tentativas_<group>`,
`pct_corretas_<group>` and `tr_mediana_<group>`.

| Group | Trials included |
|---|---|
| `sem_troca` | Same type as the previous trial |
| `com_troca` | Different type from the previous trial |
| `sem_troca_cong` / `sem_troca_inc` | Congruent after congruent / incongruent after incongruent |
| `com_troca_cong` / `com_troca_inc` | Congruent after incongruent / incongruent after congruent |
| `sem_troca_mesmo_lado` / `sem_troca_lado_oposto` | Nonswitch, with the correct response on the same key / the other key as the previous trial |
| `com_troca_mesmo_lado` / `com_troca_lado_oposto` | Switch, with the correct response on the same key / the other key |

| Column | Formula | How to read it |
|---|---|---|
| `custo_troca_local_pct` | `pct_corretas_sem_troca` − `pct_corretas_com_troca` | **Local switch cost** (Davidson, section 8) in accuracy. Larger = harder to switch rules (**cognitive flexibility**). |
| `custo_troca_local_tr` | `tr_mediana_com_troca` − `tr_mediana_sem_troca` | The same cost in ms. |

Other analyses Davidson runs with these groups:

- **Asymmetric switch cost** (section 14): compare `com_troca_cong` with
  `com_troca_inc`. In children aged 7–10, switching back to the dominant
  (congruent) response cost more accuracy.
- **Rule switch × response-side switch** (section 16): compare
  `com_troca_mesmo_lado` with `com_troca_lado_oposto`. Adults are more
  accurate and faster when the rule and the side change together.

Where these columns make sense:

- **Arrows and Dots-Mixed**: these are Davidson's analyses.
- **Pictures and Flanker**: the "type" also changes from trial to trial,
  but the rule doesn't. These are extra measures, not in the paper for
  these tasks.
- **Dots-Congruent and Dots-Incongruent**: all trials are of the same
  type. The other type's columns, the switch columns and the effects are
  empty. But `sem_troca_cong` (in the Congruent block) and `sem_troca_inc`
  (in the Incongruent block) are used for the global switch cost
  (Comparações sheet).

> **Mind the number of trials.** With 20 trials per block, some groups
> have only 2 or 3 trials, and a median of 2 values is very unstable.
> Before interpreting `pct_corretas_<group>` or `tr_mediana_<group>`,
> check `n_tentativas_<group>`.

### What each task measures (Davidson et al., 2006)

| Task | Mainly taxes | Main measures |
|---|---|---|
| Arrows | **Inhibition**, almost no memory (the arrow points to the correct key) | Overall, congruency effect, local switch cost |
| Dots-Congruent | **Memory** of one rule (no inhibition) | Overall |
| Dots-Incongruent | **Memory + inhibition** | Overall; compare with Dots-Congruent in the Comparações sheet |
| Dots-Mixed | **Memory + inhibition + flexibility** (rule switching) | Overall, congruency effect, local switch cost, global switch cost (Comparações sheet) |
| Abstract Shapes 2 vs 6 | **Working memory** (2 or 6 rules), almost no inhibition | Overall; 6 vs 2 percentage change in the Comparações sheet |
| Pictures | **Inhibition** (Simon effect), almost no memory | Overall, congruency effect |
| Flanker (not in the paper) | Selective attention / interference control | Overall, congruency effect |

### The session spreadsheet (guided mode)

**Salvar resultados** writes an `.xlsx` file with these sheets:

**`Sessão` sheet**: one row per task done, with the simplest summary:
participant, task, condition, time, `% de acerto` (% correct), `Tempo de
reação (ms)` (= `tr_mediana`), `Acertos` (correct), `Erros` (incorrect),
`Antecipadas` (anticipatory), `Sem resposta` (omissions). For Go-No-Go:
`Acertos no 6` (hits on 6), `Apertou sem ser 6` (false alarms), `Não
apertou no 6` (misses) and `Tempo de reação no 6 (ms)`.

**`Comparações` sheet**: measures that combine two tasks. Each row only
appears when both tasks were done in the session.

| Measure | Formula | How to read it |
|---|---|---|
| Global switch cost, Dots, congruent (% correct) | `pct_corretas_sem_troca_cong` of the Congruent block − the same in the Mixed block | **Global switch cost** or mixing cost (Davidson, section 12): the same kind of trial (congruent after congruent) gets worse just because it is in a block where the rules are mixed. Larger = more cost. |
| Global switch cost, Dots, congruent (median RT, ms) | `tr_mediana_sem_troca_cong` of the Mixed block − the same in the Congruent block | The same, in ms. |
| Global switch cost, Dots, incongruent (% and RT) | Same, with `sem_troca_inc` of the Incongruent and Mixed blocks | Same, for incongruent trials. |
| Dots Incongruent vs Congruent: change in % correct / in median RT (%) | (Incongruent − Congruent) ÷ Congruent × 100 | Cost of adding **inhibition** to the same rule (Davidson, Fig. 6). For accuracy, negative = lost accuracy; for RT, positive = got slower. |
| Dots Mixed vs Congruent: change in % correct / in median RT (%) | (Mixed − Congruent) ÷ Congruent × 100 | Cost of adding **rule switching** (Davidson, Fig. 6). |
| Abstract Shapes 6 vs 2 shapes: change in % correct / in median RT (%) | (6 shapes − 2 shapes) ÷ 2 shapes × 100 | **Memory** cost: remembering 6 rules instead of 2 (Davidson, Fig. 12). |

**One sheet per task** (`Arrows`, `Dots congruent`, `Dots incongruent`,
`Dots mixed`, `Abstract Shapes 2`, `Abstract Shapes 6`, `Pictures`,
`Flanker azul`, `Flanker rosa`, `Flanker mixed`, `Go-No-Go`): every
summary column, as described above.

Advanced mode and single tasks have no Comparações sheet: each task saves
its own CSV, and the comparisons can be computed with the formulas above.

### Go-No-Go

| Column | Meaning |
|---|---|
| `cod_suj` | Participant code |
| `n_tentativas` | Number of trials |
| `n_go` | How many times the 6 appeared (trials where the participant must press) |
| `acertos_go` | Pressed on 6 |
| `omissoes_go` | Did not press on 6 (inattention) |
| `falsos_alarmes` | Pressed on a number other than 6: **inhibition failure** |
| `rejeicoes_corretas` | Did not press on a number other than 6 (correct) |
| `tr_mediana_go`, `tr_medio_go` | Median and mean RT (ms) of hits on 6, counted from the start of the number |

The trial-by-trial spreadsheet (`tarefa_manual/<code>_resultados.xlsx`)
has: `Tentativa` (trial), `Número Apresentado` (number shown),
`Pressionou?` (Sim/Não = pressed yes/no), `Resultado` (`Acerto` = pressed
on 6; `Erro` = pressed on another number; `Erro!` = did not press on 6;
`Nenhuma resposta` = did not press on another number, which is correct)
and `Tempo de Reação` (in **seconds**).

### Raw trial files

`trials/SUJ<code>_trial<N>.csv` has one row per screen frame (about every
5 ms) and three columns:

- `Time`: ms since the start of the trial (real clock);
- `Key_press`: 0 = left arrow pressed, 1 = right arrow, −1 = none;
- `Stimulus`: the stimulus code, explained in `legend.txt` in the same folder.

`sequence.csv` has the stimulus order of the last session.

> **Data collected before 2026-10-20.** Until then the `Time` column was
> written as 0, 5, 10, 15… (assuming frames of exactly 5 ms). Frames are
> longer and vary, so RT came out **shorter than it really was**: in the
> test data we checked, the median RT was 28 to 78 ms too short. The
> script `processar_dados/corrigir_tempo_dados_antigos.py` rescales the
> time in those files and recomputes the summaries with the measures
> above. The originals are not changed. The correction is
> **approximate**, because it assumes every frame of a trial lasted the
> same. See the instructions at the top of the script. The
> `read_trials_*.py` scripts in the same folder still use the old
> calculation.

### Differences from Davidson's protocol

- **Practice:** the paper requires 75–80% correct in practice and that the
  participant can state the rule. Here practice can be repeated, but
  there is no automatic criterion.
- **Dots:** the paper counterbalances the rule (for half the participants
  gray means "same side"). Here striped is always same side.
- **Abstract Shapes:** the paper uses 2 blocks of 20 trials (40) per
  condition. The default here is 48.
- **Ages 4–6:** the paper uses 2500 ms presentation. Here that can only
  be set in advanced mode; guided mode uses 750 ms.
- **Pictures:** the paper sticks small butterfly and frog pictures on the
  buttons. Here the mapping is shown on the instructions screen.

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

Batch analysis scripts (all subjects at once) live in `processar_dados/`. For old data, use `corrigir_tempo_dados_antigos.py` (see "Raw trial
files", above). The `dados_corrigidos/` folder it creates is also kept
out of GitHub.

## Contact

Tércio Apolinário-Souza — edf.tercio@gmail.com
