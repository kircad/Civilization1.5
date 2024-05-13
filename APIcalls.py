import time

def make_request(context, map, units, cities, turn):
    request = context[0]['content']
    request+=("TURN " + str(turn) + ":\n")
    request+=( # TODO add previous turns as context TODO incorporate knowntiles stuff
    """
        ---- THE GAME MAP WILL BE GIVEN TO YOU BELOW THIS LINE ----

        Each | (CHARACTER) | cell represents a 1x1 tile on the map, with (CHARACTER) corresponding to:
        - 'P' for plains
        - 'M' for mountains
        - 'R' for rivers
        - 'F' for forests
        - '\n' represents a new row
    """
    )
    request += (map.print_map_opponent())
    request += "BELOW ARE YOUR UNITS AND THEIR COORDINATES (0-INDEXED IN FORMAT (X, Y))"
    for unit in units:
        if unit.civ == "opponent":
            request+=("UNIT TYPE: " + unit.name)
            request+=(" UNIT ID: " + str(unit.id))
            request+=(" LOCATION: (" + str(unit.coordinates[0]) + "," + str(unit.coordinates[1]) + ")")
    request += "BELOW ARE YOUR CITIES AND THEIR COORDINATES (0-INDEXED IN FORMAT (X, Y))"
    for city in cities:
        request+=("UNIT: " + city.name)
        request+=(" LOCATION: (" + str(city.coordinates[0]) + "," + str(city.coordinates[1]) + ")")
    return request

def get_response(model, request):
    tries = 0
    while tries<10:
        try:
            out = model.generate_content(request, request_options={"timeout": 600})
            return out.candidates[0].content.parts[0].text
        except Exception as e:
            print("Failed to get response from Gemini")
            time.sleep(5)
            tries+=1
    return None