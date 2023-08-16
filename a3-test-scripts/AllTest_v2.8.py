'''
Refactored and rewritten by Brian Lin, TA C01 Fall 2020
Based on AllTest.py
briankw.lin@mail.utoronto.ca
linkedin.com/in/briankwlin
'''

import requests
from ProfileDb import ProfileDb
from SongDb import SongDb
import json
import sys
import traceback

SONG_SERVICE_PORT = 3001
SONG_SERVICE_URI = "http://localhost:{0}".format(SONG_SERVICE_PORT)
MONGO_DB_URI = "mongodb://localhost:27017/"
songDb = SongDb(MONGO_DB_URI)

PROFILE_SERVICE_PORT = 3002
PROFILE_SERVICE_URI = "http://localhost:{0}".format(PROFILE_SERVICE_PORT)
NEO4J_DB_URI = "bolt://localhost:7687"
profileDb = ProfileDb(NEO4J_DB_URI, 'neo4j', '1234')

testPassedString = "Test Passed!"
testFailedString = "Test Failed!"

testResults = {}
totalStudentGrade = 0  # student's total grade
totalTestCasePoints = 0     # total number of marks allocated to the automarker
ABSOLUTE_TOTAL_MARKS = 48   # IMPORTANT: edit this if you change the test cases!

OK = "OK"
NOT_FOUND = "NOT_FOUND"
INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

testNumber = 1  # which test we're currently testing

# outputs test result in a prettified format
def outputTestResult(testInfo, result, expected, received, totalTestMarks):
    global testNumber
    global totalStudentGrade
    global totalTestCasePoints
    totalMarks = 0  # student doesn't get any marks at first
    if(result == testPassedString): 
        totalMarks = totalTestMarks     # if test passes, student gets full marks
    print("Test #" + str(testNumber) + " - \"" + testInfo + "\" - " + result + " | " + str(totalMarks) + "/" + str(totalTestMarks))
    print("  Expected: \"" + str(expected) + "\" of type " + str(type(expected).__name__))
    print("  Received: \"" + str(received) + "\" of type " + str(type(received).__name__))
    testNumber += 1
    totalStudentGrade += totalMarks
    totalTestCasePoints += totalTestMarks

# outputs more information regarding a test. function expects to be used after outputTestResult() is called
def outputTestDetails(details):
    print("  More details: " + details)

