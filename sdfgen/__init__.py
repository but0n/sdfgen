__version__ = '0.1.0'

import os
import subprocess
import argparse
from pyrender import Mesh, Scene, Viewer
import trimesh
import numpy as np
import math
import random

# def myInit():
#     glClearColor(1.0, 1.0, 1.0, 1.0)
#     glColor3f(0.0, 0.0, 1.0)
#     gluOrtho2D(0, 500, 0, 500)

# def render():
#     print('render?')
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glBegin(GL_POINTS)
#     glVertex2f(100, 100)
#     glVertex2f(200, 200)
#     glEnd()

#     glFlush()




# def showWindow():
#     glutInit()
#     glutInitWindowSize(500, 500)
#     glutInitWindowPosition(100, 100)
#     glutCreateWindow('Test Window')
#     myInit()
#     glutDisplayFunc(render)
#     glutMainLoop()

def blender(cmd):
    path = '/Applications/Blender.app/Contents/MacOS/Blender'
    return subprocess.check_call(f'{path} {cmd}', stderr=subprocess.STDOUT, shell=True)

def main():
    parser = argparse.ArgumentParser(description='Signed distance fields generation on GPUs')
    parser.add_argument('-i', '--in', help='input file [ .obj, .gltf ]', dest='file', required=True)
    parser.add_argument('-o', '--out', help='output file name, without extension', dest='output', default='output.bin')
    parser.add_argument('-d', help='Y precision', dest='res', default='2')
    parser.add_argument('--nofit', action='store_true', help='disable offset model')
    args = parser.parse_args()

    # # gltf = trimesh.load(args.file, force='mesh')
    # gltf = trimesh.load(args.file, force='mesh')
    # a = trimesh.primitives.Box()
    # a.apply_transform(trimesh.transformations.compose_matrix([4, .06, 4]))
    # # (a + gltf).show()

    # check blender backend
    blender_verify = blender('--version')
    # print(blender_verify)


    pwd = os.path.expanduser(os.path.abspath(os.path.dirname(__file__)))
    with open(os.path.join(pwd, 'bpy_template.py'), 'rb') as f:
        template = f.read().decode('utf-8')

    script = template.replace('#include', f'scene=\'{os.path.abspath(args.file)}\'\nresolution={args.res}')
    script_path = os.path.join(pwd, 'script.py')
    with open(script_path, 'w') as temp:
        # print(script_path)
        temp.write(script)

    blender(f'pospass.blend --python {script_path} -b')

    # result = []
    # t = type(a)
    # for offset in range(-5, 6):
    #     print(f'offset {offset}')
    #     b = a.copy()
    #     b.apply_translation((0, offset * .11, 0))
    #     # result += [b]
    #     cu = trimesh.boolean.boolean_automatic([gltf, b][::-1], 'intersection')
    #     # if type(cu) == t:
    #     if 'Scene' not in str(type(cu)):
    #         print(' * Succeed!')
    #         result += [cu]
    #         cu.apply_translation((math.sin(offset * .4) * .1, 0, 0))
    # # print(type(result))
    # # gltf = trimesh.load(args.file)
    # # mesh = Mesh.from_trimesh(gltf)
    # # # mesh = Mesh.from_trimesh([*gltf.geometry.values()])
    # # print(mesh)

    # # (gltf + a).show()
    # # result.show()

    # scene = Scene(ambient_light=np.array([1.0] * 4), bg_color=[0] * 3)

    # for r in result:
    #     try:
    #         scene.add(Mesh.from_trimesh(result))
    #     except:
    #         print('Wrong result')
    # # scene.add(Mesh.from_trimesh(result))
    # # print(scene.main_camera_node)



    # Viewer(scene)

    # showWindow()

if __name__ == '__main__':
    main()