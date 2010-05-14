import wx
import time

from mplot import PlotFrame, ImageFrame

class PlotDisplay(PlotFrame):
    def __init__(self, parent=None, wid=1, larch=None, **kws):
        PlotFrame.__init__(self, parent=parent, 
                                 exit_callback=self.onExit, **kws)
        self.Show()
        self.Raise()
        self.cursor_pos = []
        self.panel.cursor_callback = self.onCursor
        self.wid = int(wid)
        self.larch = larch
        self.symname = '_plotter.plot%i' % self.wid
        if larch is not None:
            symtable = larch.symtable
            if not symtable.has_group('_plotter'):
                symtable.newgroup('_plotter')
            symtable.set_symbol(self.symname, self)
        
    def onExit(self, o, **kw):
        try:
            symtable = self.larch.symtable
            if symtable.has_group('_plotter'):
                symtable.del_symbol(self.symname)
        except:
            pass
        self.Destroy()

    def onCursor(self,x=None, y=None,**kw):
        symtable = self.larch.symtable
        if not symtable.has_group('_plotter'):
            symtable.newgroup('_plotter')
        symtable.set_symbol('%s_x'  % self.symname, x)
        symtable.set_symbol('%s_y'  % self.symname, y)        
       

class ImageDisplay(ImageFrame):
    def __init__(self, parent=None, wid=1, larch=None, **kws):
        ImageFrame.__init__(self, parent=parent,
                                  exit_callback=self.onExit, **kws)
        self.Show()
        self.Raise()
        self.cursor_pos = []
        self.panel.cursor_callback = self.onCursor
        self.wid = int(wid)
        self.larch = larch
        if larch is not None:
            symtable = larch.symtable
            if not symtable.has_group('_plotter'):
                symtable.newgroup('_plotter')
            symtable.set_symbol('_plotter.img%i' % self.wid, self)
        
    def onExit(self, o, **kw):
        try:
            symtable = self.larch.symtable
            if symtable.has_group('_plotter'):
                symtable.del_symbol('_plotter.img%i' % self.wid)
        except:
            pass
        self.Destroy()
        
    def onCursor(self,x=None, y=None,**kw):
        symtable = self.larch.symtable
        if not symtable.has_group('_plotter'):
            symtable.newgroup('_plotter')
        symtable.set_symbol('_plotter.img%i_x' % self.wid, x)
        symtable.set_symbol('_plotter.img%i_y' % self.wid, y)

def _getDisplay(win=1, larch=None, parent=None, image=False):
    """make a plotter"""
    # print "_getDisplay ", win, image, larch, parent
    if larch is None:
        return
    win = max(1, int(abs(win)))
    
    symname = '_plotter.plot%i' %win
    title   = 'Larch Plot Display Window %i' % win
    creator = PlotDisplay
    if image:
        creator = ImageDisplay
        title   = 'Larch Image Display Window %i' % win
    display = larch.symtable.get_symbol(symname, create=True)
    
    if display is None:
        display = creator(wid=win, parent=parent, larch=larch)
        larch.symtable.set_symbol(symname, display)
        t0 = time.time()
        while display is None:
            display = larch.symtable.get_symbol(symname)
            time.sleep(0.05)
            if t0 - time.time() > 5.0:
                break
    if display is not None:
        display.SetTitle(title)
    return display

def _plot(x,y, win=1, larch=None, parent=None, **kws):
    """plot(x, y[, win=1], options])

    Plot 2-D trace of x, y arrays in a Plot Frame, clearing
    any plot currently in the Plot Frame.

    Parameters:
    --------------
        x :  array of ordinate values
        y :  array of abscissa values (x and y must be same size!)

        win: index of Plot Frame (0, 1, etc).  May create a new Plot Frame.

        label: label for trace
        title:  title for Plot
        xlabel: x-axis label
        ylabel: y-axis label
        ylog_scale: whether to show y-axis as log-scale (True or False)
        grid: whether to draw background grid (True or False)
        
        color: color for trace (name such as 'red', or '#RRGGBB' hex string)
        style: trace linestyle (one of 'solid', 'dashed', 'dotted', 'dot-dash')
        linewidth:  integer width of line
        marker:  symbol to draw at eac point ('+', 'o', 'x', 'square', etc)
        markersize: integer size of marker

        drawstyle: ?
        
        dy: array for error bars in y (must be same size as y!)
        yaxis='left'??
        use_dates 
        autoscale=True,
        refresh=True, 
 
    See Also:
    -----------
    oplot
    
    """
    # print '_plot: ', win, larch, parent, kws
    plotter = _getDisplay(parent=parent, win=win, larch=larch)
    if plotter is not None:
        plotter.plot(x, y, **kws)    
    
def _oplot(x,y, win=1, larch=None, parent=None, **kws):
    """oplot(x, y[, win=0], options])

    Plot 2-D trace of x, y arrays in a Plot Frame, over-plotting
    any plot currently in the Plot Frame.

    See Also:
    -----------
    plot
    
    """
    plotter = _getDisplay(parent=parent, win=win, larch=larch)
    if plotter is not None:
        plotter.oplot(x, y, **kws)

def _imshow(map, win=1, larch=None, parent=None, **kws):
    """imshow(map[, options])
    
    Display an image for a 2-D array, as a map

    map:
    """
    img = _getDisplay(parent=parent, win=win, larch=larch, image=True)
    if img is not None:
        img.display(map, **kws)
    
def registerPlugin():
    return ('_plotter', True,
            {'plot':_plot,
             'oplot': _oplot,
             'imshow':_imshow})

        
