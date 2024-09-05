import json
import xml.etree.ElementTree as ElementTree
from abc import (
    ABC,
    abstractmethod,
)


class SongSerializerFactory(ABC):
    """Creator"""
    @abstractmethod
    def factory_method(self):
        pass

    def serialize(self, song) -> str:
        product = self.factory_method()
        result = f"{product.serialize(song)}"

        return result


class JSONSongSerializer(SongSerializerFactory):
    """Concrete creators"""
    def factory_method(self):
        return JSONSongData()


class XMLSongSerializer(SongSerializerFactory):
    def factory_method(self):
        return XMLSongData()


class SongSerializer:
    """Abstract product"""
    @abstractmethod
    def serialize(self, song):
        pass


class JSONSongData(SongSerializer):
    """Concrete products"""
    def serialize(self, song):
        return json.dumps({
            'id': song.song_id,
            'title': song.title,
            'artist': song.artist
        })


class XMLSongData(SongSerializer):
    def serialize(self, song):
        song_info = ElementTree.Element('song', attrib={'id': str(song.song_id)})
        title = ElementTree.SubElement(song_info, 'title')
        title.text = song.title
        artist = ElementTree.SubElement(song_info, 'artist')
        artist.text = song.artist
        return ElementTree.tostring(song_info, encoding='unicode')


class Song:
    """Client code"""
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist


def main():
    """Example usage"""
    song = Song(1, "Imagine", "John Lennon")
    print(JSONSongSerializer().serialize(song))
    print(XMLSongSerializer().serialize(song))


if __name__ == "__main__":
    main()
