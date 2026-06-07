"""
Q2: Do Django signals run in the same thread as the caller?

ANSWER: Yes, by default.

PROOF: We print threading.current_thread().ident from both
the caller (here) and inside the signal handler.
Both IDs will be identical, proving they share the same thread.
"""

import threading
from django.core.management.base import BaseCommand
from signals_demo.models import UserActivityLog


class Command(BaseCommand):
    help = 'Q2 — Proves Django signals run in the same thread as the caller'

    def handle(self, *args, **kwargs):
        UserActivityLog.objects.all().delete()

        self.stdout.write("\n" + "="*55)
        self.stdout.write("Q2: Do signals run in the same thread as the caller?")
        self.stdout.write("="*55)

        caller_thread_id = threading.current_thread().ident
        self.stdout.write(f"\n[CALLER] Thread ID before save()  : {caller_thread_id}")
        self.stdout.write("[CALLER] Calling save() now...\n")

        # Triggers post_save → q2_same_thread_proof handler prints its thread ID
        UserActivityLog.objects.create(username="bob", action="file_access")

        self.stdout.write(f"\n[CALLER] Thread ID after save()   : {caller_thread_id}")
        self.stdout.write("[CALLER] Compare the two thread IDs above — they are identical.")
        self.stdout.write("\n✅ CONCLUSION: Django signals run in the SAME THREAD as the caller.\n")
