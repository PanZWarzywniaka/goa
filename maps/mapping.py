from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.api import Api
import numpy as np
import drawsvg as dw
import typing
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from shapely import line_merge, polygonize, MultiLineString, LineString, Polygon
import pathlib
from dataclasses import dataclass

@dataclass(frozen=True)
class Color:
    rgba: str = "#ffffffff"

    @property
    def rgb(self) -> str:
        return self.rgba[:-2]
    
    @property
    def opacity(self) -> float:
        opacity_hex = self.rgba[-2:]
        opacity = int(opacity_hex, 16) / 255.0
        return opacity


def create_path(points, **options) -> dw.Lines:
    
    points = points.flatten().tolist() #flatten to list of numbers [x1, y1, x2, y2...]
    l = dw.Lines(*points, #unpack list to separate arguments
                **options)
    return l


def query(selector, el_type, bbox, includeGeometry=True):
    query = overpassQueryBuilder(bbox=bbox,  selector=selector, elementType=el_type, includeGeometry=includeGeometry)
    result = Overpass().query(query).toJSON()
    return result


def project_web_mercator(points, zoom): #numpy array of point degrees
    points = np.deg2rad(points)

    lats = points[:, 1]
    lons = points[:, 0]

    projection_constant = np.divide(256, 2*np.pi) * np.exp2(zoom)
   
    xs = projection_constant * (lons + np.pi)
    ys = projection_constant * (np.pi - np.log(np.tan((np.pi/4) +  (lats/2))))

    return np.column_stack((xs, ys))

def get_center_projection(bbox, zoom):
    left, bottom, right, top = bbox
    center = (bottom+top)/2, (left+right)/2
    center_point = np.array(center).reshape(1, 2)
    return project_web_mercator(center_point, zoom)

def parse_geometry(geometry, zoom, bbox):
    points = [(point['lon'], point['lat']) for point in geometry]
    points = np.array(points)
    points = project_web_mercator(points, zoom)
    points -= get_center_projection(bbox, zoom)
    return points

def linestring_to_path(ls: LineString, fill: str):
    points = np.array(ls.coords)
    path = create_path(points, fill=fill, close=True)
    return path

def ways_to_paths(ways, zoom, bbox, fill="black"):
    lines = []
    for way in ways:
        g = parse_geometry(way['geometry'], zoom, bbox)
        lines.append(g)

    mls = MultiLineString(lines)
    mls = line_merge(mls)

    if mls.is_empty:
        return []

    if isinstance(mls, MultiLineString):
        return [linestring_to_path(ls, fill) for ls in mls.geoms]
        
    if isinstance(mls, LineString):
        return [linestring_to_path(mls, fill)]


def plot_relations(relations, mask, zoom, bbox):
    for r in relations:
        members = r['members']

        #filter outer members
        outers = [m for m in members if m['role']=='outer']
        [mask.append(p) for p in ways_to_paths(outers, zoom, bbox, fill="white")]

        #filter
        inners = [m for m in members if m['role']=='inner']
        [mask.append(p) for p in ways_to_paths(inners, zoom, bbox, fill="black")]


def plot_closed_ways(ways, mask, zoom, bbox):
    _ = [mask.append(p) for p in ways_to_paths(ways, zoom, bbox,fill="white")]

def create_drawing(width, height, bg_col: Color):
    d = dw.Drawing(width, height, id_prefix='map', origin='center')
    r = dw.Rectangle(-width/2,-height/2, width, height, id="background",
         fill=bg_col.rgb, fill_opacity=bg_col.opacity)
    d.append(r)

    return d

def add_areas(bbox, zoom, drawing, selector, color: Color, name):
    result = query(selector, ['relation', 'way'], bbox)
    els = result['elements']
    ways = [el for el in els if el['type'] == 'way']
    relations = [el for el in els if el['type'] == 'relation' ]

    print(f"""For {selector} got {len(els)} elements. 
        -{len(ways)} ways
        -{len(relations)} relations""")

    mask = dw.Mask()
    plot_relations(relations, mask, zoom, bbox)
    plot_closed_ways(ways, mask, zoom, bbox)

    areas = dw.Rectangle(-drawing.width/2,-drawing.height/2, drawing.width, drawing.height,
        fill=color.rgb, fill_opacity=color.opacity, mask=mask, id=name)
    drawing.append(areas)
    return drawing  


def plot_open_ways(ways, group, zoom, bbox):
    for way in ways:
        g = parse_geometry(way['geometry'], zoom, bbox)
        group.append(create_path(g))
    return group
    

def add_ways(bbox, zoom, drawing, selector, color: Color, name, width = 0.5):
    result = query(selector, ['way'], bbox)
    els = result['elements']
    ways = [el for el in els if el['type'] == 'way']

    print(f"For {selector} got {len(els)} ways.")

    g = dw.Group(stroke=color.rgb, stroke_opacity=color.opacity,
        stroke_width=width, fill="none", close=False, stroke_linecap='round',stroke_linejoin='round', id=name)
    g = plot_open_ways(ways, g, zoom, bbox)
    drawing.append(g)
    return drawing



if __name__ == "__main__":
    print("Mapping hello")
