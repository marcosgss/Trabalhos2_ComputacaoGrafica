from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import sys
import math

cores = ( (1,0,0),(1,1,0),(0,1,0),(0,1,1),(0,0,1),(1,0,1),(0.5,1,1),(1,0,0.5) )

def calculaNormal(a,b,c):
    x = 0
    y = 1
    z = 2
    v0 = a
    v1 = b
    v2 = c
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( ((U[y]*V[z])-(U[z]*V[y])),((U[z]*V[x])-(U[x]*V[z])),((U[x]*V[y])-(U[y]*V[x])))
    NLength = sqrt((N[x]*N[x])+(N[y]*N[y])+(N[z]*N[z]))
    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)

def piramide():
    raio = 2
    N = 5
    H = 4
    pontosBase = []
    angulo = (2*math.pi)/N

    glPushMatrix()
    glTranslatef(0,-2,0)
    glRotatef(-90,2.0,1.0,1.0)

    # BASE
    glBegin(GL_POLYGON)
    for i in range(N):
        x = raio * math.cos(i*angulo)
        y = raio * math.sin(i*angulo)
        pontosBase += [ (x,y) ]
        glVertex3f(x,y,0.0)
    a1 = (pontosBase[0][0],pontosBase[0][1],0.0)
    b1 = (pontosBase[1][0],pontosBase[1][1],0.0)
    c1 = (pontosBase[2][0],pontosBase[2][1],0.0)
    glNormal3fv(calculaNormal(a1,b1,c1))
    glEnd()

    # LATERAL
    glBegin(GL_TRIANGLES)
    for i in range(N):
        a = (0.0,0.0,H)
        b = (pontosBase[i][0],pontosBase[i][1],0.0)
        c = (pontosBase[(i+1)%N][0],pontosBase[(i+1)%N][1],0.0)
        glNormal3fv(calculaNormal(a,b,c))

        glVertex3fv(a)
        glVertex3fv(b)
        glVertex3fv(c)

    glEnd()
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(2,1,3,0)
    piramide()
    glutSwapBuffers()
  
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def reshape(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,1,10,0,0,0,0,1,0)

def init():
    mat_ambient = (0.0215, 0.45, 0.0215,1)
    mat_diffuse = (0.07568, 0.61424, 0.07568,1)
    mat_specular = (0.633, 0.727811, 0.633,1)
    mat_shininess = (50,)
    light_position = (10, 0 , 0)
    glShadeModel(GL_SMOOTH)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Iluminacao - piramide")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()
