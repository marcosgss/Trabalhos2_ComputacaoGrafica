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

def prisma():
    raio = 2
    N = 10
    H = 4
    pontosBase = []
    pontosTampa = []
    angulo = (2*math.pi)/N

    glPushMatrix()
    glTranslatef(0,-1,0)
    glRotatef(-110,1.0,0.0,0.0)

    # BASE
    glBegin(GL_POLYGON)
    for i in range(N):
        x1 = raio * math.cos(i*angulo)
        y1 = raio * math.sin(i*angulo)
        pontosBase += [ (x1,y1) ]
        glVertex3f(x1,y1,0.0)
    a2 = (pontosBase[0][0],pontosBase[0][1],0.0)
    b2 = (pontosBase[1][0],pontosBase[1][1],0.0)
    c2 = (pontosBase[2][0],pontosBase[2][1],0.0)
    glNormal3fv(calculaNormal(a2,b2,c2))
    glEnd()

    # TAMPA
    glBegin(GL_POLYGON)
    for i in range(N):
        x2 = raio * math.cos(i*angulo)
        y2 = raio * math.sin(i*angulo)
        pontosTampa += [ (x2,y2) ]
        glVertex3f(x2,y2,H)
    a1 = (pontosTampa[0][0],pontosTampa[0][1],H)
    b1 = (pontosTampa[1][0],pontosTampa[1][1],H)
    c1 = (pontosTampa[2][0],pontosTampa[2][1],H)
    glNormal3fv(calculaNormal(a1,b1,c1))
    glEnd()

    # LATERAL
    glBegin(GL_QUADS)
    for i in range(N):
        a = (pontosBase[i][0],pontosBase[i][1],H)
        b = (pontosBase[i][0],pontosBase[i][1],0.0)
        c = (pontosBase[(i+1)%N][0],pontosBase[(i+1)%N][1],0.0)
        d = (pontosBase[(i+1)%N][0],pontosBase[(i+1)%N][1],H)
        glNormal3fv(calculaNormal(a,b,d))

        glVertex3fv(a)
        glVertex3fv(b)
        glVertex3fv(c)
        glVertex3fv(d)
    glEnd()
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(2,1,3,0)
    prisma()
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
    mat_ambient = (0.7, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (1.0, 0.5, 0.5, 1.0)
    mat_shininess = (50,)
    light_position = (10, 0, 0)
    glClearColor(0.0,0.0,0.0,0.0)
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
    glutCreateWindow("Iluminacao - prisma")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()
