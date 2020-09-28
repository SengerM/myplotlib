import matplotlib.pyplot as plt
import matplotlib.colors as colors
import plotly.graph_objects as go
import os
import numpy as np
from .utils import get_timestamp
import __main__

class _Figure:
	def __init__(self, this_figure_package):
		self.this_figure_package = this_figure_package

		if self.this_figure_package == 'matplotlib':
			fig, ax = plt.subplots()
			self.fig = fig
			self.ax = ax
			ax.grid(b=True, which='minor', color='#000000', alpha=0.1, linestyle='-', linewidth=0.25)
		elif self.this_figure_package == 'plotly':
			self.fig = go.Figure()
			self.fig_title = ''
		else:
			raise ValueError("Don't know how to handle " + this_figure_package + ' plotting package')
	
	@property
	def title(self):
		if self.this_figure_package == 'matplotlib':
			return self.fig.get_label()
		elif self.this_figure_package == 'plotly':
			return self.fig_title
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)
	
	def plot(self, *args, scalex=True, scaley=True, data=None, **kwargs):
		if self.this_figure_package == 'matplotlib':
			self.ax.plot(*args, scalex=True, scaley=True, data=None, **kwargs)
			if kwargs.get('label') != None:
				self.ax.legend()
		elif self.this_figure_package == 'plotly':
			if kwargs.get('marker') == None and kwargs.get('linestyle') != '':
				_mode = 'lines'
			elif kwargs.get('marker') != None and kwargs.get('linestyle') != '':
				_mode = 'lines+markers'
			elif kwargs.get('marker') != None and kwargs.get('linestyle') == '':
				_mode = 'markers'
			self.fig.add_trace(
				go.Scatter(
					x = args[0],
					y = args[1],
					name = kwargs.get('label'),
					opacity = kwargs.get('alpha'),
					mode = _mode
				)
			)
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)
	
	def hist(self, x, **kwargs):
		if self.this_figure_package == 'matplotlib':
			self.ax.hist(x = x, **kwargs)
			if kwargs.get('label') != None:
				self.ax.legend()
		elif self.this_figure_package == 'plotly':
			self.fig.add_trace(
				go.Histogram(
					x = x,
					name = kwargs.get('label'),
					nbinsx = kwargs.get('bins'),
					histnorm = 'probability density' if kwargs.get('density') == True else None,
					opacity = kwargs.get('alpha'),
				)
			)
			self.fig.update_layout(barmode='overlay')
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)
	
	def hist2d(self, x, y, bins=10, range=None, density=False, weights=None, cmin=None, cmax=None, *args, data=None, **kwargs):
		if self.this_figure_package == 'matplotlib':
			self.ax.hist2d(x, y, bins=bins, range=range, density=density, weights=weights, cmin=cmin, cmax=cmax, data=data, **kwargs)
			if kwargs.get('label') != None:
				self.ax.legend()
		elif self.this_figure_package == 'plotly':
			self.fig.add_trace(
				go.Histogram2d(
					x = x,
					y = y,
					xbins = {'start': min(x), 'end': max(x), 'size': (max(x)-min(x))/bins},
					ybins = {'start': min(y), 'end': max(y), 'size': (max(y)-min(y))/bins},
					name = kwargs.get('label'),
					histnorm = 'probability density' if kwargs.get('density') == True else None,
					opacity = kwargs.get('alpha'),
				)
			)
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)
	
	def colormap(self, z, x=None, y=None, cmap='Blues_r', norm=None, **kwargs):
		NORM_OPTIONS = ['lin', 'log']
		if self.this_figure_package == 'matplotlib':
			if norm in [None, 'lin']: # linear normalization
				norm = colors.Normalize(vmin=z.min(), vmax=z.max())
			elif norm == 'log':
				temp = np.squeeze(np.asarray(z))
				while temp.min() <= 0:
					temp = temp[temp!=temp.min()]
				norm = colors.LogNorm(vmin=temp.min(), vmax=z.max())
			else:
				raise ValueError('The argument "norm" must be one of ' + str(NORM_OPTIONS))
			if x is None and y is None:
				cs = self.ax.pcolormesh(z, cmap=cmap, norm=norm, rasterized=True, **kwargs)
			elif x is not None and y is not None:
				cs = self.ax.pcolormesh(x, y, z, cmap=cmap, norm=norm, rasterized=True, **kwargs)
			else: 
				raise ValueError('You must provide either "both x and y" or "neither x nor y"')
			self.fig.colorbar(cs)
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)
	
	def set(self, **kwargs):
		IMPLEMENTED_KWARGS_MATPLOTLIB = ['xlabel', 'ylabel', 'title', 'show_title', 'xscale', 'yscale', 'xlim', 'ylim']
		IMPLEMENTED_KWARGS_PLOTLY     = ['xlabel', 'ylabel', 'title', 'show_title', 'xscale', 'yscale']
		if self.this_figure_package == 'matplotlib':
			for key in kwargs:
				if key not in IMPLEMENTED_KWARGS_MATPLOTLIB:
					raise NotImplementedError(key + ' not implemented yet for ' + 'matplotlib' + '. Available options: ' + str(IMPLEMENTED_KWARGS_MATPLOTLIB))
			self.ax.set_xlabel(kwargs.get('xlabel'))
			self.ax.set_ylabel(kwargs.get('ylabel'))
			self.ax.set_xscale('linear' if kwargs.get('xscale') == None else kwargs.get('xscale'))
			self.ax.set_yscale('linear' if kwargs.get('yscale') == None else kwargs.get('yscale'))
			if kwargs.get('xlim') != None:
				self.ax.set_xlim(kwargs.get('xlim'))
			if kwargs.get('ylim') != None:
				self.ax.set_ylim(kwargs.get('ylim'))
			if kwargs.get('title') != None:
				self.fig.set_label(kwargs.get('title'))
				self.fig.canvas.set_window_title(kwargs.get('title'))
				if kwargs.get('show_title') == None or kwargs.get('show_title') == True:
					self.ax.set_title(kwargs.get('title'))
		elif self.this_figure_package == 'plotly':
			for key in kwargs:
				if key not in IMPLEMENTED_KWARGS_PLOTLY:
					raise NotImplementedError(key + ' not implemented yet for ' + 'plotly' + '. Available options: ' + str(IMPLEMENTED_KWARGS_PLOTLY))
			self.fig.update_layout(
				title = kwargs.get('title'),
				xaxis_title = kwargs.get('xlabel'),
				yaxis_title = kwargs.get('ylabel'),
				xaxis_type = 'linear' if kwargs.get('xscale') == None else kwargs.get('xscale'),
				yaxis_type = 'linear' if kwargs.get('yscale') == None else kwargs.get('yscale'),
			)
			self.fig_title =  kwargs.get('title') if kwargs.get('title') != None else ''
				
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)
	
	def show(self):
		if self.this_figure_package == 'matplotlib':
			plt.show() # I really don't know how to show only the current figure...
		elif self.this_figure_package == 'plotly':
			self.fig.show()
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)
	
	def save(self, *args, **kwargs):
		if self.this_figure_package == 'matplotlib':
			self.fig.savefig(facecolor=(1,1,1,0), *args, **kwargs)
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)
	
	def close(self):
		if self.this_figure_package == 'matplotlib':
			plt.close(self.fig)
		else:
			raise NotImplementedError('Method not implemented yet for package ' + self.this_figure_package)

