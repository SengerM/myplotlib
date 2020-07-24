import matplotlib.pyplot as plt
import os
from .utils import get_timestamp

class FigureManager:
	def __init__(self):
		self.plotting_package = 'matplotlib'
		self.figures = []
	
	def set_plotting_package(package):
		IMPLEMENTED_PACKAGES = ['matplotlib']
		if package not in IMPLEMENTED_PACKAGES:
			raise ValueError('<package> must be one of ' + str(IMPLEMENTED_PACKAGES))
		self.plotting_package = package
	
	def new(self):
		self.figures.append(_Figure(this_figure_package = self.plotting_package))
		return self.figures[-1]
	
	def set_style(self, style):
		PLOTTING_STYLES = ['latex one column']
		if style not in PLOTTING_STYLES:
			raise ValueError('<style> must be one of ' + str(PLOTTING_STYLES))
		elif style == 'latex one column' and self.plotting_package == 'matplotlib':
			plt.style.use(os.path.dirname(os.path.abspath(__file__)) + '/rc_styles/latex_one_column_rc_style')
	
	def save_all(self, timestamp=False, mkdir=None, format='png', *args, **kwargs):
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
		mkdir : str or None, optional
			Default: None
			If a string is passed then a directory will be created (with the
			specified name) and all figures will be saved in there. If None,
			all figures will be saved in the current working directory.
			Default value is 'figures'.
		format : string, optional
			Default: 'png'
			Format of image files. Default is 'png'. 
		"""
		current_timestamp = get_timestamp()
		if mkdir != None:
			directory = mkdir + '/'
			if not os.path.exists(directory):
				os.makedirs(directory)
		else:
			directory = './'
		for k,_fig in enumerate(self.figures):
			file_name = current_timestamp + ' ' if timestamp == True else ''
			file_name += _fig.title if _fig.title != '' else 'figure ' + str(k)
			_fig.save(directory + '/' + file_name + '.' + format, *args, **kwargs)

class _Figure:
	def __init__(self, this_figure_package):
		self.this_figure_package = this_figure_package

		if self.this_figure_package == 'matplotlib':
			fig, ax = plt.subplots()
			self.fig = fig
			self.ax = ax
		else:
			raise ValueError("Don't know how to handle " + this_figure_package + ' plotting package')
	
	@property
	def title(self):
		if self.this_figure_package == 'matplotlib':
			return self.fig.get_label()
	
	def plot(self, *args, scalex=True, scaley=True, data=None, **kwargs):
		if self.this_figure_package == 'matplotlib':
			self.ax.plot(*args, scalex=True, scaley=True, data=None, **kwargs)
			if kwargs.get('label') != None:
				self.ax.legend()
	
	def set(self, **kwargs):
		if self.this_figure_package == 'matplotlib':
			IMPLEMENTED_SET_KWARGS_MATPLOTLIB = ['xlabel', 'ylabel', 'title', 'show_title']
			for key in kwargs:
				if key not in IMPLEMENTED_SET_KWARGS_MATPLOTLIB:
					raise ValueError(key + ' not implemented yet for ' + 'matplotlib' + '. Available options: ' + str(IMPLEMENTED_SET_KWARGS_MATPLOTLIB))
			self.ax.set_xlabel(kwargs.get('xlabel'))
			self.ax.set_ylabel(kwargs.get('ylabel'))
			if kwargs.get('title') != None:
				self.fig.set_label(kwargs.get('title'))
				self.fig.canvas.set_window_title(kwargs.get('title'))
				if kwargs.get('show_title') == None or kwargs.get('show_title') == True:
					self.fig.suptitle(kwargs.get('title'))
	
	def show(self):
		if self.this_figure_package == 'matplotlib':
			plt.show() # I really don't know how to show only the current figure...
	
	def save(self, *args, **kwargs):
		if self.this_figure_package == 'matplotlib':
			self.fig.savefig(facecolor=(1,1,1,0), *args, **kwargs)
