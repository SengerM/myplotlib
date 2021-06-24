import myplotlib as mpl
import numpy as np

def calc_error(y):
	return ((y**2)**.5)*.1 + max(y*.01)

x = np.linspace(-1,1)
y = [
	x**3,
	np.cos(x),
	x**2,
	np.exp(x),
	x,
	2*x,
	3*(x**2)**.5,
	-x,
]

for package in ['plotly']:
	fig = mpl.manager.new(
		title = f'Fill between with {package}',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
	)
	for idx,yy in enumerate(y):
		fig.error_band(
			x,
			yy,
			yy + calc_error(yy),
			yy - calc_error(yy),
			label = f'Function {idx}',
		)

mpl.manager.save_all()
