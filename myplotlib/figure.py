import matplotlib.pyplot as plt
import matplotlib.colors as colors
import plotly.graph_objects as go
import os
import numpy as np
from .utils import get_timestamp
import __main__
import plotly

class MPLFigure:
	"""
	This class defines the interface to be implemented in the subclasses
	and does all the validation of arguments. For example "title" must
	be a string, this is validated in this class. How to write the title
	in the figure is to be implemented in the respective subclass for
	some particular ploting package, not here.
	Convention for getting/setting the properties:
	- Each property (e.g. title) has to be defined with 3 @property methods,
	  1) title
	  2) _title getter
	  3) _title setter
	See the definition of title for implementation details.
	"""
	def __init__(self):
		pass
	
	@property
	def title(self):
		return self._title
	@property
	def _title(self):
		if hasattr(self, '_title_'):
			return self._title_
		else:
			return None
	@_title.setter
	def _title(self, value: str):
		if not isinstance(value, str):
			raise TypeError(f'<_title> must be a string, but received <{value}> of type {type(value)}.')
		self._title_ = value
	
	@property
	def subtitle(self):
		return self._subtitle
	@property
	def _subtitle(self):
		if hasattr(self, '_subtitle_'):
			return self._subtitle_
		else:
			return None
	@_subtitle.setter
	def _subtitle(self, value: str):
		if not isinstance(value, str):
			raise TypeError(f'<_subtitle> must be a string, but received <{value}> of type {type(value)}.')
		self._subtitle_ = value
	
	@property
	def xlabel(self):
		return self._xlabel
	@property
	def _xlabel(self):
		if hasattr(self, '_xlabel_'):
			return self._xlabel_
		else:
			return None
	@_xlabel.setter
	def _xlabel(self, value: str):
		if not isinstance(value, str):
			raise TypeError(f'<_xlabel> must be a string, but received <{value}> of type {type(value)}.')
		self._xlabel_ = value
	
	@property
	def ylabel(self):
		return self._ylabel
	@property
	def _ylabel(self):
		if hasattr(self, '_ylabel_'):
			return self._ylabel_
		else:
			return None
	@_ylabel.setter
	def _ylabel(self, value: str):
		if not isinstance(value, str):
			raise TypeError(f'<_ylabel> must be a string, but received <{value}> of type {type(value)}.')
		self._ylabel_ = value
	
	@property
	def xscale(self):
		return self._xscale
	@property
	def _xscale(self):
		if hasattr(self, '_xscale_'):
			return self._xscale_
		else:
			return None
	@_xscale.setter
	def _xscale(self, value: str):
		if not isinstance(value, str):
			raise TypeError(f'<_xscale> must be a string, but received <{value}> of type {type(value)}.')
		self._validate_axis_scale(value)
		self._xscale_ = value
	
	@property
	def yscale(self):
		return self._yscale
	@property
	def _yscale(self):
		if hasattr(self, '_yscale_'):
			return self._yscale_
		else:
			return None
	@_yscale.setter
	def _yscale(self, value: str):
		if not isinstance(value, str):
			raise TypeError(f'<_yscale> must be a string, but received <{value}> of type {type(value)}.')
		self._validate_axis_scale(value)
		self._yscale_ = value
	
	@property
	def aspect(self):
		return self._aspect
	@property
	def _aspect(self):
		if hasattr(self, '_aspect_'):
			return self._aspect_
		else:
			return None
	@_aspect.setter
	def _aspect(self, value: str):
		if not isinstance(value, str):
			raise TypeError(f'<_aspect> must be a string, but received <{value}> of type {type(value)}.')
		self._validate_aspect(value)
		self._aspect_ = value
	
	def _validate_axis_scale(self, scale: str):
		# Assume that <scale> is a string. Raises an error if "scale" is not a valid scale.
		valid_scales = ['lin', 'log']
		if scale not in valid_scales:
			raise ValueError(f'Axis scale must be one of {valid_scales}.')
	
	def _validate_aspect(self, aspect: str):
		# Assuming that <aspect> is a string. Raises an error if it is not a valid option.
		valid_aspects = ['equal']
		if aspect not in valid_aspects:
			raise ValueError(f'<aspect> must be one of {valid_aspects}.')
	
	def set(self, **kwargs):
		for key in kwargs.keys():
			if not hasattr(self, f'_{key}'):
				raise ValueError(f'Cannot set <{key}>, invalid property.')
			setattr(self, f'_{key}', kwargs[key])

# ~ class MPLMatplotlibWrapper(MPLFigure):
	# ~ def __init__(self):
		# ~ fig, ax = 

class _Figure:
	pass

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
		self.figures.append(_Figure(this_figure_package = kwargs.get('package') if kwargs.get('package')!=None else self.plotting_package))
		self.figures[-1].set(**kwargs)
		return self.figures[-1]
	
	def set_style(self, style):
		PLOTTING_STYLES = ['latex one column', 'latex two columns']
		style = style.lower()
		if style not in PLOTTING_STYLES:
			raise ValueError('<style> must be one of ' + str(PLOTTING_STYLES))
		elif style == 'latex one column' and self.plotting_package == 'matplotlib':
			plt.style.use(os.path.dirname(os.path.abspath(__file__)) + '/rc_styles/latex_one_column_rc_style')
		elif style == 'latex two columns' and self.plotting_package == 'matplotlib':
			plt.style.use(os.path.dirname(os.path.abspath(__file__)) + '/rc_styles/latex_two_columns_rc_style')
	
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
			file_name += _fig.title if _fig.title != None else 'figure ' + str(k+1)
			_fig.save(fname = f'{directory}/{file_name}.{format}', *args, **kwargs)
	
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
