import matplotlib
# from matplotlib.ticker import AutoMinorLocator
import numpy as np

# If the code gives a lot of matplotlib deprecation warnings
# these can be turned off (although this is not a recommended procedure)
# import warnings
# warnings.filterwarnings("ignore")

# Store original plot parameters so that we can revert:
ORIG_MATPLOTLIB_CONF = dict(matplotlib.rcParams)

def set_params(fig_width=None, fig_height=None, columns=1, fontsize=8, dpi=300,
            serif='serif', font=None, latex=True, latex_extra='',
            ticks='', minor=False):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this function before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    columns : {1, 2}; 1 is default
    fontsize : 8 pt is default
    dpi : 300 is default, set to 600 for poster printing or PR figures
    serif : serif is default, set to sans-serif as an alternative
    font : name of font to be used (if not default)
    latex : True is default, use LaTeX for text (this is slow!)
    latex_extra : extra text to add to LaTeX preamble
    ticks : {'', 'in', 'out', 'inall'} out is default, set to 'in' or 'inall'
    minor : False is default, set to True to also get minor ticks 
    """

    assert(columns in [1, 2])
    assert(ticks in ['', 'in', 'out', 'inall'])

    if fig_width is None:
        # Figure widths for one-column and two-column printing
        # (taken from https://www.elsevier.com/authors/author-schemas/artwork-and-media-instructions/artwork-sizing)
        if columns == 2:
            fig_width = 3.5
        else:
            fig_width = 7.0

    if fig_height is None:
        golden_mean = (np.sqrt(5.0) - 1.0) / 2.0 # aesthetic ratio
        fig_height = fig_width * golden_mean # height in inches

    # print('\nOld keys:')
    # print(matplotlib.rcParams.keys())
    
    # May have to set 'backend': 'ps'
    params = {
        'axes.labelsize' : fontsize,
        'axes.titlesize' : 1.2*fontsize,
        'font.size': fontsize,
        'legend.fontsize' : fontsize,
        'xtick.labelsize' : fontsize,
        'ytick.labelsize' : fontsize,
        'axes.linewidth' : 1,
        'lines.linewidth' : 1,
        'figure.figsize' : [fig_width, fig_height],
        'font.family' : serif,
        'savefig.bbox' : 'tight',
        'savefig.dpi' : dpi
    }

    # Set serif or sans serif font
    if serif == 'sans-serif':
        if font: params['font.sans-serif'] = [font]
    elif serif == 'serif':
        if font: params['font.serif'] = [font]
    
    # LaTeX preamble
    latex_preamble = r'\usepackage{siunitx}'
    latex_preamble += r'\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}'
    if latex_extra: latex_preamble += latex_extra
    latex_params = {'text.usetex' : latex,
        'text.latex.preamble' : latex_preamble
    }
    # print(params)
    # print(latex_params)
    matplotlib.rcParams.update(params)
    matplotlib.rcParams.update(latex_params)

    # Tick settings
    if ticks == 'in':
        tick_params = {'xtick.direction' : 'in',
            'ytick.direction' : 'in'
        }
    elif ticks == 'out':
        tick_params = {'xtick.direction' : 'out',
            'ytick.direction' : 'out'
        }
    elif ticks == 'inall':
        tick_params = {
            'xtick.direction' : 'in',
            'ytick.direction' : 'in',
            'xtick.top' : True,
            'xtick.bottom' : True,
            'ytick.left' : True,
            'ytick.right' : True
        }
    if ticks:
        # print('Setting tick parameters to', tick_params)
        matplotlib.rcParams.update(tick_params)

    # Turn on minor ticks; make ticks bigger
    if minor:
        # print('Turn on minor ticks')
        tick_extra = {
            'xtick.minor.visible' : True,
            'ytick.minor.visible' : True,
            'xtick.major.size': 5.0,
            'ytick.major.size': 5.0,
            'xtick.minor.size': 3.5,
            'ytick.minor.size': 3.5,
        }
        matplotlib.rcParams.update(tick_extra)

    # print('\nNew keys:')
    # print(matplotlib.rcParams.keys())
        
def revert_params():
    """Revert any changes done to matplotlib parameters and restore
    the state before homogenise_plot was called
    """
    
    dict.update(matplotlib.rcParams, ORIG_MATPLOTLIB_CONF)
    # matplotlib.rcParams.update(ORIG_MATPLOTLIB_CONF)
