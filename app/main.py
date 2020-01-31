from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os

# Start the app and setup the static directory for the html, css, and js files.
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

# This is your 'database' of scripts with their blocking info.
# You can store python dictionaries in the format you decided on for your JSON
   # parse the text files in script_data to create these objects - do not send the text
   # files to the client! The server should only send structured data in the sallest format necessary.
scripts = []

## load actor.csv and all script_data into scripts
def load_scripts():
    # parse actors.csv into a dictionary
    actors_file = open("./app/actors.csv")
    lines = actors_file.readlines()
    actors_dict = {}
    for line in lines:
        actor = line.split(",")
        actors_dict[actor[0].strip()] = actor[1].strip()
    scripts.append(actors_dict)
    
    directory_in_str = "./app/script_data/"
    directory = os.fsencode(directory_in_str)

    # parse scripts into a nested dictionary
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        f = open(directory_in_str + filename)
        script = {}
        # parse script number
        script["script_num"] = f.readline().strip()
        f.readline()
        # parse script text
        script["script_text"] = f.readline().strip()
        script["parts"] = []
        f.readline()
        lines = f.readlines()
        for line in lines:
            # parse part number
            part = {}
            part["part_num"] = line[:line.index(".")]
            line = line[line.index(".") + 2:]
            lst = line.split(", ")
            # parse start and end
            part["start"] = int(lst[0].strip())
            part["end"] = int(lst[1].strip())
            part["actors"] = []
            part["positions"] = []
            for i in range(2, len(lst)):
                actor_pos = lst[i].split("-")
                # parse actor and position
                part["actors"].append(actor_pos[0].strip())
                part["positions"].append(actor_pos[1].strip())
            script["parts"].append(part)
        scripts.append(script)

## overwrite a txt files


### DO NOT modify this route ###
@app.route('/')
def hello_world():
    return 'Theatre Blocking root route'

### DO NOT modify this example route. ###
@app.route('/example')
def example_block():
    # example_script = "O Romeo, Romeo, wherefore art thou Romeo? Deny thy father and refuse thy name. Or if thou wilt not, be but sworn my love And I'll no longer be a Capulet." '''
    example_script = "O Romeo, Romeo, wherefore art thou Romeo? Deny thy father and refuse thy name. Or if thou wilt not, be but sworn my love And I'll no longer be a Capulet."

    # This example block is inside a list - not in a dictionary with keys, which is what
    # we want when sending a JSON object with multiple pieces of data.
    return jsonify([example_script, 0, 41, 4])


''' Modify the routes below accordingly to 
parse the text files and send the correct JSON.'''

## GET route for script and blocking info
@app.route('/script/<int:script_id>')
def script(script_id):
    load_scripts()
    # right now, just sends the script id in the URL
    for i in range(1, len(scripts)):
        if int(scripts[i]["script_num"]) == script_id:
            return jsonify([scripts[i]["script_text"], scripts[i]["parts"]])
    abort(404)


## POST route for replacing script blocking on server
# Note: For the purposes of this assignment, we are using POST to replace an entire script.
# Other systems might use different http verbs like PUT or PATCH to replace only part
# of the script.
@app.route('/script', methods=['POST'])
def addBlocking():
    # right now, just sends the original request json

    return jsonify(request.json)



if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 80))