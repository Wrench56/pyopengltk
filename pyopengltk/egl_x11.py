from __future__ import print_function
import logging
from ctypes import c_char_p, c_void_p, cdll, POINTER, util
from OpenGL import GL, EGL
from pyopengltk.base import BaseOpenGLFrame

_log = logging.getLogger(__name__)

_x11lib = cdll.LoadLibrary(util.find_library("X11"))
XOpenDisplay = _x11lib.XOpenDisplay
XOpenDisplay.argtypes = [c_char_p]
XOpenDisplay.restype = c_void_p

_config_attrs = [
    EGL.EGL_SURFACE_TYPE,
    EGL.EGL_WINDOW_BIT,
    EGL.EGL_RENDERABLE_TYPE,
    EGL.EGL_OPENGL_BIT,
    EGL.EGL_RED_SIZE,
    8,
    EGL.EGL_GREEN_SIZE,
    8,
    EGL.EGL_BLUE_SIZE,
    8,
    EGL.EGL_DEPTH_SIZE,
    16,
    EGL.EGL_NONE,
]

_ctx_attrs = [
    EGL.EGL_CONTEXT_MAJOR_VERSION,
    3,
    EGL.EGL_CONTEXT_MINOR_VERSION,
    3,
    EGL.EGL_CONTEXT_OPENGL_PROFILE_MASK,
    EGL.EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT,
    EGL.EGL_NONE,
]


def _arr(values):
    return (EGL.EGLint * len(values))(*values)


class OpenGLFrame(BaseOpenGLFrame):
    def tkCreateContext(self):
        self.update_idletasks()

        xdisplay = XOpenDisplay(self.winfo_screen().encode("utf-8"))
        self.__display = EGL.eglGetDisplay(xdisplay)
        if self.__display == EGL.EGL_NO_DISPLAY:
            _log.error("eglGetDisplay() failed")

        major = EGL.EGLint()
        minor = EGL.EGLint()
        if not EGL.eglInitialize(self.__display, major, minor):
            _log.error("eglInitialize() failed: 0x%x", EGL.eglGetError())
        _log.info("EGL version: %d.%d", major.value, minor.value)

        if not EGL.eglBindAPI(EGL.EGL_OPENGL_API):
            _log.error("eglBindAPI() failed: 0x%x", EGL.eglGetError())

        configs = (EGL.EGLConfig * 1)()
        n = EGL.EGLint()
        if (
            not EGL.eglChooseConfig(self.__display, _arr(_config_attrs), configs, 1, n)
            or n.value == 0
        ):
            _log.error("eglChooseConfig() failed: 0x%x", EGL.eglGetError())
        self.__config = configs[0]

        self.__surface = EGL.eglCreateWindowSurface(self.__display, self.__config, self._wid, None)
        if self.__surface == EGL.EGL_NO_SURFACE:
            _log.error("eglCreateWindowSurface() failed: 0x%x", EGL.eglGetError())

        self.__context = EGL.eglCreateContext(
            self.__display, self.__config, EGL.EGL_NO_CONTEXT, _arr(_ctx_attrs)
        )
        if self.__context == EGL.EGL_NO_CONTEXT:
            _log.error("eglCreateContext() failed: 0x%x", EGL.eglGetError())

        EGL.eglMakeCurrent(self.__display, self.__surface, self.__surface, self.__context)

    def tkMakeCurrent(self):
        if self.winfo_ismapped() and hasattr(self, "_OpenGLFrame__context"):
            EGL.eglMakeCurrent(self.__display, self.__surface, self.__surface, self.__context)

    def tkSwapBuffers(self):
        if self.winfo_ismapped() and hasattr(self, "_OpenGLFrame__context"):
            EGL.eglSwapBuffers(self.__display, self.__surface)