def testCreateUser():
    ENDPOINT = "/profile"

    # Test 1: add non-existing user
    username, userPass, userFullName = 'user1', 'user1-password', 'user1-fullName'
    try:
        response = requests.post(PROFILE_SERVICE_URI + ENDPOINT, data={
                                'userName': username, 'password': userPass, 'fullName': userFullName}).json()
        if (response["status"] != OK):
            outputTestResult("Add non-existing user - calling route /profile to add user with userName 'user1' and check response status", testFailedString, OK, response["status"], 1)
        else:
            outputTestResult("Add non-existing user - calling route /profile to add user with userName 'user1' and check response status", testPassedString, OK, response["status"], 1)
    except Exception as e:
        print(e)
        outputTestResult("Add non-existing user - calling route /profile to add user with userName 'user1' and check response status", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")
    
    # Test 2: ensure user was added successfully
    try:
        result = profileDb.getUserFromDb(username)
        # if no response was given, give it a default response to fail the test
        if(not('userName' in result) or not('userName' in result) or not('password' in result)):
            result['userName'], result['password'], result['fullName'] = "NONE_PROVIDED_AUTOGRADER", "NONE_PROVIDED_AUTOGRADER", "NONE_PROVIDED_AUTOGRADER"
            outputTestResult("Add non-existing user - ensure user #1 was successfully stored", testFailedString,
                "username: {username}, password: {password}, fullname: {fullname}".format(username=username, password=userPass, fullname=userFullName),
                "username: {username}, password: {password}, fullname: {fullname}".format(username=result['userName'], password=result['password'], fullname=result['fullName']),
                1)
        elif (result['userName'] == username and result['fullName'] == userFullName and result['password'] == userPass):
            outputTestResult("Add non-existing user - ensure user #1 was successfully stored", testPassedString,
                "username: {username}, password: {password}, fullname: {fullname}".format(username=username, password=userPass, fullname=userFullName),
                "username: {username}, password: {password}, fullname: {fullname}".format(username=result['userName'], password=result['password'], fullname=result['fullName']),
                1)
        else:
            outputTestResult("Add non-existing user - ensure user #1 was successfully stored", testFailedString,
                "username: {username}, password: {password}, fullname: {fullname}".format(username=username, password=userPass, fullname=userFullName),
                "username: {username}, password: {password}, fullname: {fullname}".format(username=result['userName'], password=result['password'], fullname=result['fullName']),
                1)
    except Exception as e:
        outputTestResult("Add non-existing user - ensure user #1 was successfully stored", testFailedString,
            "username: {username}, password: {password}, fullname: {fullname}".format(username=username, password=userPass, fullname=userFullName), e, 1)
        outputTestDetails("Exception raised!")

    # Test 3: add non-existing user again for testing
    username, userPass, userFullName = 'ilir', 'ilir-password', 'ilir-fullName'
    try:
        response = requests.post(PROFILE_SERVICE_URI + ENDPOINT, data={
                                'userName': username, 'password': userPass, 'fullName': userFullName}).json()
        if (response["status"] != OK):
            outputTestResult("Add non-existing user #2 - calling route /profile to add user with userName 'user1' and check response status", testFailedString, OK, response["status"], 1)
        else:
            outputTestResult("Add non-existing user #2 - calling route /profile to add user with userName 'user1' and check response status", testPassedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Add non-existing user #2 - calling route /profile to add user with userName 'user1' and check response status", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")

    # Test 4: ensure user #2 was added successfully
    try:
        result = profileDb.getUserFromDb(username)
        # if no response was given, give it a default response to fail the test
        if(not('userName' in result) or not('userName' in result) or not('password' in result)):
            result['userName'], result['password'], result['fullName'] = "NONE_PROVIDED_AUTOGRADER", "NONE_PROVIDED_AUTOGRADER", "NONE_PROVIDED_AUTOGRADER"
            outputTestResult("Add non-existing user - ensure user #2 was successfully stored", testFailedString,
                "username: {username}, password: {password}, fullname: {fullname}".format(username=username, password=userPass, fullname=userFullName),
                "username: {username}, password: {password}, fullname: {fullname}".format(username=result['userName'], password=result['password'], fullname=result['fullName']),
                1)
        elif (result['userName'] == username and result['fullName'] == userFullName and result['password'] == userPass):
            outputTestResult("Add non-existing user - ensure user #2 was successfully stored", testPassedString,
                "username: {username}, password: {password}, fullname: {fullname}".format(username=username, password=userPass, fullname=userFullName),
                "username: {username}, password: {password}, fullname: {fullname}".format(username=result['userName'], password=result['password'], fullname=result['fullName']),
                1)
        else:
            outputTestResult("Add non-existing user - ensure user #2 was successfully stored", testFailedString,
                "username: {username}, password: {password}, fullname: {fullname}".format(username=username, password=userPass, fullname=userFullName),
                "username: {username}, password: {password}, fullname: {fullname}".format(username=result['userName'], password=result['password'], fullname=result['fullName']),
                1)
    except Exception as e:
        outputTestResult("Add non-existing user - ensure user #2 was successfully stored", testFailedString,
            "username: {username}, password: {password}, fullname: {fullname}".format(username=username, password=userPass, fullname=userFullName), e, 1)
        outputTestDetails("Exception raised!")

    # Test 5: add existing user
    try:
        response = requests.post(PROFILE_SERVICE_URI + ENDPOINT, data={
                                'userName': username, 'password': userPass, 'fullName': userFullName}).json()
        if (response["status"] == OK):
            outputTestResult("Add existing user - calling route /profile to add user with userName 'user1'", testFailedString, "Any response except " + OK + " since 'user1' already exists", response["status"], 1)
        else:
            outputTestResult("Add existing user - calling route /profile to add user with userName 'user1'", testPassedString, "Any response except " + OK + " since 'user1' already exists", response["status"], 1)
    except Exception as e:
        outputTestResult("Add existing user - calling route /profile to add user with userName 'user1'", testFailedString, "Any response except " + OK + " since 'user1' already exists", e, 1)
        outputTestDetails("Exception raised!")

    # Test 6: call /profile route with missing params
    try:
        response = requests.post(PROFILE_SERVICE_URI + ENDPOINT,
                                data={'userName': username, 'password': userPass}).json()

        if (response["status"] == OK and (not isinstance(response["status"], int))):
            outputTestResult("Add existing user - calling route /profile with missing params'", testFailedString, "Any response except " + OK + " since params are missing", response["status"], 1)
            outputTestDetails("This test also checks to make sure 'status' isn't an int. Your status property was parsed as a " + str(type(response["status"]).__name__))
        else:
            outputTestResult("Add existing user - calling route /profile with missing params'", testPassedString, "Any response except " + OK + " since params are missing", response["status"], 1)

    except Exception as e:
        outputTestResult("Add existing user - calling route /profile to add user with userName 'user1'", testFailedString, "Any response except " + OK + " since params are missing", e, 1)
        outputTestDetails("Exception raised!")

existingSongId = ""
existingSongName, existingSongArtistFullName, existingSongAlbum, existingSongAmountFavourites = "Hey There Delilah", "Plain White T's", "All That We Needed", 0
def testAddingSongs():
    global existingSongId, existingSongName, existingSongArtistFullName, existingSongAlbum, existingSongAmountFavourites
    ENDPOINT = "/addSong"

    songName, songArtistFullName, songAlbum, songAmountFavourites = "Hey There Delilah", "Plain White T's", "All That We Needed", 0

    response = {}
    # Begin testing adding of songs with valid params
    try:
        response = requests.post(SONG_SERVICE_URI + ENDPOINT, data={
                                "songName": existingSongName, "songArtistFullName": existingSongArtistFullName, "songAlbum": existingSongAlbum}).json()
        if (response["status"] == OK):
            outputTestResult("Add new song with correct parameters - check status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Add new song with correct parameters - check status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Add new song with correct parameters - check status is OK", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")

    # Test
    try:
        # check to ensure response is correct
        if('data' in response and 'id' in response['data']):
            existingSongId = response["data"]["id"]
        if(not('data' in response) or not('songName' in response["data"]) or not('songArtistFullName' in response["data"]) or not('songAlbum' in response["data"]) or not('songAmountFavourites' in response["data"])):
            outputTestResult("Add new song with correct parameters - check if response is as expected", testFailedString, 
            "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=existingSongName, songArtistFullName=existingSongArtistFullName, songAlbum=existingSongAlbum, songAmountFavourites=existingSongAmountFavourites),
                "Your endpoint didn't return the proper response body! Received: " + str(response), 1)
        elif(existingSongName == response["data"]["songName"] and existingSongArtistFullName == response["data"]["songArtistFullName"] and existingSongAlbum == response["data"]["songAlbum"] and str(existingSongAmountFavourites) == response["data"]["songAmountFavourites"]):
            outputTestResult("Add new song with correct parameters - check if response is as expected", testPassedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=existingSongName, songArtistFullName=existingSongArtistFullName, songAlbum=existingSongAlbum, songAmountFavourites=existingSongAmountFavourites),
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=response["data"]["songName"], songArtistFullName=response["data"]["songArtistFullName"], songAlbum=response["data"]["songAlbum"], songAmountFavourites=response["data"]["songAmountFavourites"]),
                1)
        else:
            outputTestResult("Add new song with correct parameters - check if response is as expected", testFailedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=existingSongName, songArtistFullName=existingSongArtistFullName, songAlbum=existingSongAlbum, songAmountFavourites=existingSongAmountFavourites),
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=response["data"]["songName"], songArtistFullName=response["data"]["songArtistFullName"], songAlbum=response["data"]["songAlbum"], songAmountFavourites=response["data"]["songAmountFavourites"]),
                1)
            outputTestDetails("Extra debug help - the type of your songAmountFavourites returned by the response is " + type(response["data"]["songAmountFavourites"]).__name__)
    except Exception as e:
        outputTestResult("Add new song with correct parameters - check if response is as expected", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")
    
    # Test
    # check to ensure db data is stored correctly
    songFromDb = {}
    try:
        # check to ensure response is correct
        songFromDb = songDb.getSongById(existingSongId)
        if(songFromDb == None or not('songName' in songFromDb) or not('songArtistFullName' in songFromDb) or not('songAlbum' in songFromDb) or not('songAmountFavourites' in songFromDb)):
            outputTestResult("Add new song with correct parameters - check song is stored correctly in DB", testFailedString, 
            "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}",
            "Your endpoint didn't return the proper response body! Received: " + str(response), 1)
        elif(songFromDb != None and existingSongName == songFromDb['songName'] and existingSongArtistFullName == songFromDb['songArtistFullName'] and existingSongAlbum == songFromDb['songAlbum'] and existingSongAmountFavourites == songFromDb['songAmountFavourites']):
            outputTestResult("Add new song with correct parameters - check song is stored correctly in DB", testPassedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=songName, songArtistFullName=existingSongArtistFullName, songAlbum=existingSongAlbum, songAmountFavourites=existingSongAmountFavourites),
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=songFromDb['songName'], songArtistFullName=songFromDb['songArtistFullName'], songAlbum=songFromDb['songAlbum'], songAmountFavourites=songFromDb['songAmountFavourites']),
                1)
        else:
            outputTestResult("Add new song with correct parameters - check song is stored correctly in DB", testFailedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=existingSongName, songArtistFullName=existingSongArtistFullName, songAlbum=existingSongAlbum, songAmountFavourites=existingSongAmountFavourites),
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=songFromDb['songName'], songArtistFullName=songFromDb['songArtistFullName'], songAlbum=songFromDb['songAlbum'], songAmountFavourites=songFromDb['songAmountFavourites']),
                1)
    except Exception as e:
        outputTestResult("Add new song with correct parameters - check song is stored correctly in DB", testFailedString, "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites: {songAmountFavourites}".format(
                songName=existingSongName, songArtistFullName=existingSongArtistFullName, songAlbum=existingSongAlbum, songAmountFavourites=existingSongAmountFavourites), e, 1)
        outputTestDetails("Exception raised!")

    # Begin testing adding songs with incorrect params
    secondSongName, secondSongArtistFullName, secondSongAlbum, secondSongAmountFavourites = "Soul Sister", "Train", "Save Me, San Francisco", 0
    ENDPOINT = "/addSong"
    documentCountAfterRequest = 99999
    try:
        documentCountBeforeRequest = len(songDb.getAllSongs())

        response = requests.post(SONG_SERVICE_URI + ENDPOINT,
                                data={"songName": secondSongName, "songAlbum": secondSongAlbum}).json()

        documentCountAfterRequest = len(songDb.getAllSongs())

        if (response["status"] != OK):
            outputTestResult("Add song with missing parameter songArtistFullName - check status non-OK", testPassedString, "Any string that isn't " + OK, response["status"], 1)
        else:
            outputTestResult("Add song with missing parameter songArtistFullName - check status non-OK", testFailedString, "Any string that isn't " + OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Add song with missing parameter songArtistFullName - check status non-OK", testFailedString, "Any string that isn't " + OK, e, 1)
        outputTestDetails("Exception raised!")

    try:
        if (documentCountBeforeRequest == documentCountAfterRequest):
            outputTestResult("Add song with missing parameter songArtistFullName - ensure number of documents hasn't changed", testPassedString, documentCountBeforeRequest, documentCountAfterRequest, 1)
        else:
            outputTestResult("Add song with missing parameter songArtistFullName - ensure number of documents hasn't changed", testFailedString, documentCountBeforeRequest, documentCountAfterRequest, 1)
    except Exception as e: 
        outputTestResult("Add song with missing parameter songArtistFullName - ensure number of documents hasn't changed", testFailedString, documentCountBeforeRequest, e, 1)
        outputTestDetails("Exception raised!")
    
    outputTestDetails("For the above test, if the received result is 99999, the endpoint is coded incorrectly.")

    response = {"INCORRECT_RESPONSE_AUTOGRADER": ""}
    try:
        response = requests.post(SONG_SERVICE_URI + ENDPOINT, data={
                                "songName": secondSongName, "songArtistFullName": secondSongArtistFullName, "songAlbum": secondSongAlbum, "unexpectedParam": 12345}).json()
        if(not('status' in response)):
            outputTestResult("Add song with unexpected parameter 'unexpectedParam' - ensure unexpected parameter is ignored and status is OK", testFailedString, OK, response, 1)
        elif (response["status"] == OK) :
            outputTestResult("Add song with unexpected parameter 'unexpectedParam' - ensure unexpected parameter is ignored and status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Add song with unexpected parameter 'unexpectedParam' - ensure unexpected parameter is ignored and status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Add song with unexpected parameter 'unexpectedParam' - ensure unexpected parameter is ignored and status is OK", testFailedString, e, response if response == None or not("status" in response) else response["status"], 1)
        outputTestDetails("Exception raised!")
    
    try:
        songId = response["data"]["id"]
        if songDb.getSongById(songId) != None:
            outputTestResult("Add song with unexpected parameter 'unexpectedParam' - ensure unexpected parameter is ignored and song was added successfully by checking if ID exists", testPassedString, True, songDb.getSongById(songId) != None, 1)
        else:
            outputTestResult("Add song with unexpected parameter 'unexpectedParam' - ensure unexpected parameter is ignored and song was added successfully by checking if ID exists", testFailedString, True, songDb.getSongById(songId) != None, 1)
    except Exception as e: 
        outputTestResult("Add song with unexpected parameter 'unexpectedParam' - ensure unexpected parameter is ignored and song was added successfully by checking if ID exists", testFailedString, True, e, 1)
        outputTestDetails("Exception raised!")
    
    # Test with all invalid parameters
    try:
        documentCountBeforeRequest = len(songDb.getAllSongs())

        response = requests.post(SONG_SERVICE_URI + ENDPOINT, data={
                                "invalidSongName": songName, "invalidSongArtistFullName": songArtistFullName, "invalidSongAlbum": songAlbum}).json()

        documentCountAfterRequest = len(songDb.getAllSongs())

        if response["status"] != OK:
            outputTestResult("Add song with all invalid parameters - ensure correct status of not-OK", testPassedString, "Any response that isn't " + OK, response["status"], 1)
        else:
            outputTestResult("Add song with all invalid parameters - ensure correct status of not-OK", testFailedString, "Any response that isn't " + OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Add song with all invalid parameters - ensure correct status of not-OK", testFailedString, "Any response that isn't " + OK, e, 1)
    
    try:
        if documentCountAfterRequest == documentCountBeforeRequest:
            outputTestResult("Add song with all invalid parameters - ensure no documents were added", testPassedString, documentCountBeforeRequest, documentCountAfterRequest, 1)
        else:
            outputTestResult("Add song with all invalid parameters - ensure no documents were added", testFailedString, documentCountBeforeRequest, documentCountAfterRequest, 1)
    except Exception as e:
        outputTestResult("Add song with all invalid parameters - ensure no documents were added", testFailedString, documentCountBeforeRequest, e, 1)

def testGettingSongs():
    global existingSongId, existingSongName

    manuallyAddedSong1SongName, manuallyAddedSong1SongArtistFullName, manuallyAddedSong1SongAlbum, manuallyAddedSong1SongAmountFavourites = "Moon River", "Frank Ocean", "Moon River (Album)", 0
    songId = songDb.addSong(manuallyAddedSong1SongName, manuallyAddedSong1SongArtistFullName, manuallyAddedSong1SongAlbum)

    '''try:
        ENDPOINT = "/getSongById/" + str(songId)
        response = requests.get(SONG_SERVICE_URI + ENDPOINT).json()
        songFromDb = songDb.getSongById(response["data"]["id"])

        if response["status"] == OK:
            outputTestResult("Get song by ID which exists - check status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Get song by ID which exists - check status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Get song by ID which exists - check status is OK", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")
    
    try:
        if manuallyAddedSong1SongName == response["data"]["songName"] and manuallyAddedSong1SongArtistFullName == response["data"]["songArtistFullName"] and manuallyAddedSong1SongAlbum == response["data"]["songAlbum"] and str(manuallyAddedSong1SongAmountFavourites) == str(response["data"]["songAmountFavourites"]):
            outputTestResult("Get song by ID which exists - check that response data matches what was sent", 
                testPassedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites (not sent): {songAmountFavourites}".format(songName=manuallyAddedSong1SongName, songArtistFullName=manuallyAddedSong1SongArtistFullName, songAlbum=manuallyAddedSong1SongAlbum, songAmountFavourites=manuallyAddedSong1SongAmountFavourites),
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites (not sent): {songAmountFavourites}".format(songName=response["data"]["songName"], songArtistFullName=response["data"]["songArtistFullName"], songAlbum=response["data"]["songAlbum"], songAmountFavourites=response["data"]["songAmountFavourites"]),
                1)
        else:
            outputTestResult("Get song by ID which exists - check that response data matches what was sent", 
                testFailedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites (not sent): {songAmountFavourites}".format(songName=manuallyAddedSong1SongName, songArtistFullName=manuallyAddedSong1SongArtistFullName, songAlbum=manuallyAddedSong1SongAlbum, songAmountFavourites=manuallyAddedSong1SongAmountFavourites),
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites (not sent): {songAmountFavourites}".format(songName=response["data"]["songName"], songArtistFullName=response["data"]["songArtistFullName"], songAlbum=response["data"]["songAlbum"], songAmountFavourites=response["data"]["songAmountFavourites"]),
                1)
    except Exception as e:
        outputTestResult("Get song by ID which exists - check that response data matches what was sent", 
                testFailedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songAmountFavourites (not sent): {songAmountFavourites}".format(songName=manuallyAddedSong1SongName, songArtistFullName=manuallyAddedSong1SongArtistFullName, songAlbum=manuallyAddedSong1SongAlbum, songAmountFavourites=manuallyAddedSong1SongAmountFavourites),
                e, 1)
        outputTestDetails("Exception raised!")

    try:
        if songFromDb != None and manuallyAddedSong1SongName == songFromDb["songName"] and manuallyAddedSong1SongArtistFullName == songFromDb["songArtistFullName"] and manuallyAddedSong1SongAlbum == songFromDb["songAlbum"] and str(manuallyAddedSong1SongAmountFavourites) == str(songFromDb["songAmountFavourites"]):
            outputTestResult("Get song by ID which exists - check that database matches what was sent", 
                testPassedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songFavourites (not sent): {songAmountFavourites}".format(songName=manuallyAddedSong1SongName, songArtistFullName=manuallyAddedSong1SongArtistFullName, songAlbum=manuallyAddedSong1SongAlbum, songAmountFavourites=manuallyAddedSong1SongAmountFavourites),
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songFavourites (not sent): {songAmountFavourites}".format(songName=songFromDb["songName"], songArtistFullName=songFromDb["songArtistFullName"], songAlbum=songFromDb["songAlbum"], songAmountFavourites=songFromDb["songAmountFavourites"]),
                1)
        else:
            outputTestResult("Get song by ID which exists - check that database matches what was sent", 
                testFailedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songFavourites (not sent): {songAmountFavourites}".format(songName=manuallyAddedSong1SongName, songArtistFullName=manuallyAddedSong1SongArtistFullName, songAlbum=manuallyAddedSong1SongAlbum, songAmountFavourites=manuallyAddedSong1SongAmountFavourites),
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songFavourites (not sent): {songAmountFavourites}".format(songName=songFromDb["songName"], songArtistFullName=songFromDb["songArtistFullName"], songAlbum=songFromDb["songAlbum"], songAmountFavourites=songFromDb["songAmountFavourites"]),
                1)
    except Exception as e:
        outputTestResult("Get song by ID which exists - check that database matches what was sent", 
                testFailedString,
                "songName: {songName}, songArtistFullName: {songArtistFullName}, songAlbum: {songAlbum}, songFavourites (not sent): {songAmountFavourites}".format(songName=manuallyAddedSong1SongName, songArtistFullName=manuallyAddedSong1SongArtistFullName, songAlbum=manuallyAddedSong1SongAlbum, songAmountFavourites=manuallyAddedSong1SongAmountFavourites),
                e, 1)
        outputTestDetails("Exception raised!")

    # Test: Get song by ID that doesn't exist
    songIdNonExistent = "123456789"
    ENDPOINT = "/getSongById/" + str(songIdNonExistent)
    try:
        response = requests.get(SONG_SERVICE_URI + ENDPOINT).json()

        if (response["status"] != OK):
            outputTestResult("Get song by ID which doesn't exist - check status is non-OK", testPassedString, "Any status that is non-" + OK, response["status"], 1)
        else:
            outputTestResult("Get song by ID which doesn't exist - check status is non-OK", testFailedString, "Any status that is non-" + OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Get song by ID which doesn't exist - check status is non-OK", testFailedString, "Any status that is non-" + OK, e, 1)
        outputTestDetails("Exception raised!")'''
    
    # Test: Getting song title by ID that exists
    ENDPOINT = "/getSongTitleById/" + str(existingSongId)
    try:
        response = requests.get(SONG_SERVICE_URI + ENDPOINT).json()

        if (response["status"] == OK):
            outputTestResult("Get song title by ID which exists - check status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Get song title by ID which exists - check status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Get song title by ID which exists - check status is OK", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")
    
    try:
        if (response["data"] == existingSongName):
            outputTestResult("Get song title by ID which exists - check title matches what was sent", testPassedString, existingSongName, response["data"], 1)
        else:
            outputTestResult("Get song title by ID which exists - check title matches what was sent", testFailingString, existingSongName, response["data"], 1)
    except Exception as e:
        outputTestResult("Get song title by ID which exists - check title matches what was sent", testFailedString, existingSongName, e, 1)
        outputTestDetails("Exception raised!")
    
    # Test: Getting song title by ID that doesn't exist
    ENDPOINT = "/getSongTitleById/" + "123456789"
    try:
        response = requests.get(SONG_SERVICE_URI + ENDPOINT).json()
        if (response["status"] != OK):
            outputTestResult("Get song title by ID which doesn't exist - check status is non-OK", testPassedString, "Any status which is non-" + OK, response["status"], 1)
        else:
            outputTestResult("Get song title by ID which doesn't exist - check status is non-OK", testFailingString, "Any status which is non-" + OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Get song title by ID which doesn't exist - check status is non-OK", testFailedString, "Any status which is non-" + OK, e, 1)
        outputTestDetails("Exception raised!")

def testIncrementingSongFavouritesCount():
    global existingSongId
    songId = existingSongId

    ENDPOINT = "/updateSongFavouritesCount/" + str(songId) + "?shouldDecrement=false"
    songAmountFavouritesBeforeRequest = 99998
    try:
        songAmountFavouritesBeforeRequest = int(songDb.getSongById(songId)["songAmountFavourites"])

        response = requests.put(SONG_SERVICE_URI + ENDPOINT).json()

        if (response["status"] == OK):
            outputTestResult("Increment valid song's favourites count - check if status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Increment valid song's favourites count - check if status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Increment valid song's favourites count - check if status is OK", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")
    
    try:
        songAmountFavouritesAfterRequest = int(songDb.getSongById(songId)["songAmountFavourites"])

        if (int(songAmountFavouritesAfterRequest) == songAmountFavouritesBeforeRequest + 1):
            outputTestResult("Increment valid song's favourites count - check if song amount favourites incremented via DB", testPassedString, songAmountFavouritesBeforeRequest + 1, songAmountFavouritesAfterRequest, 1)
        else:
            outputTestResult("Increment valid song's favourites count - check if song amount favourites incremented via DB", testFailedString, songAmountFavouritesBeforeRequest + 1, songAmountFavouritesAfterRequest, 1)
    except Exception as e:
        outputTestResult("Increment valid song's favourites count - check if song amount favourites incremented via DB", testFailedString, songAmountFavouritesBeforeRequest + 1, e, 1)
        outputTestDetails("Exception raised!")
    
    outputTestDetails("For the above test, we test to see if the number of favourites for this existing song is 1 higher than the number of favourites before incrementing.")
    outputTestDetails("If the expected result is 99999, your endpoint does not work. See the above tests for reasons why.")

    # Test incrementing a song ID that doesn't exist
    ENDPOINT = "/updateSongFavouritesCount/" + "987654321" + "?shouldDecrement=false"
    try:
        response = requests.put(SONG_SERVICE_URI + ENDPOINT).json()

        if (response["status"] != OK):
            outputTestResult("Increment non-existent song's favourites count - check if status is non-OK", testPassedString, "Any status that is non-" + OK, response["status"], 1)
        else:
            outputTestResult("Increment non-existent song's favourites count - check if status is non-OK", testFailedString, "Any status that is non-" + OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Increment non-existent song's favourites count - check if status is non-OK", testFailedString, "Any status that is non-" + OK, e, 1)
        outputTestDetails("Exception raised!")

    try:
        if (songDb.getSongById("987654321") == None):
            outputTestResult("Increment non-existent song's favourites count - ensure no song was created from a non-existent ID", testPassedString, songDb.getSongById("987654321"), None, 1)
        else:
            outputTestResult("Increment non-existent song's favourites count - ensure no song was created from a non-existent ID", testFailedString, songDb.getSongById("987654321"), None, 1)
    except Exception as e:
        outputTestResult("Increment non-existent song's favourites count - ensure no song was created from a non-existent ID", testFailedString, songDb.getSongById("987654321"), e, 1)
        outputTestDetails("Exception raised!")
    
    outputTestDetails("For the above test, we ensure that there isn't an entry in the database corresponding to the non-existing ID as a result of this increment call.")

def testDecrementingSongFavouritesCount():
    global existingSongId
    songId = existingSongId

    # Test: Decrement song favourites count for an existing song ID
    ENDPOINT = "/updateSongFavouritesCount/" + str(songId) + "?shouldDecrement=true"
    songAmountFavouritesBeforeRequest = 100000
    try:
        songAmountFavouritesBeforeRequest = int(songDb.getSongById(songId)["songAmountFavourites"])

        response = requests.put(SONG_SERVICE_URI + ENDPOINT).json()

        if (response["status"] == OK):
            outputTestResult("Decrement valid song's favourites count - check if status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Decrement valid song's favourites count - check if status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Decrement valid song's favourites count - check if status is OK", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")

    try:
        songFromDb = songDb.getSongById(songId)
        if int(songFromDb["songAmountFavourites"]) == songAmountFavouritesBeforeRequest - 1:
            outputTestResult("Decrement valid song's favourites count - check if count is decremented", testPassedString, songAmountFavouritesBeforeRequest - 1, int(songFromDb["songAmountFavourites"]), 1)
        else:
            outputTestResult("Decrement valid song's favourites count - check if count is decremented", testFailedString, songAmountFavouritesBeforeRequest - 1, int(songFromDb["songAmountFavourites"]), 1)
    except Exception as e:
        outputTestResult("Decrement valid song's favourites count - check if count is decremented", testFailedString, songAmountFavouritesBeforeRequest - 1, e, 1)
        outputTestDetails("Exception raised!")
    
    outputTestDetails("For the above test, upon decrementing a song's favourites count, we check if song's favourites count has updated in the database to be one lower than what it was before this call was made.")
    outputTestDetails("If your expected result was 99999, your endpoint doesn't work. See the above tests for reasons why.")

    # Test: Decrement song favourites count doesn't go below 0
    songId = songDb.addSong("Blinding Lights", "The Weeknd", "After Hours")
    ENDPOINT = "/updateSongFavouritesCount/" + str(songId) + "?shouldDecrement=true"
    try:
        response = requests.put(SONG_SERVICE_URI + ENDPOINT).json()

        songFromDb = songDb.getSongById(songId)
        if songFromDb["songAmountFavourites"] == 0:
            outputTestResult("Decrement valid song's favourites count past 0 - ensure count stays at 0", testPassedString, 0, songFromDb["songAmountFavourites"], 1)
        else:
            outputTestResult("Decrement valid song's favourites count past 0 - ensure count stays at 0", testFailedString, 0, songFromDb["songAmountFavourites"], 1)
    except Exception as e: 
        outputTestResult("Decrement valid song's favourites count past 0 - ensure count stays at 0", testFailedString, 0, e, 1)
        outputTestDetails("Exception raised!")

    # Test: Decrement song favourites count for a non-existing song ID
    ENDPOINT = "/updateSongFavouritesCount/" + "123456789" + "?shouldDecrement=true"
    try:
        response = requests.put(SONG_SERVICE_URI + ENDPOINT).json()

        if (response["status"] != OK):
            outputTestResult("Decrement non-existent song's favourites count - check if status is OK", testPassedString, "Any status that is not-" + OK, response["status"], 1)
        else:
            outputTestResult("Decrement non-existent song's favourites count - check if status is OK", testFailedString, "Any status that is not-" + OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Decrement non-existent song's favourites count - check if status is OK", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")

    try:
        songFromDb = songDb.getSongById("123456789")
        if songFromDb == None:
            outputTestResult("Decrement non-existent song's favourites count - check if the non-existent song was created", testPassedString, None, songFromDb, 1)
        else:
            outputTestResult("Decrement non-existent song's favourites count - check if the non-existent song was created", testFailedString, None, songFromDb, 1)
    except Exception as e:
        outputTestResult("Decrement non-existent song's favourites count - check if the non-existent song was created", testFailedString, None, songFromDb, 1)
        outputTestDetails("Exception raised!")
    
    outputTestDetails("For the above test, upon decrementing a non-existent song's favourites count, we ensure that this song wasn't created instead.")

def testFollowFriends():
    ENDPOINT = "/followFriend"

    # Test 7
    userName, friendUserName = "user1", "ilir"
    try:
        response = requests.put(
            PROFILE_SERVICE_URI + ENDPOINT + "/" + userName + "/" + friendUserName).json()

        if (response["status"] != OK):
            outputTestResult("Follow friend with correct body params - calling /followFriend as userName 'user1' to follow friend with userName 'ilir'", testFailedString, OK, response["status"], 1)
        else:
            outputTestResult("Follow friend with correct body params - calling /followFriend as userName 'user1' to follow friend with userName 'ilir'", testPassedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Follow friend with correct body params - calling /followFriend as userName 'user1' to follow friend with userName 'ilir'", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")

    # Test: Ensure relationship is one-directional
    try:
        ilirsFriends = profileDb.getAllFriends('ilir')
        if(userName in ilirsFriends):
            outputTestResult("Follow friend with correct body params - ensure the follower-followee relationship is one-directional", testFailedString, False, userName in ilirsFriends, 1)
            outputTestDetails("'ilir' should not be following 'user1'! The test only called /followFriend for 'user1' to follow 'ilir'!")
        else:
            outputTestResult("Follow friend with correct body params - ensure the follower-followee relationship is one-directional", testPassedString, False, userName in ilirsFriends, 1)
    except Exception as e: 
        outputTestResult("Follow friend with correct body params - ensure the follower-followee relationship is one-directional", testFailedString, False, e, 1)
        outputTestDetails("Exception raised!")
    
    outputTestDetails("For the above test, we test to make sure that 'ilir' is not friends with 'user1' because the relationship is one-directional. 'ilir's friend list is retrieved directly from the database.")
    
    # Test 9
    userName, friendUserName = "ilir", "user1"
    try:
        response = requests.put(
            PROFILE_SERVICE_URI + ENDPOINT + "/" + userName + "/" + friendUserName).json()

        if (response["status"] != OK):
            outputTestResult("Follow friend with correct body params - calling /followFriend as userName 'ilir' to follow friend with userName 'user1'", testFailedString, OK, response["status"], 1)
        else:
            outputTestResult("Follow friend with correct body params - calling /followFriend as userName 'ilir' to follow friend with userName 'user1'", testPassedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Follow friend with correct body params - calling /followFriend as userName 'ilir' to follow friend with userName 'user1'", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")
    
    # Test 10
    try:
        ilirsFriends = profileDb.getAllFriends('ilir')
        if(userName in ilirsFriends):
            outputTestResult("Follow friend with correct body params - ensure the follower-followee relationship is two-directional", testFailedString, False, userName in ilirsFriends, 1)
            outputTestDetails("'ilir' should not be following 'user1'! The test only called /followFriend for 'user1' to follow 'ilir'!")
        else:
            outputTestResult("Follow friend with correct body params - ensure the follower-followee relationship is two-directional", testPassedString, False, userName in ilirsFriends, 1)
    except Exception as e: 
        outputTestResult("Follow friend with correct body params - ensure the follower-followee relationship is two-directional", testFailedString, False, e, 1)
        outputTestDetails("Exception raised!")
    
    outputTestDetails("For the above test, we test to see if the user 'user1' is in 'ilir's friend list. Because the relationship is now two-directional, we expect to see 'user1' in 'ilir's friend list. Results are retrieved directly from the database.")

    # Test 11
    userName, friendUserName = "user1", "non-existing-user"
    try:
        response = requests.put(
            PROFILE_SERVICE_URI + ENDPOINT + "/" + userName + "/" + friendUserName).json()

        if (response["status"] == OK):
            outputTestResult("Follow non-existent friend as existing user - ensure a non-OK response", testFailedString, "Any response except " + OK + " since the follower is non-existent", response['status'], 1)
        else:
            outputTestResult("Follow non-existent friend as existing user - ensure a non-OK response", testPassedString, "Any response except " + OK + " since the follower is non-existent", response['status'], 1)
    except Exception as e: 
        outputTestResult("Follow non-existent friend as existing user - ensure a non-OK response", testFailedString, "Any response except " + OK + " since the follower is non-existent", e, 1)
        outputTestDetails("Exception raised!")

    # Test 12
    userName, friendUserName = "non-existing-user", "ilir"
    try:
        response = requests.put(
            PROFILE_SERVICE_URI + ENDPOINT + "/" + userName + "/" + friendUserName).json()

        if (response["status"] == OK):
            outputTestResult("Follow existing friend as non-existing user - ensure a non-OK response", testFailedString, "Any response except " + OK + " since the followee is non-existent", response['status'], 1)
        else:
            outputTestResult("Follow existing friend as non-existing user - ensure a non-OK response", testPassedString, "Any response except " + OK + " since the followee is non-existent", response['status'], 1)
    except Exception as e: 
        outputTestResult("Follow existing friend as non-existing user - ensure a non-OK response", testFailedString, "Any response except " + OK + " since the followee is non-existent", e, 1)
        outputTestDetails("Exception raised!")

    # Test 13
    userName = "user1"
    try:
        response = requests.put(PROFILE_SERVICE_URI +
                                ENDPOINT + "/" + userName).json()

        if (response["status"] == OK):
            outputTestResult("Follow friend as an existing user (missing friendUserName param) - ensure a non-OK response", testFailedString, "Any response except " + OK + " since 'friendUserName' param is missing", response['status'], 1)
        else:
            outputTestResult("Follow friend as an existing user (missing friendUserName param) - ensure a non-OK response", testPassedString, "Any response except " + OK + " since 'friendUserName' param is missing", response['status'], 1)
    except Exception as e: 
        outputTestResult("Follow friend as an existing user (missing friendUserName param) - ensure a non-OK response", testFailedString, "Any response except " + OK + " since 'friendUserName' param is missing", e, 1)

def testLikeSong():
    global existingSongId
    
    # Test: Like a song with an existing user and an existing song ID
    ENDPOINT = "/likeSong"
    try:
        userName = 'user1'
        response = requests.put(PROFILE_SERVICE_URI +
                                ENDPOINT + "/" + userName + "/" + existingSongId).json()
        if (response["status"] == OK):
            outputTestResult("Like an existing song - check to see if status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Like an existing song - check to see if status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e: 
        outputTestResult("Like an existing song - check to see if status is OK", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")
    
    try:
        songInfo = songDb.getSongById(existingSongId)
        favoriteCounter = songInfo["songAmountFavourites"]
        if (favoriteCounter == 1):
            outputTestResult("Like an existing song - check to see if liking via /likeSong increments favourites counter", testPassedString, 1, favoriteCounter, 1)
        else:
            outputTestResult("Like an existing song - check to see if liking via /likeSong increments favourites counter", testFailedString, 1, favoriteCounter, 1)
    except Exception as e: 
        outputTestResult("Like an existing song - check to see if liking via /likeSong increments favourites counter", testFailedString, 1, e, 1)
        outputTestDetails("Exception raised!")

    # try:
    #     print(profileDb.getLikedSong(userName))
    #     if(existingSongId in profileDb.getLikedSong(userName)):
    #         outputTestResult("Like an existing song - check to see if the user likes the song in the database", testPassedString, True, existingSongId in profileDb.getLikedSong(userName), 1)
    #     else:
    #         outputTestResult("Like an existing song - check to see if the user likes the song in the database", testFailedString, True, existingSongId in profileDb.getLikedSong(userName), 1)
    # except Exception as e: 
    #     outputTestResult("Like an existing song - check to see if the user likes the song in the database", testFailedString, True, e, 1)
    #     outputTestDetails("Exception raised!")

def testUnlikeSong():
    global existingSongId
    ENDPOINT = "/unlikeSong"

    # Test: Unlike a song with an existing user and an existing song ID
    try:
        userName = 'user1'
        songId = existingSongId

        response = requests.put(PROFILE_SERVICE_URI + ENDPOINT + "/" + userName + "/" + songId).json()

        if (response["status"] == OK):
            outputTestResult("Unlike an existing song - check to see if status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Unlike an existing song - check to see if status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Unlike an existing song - check to see if status is OK", testFailedString, OK, e, 1)
    
    try:
        if(not(songId in profileDb.getLikedSong(userName))):
            outputTestResult("Unlike an existing song - check to see if the user still likes the song in the database", testPassedString, False, songId in profileDb.getLikedSong(userName), 1)
        else:
            outputTestResult("Unlike an existing song - check to see if the user still likes the song in the database", testFailedString, False, songId in profileDb.getLikedSong(userName), 1)
    except Exception as e: 
        outputTestResult("Unlike an existing song - check to see if the user still likes the song in the database", testFailedString, False, e, 1)
        outputTestDetails("Exception raised!")

    favoriteCounter = 99999
    try:
        songInfo = songDb.getSongById(songId)
        favoriteCounter = songInfo["songAmountFavourites"]
        if (favoriteCounter == 0):
            outputTestResult("Unlike an existing song - check to see if the likes for the song has decreased by 1", testPassedString, favoriteCounter, 0, 1)
        else:
            outputTestResult("Unlike an existing song - check to see if the likes for the song has decreased by 1", testFailedString, favoriteCounter, 0, 1)
    except Exception as e:
        outputTestResult("Unlike an existing song - check to see if the likes for the song has decreased by 1", testFailedString, favoriteCounter, e, 1)
        outputTestDetails("Exception raised!")
    outputTestDetails("If your expected number of favourites is 99999, your endpoint doesn't work. See the above tests for reason why.")

def testUnfollowFriends():
    ENDPOINT = "/unfollowFriend"

    # Test: Standard follow test for two users that follow each other (bi-directional)
    try:
        userName, friendUserName = "user1", "ilir"
        response = requests.put(
            PROFILE_SERVICE_URI + ENDPOINT + "/" + userName + "/" + friendUserName).json()

        if (response["status"] == OK):
            outputTestResult("Unfollow existing friend - check for OK status when 'user1' unfollows 'ilir'", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Unfollow existing friend - check for OK status when 'user1' unfollows 'ilir'", testFailedString, OK, response["status"], 1)
    except Exception as e: 
        outputTestResult("Unfollow existing friend - check for OK status when 'user1' unfollows 'ilir'", testFailedString, OK, e, 1)

    # Test: Standard follow test to ensure unfollow was one-way
    try:
        ilirsFriends = profileDb.getAllFriends('ilir')
        if ('user1' in ilirsFriends):
            outputTestResult("Unfollow existing friend - check to ensure 'ilir' didn't unfollow 'user1'", testPassedString, True, 'user1' in ilirsFriends, 1)
        else:
            outputTestResult("Unfollow existing friend - check to ensure 'ilir' didn't unfollow 'user1'", testFailedString, True, 'user1' in ilirsFriends, 1)
    except Exception as e: 
        outputTestResult("Unfollow existing friend - check to ensure 'ilir' didn't unfollow 'user1'", testFailedString, True, e, 1)
    
    # Test: Ensure user1 actually unfollowed ilir
    try:
        user1Friends = profileDb.getAllFriends('user1')
        if (not('ilir' in user1Friends)):
            outputTestResult("Unfollow existing friend - check to ensure 'user1' unfollowed 'ilir' in the database", testPassedString, False, 'ilir' in user1Friends, 1)
        else:
            outputTestResult("Unfollow existing friend - check to ensure 'user1' unfollowed 'ilir' in the database", testFailedString, False, 'ilir' in user1Friends, 1)
    except Exception as e: 
        outputTestResult("Unfollow existing friend - check to ensure 'user1' unfollowed 'ilir' in the database", testFailedString, False, e, 1)
    
def testAllFriendFavouriteSongTitles():
    global existingSongName

    ENDPOINT = "/getAllFriendFavouriteSongTitles"

    # Test: Check to make sure 'user1' is in 'ilir's friends list and that 'user1's liked songs are listed
    try:
        userName = 'ilir'
        response = requests.get(PROFILE_SERVICE_URI +
                                ENDPOINT + "/" + userName).json()
        if (response["status"] == OK):
            outputTestResult("Get all friends' favorite song titles - check status is OK", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Get all friends' favorite song titles - check status is OK", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Get all friends' favorite song titles - check status is OK", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")

    try:
        data = response['data']
        if ('user1' in data):
            outputTestResult("Get all friends' favorite song titles - ensure 'user1' is in 'ilir's friends list", testPassedString, True, 'user1' in data, 1)
        else:
            outputTestResult("Get all friends' favorite song titles - ensure 'user1' is in 'ilir's friends list", testFailedString, True, 'user1' in data, 1)
    except Exception as e:
        outputTestResult("Get all friends' favorite song titles - ensure 'user1' is in 'ilir's friends list", testFailedString, True, e, 1)
        outputTestDetails("Exception raised!")
    
    try:
        if (existingSongName in data["user1"]):
            outputTestResult("Get all friends' favorite song titles - ensure existing song is in 'user1's favourited songs", testPassedString, True, existingSongName in data["user1"], 1)
        else:
            outputTestResult("Get all friends' favorite song titles - ensure existing song is in 'user1's favourited songs", testFailedString, True, existingSongName in data["user1"], 1)
    except Exception as e:
        outputTestResult("Get all friends' favorite song titles - ensure existing song is in 'user1's favourited songs", testFailedString, True, e, 1)
        outputTestDetails("Exception raised!")

def testDeleteSongs():
    global existingSongId
    songId = existingSongId

    # Test: Standard test to delete valid song
    ENDPOINT = "/deleteSongById/" + str(songId)

    try:
        response = requests.delete(SONG_SERVICE_URI + ENDPOINT).json()

        if response["status"] == OK:
            outputTestResult("Delete song with valid ID - check for OK status", testPassedString, OK, response["status"], 1)
        else:
            outputTestResult("Delete song with valid ID - check for OK status", testFailedString, OK, response["status"], 1)
    except Exception as e:
        outputTestResult("Delete song with valid ID - check for OK status", testFailedString, OK, e, 1)
        outputTestDetails("Exception raised!")

    # Test: Ensure song is deleted from the song database
    try:
        songFromDb = songDb.getSongById(existingSongId)
        if (songFromDb == None):
            outputTestResult("Delete song with valid ID - check for deletion of song in Song database", testPassedString, None, songFromDb, 1)
        else:
            outputTestResult("Delete song with valid ID - check for deletion of song in Song database", testFailedString, None, songFromDb, 1)
    except Exception as e:
        outputTestResult("Delete song with valid ID - check for deletion of song in Song database", testFailedString, None, e, 1)
        outputTestDetails("Exception raised!")
    
    # Test: Ensure song is deleted from the profile database
    try:
        user1Songs = profileDb.getPlaylistSongs("user1")
        if (user1Songs.get(existingSongId) == None):
            outputTestResult("Delete song with valid ID - check for deletion of song in Profile database", testPassedString, None, user1Songs.get(existingSongId), 1)
        else:
            outputTestResult("Delete song with valid ID - check for deletion of song in Profile database", testFailedString, None, user1Songs.get(existingSongId), 1)
    except Exception as e:
        outputTestResult("Delete song with valid ID - check for deletion of song in Profile database", testFailedString, None, e, 1)
        outputTestDetails("Exception raised!")

print("Running auto-marker")

profileDb.wipeDb()  # wipe mongodb

try:
    testCreateUser()
    testAddingSongs()
    testGettingSongs()
    testFollowFriends()
    testLikeSong()
    testAllFriendFavouriteSongTitles()
    testIncrementingSongFavouritesCount()
    testDecrementingSongFavouritesCount()
    testUnlikeSong()
    testUnfollowFriends()
    testDeleteSongs()
    
except Exception as e:
    print(e)
    print("ERR: A try-catch statement is missing and the entire test suite terminated.")

songDb.closeDb()
profileDb.close()

print("Automarker Grade: " + str(totalStudentGrade) + "/" + str(totalTestCasePoints))
if (totalTestCasePoints != ABSOLUTE_TOTAL_MARKS):
    print("WARNING: Automarker stopped prematurely and not all tests were run. Contact your TA via e-mail to discuss this.")