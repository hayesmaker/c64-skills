# Contributing / maintaining c64-skills

## Layout

```
.claude-plugin/marketplace.json      marketplace listing (one plugin: c64)
plugins/c64/
  .claude-plugin/plugin.json         plugin manifest
  .claude-plugin/icon.png            plugin directory icon (generated, see Brand)
  skills/
    c64-ready/  SKILL.md  scripts/c64-agent.sh  reference/cli.md
    c64-asm/    SKILL.md  scripts/kickass.sh    reference/{kickassembler,c64-hardware}.md  templates/main.asm
assets/brand/                        mascot, font, banner and the script that builds them
docs/                                planning notes
```

## Testing changes locally

Point Claude Code at your working copy instead of GitHub:

```
/plugin marketplace add /path/to/c64-skills
/plugin install c64@c64-skills
```

Smoke-test the scripts:

```bash
S=plugins/c64/skills
mkdir -p /tmp/demo/src && cp $S/c64-asm/templates/main.asm /tmp/demo/src/
(cd /tmp/demo && $OLDPWD/$S/c64-asm/scripts/kickass.sh src/main.asm \
  && $OLDPWD/$S/c64-ready/scripts/c64-agent.sh build/main.prg --frames 60 \
     --at 10:joy2=right --at 40:joy2=none --dump 'd000:2')
# expect: d000: be 8c
```

Set `C64_READY_DIR=/path/to/c64-ready` to test against an unreleased c64-ready checkout.

## Keeping in sync with c64-ready

`plugins/c64/skills/c64-ready/reference/cli.md` is a copy of
[`docs/AGENT_CLI.md`](https://github.com/hayesmaker/c64-ready/blob/master/docs/AGENT_CLI.md).
When the CLI changes, copy it across, update the SKILL.md recipes, and raise the
minimum version in `scripts/c64-agent.sh` (`c64-ready@^x.y.z`) if the skill depends on
new flags.

## Releasing

1. Bump `version` in **both** `plugins/c64/.claude-plugin/plugin.json` and the plugin's
   entry in `.claude-plugin/marketplace.json`. Installed users are only offered an
   update when this changes.
2. Validate: `claude plugin validate . && claude plugin validate plugins/c64 --profile directory`
3. Commit and push, then run `claude plugin tag plugins/c64 --push`. It checks that the
   two versions agree, creates a `c64--v<version>` tag and pushes it (`--dry-run`
   previews this first).

## Brand

The mascot is **cbm-buddy** (`assets/brand/cbm-buddy.png`). To regenerate the plugin
icon and the README banner, for example after swapping in a higher-resolution mascot:

```bash
python3 assets/brand/make_brand.py   # needs Pillow
```

The plugin directory only takes the icon at first submission, so finalise it before
submitting.
