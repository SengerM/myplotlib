# myplotlib

A unique interface for plotting my stuff. The idea is to implement the same interface for the basic stuff in matplotlib and in plotly. The interfase is based in *matplotlib* and some things are wrapped to *plotly*. 

## Examples

The next example shows a simple usage case:

```Python
import myplotlib as mpl
import numpy as np

mpl.manager.set_style('latex one column') # You can comment this line and use the default style.

fig1 = mpl.manager.new() # Create a new figure.
fig1.plot( # Here it is the same as "ax.plot" in matplotlib.
	[1,2,3,4],
	[1,4,7,6],
	label = 'Data 1',
	marker = '.',
)
fig1.plot( # Here it is the same as "ax.plot" in matplotlib.
	[1,2,3,4,5],
	[9,7,6,4,3],
	label = 'Data 2',
	color = (0,0,0),
	linestyle = '--',
)
fig1.set( # This is specific from "myplotlib".
	xlabel = 'x label',
	ylabel = 'y axis',
	title = 'This is the title',
	show_title = False, # This hides the title from the plot, but still uses this title for saving the file if you call "mpl.manager.save_all".
)

f2 = mpl.manager.new() # Create a new figure.
f2.plot([5,3,6,5,2,7,9,8,3,4,3,2,2,1,2]) # Same as "ax.plot" in matplotlib.

histogram = mpl.manager.new()
histogram.hist(
	np.random.randn(999),
	label = 'My data',
	color = (1,.2,.2),
	bins = 99
)

histogram.show()
mpl.manager.save_all(format = 'pdf', mkdir = 'directory for figures', timestamp = True)
```

The following example shows how the same code can be used to plot with ```matplotlib``` and also with ```plotly```:

```Python
import myplotlib as mpl
import numpy as np

data = []
for k in range(3):
	data.append((k+1)*np.random.randn(9999) + k)

for package in ['plotly', 'matplotlib']:
	mpl.manager.set_plotting_package(package)
	
	scatter_plot = mpl.manager.new()
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
	scatter_plot.set(
		xlabel = 'x axis',
		ylabel = 'y axis',
		title = 'Simple plot test',
		yscale = 'log',
		xscale = 'log'
	)
	
	histogram_plot = mpl.manager.new()
	for k in range(len(data)):
		histogram_plot.hist(
			data[k],
			label = 'Data ' + str(k),
			alpha = .5,
			bins = 99,
			density = True,
		)
	histogram_plot.set(
		xlabel = 'Samples',
		ylabel = 'Probability',
		title = 'Histogram test',
		yscale = 'log',
	)

mpl.manager.show()
```
