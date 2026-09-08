# An opengl frame for pyopengl-tkinter based on ctypes (no togl compilation)
#
# Collected together by Jon Wright, Jan 2018.
#
# Based on the work of others:
#
# C + Tcl/Tk
# http://github.com/codeplea/opengl-tcltk/
# (zlib license)
# Article at:
#   https://codeplea.com/opengl-with-c-and-tcl-tk
#
# Python + Tkinter (no pyopengl)
# http://github.com/arcanosam/pytkogl/
# (The Code Project Open License)
# Article at
#  http://www.codeproject.com/Articles/1073475/OpenGL-in-Python-with-TKinter
#
# Large parts copied from pyopengl/Tk/__init__.py

__author__  = ("Jon Wright", "Mark Devenyi")
__version__ = "0.0.5"

import sys

# Platform specific frames
if sys.platform.startswith('linux'):
    import os
    use_egl = bool(os.environ.get('PYOPENGLTK_EGL'))
    if 'OpenGL.platform' not in sys.modules:
        os.environ['PYOPENGL_PLATFORM'] = (
            'egl' if use_egl else os.environ.get('PYOPENGL_PLATFORM', 'glx')
        )

    from OpenGL import platform
    from OpenGL.platform.egl import EGLPlatform
    from OpenGL.platform.glx import GLXPlatform

    if isinstance(platform.PLATFORM, EGLPlatform):
        from pyopengltk.egl_x11 import OpenGLFrame
    elif isinstance(platform.PLATFORM, GLXPlatform) and not use_egl:
        from pyopengltk.linux import OpenGLFrame
    else:
        raise ImportError("Select a matching GLX/EGL backend before importing OpenGL.")

if sys.platform.startswith('win32'):
    from pyopengltk.win32 import OpenGLFrame

# if sys.platform.startswith('darwin'):
#     from pyopengltk.darwin import OpenGLFrame

# opengl
from pyopengltk.opengl import RawOpengl
from pyopengltk.opengl import Opengl
from pyopengltk.opengl import glTranslateScene
from pyopengltk.opengl import glRotateScene
from pyopengltk.opengl import v3distsq
