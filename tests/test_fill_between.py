import myplotlib as mpl
import numpy as np

x = np.linspace(-1,1)
y = x**3


for package in ['matplotlib']:
	fig = mpl.manager.new(
		title = f'Fill between with {package}',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
	)
	fig.fill_between(
		x,
		y,
		label = 'Fill between 0 and y',
	)
	fig.fill_between(
		x,
		y*1.1,
		y*.9,
		label = 'Fill between two curves',
	)

mpl.manager.show()
