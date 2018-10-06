import os
from pymongo import MongoClient

client = MongoClient(os.environ['database'])
db = client.veganwars
players = db.players

def get_player(chat_id, username, first_name):
    if username is not None:
        doc = players.find_one({'id':chat_id})
        if doc is None:
            players.insert_one({'id':chat_id, 'games_played':0, 'games_won':0, 'name':first_name, 'username':'@' + username, 'private_string':'0'})
    else:
        doc = players.find_one({'id':chat_id})
        if doc is None:
            players.insert_one({'id':chat_id, 'games_played':0, 'games_won':0, 'name':first_name})

def get_games(chat_id):
    doc = players.find_one({'id':chat_id})
    games_played = doc['games_played']
    games_won = doc['games_won']
    return [games_played, games_won]


def add_played_games(chat_id, game=1):
    players.update_one({'id':chat_id}, {'$inc':{'games_played':game}})


def getallplayers():
    return players.distinct('id')


def add_won_games(chat_id, game=1):
    players.update_one({'id':chat_id}, {'$inc':{'games_won':game}})


def get_dataname(chat_id):
    doc = players.find_one({'id':chat_id})
    return doc['name']


def add_column():
    players.update_many({}, {'$set':{'private_string':'0'}})


def get_current(chat_id):
    doc = players.find_one({'id':chat_id})
    current_weapon = None
    if 'current_weapon' in doc:
        current_weapon = doc['current_weapon']
    current_items = None
    if 'current_items' in doc:
        current_items = doc['current_items']
    current_skills = None
    if 'current_skills' in doc:
        current_skills = doc['current_skills']
    return [current_weapon, current_items, current_skills]


def get_unique(chat_id):
    doc = players.find_one({'id':chat_id})
    unique_weapon = None
    if 'unique_weapon' in doc:
        unique_weapon = doc['unique_weapon']
    unique_items = None
    if 'unique_items' in doc:
        unique_items = doc['unique_items']
    unique_skills = None
    if 'unique_skills' in doc:
        unique_skills = doc['unique_skills']
    return [unique_weapon, unique_items, unique_skills]


def change_weapon(cid, weapon_name):
    players.update_one({'id':cid}, {'$set':{'weapon_name':weapon_name}})


def add_item(cid, item_id):
    doc = players.find_one({'id':cid})
    data = list(doc['current_items'])
    if data[0] is None:
        data[0] = item_id
    elif len(data[0].split(',')) > 1:
        return False
    else:
        if data[0] == '':
            data[0] = item_id
        else:
            data[0] = data[0] + ',' + item_id
        while data[0] != '':
            if data[0][-1] != ',':
                break
            data[0] = data[0][:-1]
            if data[0] == '':
                data[0] = None
                break
    players.update_one({'id':cid}, {'$set':{'current_items':data[0]}})
    return True


def delete_item(cid, item_id):
    doc = players.find_one({'id':cid})
    data = list(doc['current_items'])
    if data[0] is None:
        return False
    else:
        data[0] = data[0].replace(item_id, '')
        if len(data[0])>0:
            if data[0][-1] == ',':
                data[0] = data[0][:-1]
        if len(data[0]) > 0:
            if data[0][0] == ',':
                data[0] = data[0][1:]
        if data[0] == '':
            data[0] = None
    players.update_one({'id':cid}, {'$set':{'current_items':data[0]}})
    return True


def get_private_string(chat_id):
    doc = players.find_one({'id':chat_id})
    private_string = None
    if 'private_string' in doc:
        private_string = doc['private_string']
    return private_string

def change_private_string(chat_id):
    doc = players.find_one({'id':chat_id})
    string = doc['private_string']
    if string == '0':
        string = '1'
    else:
        string = '0'
    players.update_one({'id':chat_id}, {'$set':{'private_string':string}})

def add_skill(cid, skill_name):
    doc = players.find_one({'id':cid})
    data = list()
    if 'current_skills' in doc:
        data = list(doc['current_skills'])
    if data[0] is None:
        data[0] = skill_name
    elif len(data[0].split(',')) > 1:
        return False
    else:
        if data[0] == '':
            data[0] = skill_name
        else:
            data[0] = data[0] + ',' + skill_name
        while data[0] != '':
            if data[0][-1] != ',':
                break
            data[0] = data[0][:-1]
            if data[0] == '':
                data[0] = None
                break
    players.update_one({'id':cid}, {'$set':{'current_skills':data[0]}})
    return True


def add_unique_weapon(username, weapon_name):
    doc = players.find_one({'username':username})
    data = list()
    if 'unique_weapon' in doc:
        data = list(doc['unique_weapon'])
    if data[0] is None:
        data[0] = weapon_name
    else:
        if data[0] == '':
            data[0] = weapon_name
        else:
            weapons = data[0].split(',')
            if weapon_name not in weapons:
                data[0] = data[0] + ',' + weapon_name
            else:
                return False
        while data[0] != '':
            if data[0][-1] != ',':
                break
            data[0] = data[0][:-1]
            if data[0] == '':
                data[0] = None
                break
    players.update_one({'username':username}, {'$set':{'unique_weapon':data[0]}})
    return True


def delete_unique_weapon(username, weapon_name):
    doc = players.find_one({'username':username})
    data = list(doc['unique_weapon'])
    if data[0] is None:
        return False
    else:
        data[0] = data[0].replace(weapon_name, '')
        if len(data[0]) > 0:
            if data[0][-1] == ',':
                data[0] = data[0][:-1]
        if len(data[0]) > 0:
            if data[0][0] == ',':
                data[0] = data[0][1:]
        if data[0] == '':
            data[0] = None
    players.update_one({'username':username}, {'$set':{'unique_weapon':data[0]}})
    db.commit()
    db.close()
    return True


def delete_inventory(username):
    players.update_one({'username':username}, {'$set':{'current_skills':None, 'current_items':None, 'current_weapon':None}})


def delete_skill(cid, skill_name):
    doc = players.find_one({'id':cid})
    data = list(doc['current_skills'])
    if data[0] is None:
        return False
    else:
        data[0] = data[0].replace(skill_name, '')
        if len(data[0]) > 0:
            if data[0][-1] == ',':
                data[0] = data[0][:-1]
        if len(data[0]) > 0:
            if data[0][0] == ',':
                data[0] = data[0][1:]
        if data[0] == '':
            data[0] = None
    players.update_one({'id':cid}, {'$set':{'current_skills':data[0]}})
    return True


def refresh_string():
    players.update_many({}, {'$set':{'private_string':'0'}})