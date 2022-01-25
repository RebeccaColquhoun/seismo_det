import numpy as np
from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path
from obspy.clients.fdsn import Client
import obspy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import util
import matplotlib.patches as patches
import pandas as pd


class SelectFromCollection(object):
    """Select indices from a matplotlib collection using `PolygonSelector`.

    Selected indices are saved in the `ind` attribute. This tool fades out the
    points that are not part of the selection (i.e., reduces their alpha
    values). If your collection has alpha < 1, this tool will permanently
    alter the alpha values.

    Note that this tool selects collection objects based on their *origins*
    (i.e., `offsets`).

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to interact with.

    collection : :class:`matplotlib.collections.Collection` subclass
        Collection you want to select from.

    alpha_other : 0 <= float <= 1
        To highlight a selection, this tool sets all selected points to an
        alpha value of 1 and non-selected points to `alpha_other`.
    """

    def __init__(self, ax, collection, alpha_other=0.3):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError("Collection must have a facecolor")
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, (self.Npts, 1))

        self.poly = PolygonSelector(ax, self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero(path.contains_points(self.xys))[0]
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.poly.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()


root = "/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3/"


def eq_with_data():
    cat = obspy.read_events(
        "/home/earthquakes1/homes/Rebecca/phd/data/2019_global_m3_catalog.xml"
    )
    eq_with_data = []
    cat_with_data = cat.copy()
    cat_with_data.clear()
    loc = []
    lats = []
    longs = []
    depths = []
    for event in cat:
        eq_name = util.catEventToFileName(event)
        if (
            os.path.isdir(root + eq_name)
            and os.path.isdir(root + eq_name + "/station_xml_files")
            and os.path.exists(root + eq_name + "/picks.pkl")
        ):
            eq_with_data.append(eq_name)
            cat_with_data.extend([event])
            loc.append([event.origins[0].longitude, event.origins[0].latitude])
            lats.append(event.origins[0].latitude)
            longs.append(event.origins[0].longitude)
            depths.append(event.origins[0].depth/1000)
    return eq_with_data, cat_with_data, loc, lats, longs, depths


def polygon_selector(earthquakes=[[], [], []], already_found_polygons=[]):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()

    for p in already_found_polygons:
        path = Path(p)
        patch = patches.PathPatch(path, facecolor='orange', lw=2, alpha=0.2)
        ax.add_patch(patch)

    pts = ax.scatter(earthquakes[0], earthquakes[1], c=earthquakes[2], cmap='plasma')
    im_ratio = ax.bbox.width/ax.bbox.height
    plt.colorbar(pts, fraction=0.01*im_ratio, pad=0.04, label='depth (km)')
    selector = SelectFromCollection(ax, pts)

    print("Select points in the figure by enclosing them within a polygon.")
    print("Press the 'esc' key to start a new polygon. 'esc' and then close window to use that polygon")
    print("Try holding the 'shift' key to move all of the vertices.")
    print("Try holding the 'ctrl' key to move a single vertex.")

    plt.show()

    selector.disconnect()

    polygon_x_coords = selector.poly._xs_at_press
    polygon_y_coords = selector.poly._ys_at_press
    return polygon_x_coords, polygon_y_coords


def make_polygon(polygon_x_coords, polygon_y_coords):
    polygon = []
    codes = []
    for i in range(len(polygon_x_coords)):
        polygon.append([polygon_x_coords[i], polygon_y_coords[i]])
        codes.append(Path.LINETO)

    codes[0] = (Path.MOVETO,)
    codes.append(
        Path.CLOSEPOLY,
    )
    polygon.append([polygon_x_coords[0], polygon_y_coords[0]])
    return polygon


def load_dataframe():
    df = 'a'
    if (os.path.exists(root + "polygons_dataframe.pkl")):
        df = pd.read_pickle(root + "polygons_dataframe.pkl")
    else:
        df = pd.DataFrame({"type": [], "polygons": [], "eq_lists": [], "catalogs": []})
    return df


def save_dataframe(df):
    df.to_pickle(root + "polygons_dataframe.pkl")


def sort_cat(polygon, locations, eq_use, cat_use):
    path = Path(polygon)
    inside_region_bool = path.contains_points(locations)
    inside_indices = np.where(inside_region_bool)
    eq_region = []
    cat_region = cat_use.copy()
    cat_region.clear()
    for index in inside_indices[0]:
        eq_region.append(eq_use[0])
        cat_region.extend([cat_use[0]])
    return cat_region, eq_region


def plot_region():
    path = Path(polygon)
    fig, ax = plt.subplots()
    patch = patches.PathPatch(path, facecolor="orange", lw=2)
    ax.add_patch(patch)
    ax.scatter(longs, lats)
    plt.show()

    sort_cat()


def add_to_dataframe(polygon, cat_region, eq_region):
    print("name of region?")
    name_input = input()
    print("type? subduction zone/transform/continental")
    type_input = input()
    polygons_df = load_dataframe()

    new_line = pd.Series(
        {"type": type_input, "polygons": polygon, "eq_lists": eq_region, "catalogs": cat_region},
        name=name_input)
    polygons_df = polygons_df.append(new_line, ignore_index=False)
    print(polygons_df)
    save_dataframe(polygons_df)


def pick_out_region(df, name):
    polygon = df.loc[name].catalogs
    eq_region = df.loc[name].eq_lists
    cat_region = df.loc[name].catalogs
    return polygon, eq_region, cat_region


eq_use, cat_use, locations, lats, longs, depths = eq_with_data()
polygons_df = load_dataframe()
polygon_x_coords, polygon_y_coords = polygon_selector(earthquakes=[longs, lats, depths], already_found_polygons=polygons_df.polygons)
polygon = make_polygon(polygon_x_coords, polygon_y_coords)
cat_region, eq_region = sort_cat(polygon, locations, eq_use, cat_use)
add_to_dataframe(polygon, cat_region, eq_region)
