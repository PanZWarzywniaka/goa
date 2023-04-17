from map import Map, Color

def main():

    #PARIS
    colour_set = [
        ("1", Color("#355b67ff"), Color("#a689e1ff"), Color("#2e4f59ff"), Color("#dfdfdfff")),
        ("2", Color("#5b539dff"), Color("#e788b7ff"), Color("#4d4587ff"), Color("#e5e5e5ff")),
        ("3", Color("#cb737cff"), Color("#bdb76bff"), Color("#c45a65ff"), Color("#e5e5e5ff")),
        ("4", Color("#da585bff"), Color("#062855ff"), Color("#c32b2fff"), Color("#002a37ff")),
        ("5", Color("#aabf95ff"), Color("#092c59ff"), Color("#9db686ff"), Color("#292929ff")),
        ("6", Color("#b9167dff"), Color("#ff9515ff"), Color("#c91888ff"), Color("#ffffffff")),
        ("7", Color("#949494ff"), Color("#002232ff"), Color("#8a8a8aff"), Color("#eeeeeeff")),
        ("8", Color("#12392aff"), Color("#8098afff"), Color("#154234ff"), Color("#ddddddff")),
        ("9", Color("#a36d6dff"), Color("#5a0000ff"), Color("#996161ff"), Color("#280000ff")),
        ("10", Color("#00185bff"), Color("#ffc51aff"), Color("#001d70ff"), Color("#f0f0f0ff")),
    ]
    for name, city_col, water_col, greenery_col, roads_col in colour_set:

        map = Map(
            title=f"paris-{name}",
            bbox=[48.655304, 2.071203, 49.016367, 2.641330],
            zoom=12,
            width=1000,
            height=1000,
            bg_col=water_col)


        #CITY BOUNDARY
        map.add_areas("'admin_level'='6'", color=city_col, name="city")

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


if __name__ == "__main__":
    main()