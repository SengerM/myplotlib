import myplotlib as mpl
import numpy as np

x = np.linspace(1,3)
y = x**3


for package in ['matplotlib', 'plotly']:
	fig = mpl.manager.new(
		title = f'simple plot with {package}',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
	)
	fig.plot(
		x,
		y,
		label = 'Simple plot',
	)
	fig = mpl.manager.new(
		title = f'Markers test {package}',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
	)
	for marker in ['.', '+', 'x', 'o']:
		fig.plot(
			x,
			y + np.random.randn(len(x)),
			marker = marker,
			label = f'Markers {marker}',
		)
	
	fig = mpl.manager.new(
		title = f'Linestyle test {package}',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
	)
	for linestyle in ['-', '', '--']:
		fig.plot(
			x,
			y + np.random.randn(len(x)),
			marker = '.',
			linestyle = linestyle,
			label = f'Linestyle {linestyle}',
		)

mpl.manager.save_all()
