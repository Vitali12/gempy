import numpy as np
from .create_topography import LoadDEMArtificial


class Topography:
    """
    Object to include topography in the model.

    Notes:
        This always assumes that the topography we pass fits perfectly the extent

    """
    def __init__(self, regular_grid=None, extent=None, resolution=None):
        if regular_grid is None and (extent is None or resolution is None):
            raise AttributeError('You need to pass either a regular grid or'
                                 'extent and resolution')

        # Set the extent and resolution of the grid
        self.resolution = regular_grid.resolution[:2] if resolution is None else resolution
        assert all(np.asarray(self.resolution) >= 2), 'The regular grid needs to be at least of size 2 on all ' \
                                                      'directions.'
        self.extent = regular_grid.extent[:] if extent is None else extent

        # Values (n, 3)
        self.values = np.zeros((0, 3))

        # Values (n, n, 3)
        self.values_2d = np.zeros((0, 3))

        # Shape original
        self.raster_shape = tuple()

        # Source for the
        self.source = None

    def set_values(self, values_2d: np.ndarray):
        """General method to set topography

        Args:
            values_2d (numpy.ndarray[float,float, 3]): array with the XYZ values
             in 2D

        Returns:
            :class:`gempy.core.grid_modules.topography.Topography`


        """
        # Original topography data
        self.values_2d = values_2d

        # n,3 array
        self.values = values_2d.reshape(-1, 3)
        return self

    def crop_topography(self, extent):
        """Crop the topography to a given extent.

        This may be useful for example to mask the regular grid.

        Args:
            extent:

        Returns:

        """
        raise NotImplementedError

    def load_random_hills(self, **kwargs):
        dem = LoadDEMArtificial(extent=self.extent,
                                resolution=self.resolution, **kwargs)
        self.set_values(dem.get_values())
        self.source = 'artificial'
