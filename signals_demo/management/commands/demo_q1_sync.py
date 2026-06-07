"""
Q1: Are Django signals synchronous or asynchronous by default?

ANSWER: Synchronous.

PROOF: The signal handler (in signals.py) sleeps for 2 seconds.
If signals were async, the line "CALLER: save() returned immediately"
would print right after the save — but it doesn't.
The caller is blocked until the handler finishes sleeping.
That conclusively proves signals are synchronous.
"""

import time
from django.core.management.base import BaseCommand
from signals_demo.models import UserActivityLog


class Command(BaseCommand):
    help = 'Q1 — Proves Django signals are synchronous by default'

    def handle(self, *args, **kwargs):
        # Clean up previous runs
        UserActivityLog.objects.all().delete()

        self.stdout.write("\n" + "="*55)
        self.stdout.write("Q1: Are Django signals synchronous or asynchronous?")
        self.stdout.write("="*55)

        self.stdout.write("\n[CALLER] About to call .save() on UserActivityLog...")
        self.stdout.write("[CALLER] If signals were async, next line prints immediately.\n")

        start = time.time()

        # This triggers the post_save signal → q1_synchronous_proof handler
        UserActivityLog.objects.create(username="alice", action="login_attempt")

        elapsed = round(time.time() - start, 2)

        self.stdout.write(f"\n[CALLER] save() returned. Total wait time: {elapsed}s")
        self.stdout.write("[CALLER] We waited ~2s → signal ran SYNCHRONOUSLY (blocked the caller).")
        self.stdout.write("\n✅ CONCLUSION: Django signals are SYNCHRONOUS by default.\n")
