from .figure import MPLMatplotlibWrapper, MPLPlotlyWrapper, MPLSaoImageDS9Wrapper
from .utils import get_timestamp
import os
import __main__

class FigureManager:
	def __init__(self):
		self.set_plotting_package('plotly')
		self.figures = []
	
	def set_plotting_package(self, package):
		IMPLEMENTED_PACKAGES = ['matplotlib', 'plotly', 'ds9']
		if package not in IMPLEMENTED_PACKAGES:
			raise ValueError('<package> must be one of ' + str(IMPLEMENTED_PACKAGES))
		self.plotting_package = package
	
	def new(self, **kwargs):
		package_for_this_figure = kwargs.get('package') if 'package' in kwargs else self.plotting_package
		if 'package' in kwargs: kwargs.pop('package')
		if package_for_this_figure == 'plotly':
			self.figures.append(MPLPlotlyWrapper())
		elif package_for_this_figure == 'matplotlib':
			self.figures.append(MPLMatplotlibWrapper())
		elif package_for_this_figure == 'ds9':
			self.figures.append(MPLSaoImageDS9Wrapper())
		self.figures[-1].set(**kwargs)
		return self.figures[-1]
	
	# ~ def set_style(self, style):
		# ~ PLOTTING_STYLES = ['latex one column', 'latex two columns']
		# ~ style = style.lower()
		# ~ if style not in PLOTTING_STYLES:
			# ~ raise ValueError('<style> must be one of ' + str(PLOTTING_STYLES))
		# ~ elif style == 'latex one column' and self.plotting_package == 'matplotlib':
			# ~ plt.style.use(os.path.dirname(os.path.abspath(__file__)) + '/rc_styles/latex_one_column_rc_style')
		# ~ elif style == 'latex two columns' and self.plotting_package == 'matplotlib':
			# ~ plt.style.use(os.path.dirname(os.path.abspath(__file__)) + '/rc_styles/latex_two_columns_rc_style')
	
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
				mkdir = __main__.__file__.replace('.py', '') + '_saved_plots'
			directory = mkdir + '/'
			if not os.path.exists(directory):
				os.makedirs(directory)
		else:
			directory = './'
		for k,_fig in enumerate(self.figures):
			file_name = current_timestamp + ' ' if timestamp == True else ''
			file_name += _fig.title if _fig.title != None else 'figure ' + str(k+1)
			_fig.save(fname = f'{directory}/{file_name}.{format}', *args, **kwargs)
	
	def show(self):
		for fig in self.figures:
			fig.show()
	
	# ~ def delete(self, fig: _Figure):
		# ~ if not isinstance(fig, _Figure):
		  # ~ raise TypeError('"fig" must be a figure')
		# ~ self.figures.remove(fig)
		# ~ fig.close()
	
	# ~ def delete_all_figs(self):
		# ~ for fig in self.figures:
			# ~ fig.close()
		# ~ self.figures = []

manager = FigureManager()
