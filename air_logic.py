# air_logic.py

def classify_pm25(pm25):
    """Return category + short description for PM2.5 value."""
    if pm25 <= 12:
        return "Good", "Air quality is satisfactory. Minimal health risk."
    elif pm25 <= 35.4:
        return "Moderate", "Air is acceptable, but sensitive groups may feel mild effects."
    elif pm25 <= 55.4:
        return "Unhealthy for Sensitive Groups", "People with asthma, children, and elderly should reduce outdoor activity."
    elif pm25 <= 150.4:
        return "Unhealthy", "Everyone may start to feel health effects. Limit outdoor activities."
    elif pm25 <= 250.4:
        return "Very Unhealthy", "Health alert: serious effects for sensitive groups. Stay indoors if possible."
    else:
        return "Hazardous", "Health warning: emergency conditions. Avoid outdoor exposure."


def classify_pm10(pm10):
    """Simple category for PM10 (optional extra pollutant)."""
    if pm10 <= 54:
        return "Good"
    elif pm10 <= 154:
        return "Moderate"
    elif pm10 <= 254:
        return "Unhealthy for Sensitive Groups"
    elif pm10 <= 354:
        return "Unhealthy"
    elif pm10 <= 424:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def overall_health_risk(pm25, pm10=None):
    """Combine PM2.5 + PM10 into a single health risk score."""
    pm25_cat, pm25_desc = classify_pm25(pm25)

    if pm10 is not None:
        pm10_cat = classify_pm10(pm10)
        ranks = {
            "Good": 1,
            "Moderate": 2,
            "Unhealthy for Sensitive Groups": 3,
            "Unhealthy": 4,
            "Very Unhealthy": 5,
            "Hazardous": 6
        }
        worse_cat = pm25_cat if ranks[pm25_cat] >= ranks[pm10_cat] else pm10_cat
    else:
        worse_cat = pm25_cat

    score_map = {
        "Good": 0,
        "Moderate": 1,
        "Unhealthy for Sensitive Groups": 2,
        "Unhealthy": 3,
        "Very Unhealthy": 4,
        "Hazardous": 5
    }
    risk_score = score_map[worse_cat]

    return worse_cat, risk_score, pm25_desc
