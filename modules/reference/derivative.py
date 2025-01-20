from scipy._lib._finite_differences import _derivative

# 廃止されたので持ってきてる
def derivative(func, x0, dx=1.0, n=1, args=(), order=3):
    """
    Find the nth derivative of a function at a point.

    Given a function, use a central difference formula with spacing `dx` to
    compute the nth derivative at `x0`.

    .. deprecated:: 1.10.0
        `derivative` has been deprecated from `scipy.misc.derivative`
        in SciPy 1.10.0 and it will be completely removed in SciPy 1.12.0.
        You may consider using
        findiff: https://github.com/maroba/findiff or
        numdifftools: https://github.com/pbrod/numdifftools

    Parameters
    ----------
    func : function
        Input function.
    x0 : float
        The point at which the nth derivative is found.
    dx : float, optional
        Spacing.
    n : int, optional
        Order of the derivative. Default is 1.
    args : tuple, optional
        Arguments
    order : int, optional
        Number of points to use, must be odd.

    Notes
    -----
    Decreasing the step size too small can result in round-off error.

    Examples
    --------
    # >>> from scipy.misc import derivative
    # >>> def f(x):
    # ...     return x**3 + x**2
    # >>> derivative(f, 1.0, dx=1e-6)
    # 4.9999999999217337

    """
    return _derivative(func, x0, dx, n, args, order)