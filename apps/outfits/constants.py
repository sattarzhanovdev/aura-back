# Thresholds (°C) for bucketing weather into a target warmth level.
# Tunable without touching the suggestion logic itself.
WARMTH_TEMP_THRESHOLDS = [
    (5, 4),   # < 5°C -> very warm
    (15, 3),  # < 15°C -> warm
    (22, 2),  # < 22°C -> medium
]
DEFAULT_WARMTH_LEVEL = 1  # >= 22°C -> light

OUTERWEAR_MIN_WARMTH = 3  # only suggest outerwear when target warmth >= this

REQUIRED_CATEGORY_SLUGS = ["tops", "bottoms", "shoes"]
OPTIONAL_CATEGORY_SLUGS = ["outerwear"]
