"""
Q3: Do Django signals run in the same database transaction as the caller?

ANSWER: Yes, by default.

PROOF:
- Inside the signal handler, we create an AlertRecord in the DB.
- In the caller, we wrap the save() in transaction.atomic()
  and then raise an exception to force a rollback.
- After the rollback, we check if the AlertRecord exists.
- It doesn't — because the signal's DB write was part of
  the same transaction that got rolled back.

This conclusively proves signals share the caller's transaction.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from signals_demo.models import UserActivityLog, AlertRecord


class Command(BaseCommand):
    help = 'Q3 — Proves Django signals run in the same DB transaction as the caller'

    def handle(self, *args, **kwargs):
        UserActivityLog.objects.all().delete()
        AlertRecord.objects.all().delete()

        self.stdout.write("\n" + "="*60)
        self.stdout.write("Q3: Do signals share the caller's database transaction?")
        self.stdout.write("="*60)

        self.stdout.write(f"\n[CALLER] AlertRecord count before anything : {AlertRecord.objects.count()}")
        self.stdout.write("[CALLER] Starting atomic transaction block...")
        self.stdout.write("[CALLER] Will save a UserActivityLog, then force a rollback.\n")

        try:
            with transaction.atomic():
                # This triggers post_save → q3_same_transaction_proof
                # which creates an AlertRecord inside the handler
                UserActivityLog.objects.create(username="charlie", action="sudo_attempt")

                self.stdout.write(f"\n[CALLER] AlertRecord count INSIDE transaction (before rollback): "
                                  f"{AlertRecord.objects.count()}")
                self.stdout.write("[CALLER] Now forcing a rollback with an intentional exception...\n")

                raise Exception("Intentional rollback to test signal transaction scope")

        except Exception as e:
            self.stdout.write(f"[CALLER] Exception caught: {e}")

        final_count = AlertRecord.objects.count()
        self.stdout.write(f"\n[CALLER] AlertRecord count AFTER rollback : {final_count}")

        if final_count == 0:
            self.stdout.write("[CALLER] AlertRecord is gone — the signal's DB write rolled back too.")
            self.stdout.write("\n✅ CONCLUSION: Django signals run in the SAME TRANSACTION as the caller.\n")
        else:
            self.stdout.write("[CALLER] AlertRecord still exists — signal used a separate transaction.")
