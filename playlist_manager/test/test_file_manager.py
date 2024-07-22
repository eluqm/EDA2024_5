import unittest
from util.file_manager import FileManager
from util.memory_manager import MemoryManager
from model.song import Song
import os

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.memory_manager = MemoryManager(max_cache_size=10)
        self.test_file = "test_songs.csv"
        self.create_test_file()
        self.file_manager = FileManager(self.test_file, self.memory_manager)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def create_test_file(self):
        with open(self.test_file, 'w') as f:
            f.write("song_id,artist_name,track_name,track_id,popularity,year,genre\n")
            f.write("1,Artist1,Test Song 1,T1,80,2020,Pop\n")
            f.write("2,Artist2,Test Song 2,T2,75,2019,Rock\n")
            f.write("3,Artist3,Another Song,T3,90,2021,Hip Hop\n")

    def test_load_songs(self):
        self.file_manager.load_songs()
        self.assertEqual(len(self.file_manager.song_index), 3)
        self.assertIn('1', self.file_manager.song_index)
        self.assertIn('2', self.file_manager.song_index)
        self.assertIn('3', self.file_manager.song_index)

    def test_get_song_by_id(self):
        self.file_manager.load_songs()
        song = self.file_manager.get_song_by_id('1')
        self.assertIsNotNone(song)
        self.assertEqual(song.song_id, '1')
        self.assertEqual(song.track_name, 'Test Song 1')

    def test_search_songs_by_name(self):
        self.file_manager.load_songs()
        songs = self.file_manager.search_songs_by_name("Test Song")
        self.assertEqual(len(songs), 2)
        self.assertEqual(songs[0].track_name, 'Test Song 1')
        self.assertEqual(songs[1].track_name, 'Test Song 2')

    def test_search_nonexistent_song(self):
        self.file_manager.load_songs()
        songs = self.file_manager.search_songs_by_name("Nonexistent Song")
        self.assertEqual(len(songs), 0)

    def test_memory_manager_integration(self):
        self.file_manager.load_songs()
        song1 = self.file_manager.get_song_by_id('1')
        self.assertIsNotNone(self.memory_manager.get_from_cache('1'))
        for i in range(11):
            self.file_manager.get_song_by_id(str(i % 3 + 1))
        self.assertIsNone(self.memory_manager.get_from_cache('1'))

if __name__ == '__main__':
    unittest.main()