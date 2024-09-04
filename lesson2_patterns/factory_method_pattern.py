import json
import xml.etree.ElementTree as ElementTree
from abc import (
    ABC,
    abstractmethod,
)


# Creator
class SongSerializerFactory(ABC):
    @abstractmethod
    def factory_method(self):
        pass

    def serialize(self, song) -> str:
        product = self.factory_method()
        result = f"{product.serialize(song)}"

        return result


# Concrete creators
class JSONSongSerializer(SongSerializerFactory):
    def factory_method(self):
        return JSONSongData()


class XMLSongSerializer(SongSerializerFactory):
    def factory_method(self):
        return XMLSongData()


# Abstract product
class SongSerializer:
    def serialize(self, song):
        pass


# Concrete products
class JSONSongData(SongSerializer):
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


# Client code
class Song:
    def __init__(self, song_id, title, artist):
        self.song_id = song_id
        self.title = title
        self.artist = artist


# Example usage
def main():
    song = Song(1, "Imagine", "John Lennon")
    print(JSONSongSerializer().serialize(song))
    print(XMLSongSerializer().serialize(song))


if __name__ == "__main__":
    main()
