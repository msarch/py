
#!/usr/bin/env python
# To change this template, choose Tools | Templates
# and open the template in the editor.
import pyglet.window
import pyglet
import squirtle
from pyglet import clock
from pyglet import window
from pyglet.gl import *
from pyglet.window import key
import xml.etree.ElementTree
from xml.etree.cElementTree import parse
from pyglet.window import mouse
import cairo
import rsvg_di

import logging
import os

class button():
    def __init__(self,x,y,width,height,color,hovercolor,text):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.hovercolor=hovercolor
        self.text=text
        self.ismouseover=False
        self.ismovable=False
        self.isclicked=False
        self.isvisible=True
    def set_position(self,x,y):
        self.x=x
        self.y=y

        
    def check_mouse_position(self,mousex,mousey,mousedx,mousedy,mousestate):
        if mousex>self.x and mousex<self.x+self.width and mousey>self.y and mousey<self.y+self.height:
            self.ismouseover=True
            self.isclicked=mousestate
            
            if self.ismovable==True:
                if mousestate == True:
                    self.x+=mousedx
                    self.y+=mousedy
 
        else:
            self.ismouseover=False

    def on_mouse_moved(self,mousex,mousey,mousedx,mousedy):
        pass
    
    def on_clicked(self,mousex,mousey):
        if mousex>self.x and mousex<self.x+self.width and mousey>self.y and mousey<self.y+self.height:
            self.ismouseover=True
            self.isclicked=True
            return True

    def on_released(self):
        self.isclicked=False
        
    
    def draw2(self,x,y):
        if self.isvisible==True:
            color=self.color
            if self.ismouseover==True:
                color=self.hovercolor
            self.draw_rect(x, y, self.width,self.height, color)
            self.textlabel = pyglet.text.Label(self.text,'Arial',font_size=25, x=x+5, y=y+5,color=(0,0,0,255))
            self.textlabel.draw()
            
    def draw(self):
        if self.isvisible==True:
            color=self.color
            if self.ismouseover==True:
                color=self.hovercolor
            self.draw_rect(self.x, self.y, self.width,self.height, color)
            self.textlabel = pyglet.text.Label(self.text,'Arial',font_size=25, x=self.x+5, y=self.y+5,color=(0,0,0,255))
            self.textlabel.draw()
        
    def draw_rect(self, x, y,width,height,color):
        pyglet.graphics.draw_indexed(4,GL_TRIANGLES,[0, 1, 2, 0, 2, 3],
                                         ('v2i', (x, y,x+width, y,x+width, y+height,x, y+height)),
                                          ('c3B',(color[0],color[1],color[2],color[0],color[1],color[2],color[0],color[1],color[2],color[0],color[1],color[2]))

                                         )


class scrollbar(button):
    def __init__(self,x,y,width,height,color,hovercolor,scrollcolor,text,vertical=True,lines=1):
            button.__init__(self, x,y,width,height,color,color,"")
            self.vertical=vertical
            self.lines=lines
            self.index=0
            #self.scrollbutton=button(x,y+height-width,width,width,scrollcolor,hovercolor,"")
            self.scrollbutton=button(x,y+height-height/lines,width,height/lines,scrollcolor,hovercolor,"")
            self.scrollbutton.ismovable=True
            
    def check_mouse_position(self,mousex,mousey,mousedx,mousedy,mousestate):
        if self.lines>0:
            if self.scrollbutton.y+self.height/self.lines>self.y+self.height:
                self.scrollbutton.y=self.y+self.height-self.height/self.lines
            elif self.scrollbutton.y<self.y:
                self.scrollbutton.y=self.y
            self.scrollbutton.check_mouse_position(mousex,mousey,mousedx,mousedy,mousestate)
            self.scrollbutton.x=self.x
            self.index=self.lines-((self.scrollbutton.y-self.y)/self.scrollbutton.height)
            self.index-=1
            if self.index<0:
                self.index=0
            if self.index>=self.lines:
                self.index=self.lines-1
        #print(self.scrollbutton.y," ",self.y)
        #print(self.index)
        

    def draw(self):
        if self.lines>1:
            button.draw(self)
            self.scrollbutton.draw()
            
