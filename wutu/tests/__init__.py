import os
import sys
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../wutu")
sys.path.append("../../wutu/compiler")
sys.path.append("modules/")

__all__ = ["modules", "wutu", "wutu.compiler"]
