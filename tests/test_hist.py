import myplotlib as mpl
import numpy as np

samples = [np.random.randn(999)*2*i for i in range(3)]

for package in ['matplotlib', 'plotly']:
	fig = mpl.manager.new(
		title = f'simple histogram with {package}',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
	)
	for idx,s in enumerate(samples):
		fig.hist(
			s,
			label = f'Plain histogram {idx}',
			linestyle = ['solid','dashed','dotted'][idx],
		)
	
	fig = mpl.manager.new(
		title = f'specifying bins with {package}',
		subtitle = f'This is a test',
		xlabel = 'x axis',
		ylabel = 'y axis',
		package = package,
	)
	for idx,s in enumerate(samples):
		fig.hist(
			s,
			bins = 5 if idx==0 else [0,2,3,3.5,4.4,4.5,4.6],
			label = f'Plain histogram {idx}',
		)
	
mpl.manager.save_all()