class svgbutton(button):
    def __init__(self,x,y,width,height,color,hovercolor,text,filename):
            button.__init__(self, x,y,width,height,color,hovercolor,"")
            self.filename=filename
            self.svg=squirtle.SVG(filename, bezier_points=150, circle_points=150)
    def draw(self):
        button.draw(self)
        self.svg.draw(self.x, self.y, angle=0, scale=0.1)
        
    def draw2(self,x,y):
        button.draw2(self,x,y)
        self.svg.draw(x, y, angle=0, scale=0.1)
    
###########################
class glasswarecontainer(button):
    def __init__(self,x,y,width,height,headerheight,color,hovercolor,headercolor,text,containees):
            button.__init__(self, x,y,width,height,color,color,text)
            self.headerheight=headerheight

            self.elementwidth=(self.width-20)/3
            self.elementheight=self.height
            self.containees=[]

            
            i=0
            for subdir, dirs, files in os.walk("./res/"+self.text+"/"):
                for file in files:
                    print("file",file)
                    (shortname, extension) = os.path.splitext(file)
                    if extension ==".svg":
                        el=svgbutton(self.x+i,self.y,self.elementwidth,self.elementheight,(125,125,125),(255,120,0),"","./res/"+self.text+"/"+file)
                        el.ismovable=False
                        self.containees.append(el)
                        i+=self.elementwidth
            
            
            self.header=button(x,y+height,width,headerheight,headercolor,hovercolor,text)
            self.header.ismovable=True
            self.ismovable=False
            self.selectedelement=None
            tmp=len(self.containees)/(self.width/(self.elementwidth+30))

            self.scrollbar=scrollbar(x+width-20,y,20,self.elementheight,(125,125,125),(255,120,0),(0,120,255),"text",True,tmp+1)
            
    
        

    def check_mouse_position(self,mousex,mousey,mousedx,mousedy,mousestate):
        #self.header.check_mouse_position(mousex,mousey,mousedx,mousedy,mousestate)
        self.scrollbar.check_mouse_position(mousex,mousey,mousedx,mousedy,mousestate)
        #self.x=self.header.x
        #self.y=self.header.y-self.height
        #self.scrollbar.set_position(self.x+self.width-20,self.y)
        
        min=(self.scrollbar.index)*3
        max=len(self.containees)
        
        if max>3*(self.scrollbar.index+1):
            max=3*(self.scrollbar.index+1)
        u=0
        for i in range(min,max):
            self.containees[i].x=self.x+u*self.elementwidth
            self.containees[i].y=self.y
            u+=1

        i=0
        for element in self.containees:
            element.check_mouse_position(mousex,mousey,mousedx,mousedy,mousestate)
            #element.x=self.x+i
            #element.y=self.y
            i+=self.elementwidth
               #if element.isclicked == True:
                   #self.selectedelement=element
                   #print (element.filename)

                   
    def on_clicked(self,mousex,mousey):
        min=(self.scrollbar.index)*3
        max=len(self.containees)

        if max>3*(self.scrollbar.index+1):
            max=3*(self.scrollbar.index+1)
        u=0
        for i in range(min,max):
            self.containees[i].on_clicked(mousex,mousey)
            if self.containees[i].isclicked == True:
                   self.selectedelement=self.containees[i]
        #i=0
        #for element in self.containees:
            #element.on_clicked(mousex,mousey)
            #element.x=self.x+i
            #element.y=self.y
            #i+=self.elementwidth
            #if element.isclicked == True:
                   #self.selectedelement=element
                  

    def draw(self):
            button.draw(self)
            self.header.draw()
            self.scrollbar.draw()

            min=(self.scrollbar.index)*3

            max=len(self.containees)
            if max>3*(self.scrollbar.index+1):
                max=3*(self.scrollbar.index+1)
            u=0
            for i in range(min,max):
                self.containees[i].draw2(self.x+u*self.elementwidth,self.y)
                u+=1
            #print(min," ",max)
            
                
                

    def draw_rect(self, x, y,width,height,color):
            pyglet.graphics.draw_indexed(4,GL_TRIANGLES,[0, 1, 2, 0, 2, 3],
                                             ('v2i', (x, y,x+width, y,x+width, y+height,x, y+height)),
                                              ('c3B',(color[0],color[1],color[2],color[0],color[1],color[2],color[0],color[1],color[2],color[0],color[1],color[2]))

                                             )

