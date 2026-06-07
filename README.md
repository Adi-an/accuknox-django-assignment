# AccuKnox Django Assignment

## Setup & Run

```bash
# 1. Install Django
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Run each demo
python manage.py demo_q1_sync
python manage.py demo_q2_thread
python manage.py demo_q3_transaction

# 4. Rectangle class (pure Python, no Django needed)
python rectangle/rectangle.py
```

---

## Django Signals — Answers

### Q1: Synchronous or Asynchronous?
**Synchronous.** The signal handler blocks the caller until it finishes.
I proved this by adding a deliberate 2-second sleep inside the handler —
the caller waits the full 2 seconds before continuing.

### Q2: Same Thread as Caller?
**Yes.** I printed `threading.current_thread().ident` from both the caller
and inside the handler. The IDs are identical.

### Q3: Same Database Transaction as Caller?
**Yes.** The handler creates an `AlertRecord` inside the signal.
When I force a rollback in the caller using `transaction.atomic()`,
the `AlertRecord` disappears too — it was never committed independently.

---

## Why Management Commands?

Each question is a standalone proof-of-concept — not a web feature.
Management commands felt like the cleanest way to run isolated demos
without wiring up URLs and views unnecessarily.

---

## Project Structure

```
accuknox_assignment/
├── manage.py
├── requirements.txt
├── accuknox_project/       ← Django project config
│   └── settings.py
├── signals_demo/           ← App for Q1, Q2, Q3
│   ├── models.py           ← UserActivityLog, AlertRecord
│   ├── signals.py          ← All three signal handlers
│   ├── apps.py             ← Registers signals on startup
│   └── management/
│       └── commands/
│           ├── demo_q1_sync.py
│           ├── demo_q2_thread.py
│           └── demo_q3_transaction.py
└── rectangle/
    └── rectangle.py        ← Custom iterable Rectangle class
```

---

## Assumptions

- SQLite used for simplicity — no external DB setup needed to run this
- `rectangle.py` kept outside the Django app since it has no Django dependency
- Signal handlers in `signals.py` are connected via `apps.py ready()` — the standard Django approach
