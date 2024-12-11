# from RPA.Windows import Windows
from RPA.JavaAccessBridge import JavaAccessBridge
import os
import subprocess
import sys
# windows = Windows()
# jab = JavaAccessBridge(access_bridge_path=)


class JavaNotFoundException(Exception): pass
class JavaAccessBridgeNotFoundException(Exception): pass


class Desktop:
    def __init__(self):
        if not self._java_installed():
            raise JavaNotFoundException("JAVA_HOME variable not found!")
        java_home = os.environ.get("JAVA_HOME", None)
        java_bin = os.path.join(java_home, "bin")
        if not self._jab_variable_found():
            self._set_jab_variable(java_bin)
        self._activate_jab(java_bin)
        self.jab = JavaAccessBridge(access_bridge_path=self._get_jab_path(java_bin))

    def _java_installed(self):
        if "JAVA_HOME" in os.environ:
            return True
        else:
            return False

    def _jab_variable_found(self):
        if "RC_JAVA_ACCESS_BRIDGE_DLL" in os.environ:
            return True
        else:
            return False

    def _get_jab_path(self, java_bin):
        jab_path = os.path.join(java_bin, "WindowsAccessBridge-64.dll")
        if not os.path.exists(jab_path):
            raise JavaAccessBridgeNotFoundException("Java Access Bridge DLL file not found in java installation path!")
        return jab_path

    def _set_jab_variable(self, java_bin):
        os.system(f"set RC_JAVA_ACCESS_BRIDGE_DLL={self._get_jab_path(java_bin)}")

    def _activate_jab(self, java_bin):
        # enable jab
        jabswitch_path = os.path.join(java_bin, "jabswitch")
        # Construct the activation command
        activation_command = [jabswitch_path, "-enable"]
        subprocess.run(activation_command, check=True)

    def print_java_window(self):
        java_windows = self.jab.list_java_windows()
        for window in java_windows:
            print(window.title)


desktop = Desktop()
desktop.print_java_window()