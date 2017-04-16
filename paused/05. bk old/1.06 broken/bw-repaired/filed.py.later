

#--- create_output_dir --------------------------------------------------------
def make_a_dir():
    abspath = os.path.abspath(__file__)
    parent = os.path.dirname(os.path.dirname(abspath))
    imgdir = os.path.join (parent, 'out')
    try:
        os.makedirs(imgdir)
    except OSError:
        pass
    os.chdir(imgdir)

#--- write pic to disk --------------------------------------------------------
def save_a_frame(frame):
    n = str(frame).zfill(5)
    filename = "fr_" + n + '.png'
    pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
    print ' --> ', filename

#--- export image loop ----------------------------------------------------
def export_loop():
    global chrono, frame
    while chrono < movie_duration:
        chrono += DT
        frame += 1
        rules.tick(dt)
        # tick with the constant DT, regardless of real time interval
        # so that even if refresh is slow no frame should be missing
        glClear(GL_COLOR_BUFFER_BIT)
        shapes.paint()
        save_a_frame(frame)
        print(frame)
    print 'done'
    print'image dir is : ', os.getcwd()
    exit(0)

#--- run mode options 2 : file export of image files --------------------------
def export(duration):
    field.view_setup()
    #clock.schedule_interval_soft(export_loop, MOVIE FRAMERATE)
    pyglet.app.run()
    export_loop()



