class InsufficientWardrobeError(Exception):
    def __init__(self, missing_categories: list[str]):
        self.missing_categories = missing_categories
        super().__init__(
            f"Not enough wardrobe items to build an outfit. Add items to: "
            f"{', '.join(missing_categories)}."
        )
