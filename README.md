# c64-skills

![c64-skills: cbm-buddy, the c64-skills mascot](assets/brand/banner.png)

**Let your AI coding agent write Commodore 64 programs and check that they actually work.**

c64-skills teaches Claude Code (or any agent that reads `SKILL.md` Agent Skills) to:
write 6502 assembly, build it with KickAssembler, and run the result in the
[c64-ready](https://github.com/hayesmaker/c64-ready) headless emulator. The agent then
checks what happened (the screen, memory, registers and screenshots) and fixes the code
itself, instead of handing you something that "should work".

## Quick start (Claude Code)

**1. Add the c64-skills marketplace, then install the plugin:**

```
/plugin marketplace add hayesmaker/c64-skills
/plugin install c64@c64-skills
```

The first line registers this repository as a plugin source, and the second installs
its `c64` plugin. If the skills don't show up straight away, restart Claude Code.

**2. Install the tools the skills use:**

| Tool | Needed for | Check |
| ---- | ---------- | ----- |
| [Node.js](https://nodejs.org/) 24+ | running programs in the emulator | `node -v` |
| Java 8+ | KickAssembler | `java -version` |
| [KickAssembler](https://theweb.dk/KickAssembler/) (`KickAss.jar`) | building `.asm` → `.prg` | see below |
| ffmpeg *(optional)* | recording video of a run | `ffmpeg -version` |

The emulator needs no separate install: the first run fetches
[`c64-ready`](https://www.npmjs.com/package/c64-ready) through `npx`.

KickAssembler is a free download. Unzip it anywhere, then either point at it:

```bash
export KICKASS_JAR=~/KickAssembler/KickAss.jar   # add to your shell profile
```

or put `KickAss.jar` in a `tools/` folder inside your project. The agent also looks
in `~/KickAssembler/` and `/opt/`.

**3. Ask for something.** You don't need to name the skills:

> Make a C64 program with a sprite I can move with the joystick.

> My raster split flickers on the left side. Find out why and fix it.

> Add a score counter at the top of the screen and show me a screenshot after
> I've collected three coins.

The agent builds the program, runs it for a few emulated seconds, presses joystick
buttons or keys if needed, and reads back the screen or memory. Along the way it will
usually show you screenshots.

## What's included

| Skill | What your agent can do with it |
| ----- | ------------------------------ |
| [**c64-ready**](plugins/c64/skills/c64-ready/SKILL.md) | Run `.prg`, `.d64`, `.crt` and `.c64` files, and drive them with scripted joystick and keyboard input. It can stop at a breakpoint or when text appears on screen, and read the screen, memory and registers. It also saves PNG screenshots, video and snapshots. Runs are repeatable: the same command gives the same result every time. |
| [**c64-asm**](plugins/c64/skills/c64-asm/SKILL.md) | Build with KickAssembler and report errors with line numbers. It comes with a tested starter project (raster interrupt, game loop and a joystick-controlled sprite), a KickAssembler syntax guide aimed at mistakes AI models commonly make, and a C64 hardware cheat sheet covering VIC-II, sprites, SID, CIA and KERNAL. |

## What a session looks like

> **You:** Make the sprite bounce off the screen edges.
>
> **Agent:** *edits `src/main.asm`, builds it, and runs it for 8 emulated seconds, dumping
> the sprite's direction variable and saving a screenshot every second. It sees the sprite
> turn around at X = 255 instead of at the right border, fixes the `$d010` (sprite X bit 8)
> handling, runs it again to confirm, and shows you the result.*

## Updating and removing

```
/plugin marketplace update c64-skills   # fetch the latest version of the listing
/plugin update c64@c64-skills           # update the installed plugin
/plugin uninstall c64@c64-skills
```

## Other agents, or without the plugin system

The skills are plain folders. Clone this repository and copy (or symlink)
`plugins/c64/skills/c64-ready` and `plugins/c64/skills/c64-asm` into the skills
directory your agent reads. For Claude Code, that's `~/.claude/skills/` for all
projects or `.claude/skills/` for a single project.

## Using the tools yourself

The commands the agent runs work fine by hand. From a clone of this repository:

```bash
# start a project from the template and build it
mkdir -p mygame/src mygame/build
cp plugins/c64/skills/c64-asm/templates/main.asm mygame/src/ && cd mygame
java -jar "$KICKASS_JAR" src/main.asm \
  -o "$PWD/build/main.prg" -odir "$PWD/build" -symbolfile -vicesymbols

# run it: push the joystick right for 30 frames, then show the screen and sprite position
npx -y -p c64-ready@3.3.0 c64-agent build/main.prg --symbols build/main.sym \
  --frames 60 --at 10:joy2=right --at 40:joy2=none --screen --dump 'd000:2' --screenshot shot.png
```

`c64-agent --help` lists every option, and the full reference is in
[plugins/c64/skills/c64-ready/reference/cli.md](plugins/c64/skills/c64-ready/reference/cli.md).
To play the program yourself, run `npx c64-ready build/main.prg --open`. The browser
player opens with it running, and reloading the page picks up a new build.

## Troubleshooting

- **The agent can't find KickAssembler:** set `KICKASS_JAR` to the full path of `KickAss.jar`, or put
  it in your project's `tools/` folder.
- **c64-ready fails to start:** check `node -v`. c64-ready needs Node.js 24 or newer.
- **The first run is slow:** `npx` is downloading c64-ready. Later runs start
  immediately. For an always-installed copy, run `npm install -g c64-ready`.
- **`npx c64-ready build/main.prg` opens a different game:** an old copy of c64-ready is
  installed globally and `npx` is running it. Update it with `npm install -g c64-ready@latest`,
  or remove it with `npm uninstall -g c64-ready`.
- **A small `lvllvl` label in the middle of screenshots:** that's the emulator core's
  watermark, not a bug in your program.
- **Disk images (`.d64`) take a while to start:** the 1541 drive is emulated accurately,
  speed included. The agent knows to wait.

## Roadmap

Planned skills: C64 graphics (charsets, sprites and bitmaps with
[c64-pad](https://github.com/hayesmaker/c64-pad)), SID music, and
[c64-cheevos](https://github.com/hayesmaker/c64-cheevos) achievements. Ideas and issues
are welcome.

## Credits

- Emulation: [c64-ready](https://github.com/hayesmaker/c64-ready), based on the c64.js core
  from [lvllvl](https://github.com/jaammees/lvllvl) by James.
- Mascot: **cbm-buddy**.
- Font in the banner: the freeware *Commodore 64* TrueType font by Devin Cook.

## License

MIT
