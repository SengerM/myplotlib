import myplotlib as mpl
import numpy as np

x = np.linspace(0,1)

for package in ['plotly', 'matplotlib']:
	fig = mpl.manager.new(
		title = 'Markers test',
		package = package,
	)
	fig.plot(
		x,
		x**3,
		label = 'No markers',
	)
	for marker in ['.','x','+','o']:
		fig.plot(
			x,
			x**np.random.rand(),
			marker = marker,
			label = f'Marker = {marker}',
			linestyle = '',
		)

mpl.manager.show()
