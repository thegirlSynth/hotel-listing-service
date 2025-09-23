def evaluate_luxury(scores: dict):
    """
    scores: dict = {
    "design": int,
    "service": int,
    "audience": int,
    "reputation": int,
    "amenities": bool,
    "price": bool
    }
    """

    design_ok = scores["design"] >= 4
    service_ok = scores["service"] >= 4
    audience_ok = scores["audience"] >= 4
    reputation_ok = scores["reputation"] >= 4
    amenities_ok = scores["amenities"]
    price_ok = scores["price"]

    is_luxury = all([design_ok, service_ok, audience_ok, reputation_ok, amenities_ok, price_ok])
    return is_luxury


def evaluate_budget(scores: dict):
    """
    scores: dict = {
    "cleanliness": int,
    "service": int,
    "audience": int,
    "visual": int,
    "amenities": bool,
    "price": bool
    }
    """

    cleanliness_ok = scores["cleanliness"] >= 3
    service_ok = scores["service"] >= 3
    audience_ok = scores["audience"] >= 3
    visual_ok = scores["visual"] >= 3
    amenities_ok = scores["amenities"]
    price_ok = scores["price"]

    is_budget = all([price_ok, cleanliness_ok, service_ok, audience_ok, visual_ok, amenities_ok])
    return is_budget


def evaluate_featured(scores: dict):
    """
    scores: dict = {
      "visual": int,
      "cleanliness": int,
      "value": int,
      "reputation": int,
      "booking_ready": bool,
      "amenities": bool
    }
    """
    visual_ok = scores["visual"] >= 4
    cleanliness_ok = scores["cleanliness"] >= 4
    value_ok = scores["value"] >= 4
    reputation_ok = scores["reputation"] >= 4
    amenities_ok = scores["amenities"]
    booking_ok = scores["booking_ready"]

    is_featured = all([visual_ok, cleanliness_ok, value_ok, reputation_ok, amenities_ok, booking_ok])
    return is_featured


def evaluate_editors_pick(scores: dict):
    """
    scores: dict = {
      "visual_quality": int,
      "room_quality": int,
      "location_strength": int,
      "diversity_score": int,
      "owner_trust": int,
      "instagrammability": int,
      "responsiveness": int
    }
    """
    total = sum(scores.values())  # 7 factors, scale 1–5
    return total >= 28, total
