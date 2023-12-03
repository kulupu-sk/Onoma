from dataclasses import dataclass

@dataclass
class PersonName:
    """
    Model of a person name as represented on the Onoma database.
    """
    id:             int = 0    # unique Id in the onoma database;
    culture:        str = ""    # ISO code of the culture, an amalgamation of language and region ("EN" or "EN-US")
    gender:         str = ""     # The onomastic gender, wherever it exists (like feminine and masculine given names)
                            # or masculine and feminine forms of Eastern European family names; case-insensitive.
                            # Supported values: 'F': Feminine; 'M': Masculine, 'U': Unisex, or indifferent.
    component:      str = ""     # Whether a given or a family name; case-insensitive. Supported values: 'family', 'given'.
    alphabetic:     str = ""     # The alphabetic representation of the name item, case-sensitive. Example: 'Tarou'.
    ideographic:    str = ""     # The ideographic representation of the name item, case-sensitive. Example: '山田' (jp).
    phonetic:       str = ""     # The phonetic representation of the name item, case-sensitive.
                            # Examples: 'やまだ' (jp); 'Толстой' (ru); 'חיים' (he).

    def __str__(self):
        return f"{self.alphabetic} ({self.component})"
