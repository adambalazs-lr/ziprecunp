import os
import tempfile
from pathlib import Path
import zipfile
import timeit
from __version__ import __version__ as version

# CONFIG

i_dont_care_about = [
    r"webapps\ROOT\WEB-INF\patching-backup.zip",
    r"patches\liferay-fix-pack-dxp-5-7210.zip"
]
targets = [
    r"c:\liferay\liferay-dxp-7.2.10-DXP-5-2x",
    r"c:\liferay\liferay-dxp-7.2.10-DXP-5-3x"
]


# APP

def unpack(path):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except Exception as e:
                print("EXCEPTION:", path, "->", e)
                return False
            else:
                os.remove(path)
                os.rename(temp_dir, path)
                return True
    except FileNotFoundError:
        pass


def run(directory):
    pathlist = Path(directory).glob("**/*")
    unchanged = True
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)

        if not os.path.isdir(path):
            if not any((path_in_str.endswith(x) for x in i_dont_care_about)):
                if path_in_str.endswith(".jar") or path_in_str.endswith(
                        ".lpkg") or path_in_str.endswith(".zip"):

                    if unchanged:
                        unchanged = not unpack(path)
                    else:
                        unpack(path)

        # print(path_in_str)

    if not unchanged:
        print("One more time ... ")
        run(directory)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print(os.path.basename(__file__), version)
    print("Lemme tell ya a lil' somethin' about work...")

    for target in targets:
        start = timeit.default_timer()
        print("Unpacking", target)
        run(target)
        stop = timeit.default_timer()
        print('Took:', (stop - start) / 60, "minutes.")

    print("Nanako, get daddy another beer!")
