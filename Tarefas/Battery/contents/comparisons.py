"""Measures that need more than one task of the session, following
Davidson et al. (2006): the global (mixing) switch cost of Dots and the
percentage change between conditions (Dots, Abstract Shapes). They go to
the "Comparações" sheet of the session spreadsheet; the README explains
each row."""

NAN = float("nan")


def _get(results, key, column):
    if key not in results:
        return None
    value = results[key][2].get(column)
    return None if value is None or value != value else value  # NaN = not available


def _diff(a, b):
    return None if a is None or b is None else round(a - b, 1)


def _pct_change(new, base):
    return None if new is None or not base else round(100 * (new - base) / base, 1)


# (measure, task key A, column of A, task key B, column of B, how: "diff" = A − B,
#  "change" = (A − B) / B × 100, explanation)
ROWS = [
    ("Custo global de troca, Dots, congruentes (% de acerto)",
     "Dots congruent", "pct_corretas_sem_troca_cong", "Dots mixed", "pct_corretas_sem_troca_cong", "diff",
     "% de acerto nas congruentes que vêm depois de outra congruente: bloco Congruente menos bloco Misto. "
     "Positivo = errou mais quando as regras estavam misturadas."),
    ("Custo global de troca, Dots, congruentes (TR mediano, ms)",
     "Dots mixed", "tr_mediana_sem_troca_cong", "Dots congruent", "tr_mediana_sem_troca_cong", "diff",
     "TR mediano nas congruentes que vêm depois de outra congruente: bloco Misto menos bloco Congruente. "
     "Positivo = ficou mais lento quando as regras estavam misturadas."),
    ("Custo global de troca, Dots, incongruentes (% de acerto)",
     "Dots incongruent", "pct_corretas_sem_troca_inc", "Dots mixed", "pct_corretas_sem_troca_inc", "diff",
     "% de acerto nas incongruentes que vêm depois de outra incongruente: bloco Incongruente menos bloco Misto."),
    ("Custo global de troca, Dots, incongruentes (TR mediano, ms)",
     "Dots mixed", "tr_mediana_sem_troca_inc", "Dots incongruent", "tr_mediana_sem_troca_inc", "diff",
     "TR mediano nas incongruentes que vêm depois de outra incongruente: bloco Misto menos bloco Incongruente."),
    ("Dots Incongruente × Congruente: mudança no % de acerto (%)",
     "Dots incongruent", "pct_corretas", "Dots congruent", "pct_corretas", "change",
     "(acerto Incongruente − acerto Congruente) ÷ acerto Congruente × 100. Negativo = perdeu acerto."),
    ("Dots Incongruente × Congruente: mudança no TR mediano (%)",
     "Dots incongruent", "tr_mediana", "Dots congruent", "tr_mediana", "change",
     "(TR Incongruente − TR Congruente) ÷ TR Congruente × 100. Positivo = ficou mais lento."),
    ("Dots Misto × Congruente: mudança no % de acerto (%)",
     "Dots mixed", "pct_corretas", "Dots congruent", "pct_corretas", "change",
     "(acerto Misto − acerto Congruente) ÷ acerto Congruente × 100."),
    ("Dots Misto × Congruente: mudança no TR mediano (%)",
     "Dots mixed", "tr_mediana", "Dots congruent", "tr_mediana", "change",
     "(TR Misto − TR Congruente) ÷ TR Congruente × 100."),
    ("Abstract Shapes 6 × 2 formas: mudança no % de acerto (%)",
     "Abstract Shapes 6", "pct_corretas", "Abstract Shapes 2", "pct_corretas", "change",
     "(acerto 6 formas − acerto 2 formas) ÷ acerto 2 formas × 100. Mede o custo de lembrar 6 regras."),
    ("Abstract Shapes 6 × 2 formas: mudança no TR mediano (%)",
     "Abstract Shapes 6", "tr_mediana", "Abstract Shapes 2", "tr_mediana", "change",
     "(TR 6 formas − TR 2 formas) ÷ TR 2 formas × 100."),
]


def comparisons(results):
    """Rows (measure, value, explanation) for every comparison whose two
    tasks were done in this session (results: task key -> (task, time,
    summary))."""
    rows = []
    for name, key_a, col_a, key_b, col_b, how, explanation in ROWS:
        if key_a not in results or key_b not in results:
            continue
        a, b = _get(results, key_a, col_a), _get(results, key_b, col_b)
        value = _diff(a, b) if how == "diff" else _pct_change(a, b)
        rows.append({"Medida": name, "Valor": NAN if value is None else value, "Como foi calculado": explanation})
    return rows
