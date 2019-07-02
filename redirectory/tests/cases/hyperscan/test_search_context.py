from redirectory.tests.fixtures import *


class TestHyperscanManager:

    def test_handle_match(self):
        """
        Simple unit tests but part of core feature.
        Starts with a populated hyperscan database with 5 rules.
        Test the handle_match() function.
        Expected behaviour:
            1. Checks if it handles correctly the length of the original with the matched one
               and also doesn't repeat
        """
        # Import needed functions and classes
        from redirectory.libs_int.hyperscan import SearchContext

        # Check
        sc = SearchContext('bam_original')
        sc.handle_match(1, 0, 12)
        assert sc.matched_ids == [1]

        sc = SearchContext('bam')
        sc.handle_match(2, 0, 3)
        assert sc.matched_ids == [2]

        sc = SearchContext('bam_original')
        sc.handle_match(1, 0, 13)
        assert sc.matched_ids == []

        sc = SearchContext('bam_original')
        sc.handle_match(1, 0, 12)
        sc.handle_match(2, 0, 12)
        sc.handle_match(3, 0, 13)
        sc.handle_match(4, 0, 12)
        assert sc.matched_ids == [1, 2, 4]

        sc = SearchContext('bam_original')
        sc.handle_match(1, 0, 12)
        sc.handle_match(1, 0, 12)
        sc.handle_match(3, 0, 13)
        sc.handle_match(4, 0, 12)
        assert sc.matched_ids == [1, 4]
