async def plan_with_rules(weather: dict, news: list) -> dict:
    recs = []

    desc = (weather.get("description") or "").lower()
    temp = weather.get("temp_c")
    wind = weather.get("wind_kph", 0)
    humidity = weather.get("humidity", 0)

    # Temperature-based
    if temp is not None:
        if temp >= 33:
            recs.append("It's very hot today — drink plenty of water and avoid staying outside during noon.")
        elif temp >= 28:
            recs.append("Warm weather today — suitable for outdoor activities, but stay hydrated.")
        elif temp >= 20:
            recs.append("Comfortable temperature — great for walking or light exercise.")
        else:
            recs.append("Cool weather — consider wearing warm clothing when going out.")

    # Weather description
    if "rain" in desc or "shower" in desc or "storm" in desc:
        recs.append("Rain expected — carry an umbrella and consider indoor plans.")
        recs.append("Roads may be slippery, travel carefully.")
    elif "cloud" in desc or "overcast" in desc:
        recs.append("Cloudy skies — good time for indoor tasks or relaxing in a cafe.")
    elif "clear" in desc or "sun" in desc:
        recs.append("Clear weather — great opportunity for outdoor activities.")

    # Wind
    if wind and wind > 25:
        recs.append("Strong winds expected — avoid biking or long rides with children.")
    
    # Humidity
    if humidity and humidity > 80:
        recs.append("High humidity — you may feel uncomfortable outside, carry water.")

    # News-based
    for item in news:
        t = (item.get("title") or "").lower()
        s = (item.get("summary") or "").lower()

        if "traffic" in t or "accident" in s or "road" in s:
            recs.append("Traffic issues reported — leave earlier for appointments.")
            break

        if "strike" in t or "protest" in s:
            recs.append("Local protest/strike reported — plan travel accordingly.")
            break

        if "power" in t or "electricity" in s:
            recs.append("Power issues reported — charge devices before going out.")
            break

    if not recs:
        recs.append("Plan your day based on personal priorities and stay safe.")

    return {"source": "rules", "recommendations": recs[:5]}
