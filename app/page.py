import requests, os
from flask import Flask

url = "https://api.github.com/users/"
people = 'people.txt'
user_not_found_message = "User not found 😢"

app = Flask(__name__)

# Routes

@app.route('/')
def info():
    return "Add your Github username to the URL ( /MawulB ) to get the list of people you are following but are not following you back 😉\n\n Or Add /followers or /following to the username to get yours followers or following respectively 🌚"

@app.route('/<name>')
def home(name):
    update_user_count(name)
    try:
        return get_following_not_followers(name)
    except Exception as e:
        print(e)
        return user_not_found_message

@app.route('/<name>/followers')
def followers(name):
    update_user_count(name)
    try:
        return get_followers(name)
    except Exception as e:
        print(e)
        return user_not_found_message

@app.route('/<name>/following')
def following(name):
    update_user_count(name)
    try:
        return get_following(name)
    except Exception as e:
        print(e)
        return user_not_found_message


# Helper functions

def get_following_not_followers(name):
    following = get_following(name)
    followers = get_followers(name)
    diff = set(following) - set(followers)
    return list(diff)

def get_followers(name) -> list:
    response = requests.get(url + name + '/followers')
    lst = []
    for follower in response.json():
        lst.append(follower['login'])
    return lst

def get_following(name):
    response = requests.get(url + name + '/following')
    lst = []
    for following in response.json():
        lst.append(following['login'])
    return lst

def create_file_if_not_exists(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('')

def update_user_count(name):
    create_file_if_not_exists(people)
    with open(people, 'r') as file:
        lines = file.readlines()
    with open(people, 'w') as file:
        for line in lines:
            if line.startswith(name):
                count = int(line.split('=')[1].strip()) + 1
                file.write(f'{name}={count}\n')
            else:
                file.write(line)
        if not any(name in line for line in lines):
            file.write(f'{name}=1\n')


if __name__ == '__main__':
    app.run()