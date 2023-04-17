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

class Map:
    def __init__(self, bbox: list[float], zoom: float, width: int, height: int, bg_col: Color, title: str) -> None:
        self.bbox = bbox
        self.zoom = zoom
        self.width = width
        self.height = height
        self.bg_col = bg_col
        self.primary_col = None
        self.title = title
        self.center_projection = self._get_center_projection()

        self.main_group = self._create_main_group()

        self._set_background()

    def _swap_cols(self, new_colour: Color):
        if self.primary_col:
            self.bg_col = self.primary_col
        self.primary_col = new_colour

    def _create_main_group(self) -> dw.Group:

        clip = dw.ClipPath()
        clip.append(dw.Rectangle(-self.width/2,-self.height/2, self.width, self.height))

        return dw.Group(id="map-layer", clip_path=clip)

    def _set_background(self):
        
        #add a background
        r = dw.Rectangle(-self.width/2,-self.height/2, self.width, self.height, id="background",
            fill=self.bg_col.rgb, fill_opacity=self.bg_col.opacity)

        self.main_group.append(r)


    def _project_web_mercator(self, points): #numpy array of point degrees
        points = np.deg2rad(points)

        lats = points[:, 1]
        lons = points[:, 0]

        projection_constant = np.divide(256, 2*np.pi) * np.exp2(self.zoom)
    
        xs = projection_constant * (lons + np.pi)
        ys = projection_constant * (np.pi - np.log(np.tan((np.pi/4) +  (lats/2))))

        return np.column_stack((xs, ys))

    def _get_center_projection(self):
        left, bottom, right, top = self.bbox
        center = (bottom+top)/2, (left+right)/2
        center_point = np.array(center).reshape(1, 2)
        return self._project_web_mercator(center_point)

    def _create_path(self, points, **options) -> dw.Lines:
        points = points.flatten().tolist() #flatten to list of numbers [x1, y1, x2, y2...]
        l = dw.Lines(*points, #unpack list to separate arguments
                    **options)
        return l

    def _query(self, selector, el_type):
        query = overpassQueryBuilder(bbox=self.bbox,  selector=selector, elementType=el_type, includeGeometry=True)
        result = Overpass().query(query).toJSON()
        return result

    def _parse_geometry(self, geometry):
        points = [(point['lon'], point['lat']) for point in geometry]
        points = np.array(points)
        points = self._project_web_mercator(points)
        points -= self.center_projection #recenter points
        return points

    def _plot_ways(self, ways, group):
        for way in ways:
            points = self._parse_geometry(way['geometry'])
            group.append(self._create_path(points))
        return group

    # ADD WAYS
    def add_ways(self, selector, color: Color, name, width = 0.5):
        self._swap_cols(color)
        result = self._query(selector, ['way'])
        els = result['elements']
        ways = [el for el in els if el['type'] == 'way']

        print(f"For {selector} got {len(els)} ways.")

        g = dw.Group(stroke=self.primary_col.rgb, stroke_opacity=self.primary_col.opacity,
            stroke_width=width, fill="none", close=False, 
            stroke_linecap='round', stroke_linejoin='round', id=name)

        g = self._plot_ways(ways, g)
        self.main_group.append(g)

    def _plot_line_string(self, ls, group, is_outer: bool):
        points = np.array(ls.coords)

        if is_outer:
            p = self._create_path(points, close=True)
        else:
            p = self._create_path(points, close=True, fill=self.bg_col.rgb, fill_opacity=self.bg_col.opacity)
        group.append(p)


    def _plot_relation_members(self, ways, group, is_outer: bool):
        lines = []
        for way in ways:
            if way['type'] == 'way':                
                points = self._parse_geometry(way['geometry'])
                lines.append(points)

        #merge lines into rings
        mls = MultiLineString(lines)
        mls = line_merge(mls)

        if mls.is_empty:
            return

        if isinstance(mls, LineString):
            self._plot_line_string(mls, group, is_outer)

        if isinstance(mls, MultiLineString):
            for ls in mls.geoms:
                self._plot_line_string(ls, group, is_outer)
            


    def _plot_relations(self, relations, group):
        for r in relations:
            members = r['members']

            #filter outer members
            outers = [m for m in members if m['role']=='outer']
            self._plot_relation_members(outers, group, is_outer=True)

            #filter
            inners = [m for m in members if m['role']=='inner']
            self._plot_relation_members(inners, group, is_outer=False)

        return group


    def add_areas(self, selector, color: Color, name):
        self._swap_cols(color)
        result = self._query(selector, ['relation', 'way'])
        els = result['elements']
        ways = [el for el in els if el['type'] == 'way']
        relations = [el for el in els if el['type'] == 'relation' ]

        print(f"""For {selector} got {len(els)} elements. 
            -{len(ways)} ways
            -{len(relations)} relations""")

        #plot closed ways
        g = dw.Group(fill=self.primary_col.rgb, fill_opacity=self.primary_col.opacity, id=name)
        g = self._plot_ways(ways, g)
        g = self._plot_relations(relations, g)
        self.main_group.append(g)

    # SAVE TO FILE
    def save(self, dir):
        d = dw.Drawing(self.width, self.height, id_prefix='map', origin='center')
        d.append(self.main_group)
        target = f"{dir}/{self.title}.svg"
        print(f"Saving to {target}")
        d.save_svg(target)

if __name__ == "__main__":
    print("This file should not be run as main.")