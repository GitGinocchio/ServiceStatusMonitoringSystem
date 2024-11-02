from scipy.interpolate import splrep, splev
import numpy as np



def generate_spline_curve(x, y,*, line = None, num_points=1000, clip_y : tuple[int, int] | None = None, k = 3, s : int | None = None):
    """
    Creates a cubic spline interpolation for latency data and generates x and y values for the curve.

    Parameters
    - x: array-like, x data
    - y: array-like, y data
    - num_points: int, number of x points to generate the curve (default 1000)

    Returns
    - x: array of x values for the spline curve
    - y: array of interpolated y values for the spline curve
    """
    # Crea l'oggetto spline
    tck = splrep(x, y, k=k, s=s)
    # Genera valori x per la curva
    if line is None: 
        line = np.linspace(min(x), max(x), num_points)
    # Valuta la funzione interpolata per questi valori x
    y_plot = splev(line, tck)

    if clip_y: 
        y_plot = np.clip(y_plot, clip_y[0], clip_y[1])

    return line, y_plot