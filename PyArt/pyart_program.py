import sys, keyboard
from PyQt6 import QtWidgets
from PyQt6 import uic, QtCore, QtGui
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QShortcut, QKeySequence


class Object():
 
    def new_object(self, resource, name):
        self.object_name = name

        self.scale_factor = 1
        
        self.pixmap = QtGui.QPixmap(resource)
        self.qpxmap = QtWidgets.QGraphicsPixmapItem()
        self.qpxmap.setPixmap(self.pixmap)

        self.scene  = QtWidgets.QGraphicsScene()
        
        self.scene.addItem(self.qpxmap)
        self.scene.setSceneRect(self.qpxmap.boundingRect())
        
        self.brush_mouse = QtWidgets.QGraphicsEllipseItem()
        self.scene.addItem(self.brush_mouse)

        
class Example(QtWidgets.QMainWindow):

    
    def __init__(self):
        super().__init__()
        #this list will contain all images in the running program
        self.object_list = []


        #ui design
        uic.loadUi("design.ui", self)
        
        #app title
        self.title.setText("PyArt")
        
        #default wallpaper buttons. configure them with the function "add_new_image" passing the path and the object title.
        
        self.add_empty.clicked.connect(lambda: self.add_new_image("resource/empty_object.png","new_image"))
        self.add_sphere.clicked.connect(lambda: self.add_new_image("resource/sphere_object.png","sphere"))
        self.add_cube.clicked.connect(lambda: self.add_new_image("resource/cube_object.png","cube"))
        self.add_cone.clicked.connect(lambda: self.add_new_image("resource/cone_object.png","cone"))
        self.add_dodecahedron.clicked.connect(lambda: self.add_new_image("resource/dodecahedron_object.png","dodecahedron"))
        self.add_landscape1.clicked.connect(lambda: self.add_new_image("resource/landscape_1.jpg","green_landscape"))
        self.add_landscape2.clicked.connect(lambda: self.add_new_image("resource/landscape_2.jpg","pink_landscape"))
        self.add_male_face.clicked.connect(lambda: self.add_new_image("resource/male","male_face"))
        self.add_female_face.clicked.connect(lambda: self.add_new_image("resource/female","female_face"))
       
        #when a item in the qtreewidget is pressed, calls "artworl_list" 
        self.treeWidget.itemPressed.connect(lambda: self.artwork_list(self.treeWidget.currentItem().text(0)))
         
        
        #true when the user is clicking the qgraphicsview
        self.drawing = False
        
        #the user only can draw when a image is currently selected
        self.canDraw = False
        
        #used to stop repeat calls
        self.brush_size_with_mouse = True
        
        #brush-size adjust with alt + mouse move. this parameters saves the initial states
        self.start_mouse_position = 0
        self.start_brush_size = 0
        
        #brush size and color
        self.brushSize = self.spinbox_br_size.value()
        self.brush_color = Qt.GlobalColor.black
        #for the paint function
        self.lastPoint = QPoint()
        
        #add shadow effect to buttons  
        self.shadowFrame(self.scrollAreaWidgetContents.children())
        self.shadowFrame(self.tools.children())
        self.shadowFrame([self.bt_color,self.hide_left, self.show_left],0,0)

        
