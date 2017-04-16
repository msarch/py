# To change this template, choose Tools | Templates
# and open the template in the editor.


#some code to give rsvg.render_cairo(ctx) ability
#on windows.
import os
try:
    import rsvg
    WINDOWS=False
    print ("toto")
except ImportError:
    print"Warning, could not import 'rsvg'"
    if os.name == 'nt':
        print "Detected windows, creating rsvg."
        #some workarounds for windows

        from ctypes import *

        l=CDLL('librsvg-2-2.dll')
        g=CDLL('libgobject-2.0-0.dll')
        g.g_type_init()

        class rsvgHandle():
            class RsvgDimensionData(Structure):
                _fields_ = [("width", c_int),
                            ("height", c_int),
                            ("em",c_double),
                            ("ex",c_double)]

            class PycairoContext(Structure):
                _fields_ = [("PyObject_HEAD", c_byte * object.__basicsize__),
                            ("ctx", c_void_p),
                            ("base", c_void_p)]
            class props():
                def __init__(self,width,height):
                    self.width=width
                    self.height=height

            def __init__(self, path):
                self.path = path
                error = ''
                self.handle = l.rsvg_handle_new_from_file(self.path,error)
                self.props=self.props(self.get_dimension_data()[0],self.get_dimension_data()[1])

            def get_dimension_data(self):
                svgDim = self.RsvgDimensionData()
                l.rsvg_handle_get_dimensions(self.handle,byref(svgDim))
                return (svgDim.width,svgDim.height)


            def render_cairo(self, ctx):
                ctx.save()
                z = self.PycairoContext.from_address(id(ctx))
                l.rsvg_handle_render_cairo(self.handle, z.ctx)
                ctx.restore()



        class rsvgClass():
            def Handle(self,file):
                return rsvgHandle(file)

        rsvg = rsvgClass()
