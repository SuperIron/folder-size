import os
import prettytable as pt
from PyQt5 import QtWidgets


def get_directory():
    dialog = QtWidgets.QFileDialog(None, caption='Folder Size Dir')
    dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
    dialog.setDirectory('./')
    dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
    dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
    dialog.setLabelText(QtWidgets.QFileDialog.Accept, "Select")
    if dialog.exec_() == QtWidgets.QFileDialog.Accepted:
        return dialog.selectedFiles()[0]


def get_unit(sizes):
    units = ['B', 'KB', 'MB', 'GB']
    unit_idx = 0
    while sizes >= 1024:
        sizes = sizes / 1024
        unit_idx += 1
    return sizes, units[unit_idx]


def get_tb(title):
    tb = pt.PrettyTable()
    tb.title = title
    tb.field_names = ["name", "size"]
    tb.align["name"] = "l"
    tb.align["size"] = "r"
    return tb


def init():
    path = get_directory()
    tb = get_tb(path)
    child_dirs = os.listdir(path)
    for child_dir in child_dirs:
        child_dir_path = os.path.join(path, child_dir)
        if not os.path.isdir(child_dir_path):
            continue
        sizes = 0
        for dirpath, dirnames, filenames in os.walk(child_dir_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                sizes += os.path.getsize(file_path)
        sizes, unit = get_unit(sizes)
        tb.add_row(["%s" % (child_dir), "%.1f%s" % (sizes, unit)])

    print('Folder-Size v1.0.0', end='\n\n')
    print(tb, end='\n\n')
    os.system("pause")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    init()
