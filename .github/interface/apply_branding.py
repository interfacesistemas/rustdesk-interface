#!/usr/bin/env python3
"""Aplica a identidade da Interface Sistemas antes do build (só no CI).

Host e key do servidor vêm de secrets do repo (RS_HOST, RS_PUB_KEY) e não
ficam gravados no código. Rodar na raiz do repo, depois do checkout com
submódulos.
"""
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path.cwd()
ASSETS = Path(__file__).resolve().parent / "assets"

ORANGE = "F04E23"


def need(name):
    value = os.environ.get(name, "").strip()
    if not value:
        sys.exit(f"variável {name} vazia: configure o secret/variable no repo")
    return value


def patch(path, pattern, repl, count=1):
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    new, n = re.subn(pattern, repl, text, count=count)
    if n == 0:
        sys.exit(f"padrão não encontrado em {path}: {pattern}")
    file.write_text(new, encoding="utf-8")
    print(f"ok  {path} ({n}x)")


def copy(src, dst):
    target = ROOT / dst
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ASSETS / src, target)
    print(f"ok  {dst}")


def main():
    host = need("RS_HOST")
    key = need("RS_PUB_KEY")
    app = os.environ.get("APP_NAME", "").strip() or "InterfaceSuporte"
    if not re.fullmatch(r"[A-Za-z0-9_-]+", app):
        sys.exit("APP_NAME sem espaços nem acentos (vira nome do serviço do Windows)")
    if not re.fullmatch(r"[A-Za-z0-9+/=]{40,60}", key):
        sys.exit("RS_PUB_KEY não parece uma chave pública do RustDesk")

    cfg = "libs/hbb_common/src/config.rs"
    patch(cfg, r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];',
          f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{host}"];')
    patch(cfg, r'pub const RS_PUB_KEY: &str = "[^"]*";',
          f'pub const RS_PUB_KEY: &str = "{key}";')
    patch(cfg, r'(APP_NAME: RwLock<String> = RwLock::new\(")RustDesk(")',
          rf'\g<1>{app}\g<2>')

    rc = "flutter/windows/runner/Runner.rc"
    patch(rc, r'"FileDescription", "RustDesk Remote Desktop"',
          '"FileDescription", "Interface Sistemas - Suporte Remoto"')
    patch(rc, r'"ProductName", "RustDesk"', f'"ProductName", "{app}"')

    dart = "flutter/lib/common.dart"
    patch(dart, r"Color\(0xFF0071FF\)", f"Color(0xFF{ORANGE})")
    patch(dart, r"Color\(0x770071FF\)", f"Color(0x77{ORANGE})")
    patch(dart, r"Color\(0xAA0071FF\)", f"Color(0xAA{ORANGE})")
    patch(dart, r"Color\(0xFF2C8CFF\)", f"Color(0xFF{ORANGE})", count=0)

    for dst in ["res/icon.ico", "res/tray-icon.ico",
                "flutter/windows/runner/resources/app_icon.ico",
                "flutter/assets/icon.ico"]:
        copy("icon.ico", dst)
    for dst in ["res/icon.png", "res/128x128.png", "flutter/assets/icon.png"]:
        copy("icon.png", dst)
    for name in ["logo.png", "logo_light.png", "logo_dark.png"]:
        copy(name, f"flutter/assets/{name}")


if __name__ == "__main__":
    main()
