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

