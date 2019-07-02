class SearchContext(dict):
    original: str = None
    matched_ids: list = None

    def __init__(self, original: str, **kwargs):
        super().__init__(**kwargs)
        self.original = original
        self.matched_ids = []

        # Fore easy serialization to json later on
        self.__setitem__("original", original)
        self.__setitem__("matched_ids", self.matched_ids)

    def __repr__(self):
        return f"org: {self.original} | ids: {self.matched_ids}"

    def handle_match(self, destination_id: int, from_index: int, to_index: int):
        """
        Handles a hyperscan matched passed from the match_event_handler.
        If the length of the match matches the length of the original search query
        it will be added to the matched_ids.

        Args:
            destination_id: the id of the matched expression from Hyperscan
            from_index: from where the match starts
            to_index: until where the match ends
        """
        matched_len = to_index - from_index

        if matched_len == len(self.original):
            if destination_id not in self.matched_ids:
                self.matched_ids.append(destination_id)

    def is_empty(self):
        """
        Checks in any matches have been found associated with this context

        Returns:
            a boolean representing if any matches are found
        """
        return len(self.matched_ids) == 0
