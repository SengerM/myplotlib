import os
import numpy as np
from .utils import get_timestamp
import __main__


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
		self._show_title = True
	
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
	def show_title(self):
		return self._show_title
	@property
	def _show_title(self):
		return self._show_title_
	@_show_title.setter
	def _show_title(self, value):
		if value not in [True, False]:
			raise ValueError(f'<_show_title> must be either True or False, received <{value}> of type {type(value)}.')
		self._show_title_ = value
	
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
	
	def set(self, **kwargs):
		for key in kwargs.keys():
			if not hasattr(self, f'_{key}'):
				raise ValueError(f'Cannot set <{key}>, invalid property.')
			setattr(self, f'_{key}', kwargs[key])
	
	#### Validation methods ↓↓↓↓
	"""
	This methods validate arguments so we all speak the same language.
	"""
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
	
	def _validate_xy_are_arrays_of_numbers(self, x):
		if not hasattr(x, '__iter__'):
			raise TypeError(f'<x> and <y> must be "array-like" objects, e.g. lists, numpy arrays, etc.')
	
	def _validate_color(self, color):
		try:
			color = tuple(color)
		except:
			raise TypeError(f'<color> must be an iterable composed of 3 numeric elements specifying RGB. Received {color} of type {type(color)}.')
		if len(color) != 3:
			raise ValueError(f'<color> must be an iterable composed of 3 numeric elements specifying RGB. Received {color}.')
		for rgb in color:
			if not 0 <= rgb <= 1:
				raise ValueError(f'RGB elements in <color> must be bounded between 0 and 1, received {color}.')
	
	def _validate_alpha(self, alpha):
		try:
			alpha = float(alpha)
		except:
			raise ValueError(f'<alpha> must be a float number. Received {alpha} of type {type(alpha)}.')
		if not 0 <= alpha <= 1:
			raise ValueError(f'<alpha> must be bounded between 0 and 1, received {alpha}.')
	
	def _validate_linewidth(self, linewidth):
		try:
			linewidth = float(linewidth)
		except:
			raise ValueError(f'<linewidth> must be a float number. Received {linewidth} of type {type(linewidth)}.')
	
	def _validate_kwargs(self, **kwargs):
		if kwargs.get('label') != None:
			if not isinstance(kwargs.get('label'), str):
				raise TypeError(f'<label> must be a string.')
		if kwargs.get('color') != None:
			self._validate_color(kwargs['color'])
		if kwargs.get('alpha') != None:
			self._validate_alpha(kwargs['alpha'])
		if kwargs.get('linewidth') != None:
			self._validate_linewidth(kwargs['linewidth'])
	
	#### Plotting methods ↓↓↓↓
	"""
	Plotting methods here do not have to "do the job", they just validate
	things and define the interface. Each subclass has to do the job.
	"""
	def plot(self, x, y=None, **kwargs):
		implemented_kwargs = ['label', 'marker', 'color', 'alpha', 'linestyle', 'linewidth'] # This is specific for the "plot" method.
		for kwarg in kwargs.keys():
			if kwarg not in implemented_kwargs:
				raise NotImplementedError(f'<{kwarg}> not (yet) implemented for <plot> by myplotlib.')
		self._validate_xy_are_arrays_of_numbers(x)
		if y is not None:
			self._validate_xy_are_arrays_of_numbers(y)
		else:
			y = x
			x = [i for i in range(len(x))]
		self._validate_kwargs(**kwargs)
		validated_args = kwargs
		validated_args['x'] = x
		validated_args['y'] = y
		return validated_args
	
