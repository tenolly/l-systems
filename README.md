# l-systems
This application is used to draw l-systems. I have uploaded a few l-systems (they are located in the "app/systems" directory), but you can use your files (below is a guide on how to write l-system yourself).
# Installation
1) Download repository (or .zip file and unpack it):
```bash
git clone https://github.com/tenolly/l-systems.git
```
2) Install dependencies:
```bash
pip install -r requirements.txt
```
# Using
Run the main.pyw file (using a console, you must run it from the "app" directory). In the dialog window that appears, select a file with the l-system you want. How to use it: the vertical slider is responsible for the size of the l-system, and the horizontal slider is responsible for evolution's steps. Also, you can change color by clicking on the small square in the lower left corner. The rest is clear without explanation (note that the origin is the upper left corner).
# How to make your own L-system
Create txt file. L-system's file structure:
<ul>
    <li>The first line is the system name;</li>
    <li>The second line is an integer indicating how many angles the plane is divided into. This parameter is necessary to organize rotations;</li>
    <li>The third line is an axiom;</li>
    <li>The rest are theorems.</li>
</ul>
Familiarize yourself with the contents of the files in the "app/systems" firectory for more understanding.