from neo4j import GraphDatabase
from neo4j import Transaction

class ProfileDb(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def wipeDb(self):
        with self._driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def close(self):
        self._driver.close()

    def addUserToDb(self, userName, fullName, password):
        plName = userName + '-favorites'
        with self._driver.session() as session:
            result = session.run(
                "CREATE (nProfile:profile {userName:{userName}, fullName:{fullName}, password:{password}})-[rCreated:created]->(nPlaylist:playlist {plName:{plName}}) RETURN nProfile", userName=userName, fullName=fullName, password=password, plName=plName)

            for record in result:
                profileNode = record["nProfile"]

    def getUserFromDb(self, userName):
        userFound = {}
        with self._driver.session() as session:
            result = session.run(
                "MATCH (nProfile:profile) WHERE nProfile.userName={userName} RETURN nProfile", userName=userName)

            for record in result:
                for node in record:
                    userFound['userName'] = node['userName']
                    userFound['fullName'] = node['fullName']
                    userFound['password'] = node['password']
        return userFound

    def getAllFriends(self, userName):
        allFriends = {}
        with self._driver.session() as session:
            result = session.run(
                "MATCH (nProfile:profile {userName:{userName}})-[:follows]->(nProfileFollowed:profile) RETURN nProfileFollowed", userName=userName)

            for record in result:
                for node in record:
                    friendUserName = node['userName']
                    allFriends[friendUserName] = self.getUserFromDb(friendUserName)
        return allFriends

    def getPlaylistSongs(self, userName):
        allSongs = {}

        plName = userName + "-favorites"
        with self._driver.session() as session:
            result = session.run(
                "MATCH (nProfile:profile {userName:{userName}}), (nPlaylist:playlist {plName:{plName}}), (nSong:song) WHERE (nProfile)-[:created]-(nPlaylist)-[:includes]->(nSong) RETURN nSong", userName=userName, plName=plName)

            for record in result:
                for node in record:
                    allSongs[node['songId']] = node['songId']
        return allSongs

    def likeSong(self, userName, songId):
        plName = userName + '-favorites'
        with self._driver.session() as session:
            result = session.run("MERGE (nSong:song { songId: {songId}}) RETURN nSong", songId=songId)
            
            result = session.run("MATCH (nProfile:profile {userName: {userName}}), (nPlaylist:playlist {plName: {plName}}), (nSong:song {songId: {songId}}) "
								+ "WHERE (nProfile)-[:created]->(nPlaylist) "
								+ "MERGE (nPlaylist)-[:includes]->(nSong) " 
                                + "RETURN nProfile, nSong",
						userName=userName, plName=plName, songId=songId)


    def getLikedSong(self, userName):
        plName = userName + '-favorites'
        songList = []
        with self._driver.session() as session:
            result = session.run("MATCH (nProfile:profile {userName:{userName}}), (nPlaylist:playlist {plName:{plName}}), (nSong:song) WHERE (nProfile)-[:created]->(nPlaylist)-[:includes]->(nSong) RETURN nSong",
						userName=userName, plName=plName)

        for record in result:
            for node in record:
                if not node['songId']:
                    songId = node['id'] # If student used id instead of songId
                else:
                    songId = node['songId']
                songList.append(songId)

        return songList


    def followUser(self, userName, userToFollow):
        with self._driver.session() as session:
            createSongNodeResult = session.run("MATCH (nProfile1:profile {userName:{userName}}), (nProfile2:profile {userName:{userToFollow}}) MERGE (nProfile1)-[:follows]->(nProfile2) RETURN nProfile1, nProfile2", userName=userName, userToFollow=userToFollow)


    def getAllNodes(self):
        with self._driver.session() as session:
            result = session.run("MATCH (n) RETURN n")
            return result

