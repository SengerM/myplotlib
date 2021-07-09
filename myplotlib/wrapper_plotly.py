from .figure import MPLFigure
import numpy as np

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
