import myplotlib as mpl
import numpy as np

x = np.linspace(-1,1)
y = x
xx, yy = np.meshgrid(x,y)
zz = xx**4 + yy**2 + np.random.rand(*xx.shape)*.1


for package in ['matplotlib', 'plotly', 'ds9']:
	fig = mpl.manager.new(
		title = f'colormap with {package} linear scale',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
		aspect = 'equal',
	)
	fig.colormap(
		x = xx,
		y = yy,
		z = zz,
		colorscalelabel = 'Colormap value',
	)
	
	fig = mpl.manager.new(
		title = f'colormap with {package} log scale',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
		aspect = 'equal',
	)
	fig.colormap(
		x = xx,
		y = yy,
		z = zz,
		colorscalelabel = 'Colormap value',
		norm = 'log',
	)
	
mpl.manager.show()
