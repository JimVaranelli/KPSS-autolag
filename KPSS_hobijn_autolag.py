import numpy as np
from numpy.testing import assert_equal, assert_almost_equal
from statsmodels.tsa.stattools import kpss
from statsmodels.datasets import macrodata, sunspots, nile, randhie, modechoice
import warnings
import sys

def _kpss_autolag(resids, nobs):
    """
    Computes the number of lags for variance estimation in KPSS test using
    method of Hobijn et al (1998). See also Andrews (1991), Newey & West (1994),
    and Schwert (1989). Assumes Bartlett / Newey-West kernel.
    """
    covlags = int(np.power(nobs, 2. / 9.))
    s0 = sum(resids**2) / nobs
    s1 = 0
    for i in range(1, covlags + 1):
        resids_prod = np.dot(resids[i:], resids[:nobs - i])
        resids_prod /= (nobs / 2.)
        s0 += resids_prod
        s1 += i * resids_prod
    s_hat = s1 / s0;
    pwr = 1. / 3.
    gamma_hat = 1.1447 * np.power(s_hat * s_hat, pwr)
    autolags = np.amin([nobs, int(gamma_hat * np.power(nobs, pwr))])
    return autolags

def main():
    """
    Toy program to test the KPSS autolag method of Hobijn et al (1998).
    Unit tests using statsmodels data sets verified against SAS 9.3. To
    use, modify the following lines in main KPSS method:

      old:
        if lags is None:
            # from Kwiatkowski et al. referencing Schwert (1989)
            lags = int(np.ceil(12. * np.power(nobs / 100., 1 / 4.)))

      new:
        if lags is None:
            # autolag method of Hobijn et al. (1998)
            lags = _kpss_autolag(resids, nobs)
    """
    print("KPSS autolag method of Hobijn et al. (1998)")
    # real GDP from macrodata data set
    with warnings.catch_warnings(record=True) as w:
        res = kpss(macrodata.load().data['realgdp'], 'c')
    print("  realgdp('c'): stat =", "{0:0.5f}".format(res[0]), " pval =",
          "{0:0.5f}".format(res[1]), " lags =", format(res[2]))
    assert_almost_equal(res[0], 2.06851, decimal=3)
    assert_equal(res[2], 9)
    # sunspot activity from sunspots data set
    with warnings.catch_warnings(record=True) as w:
        res = kpss(sunspots.load().data['SUNACTIVITY'], 'c')
    print("  sunactivity('c'): stat =", "{0:0.5f}".format(res[0]), " pval =",
          "{0:0.5f}".format(res[1]), " lags =", format(res[2]))
    assert_almost_equal(res[0], 0.66987, decimal=3)
    assert_equal(res[2], 7)
    # volumes from nile data set
    with warnings.catch_warnings(record=True) as w:
        res = kpss(nile.load().data['volume'], 'c')
    print("  volume('c'): stat =", "{0:0.5f}".format(res[0]), " pval =",
          "{0:0.5f}".format(res[1]), " lags =", format(res[2]))
    assert_almost_equal(res[0], 0.86912, decimal=3)
    assert_equal(res[2], 5)
    # log-coinsurance from randhie data set
    with warnings.catch_warnings(record=True) as w:
        res = kpss(randhie.load().data['lncoins'], 'ct')
    print("  lncoins('ct'): stat =", "{0:0.5f}".format(res[0]), " pval =",
          "{0:0.5f}".format(res[1]), " lags =", format(res[2]))
    assert_almost_equal(res[0], 0.36762, decimal=3)
    assert_equal(res[2], 75)
    # in-vehicle time from modechoice data set
    with warnings.catch_warnings(record=True) as w:
        res = kpss(modechoice.load().data['invt'], 'ct')
    print("  invt('ct'): stat =", "{0:0.5f}".format(res[0]), " pval =",
          "{0:0.5f}".format(res[1]), " lags =", format(res[2]))
    assert_almost_equal(res[0], 0.40258, decimal=3)
    assert_equal(res[2], 18)

if __name__ == "__main__":
    sys.exit(int(main() or 0))
