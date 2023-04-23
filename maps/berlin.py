from map import Color, Map


if __name__ == "__main__":
    bbox = [52.483634, 13.359147, 52.549596, 13.448748]
    zoom = 12
    SIZE = 1000

    title = "berlin"

    colour_set = [
        ("1", Color("#355b67"), Color("#a689e1"), Color("#2e4f59"), Color("#dfdfdf")),
        ("2", Color("#5b539d"), Color("#e788b7"), Color("#4d4587"), Color("#e5e5e5")),
        ("3", Color("#cb737c"), Color("#bdb76b"), Color("#c45a65"), Color("#e5e5e5")),
        ("4", Color("#da585b"), Color("#062855"), Color("#c32b2f"), Color("#002a37")),
        ("5", Color("#aabf95"), Color("#092c59"), Color("#9db686"), Color("#292929")),
        ("6", Color("#b9167d"), Color("#ff9515"), Color("#c91888"), Color("#ffffff")),
        ("7", Color("#949494"), Color("#002232"), Color("#8a8a8a"), Color("#eeeeee")),
        ("8", Color("#12392a"), Color("#8098af"), Color("#154234"), Color("#dddddd")),
        ("9", Color("#a36d6d"), Color("#5a0000"), Color("#996161"), Color("#280000")),
        ("10", Color("#00185b"), Color("#ffc51a"), Color("#001d70"), Color("#f0f0f0")),
    ]

    for name, city_col, water_col, greenery_col, roads_col in colour_set:

        map = Map(
            title=f"berlin-{name}",
            bbox=[52.483634, 13.359147, 52.549596, 13.448748],
            zoom=12,
            width=1000,
            height=1000,
            bg_col=water_col)


        #CITY BOUNDARY
        map.add_areas("'admin_level'='4'", color=city_col, name="city")

        #CITY WATER
        map.add_areas("'natural'='water'", color=water_col, name="city_water")

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

        #ROADS
        s = '"highway"~"^(((motorway|trunk|primary|secondary|tertiary)(_link)?)|unclassified|residential|living_street|pedestrian|service|track)$"'
        map.add_ways(selector=s, color=roads_col, width = 0.2, name="roads")

        #SAVE
        map.save("graphics/")