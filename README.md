# myplotlib

A unique interface for plotting my stuff. The idea is to implement the same interface for the basic stuff in matplotlib and in plotly. The interfase is based in *matplotlib* and some things are wrapped to *plotly*. 

## Examples

The next example shows a simple usage case:

```Python
import myplotlib as mpl
import numpy as np

x_data = np.linspace(0,3)

fig1 = mpl.manager.new() # Create a new figure.
fig1.plot( # Here it is the same as "ax.plot" in matplotlib.
	x_data,
	x_data**2,
	label = '$x^2$', # If you set a label, the legend is automatically enabled.
	marker = '.',
)
fig1.plot( # Here it is the same as "ax.plot" in matplotlib.
	x_data,
	x_data**3,
	label = '$x^3$',
	color = (0,0,0),
	linestyle = '--',
)
fig1.set(
	title = 'A nice plot',
	xlabel = '$x$ axis',
	ylabel = '$y$ axis',
	show_title = False, # This hides the title from the plot, but still uses this title for saving the file if you call "mpl.manager.save_all".
)

fig2 = mpl.manager.new( # Create a new figure and configure it at creation.
	title = 'You can also "set" the figure at creation',
	xlabel = 'x axis',
	ylabel = 'y axis',
	yscale = 'log',
)
fig2.plot(1/x_data)

histogram = mpl.manager.new(
	title = 'This is a histogram',
	xlabel = 'Whatever this is',
	ylabel = 'Number of occurrences',
)
histogram.hist(
	np.random.randn(999),
	label = 'My data',
	color = (1,.2,.2),
	bins = 99,
)

mpl.manager.save_all( # Save all the figures.
	format = 'pdf',
	mkdir = 'directory with figures', # If no directory is specified, a directory with the name of the script is created.
)
mpl.manager.show() # Show all the figures.
```

### A unified interface for simple plots in **matplotlib** and **plotly**

The following example shows how the same code can be used to plot with ```matplotlib``` and also with ```plotly```:

```Python
import myplotlib as mpl
import numpy as np

data = []
for k in range(3):
	data.append((k+1)*np.random.randn(9999) + k)

for package in ['plotly', 'matplotlib']:
	mpl.manager.set_plotting_package(package)
	
	scatter_plot = mpl.manager.new(
		xlabel = 'x axis',
		ylabel = 'y axis',
		title = 'Simple plot test',
		yscale = 'log',
		xscale = 'log'
	)
	scatter_plot.plot(
		np.array([1,2,3,4,5,6,7]),
		np.array([1,2,3,4,5,6,7])**2,
		label = 'y = x²',
		alpha = .3,
	)
	scatter_plot.plot(
		np.array([1,2,3,4,5,6,7]),
		np.array([1,2,3,4,5,6,7])**3,
		label = 'y = x³',
		marker = 'x',
	)
	scatter_plot.plot(
		np.array([1,2,3,4,5,6,7]),
		np.array([1,2,3,4,5,6,7])**4,
		label = 'y = x⁴',
		marker = '.',
		linestyle = '',
	)
	
	histogram_plot = mpl.manager.new(
		xlabel = 'Samples',
		ylabel = 'Probability',
		title = 'Histogram test',
		yscale = 'log',
	)
	for k in range(len(data)):
		histogram_plot.hist(
			data[k],
			label = 'Data ' + str(k),
			alpha = .5,
			bins = 99,
			density = True,
		)
	
	colormap_plot = mpl.manager.new(
		title = 'Colormap plot',
		xlabel = 'x axis',
		ylabel = 'y axis',
		aspect = 'equal', # This sets the aspect ratio 1:1, so x and y have the same scale in the screen.
	)
	x = np.linspace(0,2*np.pi,99)
	y = x
	xx,yy = np.meshgrid(x,y)
	colormap_plot.colormap(
		x = xx,
		y = yy,
		z = np.sin(xx*yy),
	)

mpl.manager.show()
```
