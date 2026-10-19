# -*- coding: utf-8 -*-

import os
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase
resource_add_path(os.path.abspath("./data/"))
LabelBase.register('Roboto', 'msyahei.ttf')

def run_entrypoint(entrypoint):
    import runpy
    import sys
    import os
    entrypoint_path = os.path.dirname(entrypoint)
    sys.path.append(os.path.realpath(entrypoint_path))
    runpy.run_path(
        entrypoint,
        run_name="__main__")


def run_launcher(tb=None):
    from launcher.app import Launcher
    Launcher().run()


def dispatch():
    import os

    # desktop launch
    print("dispatch!")
    entrypoint = os.environ.get("KIVYLAUNCHER_ENTRYPOINT")
    if entrypoint is not None:
        return run_entrypoint(entrypoint)

    # try android
    from kivy.utils import platform
    if platform == "android":
        try:
            from jnius import autoclass
            import traceback

            activity = autoclass("org.kivy.android.PythonActivity").mActivity

            # --- File-based entrypoint (primary mechanism) -----------------
            # The launcher writes the chosen entrypoint to this file before
            # calling System.exit(). Reading from the file is more reliable
            # than reading Intent extras because FLAG_ACTIVITY_CLEAR_TASK
            # destroys the task before Android can deliver the extras to a
            # living instance; the file survives the process restart.
            android_private = os.environ.get('ANDROID_PRIVATE', '')
            entrypoint_file = os.path.join(android_private, '.launcher_entrypoint')
            entrypoint = None
            orientation = None
            if os.path.exists(entrypoint_file):
                try:
                    with open(entrypoint_file, 'r', encoding='utf-8') as f:
                        lines = f.read().splitlines()
                    entrypoint = lines[0] if lines else None
                    orientation = lines[1] if len(lines) > 1 else ""
                    os.remove(entrypoint_file)  # consume it so launcher starts next time
                    print(f"dispatch: found entrypoint file: {entrypoint}")
                except Exception:
                    traceback.print_exc()

            # --- Intent-based entrypoint (fallback) ------------------------
            if not entrypoint:
                intent = activity.getIntent()
                entrypoint = intent.getStringExtra("entrypoint")
                orientation = intent.getStringExtra("orientation")

            if orientation == "portrait":
                activity.setRequestedOrientation(0x1)  # SCREEN_ORIENTATION_PORTRAIT
            elif orientation == "landscape":
                activity.setRequestedOrientation(0x0)  # SCREEN_ORIENTATION_LANDSCAPE
            elif orientation == "sensor":
                activity.setRequestedOrientation(0x4)  # SCREEN_ORIENTATION_SENSOR

            if entrypoint:
                try:
                    return run_entrypoint(entrypoint)
                except Exception:
                    traceback.print_exc()
                    return
        except Exception:
            import traceback
            traceback.print_exc()

    run_launcher()


if __name__ == "__main__":
    dispatch()
