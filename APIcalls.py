def make_request(context, map, units, cities):
    request = context[0]['content']
    request += (map.print_map_opponent())
    request += "BELOW ARE YOUR UNITS AND THEIR COORDINATES (0-INDEXED IN FORMAT (ROW, COLUMN))"
    for name, unit in units.items():
        request+=("UNIT: " + unit.name)
        request+=(" LOCATION: (" + str(unit.coordinates[0]) + "," + str(unit.coordinates[1]) + ")")
    for name, city in cities.items():
        request+=("UNIT: " + city.name)
        request+=(" LOCATION: (" + str(city.coordinates[0]) + "," + str(city.coordinates[1]) + ")")
    return request

def get_response(request, model):
    tries = 0
    while tries<5:
        try:
            response = model.generate_content(request, request_options={"timeout": 600})
            return response
        except Exception as e:
            print("Failed to get response from Gemini")
            tries+=1
    return None