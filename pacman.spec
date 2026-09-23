from PyInstaller.utils.hooks import collect_all

jp_datas, jp_bins, jp_hidden = collect_all("just_playback")

a = Analysis(
    ["pac-man.py"],
    datas=[
        ("src/visuals/sprites", "src/visuals/sprites"),
        ("src/visuals/fonts", "src/visuals/fonts"),
        ("src/core/sounds", "src/core/sounds"),
        ("config.json", "."),
        ("INSTRUCTIONS.txt", ".")
    ] + jp_datas,
    binaries=jp_bins,
    hiddenimports=jp_hidden + ["_cffi_backend", "_ma_playback"],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="pacman", console=False)
coll = COLLECT(exe, a.binaries, a.datas, name="pacman")
