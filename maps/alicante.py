from mapping import *
import cProfile
import pstats

def main():
        #ALICANTE
    bbox = [38.308227, -0.555883, 38.395898, -0.389250]
    zoom = 12
    SIZE = 1000
    title = "alicante"

    colour_set = [
        ("1",Color("#002a3788"), Color("#9370db88"), Color("#fffafa88")),
        ("2",Color("#49428bd9"), Color("#ff69b4ca"), Color("#f5deb3ff")),
        ("3",Color("#d7515f98"), Color("#bdb76bca"), Color("#191970ff")),
        ("4",Color("#e700089b"), Color("#00224de2"), Color("#002a37ff")),
        ("5",Color("#60a4202e"), Color("#00224de2"), Color("#d3a318ff")),
        ("6",Color("#da1e95ef"), Color("#e4cd00c9"), Color("#ffffffff")),
        ("7",Color("#949494ff"), Color("#002232ff"), Color("#ffffffff")),
        ("8",Color("#12392aff"), Color("#8098afff"), Color("#c84b9dff")),
    ]
    for name, city_col, water_col, roads_col in colour_set:
        print(f"Doing poster: {name}")

        d = create_drawing(SIZE, SIZE, bg_col=water_col)

        #CITY BOUNDARY
        d = add_areas(bbox, zoom, d, "'admin_level'='6'", color=city_col, name="city")

        d = add_areas(bbox, zoom, d, "'natural'='water'", color=water_col, name="city_water")

        #ROADS
        s = '"highway"~"^(((motorway|trunk|primary|secondary|tertiary)(_link)?)|unclassified|residential|living_street|pedestrian|service|track)$"'
        d = add_ways(bbox, zoom, d, s, color=roads_col, width = 0.2, name="roads")

        # #BEACHES
        # d = add_areas(bbox, zoom, d, "'natural'='beach'", color=yellow, name="beaches")

        # #FOREST
        # d = add_areas(bbox, zoom, d, "'landuse'='forest'", color=green, name="forest")

        #CASTLE
        # d = add_areas(bbox, zoom, d, "'historic'='castle'", color="black", name="castle")

        d.save_svg(f"graphics/{title}-{name}.svg")


if __name__ == "__main__":

    with cProfile.Profile() as pr:
        main()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats("alicante.prof")