class MPLMatplotlibWrapper(MPLFigure):
	def __init__(self):
		super().__init__()
		import matplotlib.pyplot as plt # Import here so if the user does not plot with this package, it does not need to be installed.
		import matplotlib.colors as colors # Import here so if the user does not plot with this package, it does not need to be installed.
		self.matplotlib_plt = plt
		self.matplotlib_colors = colors
		fig, ax = plt.subplots()
		ax.grid(b=True, which='minor', color='#000000', alpha=0.1, linestyle='-', linewidth=0.25)
		self.matplotlib_fig = fig
		self.matplotlib_ax = ax
	
	def set(self, **kwargs):
		super().set(**kwargs) # This does a validation of the arguments and stores them in the properties of the super() figure.
		del(kwargs) # Remove it to avoid double access to the properties. Now you must access like "self.title" and so.
		self.matplotlib_ax.set_xlabel(super().xlabel)
		self.matplotlib_ax.set_ylabel(super().ylabel)
		if self.xscale in [None, 'lin']:
			self.matplotlib_ax.set_xscale('linear')
		elif self.xscale == 'log':
			self.matplotlib_ax.set_xscale('log')
		if self.yscale in [None, 'lin']:
			self.matplotlib_ax.set_yscale('linear')
		elif self.yscale == 'log':
			self.matplotlib_ax.set_yscale('log')
		if self.title != None:
			self.matplotlib_fig.canvas.set_window_title(self.title)
			if self.show_title == True:
				self.matplotlib_fig.suptitle(self.title)
		if self.aspect == 'equal':
			self.matplotlib_ax.set_aspect('equal')
		if self.subtitle != None:
			self.matplotlib_ax.set_title(self.subtitle)
	
	def plot(self, x, y=None, **kwargs):
		validated_args = super().plot(x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties. Now you must access like "self.title" and so.
		x = validated_args.get('x')
		y = validated_args.get('y')
		validated_args.pop('x')
		validated_args.pop('y')
		self.matplotlib_ax.plot(x, y, **validated_args)
		if validated_args.get('label') != None: # If you gave me a label it is obvious for me that you want to display it, no?
			self.matplotlib_ax.legend()

class MPLPlotlyWrapper(MPLFigure):
	def __init__(self):
		super().__init__()
		import plotly.graph_objects as go # Import here so if the user does not plot with this package, it does not need to be installed.
		import plotly # Import here so if the user does not plot with this package, it does not need to be installed.
		self.plotly_go = go
		self.plotly = plotly
		self.plotly_fig = go.Figure()
	
	def set(self, **kwargs):
		super().set(**kwargs) # This does a validation of the arguments and stores them in the properties of the super() figure.
		del(kwargs) # Remove it to avoid double access to the properties. Now you must access like "self.title" and so.
		if self.show_title == True and self.title != None:
			self.plotly_fig.update_layout(title = self.title)
		self.plotly_fig.update_layout(
			xaxis_title = self.xlabel,
			yaxis_title = self.ylabel,
		)
		# Axes scale:
		if self.xscale in [None, 'lin']:
			self.plotly_fig.update_layout(xaxis_type = 'linear')
		elif self.xscale == 'log':
			self.plotly_fig.update_layout(xaxis_type = 'log')
		if self.yscale in [None, 'lin']:
			self.plotly_fig.update_layout(yaxis_type = 'linear')
		elif self.yscale == 'log':
			self.plotly_fig.update_layout(yaxis_type = 'log')
		
		if self.aspect == 'equal':
			self.plotly_fig.update_yaxes(
				scaleanchor = "x",
				scaleratio = 1,
			)
		
		if self.subtitle != None:
			self.plotly_fig.add_annotation(
				text = self.subtitle,
				xref = "paper", 
				yref = "paper",
				x = .5, 
				y = 1,
				align = 'left',
				arrowcolor="#ffffff",
				font=dict(
					family="Courier New, monospace",
					color="#999999"
				),
			)
	
	def plot(self, x, y=None, **kwargs):
		validated_args = super().plot(x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties. Now you must access like "self.title" and so.
		if validated_args.get('marker') == None and validated_args.get('linestyle') != '':
			_mode = 'lines'
		elif validated_args.get('marker') != None and validated_args.get('linestyle') != '':
			_mode = 'lines+markers'
		elif validated_args.get('marker') != None and validated_args.get('linestyle') == '':
			_mode = 'markers'
		self.plotly_fig.add_trace(
			self.plotly_go.Scatter(
				x = validated_args['x'],
				y = validated_args['y'],
				name = validated_args.get('label'),
				opacity = validated_args.get('alpha'),
				mode = _mode,
				showlegend = True if validated_args.get('label') != None else False,
			)
		)
		if validated_args.get('color') != None:
			color = validated_args.get('color')
			color_str = '#'
			for rgb in color:
				color_hex_code = hex(int(rgb*255))[2:]
				if len(color_hex_code) < 2:
					color_hex_code = f'0{color_hex_code}'
				color_str += color_hex_code
			self.plotly_fig['data'][-1]['line']['color'] = color_str
		if validated_args.get('linewidth') != None:
			self.plotly_fig['data'][-1]['line']['width'] = validated_args.get('linewidth')
	
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
