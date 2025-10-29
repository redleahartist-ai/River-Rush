import importlib
import project_ui

importlib.reload(project_ui)

def run():
    try:
        global river_rush_ui_instance
        river_rush_ui_instance.close()
        river_rush_ui_instance.deleteLater()
    except:
        pass

    river_rush_ui_instance = project_ui.project_ui()
    river_rush_ui_instance.show()
    return river_rush_ui_instance