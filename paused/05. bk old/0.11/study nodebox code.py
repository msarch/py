


#==============================================================================

#--- CANVAS CLASS (EXTRACTS) --------------------------------------------------

    def _setup(self):
        # Set the window color, this will be transparent in saved images.
        glClearColor(VERY_LIGHT_GREY, VERY_LIGHT_GREY, VERY_LIGHT_GREY, 0)
        # Reset the transformation state.
        # Most of this is already taken care of in Pyglet.
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #glOrtho(0, self.width, 0, self.height, -1, 1)
        #glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # Enable line anti-aliasing.
        glEnable(GL_LINE_SMOOTH)
        # Enable alpha transparency.
        glEnable(GL_BLEND)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Start the application (if not already running).
        if not self._active:
            self._window.switch_to()
            self._window.dispatch_events()
            self._window.set_visible()
            self._active = True
        self.clear()
        self.setup()

    def _draw(self):
        """ Draws the layers.
            This method gives the same result each time it gets drawn; only _update() advances state.
        """
        glPushMatrix()
        for layer in self:
            layer._draw()
        glPopMatrix()


    def _update(self, lapse=0):
        """ Updates the canvas and its layers.
            This method does not actually draw anything, it only updates the state.
        """
        self._elapsed = lapse
        # Advance the animation by updating all layers.
        # This is only done when the canvas is not paused.
        # Events will still be propagated during pause.
        global TIME; TIME = time()
        self._frame += 1
        self.update()
        for layer in self:
            layer._update()

    def stop(self):
        # If you override this method, don't forget to call Canvas.stop() to exit the app.
        # Any user-defined stop method, added with canvas.set_method() or canvas.run(stop=stop),
        # is called first.
        try: self._user_defined_stop()
        except:
            pass
        for f in (self._update, self._draw):
            pyglet.clock.unschedule(f)
        self._window.close()
        self._active = False
        pyglet.app.exit()

    def clear(self):
        """ Clears the previous frame from the canvas.
        """
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glClear(GL_STENCIL_BUFFER_BIT)

    def run(self, draw=None, setup=None, update=None, stop=None):
        """ Opens the application windows and starts drawing the canvas.
        """
        pyglet.app.run()

    def render(self):
        """ Returns a screenshot of the current frame as a texture.
            This texture can be passed to the image() command.
        """
        return pyglet.image.get_buffer_manager().get_color_buffer().get_texture()

    def save(self, path):
        """ Exports the current frame as a PNG-file.
        """
        pyglet.image.get_buffer_manager().get_color_buffer().save(path)
