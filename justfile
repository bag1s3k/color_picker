set shell := ["powershell"]

@default:
    just --list

package_name := "color_picker"
main_modul := "src.color_picker"
main_script := "src/color_picker/__main__.py"

run file=main_modul:
    uv run -m {{file}}

dev file=main_script:
    uv run textual run --dev {{file}}


# Textual commmands
console:
    uv run textual console

colors:
    uv run textual run -c textual colors


# Ruff commmands
ruff:
    just check
    just format

check fix="":
    uv run ruff check {{ if fix == "--fix" { "--fix" } else { "" } }}

format:
    uv run ruff format