class FigureManager:
	def __init__(self):
		self.set_plotting_package('matplotlib')
		self.figures = []
	
	def set_plotting_package(self, package):
		IMPLEMENTED_PACKAGES = ['matplotlib', 'plotly']
		if package not in IMPLEMENTED_PACKAGES:
			raise ValueError('<package> must be one of ' + str(IMPLEMENTED_PACKAGES))
		self.plotting_package = package
	
	def new(self, **kwargs):
		self.figures.append(_Figure(this_figure_package = self.plotting_package))
		self.figures[-1].set(**kwargs)
		return self.figures[-1]
	
	def set_style(self, style):
		PLOTTING_STYLES = ['latex one column']
		if style not in PLOTTING_STYLES:
			raise ValueError('<style> must be one of ' + str(PLOTTING_STYLES))
		elif style == 'latex one column' and self.plotting_package == 'matplotlib':
			plt.style.use(os.path.dirname(os.path.abspath(__file__)) + '/rc_styles/latex_one_column_rc_style')
	
	def save_all(self, timestamp=False, mkdir=True, format='png', *args, **kwargs):
		"""
		Use this function to save all plots made with the current manager at once.
		
		Arguments
		---------
		timestamp : bool, optional 
			Default: False
			If true then all file names will be identified with one (and the
			same) timestamp. The timestamp is created at the moment this 
			function is called. If you call this function twice, you'll have 
			two different timestamps.
			This is usefull when you want not to overwrite the plots each 
			time you run your code. Let's say you are doing a simulation and you
			want to keep the plots of each different run, then you can use
			"timestamp = True".
		mkdir : str or True/False
			Default: True
			If a string is passed then a directory will be created (with the
			specified name) and all figures will be saved in there. If True
			the name for the directory is the same as the name of the top
			level python script that called this function. If False, no directory
			is created an figures are saved in the current working directory.
		format : string, optional
			Default: 'png'
			Format of image files. Default is 'png'. 
		"""
		current_timestamp = get_timestamp()
		if mkdir != False:
			if mkdir == True:
				mkdir = __main__.__file__.replace('.py', '') + ' saved plots'
			directory = mkdir + '/'
			if not os.path.exists(directory):
				os.makedirs(directory)
		else:
			directory = './'
		for k,_fig in enumerate(self.figures):
			file_name = current_timestamp + ' ' if timestamp == True else ''
			file_name += _fig.title if _fig.title != '' else 'figure ' + str(k+1)
			_fig.save(directory + '/' + file_name + '.' + format, *args, **kwargs)
	
	def show(self):
		for fig in self.figures:
			fig.show()
	
	def delete(self, fig: _Figure):
		if not isinstance(fig, _Figure):
		  raise TypeError('"fig" must be a figure')
		self.figures.remove(fig)
		fig.close()
	
	def delete_all_figs(self):
		for fig in self.figures:
			fig.close()
		self.figures = []
