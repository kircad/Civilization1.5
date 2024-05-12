def make_request(context, map, units, cities):
    request = context[0]['content']
    request += (map.print_map_opponent())
    request += "BELOW ARE YOUR UNITS AND THEIR COORDINATES (0-INDEXED IN FORMAT (ROW, COLUMN))"
    for unit in units:
        if unit.civ == "opponent":
            request+=("UNIT: " + unit.name)
            request+=(" LOCATION: (" + str(unit.coordinates[0]) + "," + str(unit.coordinates[1]) + ")")
    for city in cities:
        request+=("UNIT: " + city.name)
        request+=(" LOCATION: (" + str(city.coordinates[0]) + "," + str(city.coordinates[1]) + ")")
    return request

def get_response(model, request):
    tries = 0
    while tries<5:
        try:
            out = model.generate_content(request, request_options={"timeout": 600})
            return out.candidates[0].content.parts[0].text
        except Exception as e:
            print("Failed to get response from Gemini")
            print(e)
            tries+=1
    return None