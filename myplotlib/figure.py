import os
import numpy as np
from .utils import get_timestamp
import __main__
import warnings


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
	
	def show(self):
		raise NotImplementedError(f'The <show> method is not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def save(self, fname=None):
		raise NotImplementedError(f'The <save> method is not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def delete(self):
		raise NotImplementedError(f'The <delete> method is not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
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
				raise ValueError(f'RGB elements in <color> must be bounded between 0 and 1, received <{color}>.')
	
	def _validate_alpha(self, alpha):
		try:
			alpha = float(alpha)
		except:
			raise ValueError(f'<alpha> must be a float number. Received {alpha} of type {type(alpha)}.')
		if not 0 <= alpha <= 1:
			raise ValueError(f'<alpha> must be bounded between 0 and 1, received <{alpha}>.')
	
	def _validate_linewidth(self, linewidth):
		try:
			linewidth = float(linewidth)
		except:
			raise ValueError(f'<linewidth> must be a float number. Received {linewidth} of type {type(linewidth)}.')
	
	def _validate_bins(self, bins):
		if isinstance(bins, int) and bins > 0:
			return
		elif hasattr(bins, '__iter__') and len(bins) > 0:
			return
		elif isinstance(bins, str):
			return
		else:
			raise TypeError(f'<bins> must be either an integer number, an array of float numbers or a string as defined for the numpy.histogram function, see https://numpy.org/doc/stable/reference/generated/numpy.histogram.html. Received {bins} of type {type(bins)}.')
	
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
		if kwargs.get('bins') != None:
			self._validate_bins(kwargs['bins'])
		if kwargs.get('density') != None:
			if kwargs.get('density') not in [True, False]:
				raise ValueError(f'<density> must be either True or False, received <{kwargs.get("density")}>.')
		if 'norm' in kwargs:
			if kwargs['norm'] not in ['lin','log']:
				raise ValueError(f'<norm> must be either "lin" or "log", received <{kwargs["norm"]}> of type {type(kwargs["norm"])}.')
	
	#### Plotting methods ↓↓↓↓
	"""
	Plotting methods here do not have to "do the job", they just validate
	things and define the interface. Each subclass has to do the job.
	When implementing one of these plotting methods in a subclass, use
	the same signature as here.
	"""
	def plot(self, x, y=None, **kwargs):
		implemented_kwargs = ['label', 'marker', 'color', 'alpha', 'linestyle', 'linewidth'] # This is specific for the "plot" method.
		for kwarg in kwargs.keys():
			if kwarg not in implemented_kwargs:
				raise NotImplementedError(f'<{kwarg}> not implemented for <plot> by myplotlib.')
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
	
	def hist(self, samples, **kwargs):
		implemented_kwargs = ['label', 'color', 'alpha', 'bins', 'density', 'linewidth'] # This is specific for the "hist" method.
		for kwarg in kwargs.keys():
			if kwarg not in implemented_kwargs:
				raise NotImplementedError(f'<{kwarg}> not implemented for <hist> by myplotlib.')
		self._validate_xy_are_arrays_of_numbers(samples)
		self._validate_kwargs(**kwargs)
		
		count, index = np.histogram(
			samples, 
			bins = kwargs.get('bins') if kwargs.get('bins') != None else 'auto',
			density = kwargs.get('density') if kwargs.get('density') != None else False,
		)
		count = list(count)
		count.insert(0,0)
		count.append(0)
		index = list(index)
		index.insert(0,index[0] - np.diff(index)[0])
		index.append(index[-1] + np.diff(index)[-1])
		index += np.diff(index)[0]/2 # This is because np.histogram returns the bins edges and I want to plot in the middle.
		
		validated_args = kwargs
		validated_args['samples'] = samples
		validated_args['bins'] = index
		validated_args['counts'] = count
		return validated_args
	
	def colormap(self, z, x=None, y=None, **kwargs):
		implemented_kwargs = ['alpha','norm'] # This is specific for the "colormap" method.
		for kwarg in kwargs.keys():
			if kwarg not in implemented_kwargs:
				raise NotImplementedError(f'<{kwarg}> not implemented for <colormap> by myplotlib.')
		self._validate_kwargs(**kwargs)
		validated_args = kwargs
		validated_args['x'] = x
		validated_args['y'] = y
		validated_args['z'] = z
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
	
	def show(self):
		self.matplotlib_plt.show()
	
	def save(self, fname=None):
		if fname is None:
			fname = self.title
		if fname is None:
			raise ValueError(f'Please provide a name for saving the figure to a file by the <fname> argument.')
		if fname[-4] != '.': fname = f'{fname}.png'
		self.matplotlib_fig.savefig(facecolor=(1,1,1,0), fname=fname)
	
	def close(self):
		self.matplotlib_plt.close(self.matplotlib_fig)
	
	def plot(self, x, y=None, **kwargs):
		validated_args = super().plot(x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		x = validated_args.get('x')
		y = validated_args.get('y')
		validated_args.pop('x')
		validated_args.pop('y')
		self.matplotlib_ax.plot(x, y, **validated_args)
		if validated_args.get('label') != None: # If you gave me a label it is obvious for me that you want to display it, no?
			self.matplotlib_ax.legend()
	
	def hist(self, samples, **kwargs):
		validated_args = super().hist(samples, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		samples = validated_args['samples']
		validated_args.pop('samples')
		validated_args.pop('counts') # Have no idea why I have to remove "counts", otherwise the next line raises a strange error.
		self.matplotlib_ax.hist(x = samples, **validated_args)
		if validated_args.get('label') != None: # If you provided a legend I assume you want to show it.
			self.matplotlib_ax.legend()
	
	def hist2d(self, _______, **kwargs):
		# ~ validated_args = super().hist(samples, **kwargs) # Validate arguments according to the standards of myplotlib.
		# ~ del(kwargs) # Remove it to avoid double access to the properties.
		raise NotImplementedError(f'<hist2d> not yet implemented for {self.__class__.__name__}')
	
	def colormap(self, z, x=None, y=None, **kwargs):
		validated_args = super().colormap(z, x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		z = np.array(validated_args.get('z'))
		validated_args.pop('z')
		x = validated_args.get('x')
		validated_args.pop('x')
		y = validated_args.get('y')
		validated_args.pop('y')
		if validated_args.get('norm') in [None, 'lin']: # linear normalization
			validated_args['norm'] = self.matplotlib_colors.Normalize(vmin=np.nanmin(z), vmax=np.nanmax(z))
		elif validated_args.get('norm') == 'log':
			temp = np.squeeze(np.asarray(z))
			while temp.min() <= 0:
				temp = temp[temp!=temp.min()]
			if (z<=0).any():
				z[z<=0] = float('Nan')
				warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. They will be replaced by float("inf") values for plotting (i.e. they will not appear in the plot).')
			validated_args['norm'] = self.matplotlib_colors.LogNorm(vmin=np.nanmin(z), vmax=np.nanmax(z))
			z[z!=z] = float('inf')
		if x is None and y is None:
			cs = self.matplotlib_ax.pcolormesh(z, rasterized=True, shading='auto', cmap='Blues_r', **validated_args)
		elif x is not None and y is not None:
			cs = self.matplotlib_ax.pcolormesh(x, y, z, rasterized=True, shading='auto', cmap='Blues_r', **validated_args)
		else: 
			raise ValueError('You must provide either "both x and y" or "neither x nor y"')
		self.matplotlib_fig.colorbar(cs)
	
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
	
	def show(self):
		self.plotly_fig.show()
	
	def save(self, fname):
		if fname is None:
			fname = self.title
		if fname is None:
			raise ValueError(f'Please provide a name for saving the figure to a file by the <fname> argument.')
		if fname[-5:] != '.html':
			if len(fname.split('.')) > 1:
				splitted = fname.split('.')
				splitted[-1] = 'html'
				fname = '.'.join(splitted)
			else:
				fname = f'{fname}.html'
		self.plotly.offline.plot(
			self.plotly_fig, 
			filename = fname,
			auto_open = False, 
			include_mathjax='cdn', # https://community.plotly.com/t/latex-text-does-not-work-at-all-in-plotly-offline/13800/7
		)
	
	def close(self):
		del(self.plotly_fig)
	
	def plot(self, x, y=None, **kwargs):
		validated_args = super().plot(x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
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
			self.plotly_fig['data'][-1]['marker']['color'] = self._rgb2hexastr_color(validated_args.get('color'))
		if validated_args.get('linewidth') != None:
			self.plotly_fig['data'][-1]['line']['width'] = validated_args.get('linewidth')
	
	def hist(self, samples, **kwargs):
		validated_args = super().hist(samples, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		if validated_args.get('marker') == None and validated_args.get('linestyle') != '':
			_mode = 'lines'
		elif validated_args.get('marker') != None and validated_args.get('linestyle') != '':
			_mode = 'lines+markers'
		elif validated_args.get('marker') != None and validated_args.get('linestyle') == '':
			_mode = 'markers'
		self.plotly_fig.add_traces(
			self.plotly_go.Scatter(
				x = validated_args['bins'], 
				y = validated_args['counts'],
				line = dict(shape='hvh'),
				mode = _mode,
				opacity = validated_args.get('alpha'),
				name = validated_args.get('label'),
				showlegend = True if validated_args.get('label') != None else False,
			)
		)
		# ~ self.fig.update_layout(barmode='overlay')
		if validated_args.get('color') != None:
			self.plotly_fig['data'][-1]['marker']['color'] = self._rgb2hexastr_color(validated_args.get('color'))
		if validated_args.get('linewidth') != None:
			self.plotly_fig['data'][-1]['line']['width'] = validated_args.get('linewidth')
	
	def hist2d(self, _______, **kwargs):
		# ~ validated_args = super().hist(samples, **kwargs) # Validate arguments according to the standards of myplotlib.
		# ~ del(kwargs) # Remove it to avoid double access to the properties.
		raise NotImplementedError(f'<hist2d> not yet implemented for {self.__class__.__name__}')
	
	def colormap(self, z, x=None, y=None, **kwargs):
		validated_args = super().colormap(z, x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		z = np.array(validated_args.get('z'))
		validated_args.pop('z')
		x = validated_args.get('x')
		validated_args.pop('x')
		y = validated_args.get('y')
		validated_args.pop('y')
		if x is None and y is None:
			x, y = np.meshgrid([i for i in range(z.shape[0])], [i for i in range(z.shape[1])])
		z2plot = z
		if 'norm' in validated_args and validated_args['norm'] == 'log':
			if (z<=0).any():
				warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. They will be replaced by float("NaN") values for plotting (i.e. they will not appear in the plot).')
				z2plot[z2plot<=0] = float('NaN')
			z2plot = np.log(z2plot)
		self.plotly_fig.add_trace(
			self.plotly_go.Heatmap(
				z = z2plot,
				x = x[0],
				y = y.transpose()[0],
			)
		)
	
	def _rgb2hexastr_color(self, rgb_color: tuple):
		# Assuming that <rgb_color> is a (r,g,b) tuple.
		color_str = '#'
		for rgb in rgb_color:
			color_hex_code = hex(int(rgb*255))[2:]
			if len(color_hex_code) < 2:
				color_hex_code = f'0{color_hex_code}'
			color_str += color_hex_code
		return color_str

