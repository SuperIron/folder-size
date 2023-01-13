import os
import prettytable as pt
from PyQt5 import QtWidgets
import sys


def get_directory():
    app = QtWidgets.QApplication([])
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
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    else:
        path = get_directory()
    tb = get_tb(path)
    logs = []
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
        new_sizes, unit = get_unit(sizes)
        logs.append({
            'sizes': sizes,
            'row': ["%s" % (child_dir), "%.1f%s" % (new_sizes, unit)]
        })
    logs = sorted(logs, key=lambda item: item['sizes'])
    for log in logs:
        tb.add_row(log['row'])
    print('Folder-Size v1.0.0', end='\n\n')
    print(tb, end='\n\n')
    os.system("pause")


if __name__ == '__main__':
    init()
