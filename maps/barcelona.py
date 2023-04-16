from map import Color, Map


if __name__ == "__main__":
    bbox = [41.344379, 2.098893, 41.442312, 2.243356]
    zoom = 12
    SIZE = 1000

    title = "barcelona"

    colour_set = [
        ("1",Color("#355b67ff"), Color("#a689e1ff"), Color("#fffafa88"), Color("d1d1d1ff")),
        ("2",Color("#5b539dff"), Color("#e788b7ff"), Color("#4d4587ff"), Color("e5e5e5ff")),
        ("3",Color("#cb737cff"), Color("#bdb76bff"), Color("#c45a65ff"), Color("e5e5e5ff")),
        ("4",Color("#da585bff"), Color("#062855ff"), Color("#002a37ff"), Color("240808ff")),
        ("5",Color("#aabf95ff"), Color("#092c59ff"), Color("#9db686ff"), Color("292929ff")),
        ("6",Color("#b9167dff"), Color("#ff9515ff"), Color("#c91888ff"), Color("ffffffff")),
        ("7",Color("#949494ff"), Color("#002232ff"), Color("#8a8a8aff"), Color("eeeeeeff")),
        ("8",Color("#12392aff"), Color("#8098afff"), Color("#154234ff"), Color("ddddddff")),
        ("9",Color("#a36d6dff"), Color("#5a0000ff"), Color("#996161ff"), Color("280000ff")),
        ("10",Color("#00185bff"), Color("#ffc51aff"), Color("#001d70ff"), Color("f0f0f0ff")),
    ]

    #for name, city_col, water_col, greenery_col, roads_col in colour_set:
        #print(f"Doing poster: {name}")

        #d = create_drawing(SIZE, SIZE, bg_col=water_col)

        ##CITY BOUNDARY
        #d = add_areas(bbox, zoom, d, "'admin_level'='6'", color=city_col, name="city")

        #d = add_areas(bbox, zoom, d, "'natural'='water'", color=water_col, name="city_water")

        #ROADS
        #s = '"highway"~"^(((motorway|trunk|primary|secondary|tertiary)(_link)?)|unclassified|residential|living_street|pedestrian|service|track)$"'
        #d = add_ways(bbox, zoom, d, s, color=roads_col, width = 0.2, name="roads")

        ##GREEN AREAS

        ##PARKS
        #d = add_areas(bbox, zoom, d, "'leisure'='park'", color=greenery_col, name="park")

        ##FORESTS
        #d = add_areas(bbox, zoom, d, "'landuse'='forest'", color=greenery_col, name="forest")

        ##WOOD
        #d = add_areas(bbox, zoom, d, "'landuse'='forest'", color=greenery_col, name="wood")

        ##CAMP SITE
        #d = add_areas(bbox, zoom, d, "'tourism'='camp_site'", color=greenery_col, name="camp_site")

        ##CEMENTRY
        #d = add_areas(bbox, zoom, d, "'landuse'='cementry'", color=greenery_col, name="cementry")

        ##COMMON
        #d = add_areas(bbox, zoom, d, "'leisure'='common'", color=greenery_col, name="common")

        ##DOG PARK
        #d = add_areas(bbox, zoom, d, "'leisure'='dog_park'", color=greenery_col, name="dog_park")

        ##FELL
        #d = add_areas(bbox, zoom, d, "'natural'='fell'", color=greenery_col, name="fell")

        ##SCRUB
        #d = add_areas(bbox, zoom, d, "'natural'='scrub'", color=greenery_col, name="scrub")

        ##GARDEN
        #d = add_areas(bbox, zoom, d, "'leisure'='garden'", color=greenery_col, name="garden")

        ##GREENFIELD
        #d = add_areas(bbox, zoom, d, "'landuse'='greenfield'", color=greenery_col, name="greenfield")

        ##GOLF COURSE
        #d = add_areas(bbox, zoom, d, "'leisure'='golf_course'", color=greenery_col, name="golf_course")

        ##GRASS
        #d = add_areas(bbox, zoom, d, "'landuse'='grass'", color=greenery_col, name="grass")

        ##PITCH
        #d = add_areas(bbox, zoom, d, "'leisure'='pitch'", color=greenery_col, name="pitch")

        ##NATURE RESERVE
        #d = add_areas(bbox, zoom, d, "'leisure'='nature_reserve'", color=greenery_col, name="nature_reserve")

        ##VILLAGE GREEN
        #d = add_areas(bbox, zoom, d, "'landuse'='village_green'", color=greenery_col, name="village_green")

        ##RECREATION GROUND
        #d = add_areas(bbox, zoom, d, "'landuse'='recreation_ground'", color=greenery_col, name="recreation_ground")

        #d.save_svg(f"graphics/{title}-{name}.svg")

    for name, city_col, water_col, roads_col, greenery_col in colour_set:

        map = Map(
            title=f"barcelona-{name}",
            bbox=[41.344379, 2.098893, 41.442312, 2.243356],
            zoom=12,
            width=1000,
            height=1000,
            bg_col=water_col)


        #CITY BOUNDARY
        map.add_areas("'admin_level'='6'", color=city_col, name="city")

        #CITY WATER
        map.add_areas("'natural'='water'", color=water_col, name="city_water")

        #ROADS
        s = '"highway"~"^(((motorway|trunk|primary|secondary|tertiary)(_link)?)|unclassified|residential|living_street|pedestrian|service|track)$"'
        map.add_ways(selector=s, color=roads_col, width = 0.2, name="roads")

        #AIRPORTS

        #AERODROMES
        map.add_areas("'aeroway'='aerodrome'", color=greenery_col, name="aerodrome")

        #RUNWAYS
        map.add_areas("'aeroway'='runway'", color=roads_col, name="runway")

        #STOPWAY
        map.add_areas("'aeroway'='stopway'", color=roads_col, name="stopway")

        #TAXIWAYS
        map.add_areas("'aeroway'='taxiway'", color=roads_col, name="taxiway")

        #TERMINALS
        map.add_areas("'aeroway'='terminal'", color=roads_col, name="terminal")

        #GREEN AREAS

        #PARKS
        map.add_areas("'leisure'='park'", color=greenery_col, name="park")

        #FORESTS
        map.add_areas("'landuse'='forest'", color=greenery_col, name="forest")

        #WOOD
        map.add_areas("'landuse'='forest'", color=greenery_col, name="wood")

        #CAMP SITE
        map.add_areas("'tourism'='camp_site'", color=greenery_col, name="camp_site")

        #CEMENTRY
        map.add_areas("'landuse'='cementry'", color=greenery_col, name="cementry")

        #COMMON
        map.add_areas("'leisure'='common'", color=greenery_col, name="common")

        #DOG PARK
        map.add_areas("'leisure'='dog_park'", color=greenery_col, name="dog_park")

        #FELL
        map.add_areas("'natural'='fell'", color=greenery_col, name="fell")

        #SCRUB
        map.add_areas("'natural'='scrub'", color=greenery_col, name="scrub")

        #GARDEN
        map.add_areas("'leisure'='garden'", color=greenery_col, name="garden")

        #GREENFIELD
        map.add_areas("'landuse'='greenfield'", color=greenery_col, name="greenfield")

        #GOLF COURSE
        map.add_areas("'leisure'='golf_course'", color=greenery_col, name="golf_course")

        #GRASS
        map.add_areas("'landuse'='grass'", color=greenery_col, name="grass")

        #PITCH
        map.add_areas("'leisure'='pitch'", color=greenery_col, name="pitch")

        #NATURE RESERVE
        map.add_areas("'leisure'='nature_reserve'", color=greenery_col, name="nature_reserve")

        #VILLAGE GREEN
        map.add_areas("'landuse'='village_green'", color=greenery_col, name="village_green")

        #RECREATION GROUND
        map.add_areas("'landuse'='recreation_ground'", color=greenery_col, name="recreation_ground")

        #SAVE
        map.save("graphics/")