import os
from pathlib import Path
import uuid
import zipfile
import timeit
from __version__ import  __version__ as version

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

def unique_file(path):
    return str(uuid.uuid4())


def unpack(path):
    path_to_str = str(path)
    # print("Unpacking " + path_to_str)
    unique_dirname = unique_file(path)
    temp_dir = os.path.join(os.path.dirname(path), unique_dirname)
    os.mkdir(temp_dir)
    error = False
    try:
        with zipfile.ZipFile(path_to_str, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
    except Exception as e:
        print("EXCEPTION " + path_to_str + " -> " + str(e))
        try:
            zip_ref.close()
        except:
            print("Cannot close zip_ref")
        else:
            try:
                os.remove(temp_dir)
            except:
                print("Cannot delete ", temp_dir)

        error = True

    if error:
        return False

    else:
        os.remove(path)
        os.rename(temp_dir, path)

        return True


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
