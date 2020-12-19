# myplotlib

My personal unified interfase for doing plots. The idea is to implement the same interface (at least for basic stuff) for many plotting packages. Currently supports Matplotlib and Plotly.

- Matplotlib is the best if you want to end up with a single image (png, pdf) to "print" (or just embed in a PDF).
- Plotly is far better for doing interactive plots, visualize and share them. 

So each package has its own advantages and disadvantages, and they have very different interfases which is a pain.

## Installation

If you have pip (or pip3) installed, just run

```
pip install git+https://github.com/SengerM/myplotlib
```
Otherwise, check how to install a package hosted in a GitHub repository with your Python package manager.

You will also need to [install matplotlib](https://matplotlib.org/users/installing.html#installing-an-official-release) (```pip install matplotlib```) and [install plotly](https://plotly.com/python/getting-started/#installation) (```pip install plotly```).

## Example

The next example shows a simple usage case and as you can see the same code is used both for Plotly and for Matplotlib.:

```Python
import myplotlib as mpl # Easy import.
import numpy as np

x_data = np.linspace(-1,1)
random_data = np.random.randn(999)

for package in ['plotly', 'matplotlib']: # Use the same code for both packages!
	fig1 = mpl.manager.new(
		title = 'A nice plot',
		subtitle = 'Mathematical functions',
		xlabel = 'x axis',
		ylabel = 'y axis',
		show_title = False, # This hides the title from the plot, but still uses this title for saving the file if you call "mpl.manager.save_all".
		package = package, # Choose between Matplotlib/Plotly.
	)
	fig1.plot(
		x_data,
		x_data**2,
		label = 'x²',
		marker = '.',
	)
	fig1.plot(
		x_data,
		x_data**3,
		label = 'x³',
		color = (0,0,0), # Color is specified as an RGB tuple.
		linestyle = '--',
	)

	histogram = mpl.manager.new(
		title = 'This is a histogram',
		subtitle = 'Data distribution',
		xlabel = 'Whatever this is',
		ylabel = 'Number of occurrences',
		package = package, # Choose between Matplotlib/Plotly.
	)
	histogram.hist(
		random_data,
		label = 'My data',
		color = (1,.2,.2),
		bins = 99, # Set the number of bins. Any value compatible with Numpy's histogram function should work here, see https://numpy.org/doc/stable/reference/generated/numpy.histogram.html.
	)

mpl.manager.save_all( # Save all the figures.
	format = 'pdf', # Matplotlib figures will be saved in PDF, Plotly figures will be saved in HTML (interactive).
	mkdir = 'directory with figures', # If no directory is specified, a directory with the name of the script is created.
)

mpl.manager.save_all() # Creates a directory and saves all the figures automatically.
mpl.manager.show() # Show all the figures.

```

Colormaps can be plotted with Matplotlib, Plotly and also with [SAOImageDS9](https://sites.google.com/cfa.harvard.edu/saoimageds9) which is really cool to play with the scale of the colormap. This last option is very useful for images. Below there is an example:

```Python
import myplotlib as mpl
import numpy as np

x = np.linspace(-2,2)
y = np.linspace(-1,1)

xx,yy = np.meshgrid(x,y)
zz = xx*yy**2

for package in ['matplotlib', 'plotly', 'ds9']:
	colormap_figure = mpl.manager.new(
		title = 'Colormap',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
	)
	colormap_figure.colormap(
		x = xx,
		y = yy,
		z = zz,
		colorscalelabel = 'z value',
	)
mpl.manager.save_all()
mpl.manager.show()

```
