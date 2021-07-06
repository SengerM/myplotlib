from .figure import MPLFigure

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
