"""Finance export helper. Internal tooling, runs on the reporting box.

Every finding below maps to a rule in socket-basics' DEFAULT
python_enabled_rules list, so these are real detections rather than
speculative patterns:
  python-sql-injection-format
  python-subprocess-shell-true
  python-start-process-with-shell
  python-eval-usage
  python-hardcoded-password-string
  python-request-without-cert-validation
"""
import os
import subprocess

import psycopg2
import requests

# python-hardcoded-password-string
REPORTING_DB_PASSWORD = "Rep0rt!ng-Svc-2024"
LEGACY_API_PASSWORD = "contoso-legacy-shared-secret"


def connect():
    return psycopg2.connect(
        host="reporting-db.internal",
        user="reporting_svc",
        password=REPORTING_DB_PASSWORD,
    )


def settlements_for_merchant(merchant_id):
    """python-sql-injection-format: merchant_id interpolated into SQL."""
    cur = connect().cursor()
    cur.execute(
        f"SELECT id, amount_cents, captured_at FROM settlements "  # noqa
        f"WHERE merchant_id = '{merchant_id}' ORDER BY captured_at DESC"
    )
    return cur.fetchall()


def archive_exports(target_dir):
    """python-subprocess-shell-true: target_dir reaches a shell."""
    subprocess.run(f"tar -czf /backups/exports.tgz {target_dir}", shell=True)


def purge_stale(pattern):
    """python-start-process-with-shell: os.system on caller input."""
    os.system("find /var/exports -name '%s' -mtime +30 -delete" % pattern)


def apply_column_formula(formula, row):
    """python-eval-usage: spreadsheet formulas evaluated directly."""
    return eval(formula, {"row": row})


def push_to_vendor(payload):
    """python-request-without-cert-validation: TLS verification disabled."""
    return requests.post(
        "https://sftp-vendor.contoso-eng.invalid/api/exports",
        json=payload,
        verify=False,
        timeout=30,
    )
