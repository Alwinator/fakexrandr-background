from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction


def show_icon(args, update_picture, set_spanned):
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    # Adding an icon
    icon = QIcon(":icon/fakexrandr_background_64.png")

    # Adding item on the menu bar
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Creating the options
    menu = QMenu()

    m1 = QAction("fakexrandr-background")
    menu.addAction(m1)
    menu.addSeparator()

    info_menu = menu.addMenu("Info")

    i1 = QAction(f"Picture Folder: {args.picture_folder}")
    info_menu.addAction(i1)

    i2 = QAction(f"Change Duration: {args.change_duration}")
    info_menu.addAction(i2)

    i3 = QAction(f"Startup Delay: {args.delay}")
    info_menu.addAction(i3)

    m2 = QAction("Update picture")
    m2.triggered.connect(update_picture)
    menu.addAction(m2)

    m3 = QAction("Set spanned")
    m3.triggered.connect(set_spanned)
    menu.addAction(m3)

    # To quit the app
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    # Adding options to the System Tray
    tray.setContextMenu(menu)
    app.exec_()
