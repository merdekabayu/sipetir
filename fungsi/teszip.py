import zipfile
import os
print('halo')
def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    print(abs_src)
    for dirname, subdirs, files in os.walk(src):
        print(files)
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print(absname,arcname)
            zf.write(absname, arcname)
    zf.close()

zip("data/NEX/20230708.db3", "teszip")