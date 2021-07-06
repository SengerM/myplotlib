from .figure import MPLFigure

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
