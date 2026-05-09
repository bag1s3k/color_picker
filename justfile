set shell := ["powershell"]

@default:
    just --list

mainfile := "main"

run file=mainfile:
    uv run -m {{file}}

dev file=mainfile:
    uv run textual run --dev {{file}}

console:
    uv run textual console