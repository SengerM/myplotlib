import numpy as np
import warnings
from shutil import copyfile
import plotly.graph_objects as go

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
	DEFAULT_COLORS = [
		(255, 59, 59),
		(52, 71, 217),
		(4, 168, 2),
		(224, 146, 0),
		(224, 0, 183),
		(0, 230, 214),
		(140, 0, 0),
		(9, 0, 140),
		(107, 0, 96),
	]
	DEFAULT_COLORS = [tuple(np.array(color)/255) for color in DEFAULT_COLORS]

	def pick_default_color(self):
		# ~ global DEFAULT_COLORS
		color = self.DEFAULT_COLORS[0]
		self.DEFAULT_COLORS = self.DEFAULT_COLORS[1:] + [self.DEFAULT_COLORS[0]]
		return color
	
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
	
	def save(self, fname=None, *args, **kwargs):
		raise NotImplementedError(f'The <save> method is not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	def close(self):
		raise NotImplementedError(f'The <close> method is not implemented yet for the plotting package you are using! (Specifically for the class {self.__class__.__name__}.)')
	
	#### Validation methods ↓↓↓↓
	"""
	This methods validate arguments so we all speak the same language.
	"""
	def _validate_axis_scale(self, scale: str):
		# Assume that <scale> is a string. Raises an error if "scale" is not a valid scale.
		valid_scales = ['lin', 'log']
		if scale not in valid_scales:
			raise ValueError(f'Axis scale must be one of {valid_scales}, received {scale}.')
	
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
	
	def _validate_marker(self, marker):
		IMPLEMENTED_MARKERS = ['.', '+', 'x', 'o', None]
		if marker not in IMPLEMENTED_MARKERS:
			raise ValueError(f'<marker> must be one of {IMPLEMENTED_MARKERS}, received "{marker}".')
	
	def _validate_kwargs(self, **kwargs):
		if 'marker' in kwargs:
			self._validate_marker(kwargs['marker'])
		if kwargs.get('label') != None:
			if not isinstance(kwargs.get('label'), str):
				raise TypeError(f'<label> must be a string.')
		if kwargs.get('color') != None:
			self._validate_color(kwargs['color'])
		if kwargs.get('alpha') != None:
			self._validate_alpha(kwargs['alpha'])
		if kwargs.get('linewidth') != None:
			self._validate_linewidth(kwargs['linewidth'])
		if kwargs.get('bins') is not None:
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
		if 'plot' not in self.__class__.__dict__.keys(): # Raise error if the method was not overriden
			raise NotImplementedError(f'<plot> not implemented for {type(self)}.')
		implemented_kwargs = ['label', 'marker', 'color', 'alpha', 'linestyle', 'linewidth'] # This is specific for the "plot" method.
		for kwarg in kwargs.keys():
			if kwarg not in implemented_kwargs:
				raise NotImplementedError(f'<{kwarg}> not implemented for <plot> by myplotlib.')
		self._validate_xy_are_arrays_of_numbers(x)
		if y is not None:
			self._validate_xy_are_arrays_of_numbers(y)
			if len(x) != len(y):
				raise ValueError(f'Lengths of <x> and <y> are not the same, received len(x)={len(x)} and len(y)={len(y)}.')
		else:
			y = x
			x = [i for i in range(len(x))]
		if kwargs.get('color') is None:
			kwargs['color'] = self.pick_default_color()
		self._validate_kwargs(**kwargs)
		validated_args = kwargs
		validated_args['x'] = x
		validated_args['y'] = y
		return validated_args
	
	def hist(self, samples, **kwargs):
		if 'hist' not in self.__class__.__dict__.keys(): # Raise error if the method was not overriden
			raise NotImplementedError(f'<hist> not implemented for {type(self)}.')
		implemented_kwargs = ['label', 'color', 'alpha', 'bins', 'density', 'linewidth', 'linestyle'] # This is specific for the "hist" method.
		for kwarg in kwargs.keys():
			if kwarg not in implemented_kwargs:
				raise NotImplementedError(f'<{kwarg}> not implemented for <hist> by myplotlib.')
		self._validate_xy_are_arrays_of_numbers(samples)
		if kwargs.get('color') is None:
			kwargs['color'] = self.pick_default_color()
		self._validate_kwargs(**kwargs)
		
		samples = np.array(samples)
		count, index = np.histogram(
			samples[~np.isnan(samples)], 
			bins = kwargs.get('bins') if kwargs.get('bins') is not None else 'auto',
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
		if 'colormap' not in self.__class__.__dict__.keys(): # Raise error if the method was not overriden
			raise NotImplementedError(f'<colormap> not implemented for {type(self)}.')
		return self.validate_colormap_args(z=z, x=x, y=y, **kwargs)
	
	def validate_colormap_args(self, z, x=None, y=None, **kwargs):
		# I had to wrote this function because "contour" validates the same arguments as "colormap", but calling "self.colormap" inside contour created problems calling the contour method of the subclasses.
		implemented_kwargs = ['alpha','norm', 'colorscalelabel'] # This is specific for the "colormap" method.
		for kwarg in kwargs.keys():
			if kwarg not in implemented_kwargs:
				raise NotImplementedError(f'<{kwarg}> not implemented for <colormap> by myplotlib.')
		self._validate_kwargs(**kwargs)
		validated_args = kwargs
		validated_args['x'] = x
		validated_args['y'] = y
		validated_args['z'] = z
		return validated_args
	
	def contour(self, z, x=None, y=None, **kwargs):
		if 'contour' not in self.__class__.__dict__.keys(): # Raise error if the method was not overriden
			raise NotImplementedError(f'<contour> not implemented for {type(self)}.')
		if 'levels' in kwargs:
			levels = kwargs['levels']
			if not isinstance(levels, int):
				raise TypeError(f'<levels> must be an integer number specifying the number of levels for the contour plot, received {levels} of type {type(levels)}.')
		validated_args = self.validate_colormap_args(z, x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		if 'levels' in locals():
			validated_args['levels'] = levels
		return validated_args
	
	def fill_between(self, x, y1, y2=None, **kwargs):
		if 'fill_between' not in self.__class__.__dict__.keys(): # Raise error if the method was not overriden
			raise NotImplementedError(f'<fill_between> not implemented for {type(self)}.')
		implemented_kwargs = ['label', 'color', 'alpha', 'linestyle', 'linewidth'] # This is specific for the "fill_between" method.
		for kwarg in kwargs.keys():
			if kwarg not in implemented_kwargs:
				raise NotImplementedError(f'<{kwarg}> not implemented for <fill_between> by myplotlib.')
		self._validate_xy_are_arrays_of_numbers(x)
		self._validate_xy_are_arrays_of_numbers(y1)
		if y2 is None:
			y2 = np.zeros(len(x))
		self._validate_xy_are_arrays_of_numbers(y2)
		if kwargs.get('color') is None:
			kwargs['color'] = self.pick_default_color()
		self._validate_kwargs(**kwargs)
		validated_args = kwargs
		validated_args['x'] = x
		validated_args['y1'] = y1
		validated_args['y2'] = y2
		validated_args['alpha'] = .5 # Default alpha value.
		return validated_args
	
	def error_band(self, x, y, ytop, ylow, **kwargs):
		if 'error_band' not in self.__class__.__dict__.keys(): # Raise error if the method was not overriden
			raise NotImplementedError(f'<error_band> not implemented for {type(self)}.')
		self._validate_xy_are_arrays_of_numbers(x)
		self._validate_xy_are_arrays_of_numbers(y)
		self._validate_xy_are_arrays_of_numbers(ytop)
		self._validate_xy_are_arrays_of_numbers(ylow)
		if any(np.array(y)>np.array(ytop)) or any(np.array(y)<np.array(ylow)):
			raise ValueError(f'Either y>ytop or y<ylow is true for at least one point, please check your arrays.')
		if len(x) == len(y) == len(ytop) == len(ylow):
			pass
		else:
			raise ValueError(f'len(x) == len(y) == len(ytop) == len(ylow) is not True, please check your arrays.')
		if kwargs.get('color') is None:
			kwargs['color'] = self.pick_default_color()
		self._validate_kwargs(**kwargs)
		validated_args = kwargs
		validated_args['x'] = x
		validated_args['y'] = y
		validated_args['ytop'] = ytop
		validated_args['ylow'] = ylow
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
	
	def save(self, fname=None, *args, **kwargs):
		if fname is None:
			fname = self.title
		if fname is None:
			raise ValueError(f'Please provide a name for saving the figure to a file by the <fname> argument.')
		if fname[-4] != '.': fname = f'{fname}.png'
		self.matplotlib_fig.savefig(facecolor=(1,1,1,0), fname=fname, *args, **kwargs)
	
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
		validated_args['bins'] = np.array(validated_args['bins'][:-2]) + np.diff(validated_args['bins'])[:-1]/2 # This is to normalize the binning criteria with plotly.
		samples = validated_args['samples']
		validated_args.pop('samples')
		validated_args.pop('counts') # Have no idea why I have to remove "counts", otherwise the next line raises a strange error.
		self.matplotlib_ax.hist(x = samples, histtype='step', **validated_args)
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
		if 'colorscalelabel' in validated_args:
			colorscalelabel = validated_args.get('colorscalelabel')
			validated_args.pop('colorscalelabel')
		if x is None and y is None:
			cs = self.matplotlib_ax.pcolormesh(z, rasterized=True, shading='auto', cmap='Blues_r', **validated_args)
		elif x is not None and y is not None:
			cs = self.matplotlib_ax.pcolormesh(x, y, z, rasterized=True, shading='auto', cmap='Blues_r', **validated_args)
		else: 
			raise ValueError('You must provide either "both x and y" or "neither x nor y"')
		cbar = self.matplotlib_fig.colorbar(cs)
		if 'colorscalelabel' in locals():
			cbar.set_label(colorscalelabel, rotation = 90)
	
	def contour(self, z, x=None, y=None, **kwargs):
		validated_args = super().contour(z, x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
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
			cs = self.matplotlib_ax.contour(z, rasterized=True, shading='auto', cmap='Blues_r', **validated_args)
		elif x is not None and y is not None:
			cs = self.matplotlib_ax.contour(x, y, z, rasterized=True, shading='auto', cmap='Blues_r', **validated_args)
		else: 
			raise ValueError('You must provide either "both x and y" or "neither x nor y"')
		cbar = self.matplotlib_fig.colorbar(cs)
		if 'colorscalelabel' in locals():
			cbar.set_label(colorscalelabel, rotation = 90)
		self.matplotlib_ax.clabel(cs, inline=True, fontsize=10)
	
	def fill_between(self, x, y1, y2=None, **kwargs):
		validated_args = super().fill_between(x, y1, y2, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		x = validated_args['x']
		validated_args.pop('x')
		y1 = validated_args['y1']
		validated_args.pop('y1')
		y2 = validated_args['y2']
		validated_args.pop('y2')
		self.matplotlib_ax.fill_between(x, y1, y2, **validated_args)
		if validated_args.get('label') != None: # If you gave me a label it is obvious for me that you want to display it, no?
			self.matplotlib_ax.legend()
	
class MPLPlotlyWrapper(MPLFigure):
	LINESTYLE_TRANSLATION = {
		'solid': None,
		'none': None,
		'dashed': 'dash',
		'dotted':  'dot',
	}
	
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
			pass
		elif self.xscale == 'log':
			self.plotly_fig.update_layout(xaxis_type = 'log')
		if self.yscale in [None, 'lin']:
			pass
		elif self.yscale == 'log':
			self.plotly_fig.update_layout(yaxis_type = 'log')
		
		if self.aspect == 'equal':
			self.plotly_fig.update_yaxes(
				scaleanchor = "x",
				scaleratio = 1,
			)
		
		if self.subtitle != None:
			self.plotly_fig.add_annotation(
				text = self.subtitle.replace('\n','<br>'),
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
	
	def save(self, fname, include_plotlyjs='cdn', *args, **kwargs):
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
			include_plotlyjs = include_plotlyjs,
			*args, 
			**kwargs
		)
	
	def close(self):
		del(self.plotly_fig)
	
	def plot(self, x, y=None, **kwargs):
		validated_args = super().plot(x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		self.plotly_fig.add_trace(
			self.plotly_go.Scatter(
				x = validated_args['x'],
				y = validated_args['y'],
				name = validated_args.get('label'),
				opacity = validated_args.get('alpha'),
				mode = self.translate_marker_and_linestyle_to_mode(validated_args.get('marker'), validated_args.get('linestyle')),
				marker_symbol = self._map_marker_to_plotly(validated_args.get('marker')),
				showlegend = True if validated_args.get('label') != None else False,
				line = dict(
					dash = self.LINESTYLE_TRANSLATION[validated_args.get('linestyle')] if 'linestyle' in validated_args else None,
				)
			)
		)
		if validated_args.get('color') != None:
			self.plotly_fig['data'][-1]['marker']['color'] = self._rgb2hexastr_color(validated_args.get('color'))
		if validated_args.get('linewidth') != None:
			self.plotly_fig['data'][-1]['line']['width'] = validated_args.get('linewidth')
	
	def fill_between(self, x, y1, y2=None, **kwargs):
		validated_args = super().fill_between(x, y1, y2, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		x = validated_args['x']
		validated_args.pop('x')
		y1 = validated_args['y1']
		validated_args.pop('y1')
		y2 = validated_args['y2']
		validated_args.pop('y2')
		self.plot(
			x = list(x) + list(x)[::-1],
			y = list(y1) + list(y2)[::-1],
			**validated_args,
		)
		self.plotly_fig['data'][-1]['fill'] = 'toself'
		self.plotly_fig['data'][-1]['hoveron'] = 'points'
		self.plotly_fig['data'][-1]['line']['width'] = 0
	
	def error_band(self, x, y, ytop, ylow, **kwargs):
		validated_args = super().error_band(x, y, ytop, ylow, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		x = validated_args['x']
		validated_args.pop('x')
		y = validated_args['y']
		validated_args.pop('y')
		ytop = validated_args['ytop']
		validated_args.pop('ytop')
		ylow = validated_args['ylow']
		validated_args.pop('ylow')
		legendgroup = str(np.random.rand()) + str(np.random.rand())
		self.plot(x, y, **validated_args)
		self.plotly_fig['data'][-1]['legendgroup'] = legendgroup
		self.fill_between(
			x, 
			ylow, 
			ytop,
			color = validated_args['color'],
		)
		self.plotly_fig['data'][-1]['showlegend'] = False
		self.plotly_fig['data'][-1]['legendgroup'] = legendgroup
	
	def hist(self, samples, **kwargs):
		validated_args = super().hist(samples, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		self.plotly_fig.add_traces(
			self.plotly_go.Scatter(
				x = validated_args['bins'], 
				y = validated_args['counts'],
				mode = self.translate_marker_and_linestyle_to_mode(validated_args.get('marker'), validated_args.get('linestyle')),
				opacity = validated_args.get('alpha'),
				name = validated_args.get('label'),
				showlegend = True if validated_args.get('label') != None else False,
				line = dict(
					shape='hvh',
					dash = self.LINESTYLE_TRANSLATION[validated_args.get('linestyle')] if 'linestyle' in validated_args else None,
				)
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
		if x is not None and y is not None:
			if x.size == y.size == z.size:
				x = x[0]
				y = y.transpose()[0]
		z2plot = z
		if 'norm' in validated_args and validated_args['norm'] == 'log':
			if (z<=0).any():
				warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. They will be replaced by float("NaN") values for plotting (i.e. they will not appear in the plot).')
				z2plot[z2plot<=0] = float('NaN')
			z2plot = np.log(z2plot)
		self.plotly_fig.add_trace(
			self.plotly_go.Heatmap(
				z = z2plot,
				x = x,
				y = y,
				colorbar = dict(
					title = (('log ' if validated_args.get('norm') == 'log' else '') + validated_args.get('colorscalelabel')) if validated_args.get('colorscalelabel') is not None else None,
					titleside = 'right',
				),
				hovertemplate = f'{(self.xlabel if self.xlabel is not None else "x")}: %{{x}}<br>{(self.ylabel if self.ylabel is not None else "y")}: %{{y}}<br>{(validated_args.get("colorscalelabel") if "colorscalelabel" in validated_args is not None else "color scale")}: %{{z}}<extra></extra>', # https://community.plotly.com/t/heatmap-changing-x-y-and-z-label-on-tooltip/23588/6
			)
		)
		self.plotly_fig.update_layout(legend_orientation="h")
	
	def contour(self, z, x=None, y=None, **kwargs):
		validated_args = super().colormap(z, x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		if 'levels' in validated_args:
			# See in Matplotlib's documentation to see what this is supposed to do.
			raise NotImplementedError(f'<levels> not yet implemented for <contour> for Plotly.')
		z = np.array(validated_args.get('z'))
		validated_args.pop('z')
		x = validated_args.get('x')
		validated_args.pop('x')
		y = validated_args.get('y')
		validated_args.pop('y')
		if x is not None and y is not None:
			if x.size == y.size == z.size:
				x = x[0]
				y = y.transpose()[0]
		z2plot = z
		if 'norm' in validated_args and validated_args['norm'] == 'log':
			if (z<=0).any():
				warnings.warn('Warning: log color scale was selected and there are <z> values <= 0. They will be replaced by float("NaN") values for plotting (i.e. they will not appear in the plot).')
				z2plot[z2plot<=0] = float('NaN')
			z2plot = np.log(z2plot)
		self.plotly_fig.add_trace(
			self.plotly_go.Contour(
				z = z2plot,
				x = x,
				y = y,
				colorbar = dict(
					title = (('log ' if validated_args.get('norm') == 'log' else '') + validated_args.get('colorscalelabel')) if validated_args.get('colorscalelabel') is not None else None,
					titleside = 'right',
				),
				hovertemplate = f'{(self.xlabel if self.xlabel is not None else "x")}: %{{x}}<br>{(self.ylabel if self.ylabel is not None else "y")}: %{{y}}<br>{(validated_args.get("colorscalelabel") if "colorscalelabel" in validated_args is not None else "color scale")}: %{{z}}<extra></extra>', # https://community.plotly.com/t/heatmap-changing-x-y-and-z-label-on-tooltip/23588/6
				contours=dict(
					coloring = 'heatmap',
					showlabels = True, # show labels on contours
					labelfont = dict( # label font properties
						color = 'white',
					)
				)
			)
		)
		self.plotly_fig.update_layout(legend_orientation="h")
	
	def _rgb2hexastr_color(self, rgb_color: tuple):
		# Assuming that <rgb_color> is a (r,g,b) tuple.
		color_str = '#'
		for rgb in rgb_color:
			color_hex_code = hex(int(rgb*255))[2:]
			if len(color_hex_code) < 2:
				color_hex_code = f'0{color_hex_code}'
			color_str += color_hex_code
		return color_str
	
	def _map_marker_to_plotly(self, marker):
		if marker is None:
			return None
		markers_map = {
			'.': 'circle',
			'+': 'cross',
			'x': 'x',
			'o': 'circle-open',
		}
		return markers_map[marker]
	
	def translate_marker_and_linestyle_to_mode(self, marker, linestyle):
		if marker == None and linestyle != 'none':
			mode = 'lines'
		elif marker != None and linestyle != 'none':
			mode = 'lines+markers'
		elif marker != None and linestyle == 'none':
			mode = 'markers'
		else:
			mode = 'lines'
		return mode


class MPLSaoImageDS9Wrapper(MPLFigure):
	"""
	This is a very specific type of figure, intended to be used with 
	images.
	"""
	DIRECTORY_FOR_TEMPORARY_FILES = '.myplotlib_ds9_temp'
	_norm = 'lin'
	
	def __init__(self):
		super().__init__()
		import os
		self.os = os
		from astropy.io import fits
		self.astropy_io_fits = fits
		if not self.os.path.isdir(self.DIRECTORY_FOR_TEMPORARY_FILES):
			self.os.makedirs(self.DIRECTORY_FOR_TEMPORARY_FILES)
	
	@property
	def title(self):
		return self._title.replace(' ', '_')
	
	def colormap(self, z, x=None, y=None, **kwargs):
		validated_args = super().colormap(z, x, y, **kwargs) # Validate arguments according to the standards of myplotlib.
		del(kwargs) # Remove it to avoid double access to the properties.
		z = np.array(validated_args.get('z'))
		hdul_new = self.astropy_io_fits.PrimaryHDU(z)
		if f'{self.title}.fits' in self.os.listdir(self.DIRECTORY_FOR_TEMPORARY_FILES):
			self.os.remove(f'{self.DIRECTORY_FOR_TEMPORARY_FILES}/{self.title}.fits')
		hdul_new.writeto(f'{self.DIRECTORY_FOR_TEMPORARY_FILES}/{self.title}.fits')
		if 'norm' in validated_args and validated_args['norm'] == 'log':
			self._norm = 'log'
	
	def show(self):
		self.os.system(f'ds9 {self.DIRECTORY_FOR_TEMPORARY_FILES}/{self.title}.fits' + (' -log' if self._norm == 'log' else ''))
	
	def close(self):
		if len(self.os.listdir(self.DIRECTORY_FOR_TEMPORARY_FILES)) == 0:
			self.os.rmdir(self.DIRECTORY_FOR_TEMPORARY_FILES)
		self.__del__()
	
	def __del__(self):
		if self.os.path.exists(f'{self.DIRECTORY_FOR_TEMPORARY_FILES}/{self.title}.fits'):
			self.os.remove(f'{self.DIRECTORY_FOR_TEMPORARY_FILES}/{self.title}.fits')
	
	def save(self, fname):
		if fname[:-5] != '.fits':
			fname = '.'.join(fname.split('.')[:-1] + ['fits'])
		copyfile(f'{self.DIRECTORY_FOR_TEMPORARY_FILES}/{self.title}.fits', fname)