#---------------------------------window management--------------------------------------
        
        #frameless window
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(1)
        
        #resize widget
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        
        #upper buttons
        self.upper_minimize.clicked.connect(self.minimize)
        self.upper_minimize_size.clicked.connect(self.windowed)
        self.upper_maximize_size.clicked.connect(self.maximize)
        self.upper_close.clicked.connect(lambda: self.close())
        self.upper_minimize_size.hide()
        self.upper_frame.mouseMoveEvent = self.move_window
        
        #hide/show menu
        self.show_left.hide()
        self.show_right.hide()
        
        self.show_left.clicked.connect(lambda: self.hideshow(self.left_frame, "left"))
        self.show_right.clicked.connect(lambda: self.hideshow(self.right_frame, "right"))
        self.hide_left.clicked.connect(lambda: self.hideshow(self.left_frame, "left"))
        self.hide_right.clicked.connect(lambda: self.hideshow(self.right_frame, "right"))
        
                

        
        #tool buttons
        self.bt_save.clicked.connect(self.save)
        self.bt_load.clicked.connect(self.load)
        
        
        self.bt_delete.clicked.connect(self.delete_object)
        self.bt_color.clicked.connect(self.brushColor)
        self.spinbox_br_size.valueChanged.connect(self.apply_size)
        
        self.zoom_in.clicked.connect(lambda: self.zoom_function(True))
        self.zoom_out.clicked.connect(lambda: self.zoom_function(False))
        
        
        #shortcuts

        shc_save = QShortcut(QKeySequence("Ctrl+s"),self)
        shc_save.activated.connect(self.save)

        shc_load = QShortcut(QKeySequence("Ctrl+o"),self)
        shc_load.activated.connect(self.load)

        shc_load = QShortcut(QKeySequence("Del"),self)
        shc_load.activated.connect(self.delete_object)

        shc_zoom_in = QShortcut(QKeySequence("Ctrl++"),self)
        shc_zoom_in.activated.connect(lambda: self.zoom_function(True))

        shc_zoom_out = QShortcut(QKeySequence("Ctrl+-"),self)
        shc_zoom_out.activated.connect(lambda: self.zoom_function(False))

        shc_size_up = QShortcut(QKeySequence(Qt.Key.Key_Up),self)
        shc_size_up.activated.connect(lambda: self.spinbox_br_size.setValue(self.spinbox_br_size.value() + 1))

        shc_size_down = QShortcut(QKeySequence(Qt.Key.Key_Down),self)
        shc_size_down.activated.connect(lambda: self.spinbox_br_size.setValue(self.spinbox_br_size.value() - 1))

        shc_brush_color = QShortcut(QKeySequence("C"),self)
        shc_brush_color.activated.connect(self.brushColor)

        
    def hideshow(self, menu, position):

        width = menu.width()
        extender = 0
        if width == 0:
            extender = 200
            if position == "left":
                self.show_left.hide()
                self.hide_left.show()
            else:
                self.show_right.hide()
                self.hide_right.show()
            
        if width == 200:
            extender = 0
            if position == "left":
                self.show_left.show()
                self.hide_left.hide()
            else:
                self.show_right.show()
                self.hide_right.hide()
        #animation
        self.animacion = QtCore.QPropertyAnimation(menu, b"maximumWidth")
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setDuration(500)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.animacion.start()
        


    #upper buttons
    def minimize(self):
        self.showMinimized()
        
        
    def windowed(self):
        self.showNormal()
        self.upper_minimize_size.hide()
        self.upper_maximize_size.show()
    
    
    def maximize(self):
        self.showMaximized()
        self.upper_maximize_size.hide()
        self.upper_minimize_size.show()
    
    
    def move_window(self,event):
        if self.isMaximized() == False:
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.clickPosition)
                self.clickPosition = event.globalPosition().toPoint()
                event.accept()
                

        if event.globalPosition().toPoint().y() <= 12:
            self.maximize()     

        else:
            self.windowed()
        
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPosition().toPoint()
            
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)
    
    #add shadows to the entered list of widget. you can also put x and y offset, and shadow color.
    def shadowFrame(self, frames,x=10, y=10, color = QtGui.QColor(0,0,0,200)):
        for frame in range(len(frames)):
            #this is because of the layouts contained in the widgets, which throw an exception if they are not excluded.
            if (type(frames[frame]) != QtWidgets.QVBoxLayout) & (type(frames[frame]) != QtWidgets.QHBoxLayout) & (type(frames[frame]) != QtWidgets.QGridLayout) :
                shadow =  QtWidgets.QGraphicsDropShadowEffect(self)
                shadow.setBlurRadius(30)
                shadow.setXOffset(x)
                shadow.setYOffset(y)
                shadow.setColor(color)
                frames[frame].setGraphicsEffect(shadow)
                
    #self.zoom_function(True) --> zoom + /// self.zoom_function(False) --> zoom -
    def zoom_function(self, zoom):
        if zoom:
            self.current_object.scale_factor = 1.2
        else: 
            self.current_object.scale_factor = 0.8
           
        self.graphicsView.scale(self.current_object.scale_factor, self.current_object.scale_factor)

