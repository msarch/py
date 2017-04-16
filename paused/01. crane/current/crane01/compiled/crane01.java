import processing.core.*; 
import processing.xml.*; 

import java.applet.*; 
import java.awt.Dimension; 
import java.awt.Frame; 
import java.awt.event.MouseEvent; 
import java.awt.event.KeyEvent; 
import java.awt.event.FocusEvent; 
import java.awt.Image; 
import java.io.*; 
import java.net.*; 
import java.text.*; 
import java.util.*; 
import java.util.zip.*; 
import java.util.regex.*; 

public class crane01 extends PApplet {

/**
 * Load the Crane. 
 * Illustration by m.S. 
 * 
 * The loadShape() command is used to read simple SVG (Scalable Vector Graphics)
 * files into a Processing sketch. This library was specifically tested under
 * SVG files created from Adobe Illustrator. . 
 */

PShape crane;
PShape weight;
PShape load;
PShape arm;
PShape foot;

public void setup() {
  size(640, 360);
  smooth();
  // The file "bot1.svg" must be in the data folder
  // of the current sketch to load successfully
  crane = loadShape("crane.svg");
  weight = crane.getChild("weight");
  load = crane.getChild("load");
  arm = crane.getChild("arm");
  foot = crane.getChild("foot");
  noLoop(); // Only run draw() once
} 

public void draw(){
  background(102);
  shape(weight, 280, 40);  // Draw at coordinate (10, 10) at size 100 x 100
  shape(load, 280, 40);            // Draw at coordinate (70, 60) at the default size
  shape(arm, 280, 40);            // Draw at coordinate (70, 60) at the default size
  foot.disableStyle();
  stroke(102, 0, 0);
  shape(foot, 280, 40);            // Draw at coordinate (70, 60) at the default size
}




  static public void main(String args[]) {
    PApplet.main(new String[] { "--bgcolor=#FFFFFF", "crane01" });
  }
}
