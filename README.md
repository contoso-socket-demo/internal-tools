# internal-tools

Contoso internal finance tooling. Python reporting helpers plus a Go
notifier, containerised.

## What this repo demos

Socket Basics: SAST, secret scanning and container scanning, with findings
curated to roughly a dozen so each one can be talked over rather than
scrolled past.

Every planted finding maps to a rule in the action's **default** enabled rule
list, verified against `action.yml` at v3.2.0. These are real detections, not
speculative patterns.

| File | Rules triggered |
|---|---|
| `src/reporting/export.py` | `python-sql-injection-format`, `python-subprocess-shell-true`, `python-start-process-with-shell`, `python-eval-usage`, `python-hardcoded-password-string`, `python-request-without-cert-validation` |
| `src/reporting/dashboard.py` | `python-flask-debug-true`, `python-jinja2-autoescape-false` |
| `cmd/notifier/main.go` | `go-hardcoded-credentials`, `go-sql-format-string`, `go-bind-all-interfaces`, `go-ssh-insecure-ignore-host-key` |
| `config/legacy-batch.env` | unverified AWS key, Slack webhook |
| `Dockerfile` | outdated base image, no `USER` directive |

The default rule lists contain no md5 or pickle rule, which is why this repo
does not bother planting those.

## Four configuration traps

1. **Every scanner defaults to `false`.** An unconfigured run scans nothing
   and reports a clean repo.
2. **`trufflehog_show_unverified` defaults to `false`.** The planted key is
   AWS's public documentation example key, so it is fake and therefore
   unverified. At the default, trufflehog finds it and then suppresses it,
   and the demo shows zero secrets.
3. **Never set `trufflehog_exclude_dir`.** Any value disables secret scanning
   entirely rather than narrowing it.
4. **Never set `custom_sast_rule_path`.** Custom rules REPLACE the bundled
   set rather than merging, silently dropping every finding above.

## One thing to watch

Deliberately vulnerable code can trip the AI malware scanner. Socket's own
`socket-basics` repo has this problem with its `app_tests/` fixtures. This
repo avoids copying those fixtures and uses plausible business naming
instead, which lowers the risk without eliminating it. If `gptMalware` fires
on these files, it is a false positive and worth filing.

## Required secrets

- `SOCKET_SECURITY_API_TOKEN`
