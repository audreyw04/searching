import unittest
import search

class TestSearch(unittest.TestCase):
    def test_sort_and_search(self):
        Q = [1, 2, 3, 4, 5]
        D = [3, 4, 5, 6, 7]
        found = search.sort_and_search(Q, D)
        self.assertEqual(found, 3)

    def test_merge_search(self):
        Q = [1, 2, 3, 4, 5]
        D = [3, 4, 5, 6, 7]
        found = search.merge_search(Q, D)
        self.assertEqual(found, 3)

    def test_hash_table(self):
        Q = [1, 2, 3, 4, 5]
        D = [3, 4, 5, 6, 7]
        found = search.hash_table(Q, D)
        self.assertEqual(found, 3)

if __name__ == '__main__':
    unittest.main()


