# c64: Commodore 64 development skills

![cbm-buddy, the c64-skills mascot](assets/banner.png)

**Let your AI coding agent write Commodore 64 programs and check that they actually work.**

This plugin teaches Claude to write 6502 assembly, build it with KickAssembler, and run
the result in the [c64-ready](https://github.com/hayesmaker/c64-ready) headless
emulator. The agent then reads back what happened (the screen text, memory, CPU
registers and PNG screenshots) and fixes the code itself, instead of handing you
something that "should work". When it's done, it gives you one command that opens the
program in the c64-ready browser player so you can play it.

## Skills

- **c64-ready:** run `.prg`, `.d64`, `.crt` and `.c64` files headlessly, and drive
  them with scripted joystick and keyboard input. It can stop at a breakpoint or when
  text appears on screen, dump memory, and save screenshots, video and snapshots. Runs
  are deterministic, so the same command gives the same result every time.
- **c64-asm:** a build → run → verify loop with KickAssembler that reports errors with
  line numbers. It includes a tested starter project (raster interrupt, game loop and a
  joystick-controlled sprite), a KickAssembler syntax guide, and a C64 hardware
  reference covering VIC-II, sprites, SID, CIA and KERNAL.

## Requirements

| Tool | Needed for |
| ---- | ---------- |
| [Node.js](https://nodejs.org/) 24+ | running programs in the emulator |
| Java 8+ and [KickAssembler](https://theweb.dk/KickAssembler/) (`KickAss.jar`) | building `.asm` → `.prg` |
| ffmpeg *(optional)* | recording video of a run |

Download KickAssembler yourself and point `KICKASS_JAR` at `KickAss.jar`, or put it in
your project's `tools/` folder. The plugin never downloads it.

## What the plugin runs and fetches

The plugin contains only instructions, reference notes and a starter assembly project (as Markdown). It
ships no scripts or programs. The skills tell Claude to run these commands:

- `java -jar KickAss.jar …` to build your source files, locally.
- `npx -y -p c64-ready@3.3.0 c64-agent …` to run the program in the c64-ready emulator.
  On first use this downloads that exact version of the
  [c64-ready package](https://www.npmjs.com/package/c64-ready) from the npm registry.
  If your project already has c64-ready installed, Claude uses that copy instead.
- The suggested `npx c64-ready <file> --open` command starts a local web server on
  `localhost` that serves the browser player and your built file, then opens it in
  your browser.

The plugin sends no data anywhere, and the emulator runs entirely on your machine.

## Example prompts

> Make a C64 program with a sprite I can move with the joystick.

> My raster split flickers on the left side. Find out why and fix it.

More documentation, troubleshooting and the source are at
[github.com/hayesmaker/c64-skills](https://github.com/hayesmaker/c64-skills).

## License

MIT
