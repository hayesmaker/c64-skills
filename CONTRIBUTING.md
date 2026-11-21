# Contributing / maintaining c64-skills

## Layout

```
.claude-plugin/marketplace.json      marketplace listing (one plugin: c64-skills)
plugins/c64/
  .claude-plugin/plugin.json         plugin manifest
  .claude-plugin/icon.png            plugin directory icon (generated, see Brand)
  skills/
    c64-ready/  SKILL.md  reference/cli.md
    c64-asm/    SKILL.md  reference/{kickassembler,c64-hardware}.md  templates/main-asm.md
  README.md                          the directory listing text
assets/brand/                        mascot, font, banner and the script that builds them
docs/                                planning notes
```

## Testing changes locally

Point Claude Code at your working copy instead of GitHub:

```
/plugin marketplace add /path/to/c64-skills
/plugin install c64-skills@c64-skills
```

The plugin ships no scripts: the plugin directory refuses executable files from
publishers that aren't Verified, so the skills give the agent the commands inline.
Smoke-test those commands with the template:

```bash
mkdir -p /tmp/demo/src && awk '/^```asm$/{f=1;next} /^```$/{f=0} f' plugins/c64/skills/c64-asm/templates/main-asm.md > /tmp/demo/src/main.asm
cd /tmp/demo && mkdir -p build
java -jar "$KICKASS_JAR" src/main.asm -o "$PWD/build/main.prg" -odir "$PWD/build" -symbolfile -vicesymbols
npx -y -p c64-ready@3.3.1 c64-agent build/main.prg --frames 60 \
  --at 10:joy2=right --at 40:joy2=none --dump 'd000:2'
# expect: d000: be 8c
```

To test against an unreleased c64-ready checkout, run `node /path/to/c64-ready/bin/agent.mjs`
in place of the `npx` command.

## Keeping in sync with c64-ready

`plugins/c64/skills/c64-ready/reference/cli.md` is a copy of
[`docs/AGENT_CLI.md`](https://github.com/hayesmaker/c64-ready/blob/master/docs/AGENT_CLI.md).
When the CLI changes, copy it across and update the SKILL.md recipes. The skills, the
template and `plugins/c64/README.md` pin `c64-ready@x.y.z` exactly (the plugin directory
blocks version ranges in `npx` commands), so raise every pin together:
`grep -rn 'c64-ready@' plugins`.

## Releasing

1. Bump `version` in **both** `plugins/c64/.claude-plugin/plugin.json` and the plugin's
   entry in `.claude-plugin/marketplace.json`. Installed users are only offered an
   update when this changes.
2. Validate: `claude plugin validate . && claude plugin validate plugins/c64 --profile directory`
3. Commit and push, then run `claude plugin tag plugins/c64 --push`. It checks that the
   two versions agree, creates a `c64-skills--v<version>` tag and pushes it (`--dry-run`
   previews this first).

## Brand

The mascot is **cbm-buddy** (`assets/brand/cbm-buddy.png`). To regenerate the plugin
icon and the README banner, for example after swapping in a higher-resolution mascot:

```bash
python3 assets/brand/make_brand.py   # needs Pillow
```

The plugin directory only takes the icon at first submission, so finalise it before
submitting.
