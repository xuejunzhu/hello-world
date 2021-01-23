# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 19:00:39 2019
https://commons.wikimedia.org/wiki/File:Tautochrone_balls_full_oscillation.gif
@author: junz
"""

#!/usr/bin/python
# -*- coding: utf8 -*-

'''
animation of balls on a tautochrone curve
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation # https://matplotlib.org/api/animation_api.html
from math import *

# settings
fname = 'Tautochrone_balls_full_oscillation'
width, height = 640, 224
nframes = 50
fps=20

balls = [
{'a':1.0, 'color':'#0000c0'},
{'a':0.8, 'color':'#c00000'},
{'a':0.6, 'color':'#00c000'},
{'a':0.4, 'color':'#c0c000'}]

def curve(phi):
    x = phi + sin(phi)
    y = 1.0 - cos(phi)
    return np.array([x, y])

def animate(nframe, empty=False):
    t = nframe / float(nframes)
    
    # prepare a clean and image-filling canvas for each frame
    fig = plt.gcf()
    fig.clf()
    ax_canvas = plt.gca()
    ax_canvas.set_position((0, 0, 1, 1))
    ax_canvas.set_xlim(0, width)
    ax_canvas.set_ylim(0, height)
    ax_canvas.axis('off')
    
    # draw the ramp
    x0, y0 = width//2, 18
    h = 192
    npoints = 400
    points = []
    for i in range(npoints):
        phi = i / (npoints - 1.0) * 2 * pi - pi
        x, y = h/2. * curve(phi) + np.array([x0, y0])
        points.append([x, y])
    
    rampline = patches.Polygon(points, closed=False, facecolor='none',
                       edgecolor='black', linewidth=4, capstyle='butt')
    points += [[x0+h*pi/2, y0], [x0-h*pi/2, y0], [x0-h*pi/2, y0+h]]
    ramp = patches.Polygon(points, closed=True, facecolor='#c0c0c0', edgecolor='none')
    ax_canvas.add_patch(ramp)
    ax_canvas.add_patch(rampline)
    
    for b in balls:
        phi_pendulum = b['a'] * -cos(t * 2 * pi)
        phi_wheel = 2 * asin(phi_pendulum)
        x, y = h/2. * curve(phi_wheel) + np.array([x0, y0])
        ax_canvas.add_patch(patches.Circle((x, y), radius=10.,
                            facecolor=b['color'], edgecolor='black'))

fig = plt.figure(figsize=(width/100., height/100.))
anim = animation.FuncAnimation(fig, animate, frames=nframes)
print ("saving", fname + ".gif")
anim.save(fname + '.gif', writer='imagemagick', fps=fps)