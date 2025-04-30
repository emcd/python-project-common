Ensure that long Hatch commands are specified inside of double-quoted TOML
strings so that line continuation backslashes are processed rather than treated
as literals. Fixes issue on Window.
