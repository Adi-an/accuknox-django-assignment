import time
import threading

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserActivityLog, AlertRecord


# ─────────────────────────────────────────────
# Q1 — Proves signals are SYNCHRONOUS by default
# The handler sleeps for 2 seconds on purpose.
# If signals were async, the caller would continue immediately.
# But it doesn't — it waits. That's the proof.
# ─────────────────────────────────────────────
@receiver(post_save, sender=UserActivityLog)
def q1_synchronous_proof(sender, instance, created, **kwargs):
    if not created:
        return
    print(f"  [SIGNAL HANDLER] Received signal for '{instance.username}'")
    print(f"  [SIGNAL HANDLER] Sleeping 2 seconds to simulate slow work...")
    time.sleep(2)
    print(f"  [SIGNAL HANDLER] Done sleeping. Handler finished.")


# ─────────────────────────────────────────────
# Q2 — Proves signals run in the SAME THREAD as the caller
# We print the thread ID from both the caller (management command)
# and here inside the handler. They will match.
# ─────────────────────────────────────────────
@receiver(post_save, sender=UserActivityLog)
def q2_same_thread_proof(sender, instance, created, **kwargs):
    if not created:
        return
    handler_thread_id = threading.current_thread().ident
    print(f"  [SIGNAL HANDLER] Thread ID inside handler : {handler_thread_id}")


# ─────────────────────────────────────────────
# Q3 — Proves signals share the SAME DB TRANSACTION as caller
# We write an AlertRecord here inside the handler.
# If the caller's transaction rolls back, this write also disappears.
# ─────────────────────────────────────────────
@receiver(post_save, sender=UserActivityLog)
def q3_same_transaction_proof(sender, instance, created, **kwargs):
    if not created:
        return
    AlertRecord.objects.create(
        triggered_by=instance.username,
        message=f"Signal fired for action: {instance.action}"
    )
    print(f"  [SIGNAL HANDLER] AlertRecord created inside handler (within same transaction).")
