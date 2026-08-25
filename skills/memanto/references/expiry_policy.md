# Memory Expiry Policy

Memory that only grows gets worse. Stale `context` and one-off `observation` entries crowd out
the durable `decision` and `instruction` memories that actually matter, and every recall pays
for them. An expiry policy retires memories automatically by type and age.

Expiry is **not** deletion. An expired memory keeps its content and still appears in recall
labelled `[EXPIRED]`, and `memanto memory restore` brings it back. Only `policy purge` and
`memanto forget` destroy anything.

## Inspect the current policy

```bash
memanto policy show
memanto policy show --agent my-agent
```

## Presets

```bash
memanto policy list-preset
```

Three bundles ship: `conservative`, `balanced`, `aggressive`. Adopt one:

```bash
memanto policy apply-preset balanced
memanto policy apply-preset aggressive --agent my-agent --yes
```

`apply-preset` prints the preset in full and asks before replacing your current policy. It only
changes the *rules* — **nothing expires until you run `memanto policy apply`.**

## Sweep

```bash
memanto policy apply --dry-run     # show matches and stop
memanto policy apply               # show matches, then ask
memanto policy apply --yes         # skip the prompt
memanto policy apply --limit 50    # list up to 50 matched memories (default 20)
```

`apply` always shows the policy in force and exactly which memories match before asking, so
`--dry-run` is only needed when you want to stop at the preview.

## Purge

```bash
memanto policy purge --dry-run
memanto policy purge
```

Permanently deletes memories that have been expired longer than the purge window. **Destructive
and irreversible.** Disabled unless the policy sets `purge_expired_after`, so it cannot fire by
accident.

## Choosing a policy

| Situation | Preset |
|---|---|
| Long-lived project, memory is the source of truth | `conservative` |
| Normal development work | `balanced` |
| High-volume agent generating lots of transient context | `aggressive` |

Start `conservative`. Expiry is reversible, but re-deriving why a decision was made is not, and
an over-aggressive sweep on a young namespace throws away context you have not yet learned to
value.

## Working with expired memories

```bash
memanto recall "deploy"              # active and expired, each labelled
memanto recall "deploy" --active     # active only
memanto recall "deploy" --expired    # expired only
memanto memory restore <id>          # bring one back
```

## Automation

`memanto schedule enable` runs the expiry sweep nightly alongside daily summary and conflict
detection. Set the policy deliberately before enabling it — the scheduled sweep does not stop to
ask.
