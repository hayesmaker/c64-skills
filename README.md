# c64-skills

![c64-skills: cbm-buddy, the c64-skills mascot](assets/brand/banner.png)

Agent skills for **AI-assisted Commodore 64 development**. They give a coding agent
(Claude Code, or any tool that reads `SKILL.md` Agent Skills) a closed loop: write 6502
assembly, build it with KickAssembler, run it in the
[c64-ready](https://github.com/hayesmaker/c64-ready) headless emulator, and check what it
actually did: screen text, memory, registers, breakpoints and screenshots. The agent
then fixes the code itself instead of handing you something that "should work".

| Skill | What it gives the agent |
| ----- | ----------------------- |
| [`c64-ready`](plugins/c64/skills/c64-ready/SKILL.md) | Run `.prg` / `.d64` / `.crt` / `.c64` files deterministically for N frames, with scripted joystick and keyboard input, PC breakpoints, `--until-text` pass/fail tests, decoded screen text, memory dumps, PNG screenshots, video and snapshots |
| [`c64-asm`](plugins/c64/skills/c64-asm/SKILL.md) | The KickAssembler build loop (`kickass.sh`), a tested starter project (raster IRQ, game loop, joystick sprite), a KickAssembler syntax guide aimed at the mistakes models make, and a C64 hardware cheat sheet |

## Install

### Claude Code

```
/plugin marketplace add hayesmaker/c64-skills
/plugin install c64@c64-skills
```

### Other agents

Copy the folders in `plugins/c64/skills/` into the skills directory your agent reads
(for Claude Code without the plugin system, that's `~/.claude/skills/` or
`.claude/skills/` in a project).

## Requirements

- **Node.js 24+**. `c64-agent` comes from the [`c64-ready`](https://www.npmjs.com/package/c64-ready)
  npm package (3.2.0+) and is fetched with `npx` on first use. To use a local clone instead,
  set `C64_READY_DIR=/path/to/c64-ready`.
- **Java 8+** and **KickAss.jar** from https://theweb.dk/KickAssembler/. Set
  `KICKASS_JAR=/path/to/KickAss.jar`, or put it in `./tools/`.
- Optional: **ffmpeg**, for `--video`.

## What a session looks like

> **You:** Make the sprite bounce off the screen edges.
>
> **Agent:** *edits `src/main.asm` → `kickass.sh src/main.asm` → runs*
> `c64-agent.sh build/main.prg --symbols build/main.sym --frames 400 --dump sprite_dx:1 --every 50 --shots-dir /tmp/f`
> *→ reads the dumps and a couple of frames, sees the X direction flip at 255 instead of
> the right border, fixes the `$d010` handling, re-runs, confirms, and reports back with
> a screenshot.*

## Try it by hand

```bash
S=plugins/c64/skills
mkdir -p demo/src && cp $S/c64-asm/templates/main.asm demo/src/ && cd demo
../$S/c64-asm/scripts/kickass.sh src/main.asm
../$S/c64-ready/scripts/c64-agent.sh build/main.prg --symbols build/main.sym \
  --frames 60 --at 10:joy2=right --at 40:joy2=none --screen --dump 'd000:2' --screenshot shot.png
```

## Repository layout

```
.claude-plugin/marketplace.json      marketplace listing (one plugin: c64)
plugins/c64/
  .claude-plugin/plugin.json
  skills/
    c64-ready/  SKILL.md  scripts/c64-agent.sh  reference/cli.md
    c64-asm/    SKILL.md  scripts/kickass.sh    reference/{kickassembler,c64-hardware}.md  templates/main.asm
```

`c64-ready/reference/cli.md` is a copy of
[`docs/AGENT_CLI.md`](https://github.com/hayesmaker/c64-ready/blob/master/docs/AGENT_CLI.md)
in c64-ready. Update it when the CLI changes.

## Roadmap

More skills to come: graphics (charsets, sprites and bitmaps with
[c64-pad](https://github.com/hayesmaker/c64-pad)), SID music, and
[c64-cheevos](https://github.com/hayesmaker/c64-cheevos) achievement detectors.

## Brand

The mascot is **cbm-buddy**. `assets/brand/make_brand.py` regenerates the plugin icon
(`plugins/c64/.claude-plugin/icon.png`, 1024×1024) and the banner from `assets/brand/cbm-buddy.png`.
The font is the freeware *Commodore 64* TrueType font by Devin Cook.

## License

MIT
