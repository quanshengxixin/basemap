"""
These are diagnostic and debugging functions for basemap.
"""

def proj4_version():
    """
    Gives the proj.4 library's version number. (requires pyproj to be installed)

    returns string, so proj.4 version 4.9.3 will return "4.9.3"
    """
    import pyproj
    
    # Get PROJ4 version in a floating point number
    proj4_ver_num = pyproj.Proj(proj='latlong').proj_version
    
    # reformats floating point number into string (4.90 becomes '4.9.0')
    # Exploits single number version numbers for proj4,
    # This will need likely need to be change at some point as proj.4 version 4.10.0???
    return '.'.join( str(int(proj4_ver_num*100)) )
    
    
def package_versions():
    """
    Gives version information for dependent packages.

    returns namedtuple BasemapPackageVersions
    """
    from collections import namedtuple
    from sys import version as sys_version

    from matplotlib import __version__ as matplotlib_version
    from numpy import __version__ as numpy_version
    from pyproj import __version__ as pyproj_version
    from shapefile import __version__ as pyshp_version

    import _geoslib
    from mpl_toolkits.basemap import __version__ as basemap_version
    
    # import optional dependencies
    try:
        from OWSLib import __version__ as OWSLib_version
    except ImportError:
        OWSLib_version = 'not installed'

    try:
        from PIL import VERSION as pil_version
        try:
            from PIL import PILLOW_VERSION as pillow_version
        except ImportError:
            pillow_version = 'not installed'
    except ImportError:
        pil_version = 'not installed'
        pillow_version = 'not installed'
    
    
    BasemapPackageVersions = namedtuple(
                               'BasemapPackageVersions',
                               """Python, basemap, matplotlib,
                                  numpy, pyproj, pyshp, PROJ4, GEOS,
                                  OWSLib, PIL, Pillow""")

    return BasemapPackageVersions(
                   Python = sys_version,
                   basemap = basemap_version,
                   matplotlib = matplotlib_version,
                   numpy = numpy_version,
                   pyproj = pyproj_version,
                   pyshp = pyshp_version,
                   PROJ4 = proj4_version(),
                   GEOS = _geoslib.__geos_version__,
                   # optional dependencies below
                   OWSLib = OWSLib_version,
                   PIL = pil_version,
                   Pillow = pillow_version)

def check_proj_inv_hammer(segfault_protection_off=False):
    """
    Check if the inverse of the hammer projection is supported by installed
    version of PROJ4.
    
    segfault_protection_off=True  - Turns off the protection from a segfault.
                                     BE CAREFUL setting this to True.

    returns True      - inverse hammer is supported
            False     - inverse hammer is not supported
            "Unknown" - support is Unknown
    """
    from distutils.version import LooseVersion
    from pyproj import __version__ as pyproj_version
    
    if LooseVersion(proj4_version()) > LooseVersion('4.9.2'):
        return True
    
    # pyproj_version_tup = version_str_to_tuple(pyproj_version)
    if LooseVersion(pyproj_version) > LooseVersion('1.9.5.1') \
            or segfault_protection_off is True:
        from pyproj import Proj
        hammer = Proj(proj='hammer')
        
        x, y = hammer(-30.0, 40.0)
        try:
            lon, lat = hammer(x, y, inverse=True)
            return True
        except RuntimeError:            
            return False
    
    return 'Unknown'
