import os
import re
import subprocess
import urllib.request

import keys

WORKSHOP = "steamapps/workshop/content/107410/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"  # noqa: E501


def update_mods(ids):
    steamcmd = ["unbuffer", "/steamcmd/steamcmd.sh"]
    steamcmd.extend(["+force_install_dir", "/arma3"])
    steamcmd.extend(["+login", os.environ["STEAM_USER"], os.environ["STEAM_PASSWORD"]])
    for id in ids:
        steamcmd.extend(["+workshop_download_item", "107410", id])
    steamcmd.extend(["+quit"])
    subprocess.call(steamcmd)


def preset(mod_file):
    if mod_file.startswith("http"):
        req = urllib.request.Request(
            mod_file,
            headers={"User-Agent": USER_AGENT},
        )
        remote = urllib.request.urlopen(req)
        with open("preset.html", "wb") as f:
            f.write(remote.read())
        mod_file = "preset.html"
    mod_dirs = []
    with open(mod_file) as f:
        html = f.read()
        regex = r"filedetails\/\?id=(\d+)\""
        matches = re.finditer(regex, html, re.MULTILINE)
        mods = list(map(lambda a: a.group(1), matches))
        update_mods(mods)
        for mod in mods:
            mod_dir = WORKSHOP + mod
            mod_dirs.append(mod_dir)
            keys.copy(mod_dir)
    return mod_dirs
