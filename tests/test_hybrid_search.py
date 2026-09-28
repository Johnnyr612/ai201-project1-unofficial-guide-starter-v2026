import unittest

import store


class HybridSearchTest(unittest.TestCase):
    def test_search_supports_hybrid_retrieval(self):
        results = store.search(
            "hardest meal to find across the region",
            top_k=5,
            corpus="city_guides",
            hybrid=True,
        )

        self.assertGreater(len(results), 0)
        self.assertTrue(
            any("meal" in result.text.lower() for result in results),
            "Hybrid retrieval should surface the exact meal-related document terms.",
        )


if __name__ == "__main__":
    unittest.main()
