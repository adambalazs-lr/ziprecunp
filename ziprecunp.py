import os
import tempfile
from pathlib import Path
import zipfile
import timeit
from __version__ import __version__ as version

skip_these = [
    r"webapps\ROOT\WEB-INF\patching-backup.zip",
    r"patching-tool\lib\patching-tool.jar",
    r"bundles\apache-tomcat-9.0.37.zip",
]
targets = [
    r"c:\liferay\_WORK\a-3.0.22",
    r"c:\liferay\_WORK\a-nightly",
]


# APP

def unpack(path):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except Exception as e:
                print("x_x zip extraction exception; file:", path, "; temp_dir:", temp_dir, " -> ",
                      e)
                return False
            else:

                c = 0
                print(f"--- os.remove({path})...")
                while True:
                    try:
                        os.remove(path)
                        break
                    except Exception as e:
                        c += 1

                    if c > 3:
                        print(f"x_x os.remove({path}) -> {e}")
                        raise IOError(e)

                c = 0
                print(f"--- os.rename({temp_dir}, {path})...")
                while True:
                    try:
                        os.rename(temp_dir, path)
                    except Exception as e:
                        c += 1

                    if c > 3:
                        print(f"x_x os.rename({temp_dir}, {path}) -> {e}")
                        raise IOError(e)

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
            if not any((path_in_str.endswith(x) for x in skip_these)):
                if path_in_str.endswith(".jar") or path_in_str.endswith(
                        ".lpkg") or path_in_str.endswith(".zip") or path_in_str.endswith(".war"):
                    # print(f"Unpacking: {path_in_str}")
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
