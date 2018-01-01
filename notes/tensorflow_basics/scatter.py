import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.io import export_png, export_svgs

x = np.random.randn(2000,1)
w = np.array([0.7])
b = -0.2
noise = np.random.randn(1,2000) * 0.3
y = np.dot(x,w) + b + noise

p = figure(toolbar_location=None,width=550,height=500)
p.grid.grid_line_color = None
p.outline_line_color = "white"
p.scatter(x=np.hstack(x), y=y[0], line_color=None,marker="circle", size=7, fill_color="orange", alpha=0.35)

export_png(p,"scatter.png")

p = figure(toolbar_location=None,width=550,height=500)
p.grid.grid_line_color = None
p.outline_line_color = "white"
p.scatter(x=np.hstack(x), y=y[0], line_color=None,marker="circle", size=7, fill_color="orange", alpha=0.35)
p.line(np.linspace(np.min(x),np.max(x)),np.linspace(np.min(x*0.7 + b),np.max(x*0.7 + b)),line_width=2,line_color="black")

export_png(p,"line.png")
