import client
import os
from uuid import uuid1
from tabulate import tabulate


baseUrl = "https://www.thegamecrafter.com"

def createGame(session, name):
    gameName = "%s-%s" % (name, uuid1())
    designerId = "AA9F2900-5B68-11E5-8112-B32D36CD926D"
    game = client.postGame(session, gameName, designerId)
    
    gameName = game["name"]
    gameId = game["id"]
    editUrl = "%s/publish/editor/%s" % (baseUrl, gameId)
    print("Created %s. Edit it here %s" % (gameName, editUrl))

    return game

def getUser(session):
    print(client.getUser(session))

def listGames(session):
    gamesResponse = client.getGamesForUser(session)
    printGames(gamesResponse["items"])

def listGamesForUserDesigners(session):
    designersResponse = client.getDesigners(session)
    designers = designersResponse["items"]

    games = []
    for designer in designers:
        gamesResponse = client.getGamesForDesignerId(session, designer["id"])
        games.extend(gamesResponse["items"])

    printGames(games)   

def printGames(games):
    headers = ["name", "id", "link"]
    data = []

    for game in games:
        gameName = game["name"]
        gameId = game["id"]
        gameLink = "%s/%s" %(baseUrl, game["edit_uri"])
        data.append([gameName, gameId, gameLink])

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))

def createComponent(session, game, component):
    pass

def listDesigners(session):
    designersResponse = client.getDesigners(session)

    headers = ["name", "id"]
    data = []
    for designer in designersResponse["items"]:
        print(designer)
        name = designer["name"]
        designerId = designer["id"]
        data.append([name, designerId])

    print(tabulate(data, headers=headers, tablefmt='orgtbl'))

def login():
    publicApiKey = os.environ.get('THEGAMECRAFTER_PUBLIC_KEY')
    if not publicApiKey:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PUBLIC_KEY. Value is %s' % publicApiKey)
    
    userName = os.environ.get('THEGAMECRAFTER_USER')
    if not userName:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_USER. Value is %s' % userName)

    userPassword = os.environ.get('THEGAMECRAFTER_PASSWORD')
    if not userPassword:
        raise Exception('Could not log in. You need to set the env variable THEGAMECRAFTER_PASSWORD. Value is %s' % userPassword)

    return client.login(publicApiKey, userName, userPassword)