import sys
from math import cos, sin, radians

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QColorDialog


class L_System:
    start_coords = (400, 400)

    def __init__(self, title, parts, axiom, *theorems):
        self.title = title
        self.rotate_angle = 360 // int(parts)
        self.instructions = {0: axiom}
        self.theorems = dict()
        for theorem in theorems:
            predecessor, follower = theorem.split()
            self.theorems[predecessor] = follower
    
    def get_instructions(self, step):
        if step in self.instructions.keys():
            return self.instructions[step]
        
        for i in range(max(self.instructions.keys()), step):
            self.instructions[i + 1] = ""

            for elem in self.instructions[i]:
                if elem in ["-", "+", "f", "[", "]", "|"]:
                    instruction = elem
                elif elem == "F":
                    instruction = self.theorems.get(elem, "F")
                else:
                    instruction = self.theorems[elem]

                self.instructions[i + 1] += instruction
        
        return self.instructions[step]


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("window.ui", self)

        # Initial resizeEvent breaks size of slider, self.initial flag is used to avoid it
        self.initial = True

        # QPainter doesn't work with ordinary stylesheets
        self.palette = QPalette()
        self.palette.setColor(QPalette.ColorRole(10), QColor(0, 0, 0))
        self.setAutoFillBackground(True)
        self.setPalette(self.palette)

        self.l_system = self._initialize_l_system()
        self.setWindowTitle(self.l_system.title)

        self.pen_color = QColor(255, 0, 255)
        self.choose_color_button.clicked.connect(self._change_color)

        self.center_x.textChanged.connect(self._change_start_coords)
        self.center_y.textChanged.connect(self._change_start_coords)

        self.repaint_button.clicked.connect(self.repaint)
        self.line_length.valueChanged.connect(self.repaint)
        self.evolution_step.valueChanged.connect(self.repaint)
    
    def _change_color(self):
        self.pen_color = QColorDialog.getColor()
        self.choose_color_button.setStyleSheet(f"border: none; background-color: {self.pen_color.name()}")
    
    def _initialize_l_system(self):
        filename = QFileDialog.getOpenFileName(self, "Select a file", "")[0]
        title, parts, axiom, *theorems = open(filename, mode="r", encoding="utf8").read().splitlines()
        return L_System(title, parts, axiom, *theorems)
    
    def _change_start_coords(self):
        center_x, center_y = self.center_x.text(), self.center_y.text()
        if center_x.isdigit() and center_y.isdigit():
            L_System.start_coords = (int(center_x), int(center_y))
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(self.pen_color)

        instructions = self.l_system.get_instructions(self.evolution_step.sliderPosition())
        
        line_length = self.line_length.sliderPosition()
        center_coords = L_System.start_coords
        active_rotate_angle = 0

        for instruction in instructions:
            if instruction in ["F", "f"]:
                new_x = center_coords[0] + round(line_length * cos(radians(active_rotate_angle)))
                new_y = center_coords[1] + round(line_length * sin(radians(active_rotate_angle)))

                if instruction == "F":
                    qp.drawLine(*center_coords, new_x, new_y)
                
                center_coords = (new_x, new_y)
            elif instruction == "+":
                active_rotate_angle += self.l_system.rotate_angle
            elif instruction == "-":
                active_rotate_angle -= self.l_system.rotate_angle
            elif instruction == "|":
                active_rotate_angle += 180
            elif instruction == "[":
                save_coords = center_coords
            elif instruction == "]":
                center_coords = save_coords

        qp.end()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.initial:
            l_rect = self.line_length.geometry()
            e_rect = self.evolution_step.geometry()
            b_rect = self.choose_color_button.geometry()
            g_rect = self.group_box.geometry()

            delta = event.size() - event.oldSize()
            self.line_length.setGeometry(l_rect.x(), l_rect.y(), l_rect.width(), l_rect.height() + delta.height())
            self.evolution_step.setGeometry(e_rect.x(), e_rect.y() + delta.height(), e_rect.width() + delta.width(), e_rect.height())
            self.choose_color_button.setGeometry(b_rect.x(), b_rect.y() + delta.height(), b_rect.width(), b_rect.height())
            self.group_box.setGeometry(g_rect.x() + delta.width(), g_rect.y(), g_rect.width(), g_rect.height())
        else:
            self.initial = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