class main(pyglet.window.Window):
    """
    Main class for the visual interface
    """
    def __init__(self, width=320,  height=240, resizable=True, visible=True):
        super(main, self).__init__(resizable=resizable)
        self.svg = None
        self.width=width
        self.height=height
        squirtle.setup_gl()
        self.text=""
        self.set_mouse_visible(True)
        self.set_caption('Labglass Prototype')
        icon1 = pyglet.image.load('./res/icon.png')
        self.set_icon(icon1)


      
        self.scrollbar=scrollbar(400,350,30,200,(125,125,125),(255,120,0),(0,120,255),"text",True)
        self.savebutton=button(10,100,100,30,(125,125,125),(255,120,0),"Save")
        self.exportbutton=button(10,50,100,30,(125,125,125),(255,120,0),"Export")
        self.loadbutton=button(10,200,100,30,(125,125,125),(255,120,0),"Load")
        self.ismousedown=False

        self.selectedelement=None
        self.exportimageindex=0

        self.testcontainer=glasswarecontainer(10,300,250,150,30,(200,200,200),(255,120,0),(0,120,255),"glass",[""])
        self.linkcontainer=glasswarecontainer(10,100,250,150,30,(200,200,200),(255,120,0),(0,120,255),"links",["arrow_0.svg"])

    def scan_element(self,parent):
        for e in parent.getchildren():
            print(e.tag)
            self.scan_element(e)
            
    def find_element(self,parent,tofind):
        for e in parent.getchildren():
            if e.get("id") != tofind:
                self.find_element(e,tofind)
            else:
                self.toto=e
         
    def save_toxml_old(self):
        if self.svg is not None:
            if open(self.svg.filename, 'rb').read(3) == '\x1f\x8b\x08': #gzip magic numbers
                import gzip
                f = gzip.open(self.svg.filename, 'rb')
            else:
                f = open(self.svg.filename, 'rb')
                self.tree = parse(f)
                
                try:
                    textid=self.svg.textList[0][0][0]
                    self.find_element(self.tree._root,textid)
                    element=self.toto
                    
                    if element is not None:
                        element.text=self.text
                        
                        if not os.path.isdir("exports"):
                            os.mkdir("exports")
                        #tmp1=self.svg.filename[:len(self.svg.filename)-3]+"_0.svg"
                        newfileName="./exports/"+self.svg.filename[12:len(self.svg.filename)-3]+"_0.svg"
                       
                        #print(newfileName)
                        self.tree.write(newfileName)

                    else:
                        print("not found")
                        # tspan=(tmp.get('id'),tmp.text)
                except:
                    print("error")


    def save_experiment(self,filename):
        pass

    def save_toxml(self,filename):
        """
        Saving the current schematic to xml
        Params:
        Filename: the filename to save it to
        """
        if self.svg is not None:
            if open(self.svg.filename, 'rb').read(3) == '\x1f\x8b\x08': #gzip magic numbers
                import gzip
                f = gzip.open(self.svg.filename, 'rb')
            else:
                f = open(self.svg.filename, 'rb')
                self.tree = parse(f)

                try:
                    textid=self.svg.textList[0][0][0]
                    self.find_element(self.tree._root,textid)
                    element=self.toto

                    if element is not None:
                        element.text=self.text
                        if not os.path.isdir("exports"):
                            os.mkdir("exports")
                        self.tree.write(filename)

                    else:
                        pass
                        # tspan=(tmp.get('id'),tmp.text)
                except:
                    self.tree.write(filename)

    def save_tosvg(self,source,filename):
        """
        Saving the current schematic to svg
        Params:
        Source: the original svg schematic element
        Filename: the filename to save it to
        """
        try:
            svg = rsvg_di.rsvg.Handle(source)
            width = svg.props.width
            height = svg.props.height
            surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
            cr = cairo.Context (surface)


            wscale = float (width) / svg.props.width
            hscale = float (height) / svg.props.height
            cr.scale (wscale, hscale)
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(0, 0, width, height)
            cr.fill()

            svg.render_cairo (cr)
            surface.write_to_png (filename)
        except:
            print("error exporting to png")

        
    def on_draw(self):
        
        if self.testcontainer.selectedelement is not None:
            self.svg=self.testcontainer.selectedelement.svg
            if len(self.svg.textList)>0:
                self.text=str(self.svg.textList[0][0][1])
            self.selectedelement=self.testcontainer.selectedelement
            self.testcontainer.selectedelement=None
            
            #self.svgtmp.draw()

        self.draw_rect(0, 0, self.width, self.height,  (255,255,255))
        #self.draw_rect(10, 100, 100, 30,  (125,125,125))

        if self.svg is not None:
            self.svg.draw(self.width/2, 0, angle=0, scale=0.52)
            textGfx = pyglet.text.Label("Titrage:"+self.text,'Arial',font_size=30, x=10, y=10,color=(0,0,0,255))
            textGfx.draw()

        #testText=pyglet.text.layout.IncrementalTextLayout(width=100, height=30, multiline=True)
        #testText.draw()



        #self.savebutton.draw()
        self.exportbutton.draw()
        #self.loadbutton.draw()
        self.testcontainer.draw()
        self.linkcontainer.draw()
        self.scrollbar.draw()
        
    def on_mouse_motion(self, x, y, dx, dy):
        #self.savebutton.check_mouse_position(x,y,dx,dy,self.ismousedown)
        self.exportbutton.check_mouse_position(x,y,dx,dy,self.ismousedown)
        #self.loadbutton.check_mouse_position(x,y,dx,dy,self.ismousedown)
        self.testcontainer.check_mouse_position(x,y,dx,dy,self.ismousedown)
        self.linkcontainer.check_mouse_position(x,y,dx,dy,self.ismousedown)
        self.scrollbar.check_mouse_position(x,y,dx,dy,self.ismousedown)
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button==mouse.LEFT:
            self.testcontainer.on_clicked(x,y)
            self.linkcontainer.on_clicked(x,y)

            if self.exportbutton.on_clicked(x,y)==True:
               
                filename="./exports/"+self.svg.filename[12:len(self.svg.filename)-3]+str(self.exportimageindex)
                self.save_toxml(filename+".svg")
                self.save_tosvg(filename+".svg",filename+".png")
                #pyglet.image.get_buffer_manager().get_color_buffer().get_region(400, 0, self.width-450, self.height).save('./exports/export'+str(self.exportimageindex)+'.png')
                self.exportimageindex+=1
                

        elif button==mouse.RIGHT:
            pass
           
    def on_mouse_release(self, x, y, button, modifiers):
        self.testcontainer.on_released()
        self.linkcontainer.on_released()

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.savebutton.check_mouse_position(x,y,dx,dy,True)
        self.exportbutton.check_mouse_position(x,y,dx,dy,True)
        self.loadbutton.check_mouse_position(x,y,dx,dy,True)
        self.testcontainer.check_mouse_position(x,y,dx,dy,True)
        self.linkcontainer.check_mouse_position(x,y,dx,dy,True)
        self.scrollbar.check_mouse_position(x,y,dx,dy,True)
        
    def on_text(self, text):
        self.text+=text
        if self.svg is not None:
            self.svg.text=self.text
            
        
    def on_key_press(self,symbol, modifiers):
      
        
        if symbol == key.RETURN:
            pass
        elif symbol==key.BACKSPACE:
            if len(self.text)>0:
                self.text=self.text[0:len(self.text)-1]
                if self.svg is not None:
                    self.svg.text=self.text
       
        #print(self.text)

    def convert_rgb(self, r,g,b):
        return (float(r)/255,float(g)/255,float(b)/255)

    def draw_rect(self, x, y,width,height,color):
        pyglet.graphics.draw_indexed(4,GL_TRIANGLES,[0, 1, 2, 0, 2, 3],
                                         ('v2i', (x, y,x+width, y,x+width, y+height,x, y+height)),
                                          ('c3B',(color[0],color[1],color[2],color[0],color[1],color[2],color[0],color[1],color[2],color[0],color[1],color[2]))

                                         )



if __name__ == '__main__':
    app=main(1024, 600)
    pyglet.app.run()



