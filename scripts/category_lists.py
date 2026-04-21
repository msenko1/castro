categories = {
    "gay": ["gay", "queer", "fabulous", "pride", "rainbow", "flamboyant", "love", "gayborhood", "fruity", "homosexuales", "zesty", "faggy", "camp", "lgbtqixyz", "faggots"],
    "sexual": ["slut", "frisky", "fucking", "sexual", "slutty", "naked", "bountiful"],
    "fun": ["fun", "vibrant", "lively", "wonderful", "amazing", "active", "festive", "great", "fantastic", "excelente", "exciting", "awesome", "energetic", "party", "dance", "buzzy", "spanky", "poppin", "exuberant", "funner", "lit", "espectaculo", "joy", "cunt", "effervescent", "entertaining", "envigorating", "delightful", "joyous", "electric", "fun-loving", "dynamic", "expressive", "stunning", "best"],
    "nice": ["beautiful", "nice", "alive", "warm", "pleasant", "bonito", "cool", "cozy", "safe", "quaint", "approachable", "gorgeous", "clean", "happy", "good", "pretty", "cute", "cosy", "positive", "coziness", "lovely", "attractive", "enjoyable", "robust", "quiet", "peace", "comfortable", "bubbly", "peaceful", "perfect", "sleepy", "bien", "wondrous", "bright", "idyllic", "chill", "vibey", "tranquilo", "mellow"],
    "boring": ["boring", "cold", "dead", "stale", "lacking", "dull", "ehhh", "sad", "not_exciting", "dying", "meh", "less_fun", "declining", "unfun", "underwhelming", "sterile", "lame", "lazy"],
    "chaotic": ["crowded", "chaotic", "wild", "crazy", "busy", "bustling", "messy", "teaming", "unhinged", "hectic", "drunk", "whacky", "crowds", "alot", "mess"],
    "bad": ["bad", "fake", "gross", "tragic", "toxic", "buttheads", "terrifying", "less_tolerant", "horrible", "boo", "stupid", "snarky"],
    "special": ["eclectic", "interesting", "fascinating", "creative", "artsy", "artistic", "undefined", "surprising", "intriguing", "particular", "authentic", "real", "historic", "iconic", "original", "character", "heritage", "legacy", "personality", "famoso", "classic", "soulful", "bizarre"],
    "normative": ["conformist", "plain", "basic", "predictable", "monolothic", "normal", "fishy", "conformist", "white", "stereotypical", "simple", "bubble", "la", "unseasoned", "tambien", "washed", "straight", "bro", "fratty", "bro-y", "hot_girls", "douchey", "sorority", "fratboys", "barbie", "blonde", "homogenous"],
    "gentrified": ["gentrified", "bougie", "posh", "preppy", "expensive", "rich", "upscale", "yuppies", "extravagant", "affluent", "snotty", "privileged", "tech", "sophisticated", "money", "preppies", "finance", "fancy", "pretentious", "upper_middle_class", "transplant", "nannies", "cosmopolitan", "transplants", "dinero", "boujee", "wealthy", "snooty", "ivy", "snobby", "commercial", "shopping", "trendier", "trendy", "hipster", "hip"],
    "gritty": ["gritty", "grungy", "edgy", "peligroso", "raw", "edge", "sucio", "ghetto", "hood", "dirty", "poop", "dangerous", "grimy"],
    "diverse": ["diverse", "cultural", "culture", "different", "spicy", "flavorful", "multicultural", "variety", "varied", "dichotomy", "multitude", "blended", "colors", "colorful"],
    "latino": ["latino", "hispanic", "mexican", "españa", "español", "hola"],
    "community": ["community", "home", "familiar", "neighborly", "comunidad", "welcoming", "family", "neighborhood", "families", "residential", "helpful", "unity", "social"],
    "institutions": ["buildings", "architecture", "theater", "education", "dog", "marina_meats", "soulcycle", "bars"],
    "food": ["food", "restaurant", "burrito", "delicious", "foodie"],
    "actions": ["live", "visited", "walkable", "walking", "work"],
    "antitask": ["antitask", "na", "no!", "nada", "unknown", "unbeknownst", "no", "nothing"],
    "young": ["college", "young", "youthful"],
    "geography": ["water", "hilly", "sf", "castro", "flat", "far", "sinking", "marina", "sea", "valley", "harbor", "central", "farther", "close", "expansive", "mission", "chestnut", "ocean", "big", "waterside", "view", "spread", "large", "street", "hefty", "the_mission"],
    "weather": ["chilly", "sunny", "wet", "hot", "sunnier"],
    "open": ["open", "progressive", "political", "liberating", "freedom", "tolerant"],
    "change": ["changed", "changing", "change", "palimpsest", "new"],
    "other": ["tight", "okay", "euphemism", "better", "not_community", "silly", "flags", "shiny", "drugs", "gender", "complicated", "hippies", "racist", "grovel", "rasa", "working_class", "pig", "everything", "elaborate", "old", "antediluvian", "brother"]
}

lookup_dict = word_to_category = {
    word: category
    for category, words in categories.items()
    for word in words
}