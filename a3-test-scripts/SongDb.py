from pymongo import MongoClient
from bson.objectid import ObjectId


class SongDb(object):
    def __init__(self, uri):
        self.SONG_DB_NAME = "csc301-test"
        self.SONG_COLLECTION = "songs"
        self.__songDbConn = MongoClient(uri)
        self.__songs = self.__songDbConn[self.SONG_DB_NAME][self.SONG_COLLECTION]
        self.__addMockData()

    def closeDb(self):
        self.__songDbConn[self.SONG_DB_NAME][self.SONG_COLLECTION].drop()
        self.__songDbConn.close()

    def __addMockData(self):
            self.__songs.drop()
            self.__addSongWithIdAndFavouritesCounts("5d61728193528481fe5a3122", "Sliver", "Karina Hyndson", "Konklux", 49)
            self.__addSongWithIdAndFavouritesCounts("5d61728193528481fe5a3123", "Same River Twice, The", "Stefanie Berrigan", "Bamity", 13)
            self.__addSongWithIdAndFavouritesCounts("5d61728193528481fe5a3124", "Land of Milk and Honey (Pays de cocagne)", "Kelley Grix", "Subin", 54)
            self.__addSongWithIdAndFavouritesCounts("5d61728193528481fe5a3125", "Henry IV, Part I (First Part of King Henry the Fourth, with the Life and Death of Henry Surnamed Hotspur, The)", "Kelley Grix", "Zathin", 78)
            self.__addSongWithIdAndFavouritesCounts("5d61728193528481fe5a3126", "The Lego Movie", "Agnes Coot", "Opela", 45)
            self.__addSongWithIdAndFavouritesCounts("5d61728193528481fe5a3127", "Off the Black", "Ado Headrick", "Wrapsafe", 39)
            self.__addSongWithIdAndFavouritesCounts("5d620f54d78b833e34e65b46", "Sky Fighters (Les Chevaliers Du Ciel)", "Joyous Rye", "Stronghold", 44)
            self.__addSongWithIdAndFavouritesCounts( "5d620f54d78b833e34e65b47", "Run for Cover", "Analise O'Gavin", "Tresom", 57)
            self.__addSongWithIdAndFavouritesCounts("5d620f54d78b833e34e65b48", "Zulu", "Kare Borwick", "Veribet", 98)
            self.__addSongWithIdAndFavouritesCounts("5d620f54d78b833e34e65b49", "Judgment in Berlin", "Englebert Ranyell", "Bytecard", 44)


    def getSongById(self, songId):
        try:
            return self.__songs.find_one({"_id": ObjectId(songId)})
        except:
            return None


    def __addSongWithIdAndFavouritesCounts(self, songId, songName, songArtistFullName, songAlbum, songAmountFavourites):
        songToAdd = {"_id": ObjectId(songId), "songName": songName, "songArtistFullName": songArtistFullName,
                     "songAlbum": songAlbum, "songAmountFavourites": songAmountFavourites}
        return self.__songs.insert_one(songToAdd).inserted_id


    def getAllSongs(self):
        allSongs = []
        for document in self.__songs.find():
            allSongs.append(document)
        return allSongs


    def addSong(self, songName, songArtistFullName, songAlbum):
        songToAdd = {"songName": songName, "songArtistFullName": songArtistFullName,
                     "songAlbum": songAlbum, "songAmountFavourites": 0}
        return self.__songs.insert_one(songToAdd).inserted_id
