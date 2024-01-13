import sys
from math import cos, sin, radians

from PyQt5 import uic, Qt
from PyQt5.QtGui import QPainter, QColor, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("window.ui", self)

        # initial resizeEvent breaks size of slider, self.initial flag is used to avoid it
        self.initial = True

        # QPainter doesn't work with ordinary stylesheets
        self.palette = QPalette()
        self.palette.setColor(QPalette.ColorRole(10), QColor(0, 0, 0))
        self.setAutoFillBackground(True)
        self.setPalette(self.palette)
        
        filename = QFileDialog.getOpenFileName(self, "Select a file", "")[0]
        title, parts, axiom, *theorems = open(filename, mode="r", encoding="utf8").read().splitlines()

        self.rotate_angle = 360 // int(parts)
        self.axiom = axiom

        self.theorems = dict()
        for theorem in theorems:
            predecessor, follower = theorem.split()
            self.theorems[predecessor] = follower

        self.setWindowTitle(title)
        self.evolution_step.valueChanged.connect(self.repaint)
    
    def get_instructions(self):
        evolution_step = self.evolution_step.sliderPosition()
        instructions = self.axiom

        for _ in range(evolution_step):
            new_instructions = []

            for elem in instructions:
                if elem in ["-", "+", "f", "[", "]", "|"]:
                    instruction = elem
                elif elem == "F":
                    instruction = self.theorems.get(elem, "F")
                else:
                    instruction = self.theorems[elem]

                new_instructions.append(instruction)

            instructions = "".join(new_instructions)
        
        return instructions
    
    def paintEvent(self, event):
        instructions = self.get_instructions()

        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(255, 0, 255))
        
        center_x, center_y = self.center_x.text(), self.center_y.text()
        if not (center_x.isdigit() and center_y.isdigit()):
            return

        center_coords = (int(center_x), int(center_y))
        line_length = self.line_length.sliderPosition()
        active_rotate_angle = 0

        for instruction in instructions:
            if instruction in ["F", "f"]:
                new_x = center_coords[0] + round(line_length * cos(radians(active_rotate_angle)))
                new_y = center_coords[1] + round(line_length * sin(radians(active_rotate_angle)))

                if instruction == "F":
                    qp.drawLine(*center_coords, new_x, new_y)
                
                center_coords = (new_x, new_y)
            elif instruction == "+":
                active_rotate_angle += self.rotate_angle
            elif instruction == "-":
                active_rotate_angle -= self.rotate_angle
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
            rect = self.evolution_step.geometry()
            delta = event.size() - event.oldSize()
            self.evolution_step.setGeometry(rect.x(), rect.y() + delta.height(), rect.width() + delta.width(), rect.height())
        else:
            self.initial = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
