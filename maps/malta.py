from map import Color, Map


if __name__ == "__main__":
    #MALTA
    colour_set = [
        ("1",Color("#194a59ff"), Color("#9370db88"), Color("#1c5363ff"), Color("#fffafa88")),
        ("2",Color("#49428bd9"), Color("#ff69b4ca"), Color("#1c5363ff"), Color("#f5deb3ff")),
        ("3",Color("#d7515f98"), Color("#bdb76bca"), Color("#1c5363ff"), Color("#191970ff")),
        ("4",Color("#e700089b"), Color("#00224de2"), Color("#1c5363ff"), Color("#002a37ff")),
        ("5",Color("#60a4202e"), Color("#00224de2"), Color("#1c5363ff"), Color("#d3a318ff")),
        ("6",Color("#da1e95ef"), Color("#e4cd00c9"), Color("#1c5363ff"), Color("#ffffffff")),
        ("7",Color("#949494ff"), Color("#002232ff"), Color("#1c5363ff"), Color("#ffffffff")),
        ("8",Color("#12392aff"), Color("#8098afff"), Color("#1c5363ff"), Color("#c84b9dff")),
        ("9",Color("#12392aff"), Color("#8098afff"), Color("#1c5363ff"), Color("#c84b9dff")),
    ]
    for name, city_col, water_col, greenery_col, roads_col in colour_set:

        map = Map(
            title=f"malta-{name}",
            bbox=[35.778204, 14.139387, 36.082335, 14.658491],
            zoom=11,
            width=1000,
            height=1000,
            bg_col=water_col)


        #CITY BOUNDARY
        map.add_areas("'place'='archipelago'", color=city_col, name="city")

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