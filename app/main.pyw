import sys
from math import cos, sin, radians

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QColorDialog


class L_System:
    start_coords = (400, 400)

    def __init__(self, title, angle, axiom, *theorems):
        self.title = title
        self.rotate_angle = int(angle)
        self.instructions = {1: axiom}
        self.theorems = dict()
        for theorem in theorems:
            # split(" ") using for theorems where no follower
            predecessor, follower = theorem.split(" ")
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
    
    def get_possible_count_steps(self):
        step = 1
        while len(self.get_instructions(step)) < 50_000:
            step += 1

        return step


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

        self.l_system = None
        self._initialize_l_system()
        self.change_l_system_button.clicked.connect(self._initialize_l_system)

        if self.l_system is not None:
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
        try:
            title, angle, axiom, *theorems = open(filename, mode="r", encoding="utf8").read().splitlines()
            self.l_system = L_System(title, angle, axiom, *theorems)
            self.evolution_step.setMaximum(self.l_system.get_possible_count_steps())

            self.line_length.setValue(1)
            self.evolution_step.setValue(1)
        except Exception as e:
            print("error", e)
    
    def _change_start_coords(self):
        center_x, center_y = self.center_x.text(), self.center_y.text()
        if center_x.isdigit() and center_y.isdigit():
            L_System.start_coords = (int(center_x), int(center_y))
    
    def paintEvent(self, event):
        if self.l_system is None:
            return
        
        qp = QPainter()
        qp.begin(self)
        qp.setPen(self.pen_color)

        instructions = self.l_system.get_instructions(self.evolution_step.sliderPosition())
        
        line_length = self.line_length.sliderPosition() * 2
        center_coords = L_System.start_coords
        if self.rotation_angle.text().isdigit():
            active_rotate_angle = int(self.rotation_angle.text())
        else:
            active_rotate_angle = 0

        saved = []
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
                saved.append([center_coords, active_rotate_angle])
            elif instruction == "]":
                center_coords, active_rotate_angle = saved.pop()

        qp.end()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.initial:
            l_rect = self.line_length.geometry()
            e_rect = self.evolution_step.geometry()
            b_rect = self.choose_color_button.geometry()
            g_rect = self.group_box.geometry()
            g2_rect = self.group_box_2.geometry()
            r_rect = self.repaint_button.geometry()
            c_rect = self.change_l_system_button.geometry()

            delta = event.size() - event.oldSize()
            self.line_length.setGeometry(l_rect.x(), l_rect.y(), l_rect.width(), l_rect.height() + delta.height())
            self.evolution_step.setGeometry(e_rect.x(), e_rect.y() + delta.height(), e_rect.width() + delta.width(), e_rect.height())
            self.choose_color_button.setGeometry(b_rect.x(), b_rect.y() + delta.height(), b_rect.width(), b_rect.height())
            self.group_box.setGeometry(g_rect.x() + delta.width(), g_rect.y(), g_rect.width(), g_rect.height())
            self.group_box_2.setGeometry(g2_rect.x() + delta.width(), g2_rect.y(), g2_rect.width(), g2_rect.height())
            self.repaint_button.setGeometry(r_rect.x() + delta.width(), r_rect.y(), r_rect.width(), r_rect.height())
            self.change_l_system_button.setGeometry(c_rect.x() + delta.width(), c_rect.y(), c_rect.width(), c_rect.height())
        else:
            self.initial = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