#------------------------------------------------------------------------------------------
    #add the object name as a qtree item
    def add_new_image(self, resource, name):
        my_object = Object()
        my_object.new_object(resource,name)
        
        for obj in self.object_list:
            #this is so that no two objects have the same names. 
            # if an attempt is made to add an object with an existing name, 
            # a "_0" is added to it. if it occurs again, "_1", "_2", and continues adding to infinity.
            
            if my_object.object_name == obj.object_name:
                digits = 0
                if my_object.object_name[-1].isnumeric():
                    for digit in enumerate(my_object.object_name):
                        if my_object.object_name[digits-1].isnumeric():
                            digits+=-1
                    else:
                        a = int(my_object.object_name[digits:])
                        b = a+1
                        my_object.object_name = my_object.object_name.replace(str(a), str(b))
                else:
                    my_object.object_name += "_0"
                       
        self.object_list.append(my_object)
        item = QtWidgets.QTreeWidgetItem(self.treeWidget, [my_object.object_name])   
        item.setIcon(0, QtGui.QIcon("resource/landscape"))


    #show an specific image depending the current selection of treeWidget.
    def artwork_list(self, name):

        for object in self.object_list:
            if name == object.object_name:
                self.current_object = object
                #sets canDraw to true so that the brush is enabled.
                self.canDraw = True
                
        self.graphicsView.setScene(self.current_object.scene) 
        self.title.setText(f"PyArt - {self.current_object.object_name}")

        #--paint parameters
        self.current_object.scene.mouseMoveEvent = self.mouseMovementEvent
        self.current_object.scene.mousePressEvent = self.mousePressedEvent
        #for the ellipse of the brush
        self.graphicsView.setMouseTracking(True)
        self.current_object.brush_mouse.setRect(0,0, self.brushSize, self.brushSize)

    # |DEL| --> self.delete_object(self)
    
    def delete_object(self):
        if self.canDraw:
            self.object_list.remove(self.current_object)
            self.treeWidget.takeTopLevelItem(self.treeWidget.currentIndex().row())
            self.graphicsView.setScene(None)
            
            #drawing is disabled since now there is no image on the screen
            self.canDraw = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

         
    def mousePressedEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.canDraw:
                self.drawing = True
                self.lastPoint = event.scenePos().toPoint()
                
                painter = QtGui.QPainter(self.current_object.pixmap)
                painter.setPen(QtGui.QPen(self.brush_color, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
                painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
                painter.drawPoint(event.scenePos().toPoint())
                
                
                #///update image///
                self.current_object.qpxmap.setPixmap(self.current_object.pixmap)
                

        
        
    def mouseMovementEvent(self, event):
        #pretty draw cursor
        self.setCursor(QtGui.QCursor(QtGui.QPixmap("resource/paint_cursor.png")))
        
        #brush ellipse settings
        self.mouse_curr_point = event.scenePos()
        self.current_object.brush_mouse.setX(self.mouse_curr_point.x() - self.brushSize/2)
        self.current_object.brush_mouse.setY(self.mouse_curr_point.y() - self.brushSize/2)
        
        
        #---brush size with mouse movement
        if keyboard.is_pressed("Alt"):
            if self.brush_size_with_mouse:
                self.start_mouse_position = self.mouse_curr_point.x()
                self.start_brush_size = self.spinbox_br_size.value()
                self.brush_size_with_mouse = False
            self.spinbox_br_size.setValue(int(self.start_brush_size + (self.start_mouse_position - self.mouse_curr_point.x()) *-1))
        else:
            self.brush_size_with_mouse = True
            
        #paint function
        if (event.buttons() == Qt.MouseButton.LeftButton) & self.drawing:
            painter = QtGui.QPainter(self.current_object.pixmap)

            
            painter.setPen(QtGui.QPen(self.brush_color, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawLine(self.lastPoint, event.scenePos().toPoint())

            self.lastPoint = event.scenePos().toPoint()

            #///update image///
            self.current_object.qpxmap.setPixmap(self.current_object.pixmap)


                  
    def mouseReleaseEvent(self, event):
        if event.button == Qt.MouseButton.LeftButton:
            self.drawing = False



    def brushColor(self):
            color = QtWidgets.QColorDialog.getColor()
            self.brush_color = color
            self.bt_color.setStyleSheet(f"background-color: rgba{color.getRgb()}; border:3px solid rgb(70, 70, 70)") 
            self.shadowFrame([self.bt_color],0,0, color)
            
    def apply_size(self):
        
        #brush size spinbox to brush
        self.brushSize = self.spinbox_br_size.value()
        
        if self.canDraw:
            #brush ellipse settings
            self.current_object.brush_mouse.setRect(0,0, self.brushSize, self.brushSize)
            self.current_object.brush_mouse.setX(self.mouse_curr_point.x() - self.brushSize/2)
            self.current_object.brush_mouse.setY(self.mouse_curr_point.y() - self.brushSize/2)
            
        
    def save(self):
        if self.canDraw:
            filePath, _=QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg);;ALL Files(*.*)")
            if filePath == "":
                return
            self.current_object.pixmap.save(filePath)
        
    def load(self):

        filePath, _=QtWidgets.QFileDialog.getOpenFileName(self, "Load Image", "", "PNG(*.png);;JPEG(*.jpg)")
        if filePath == "":
            return
            
        self.add_new_image(filePath,"my_image")


#initialize  
app = QtWidgets.QApplication(sys.argv)
window = Example()
window.show()
sys.exit(app.exec())

