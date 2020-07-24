# myplotlib

A unique interface for plotting my stuff. The idea is to implement the same interface for the basic stuff in matplotlib and in plotly.

## Example

```Python
import myplotlib as mpl

mpl.manager.set_style('latex one column') # You can comment this line and use the default style

fig1 = mpl.manager.new() # Create a new figure
fig1.plot( # Here it is the same as "ax.plot" in matplotlib
	[1,2,3,4],
	[1,4,7,6],
	label = 'Data 1',
	marker = '.',
)
fig1.plot( # Here it is the same as "ax.plot" in matplotlib
	[1,2,3,4,5],
	[9,7,6,4,3],
	label = 'Data 2',
	color = (0,0,0),
	linestyle = '--',
)
fig1.set( # This is specific from "myplotlib"
	xlabel = 'x label',
	ylabel = 'y axis',
	title = 'This is the title',
	show_title = False, # This hides the title from the plot, but still uses this title for saving the file if you call "mpl.manager.save_all"
)

f2 = mpl.manager.new() # Create a new figure
f2.plot([5,3,6,5,2,7,9,8,3,4,3,2,2,1,2]) # Same as "ax.plot" in matplotlib

mpl.manager.save_all(format = 'pdf', mkdir = 'directory for figures', timestamp = True)
```
