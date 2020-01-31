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

# load actor.csv and all script_data into scripts


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
            # part["part_num"] = line[:line.index(".")]
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

# rewrite a txt files


def write_scripts():
    directory_in_str = "./app/script_data/"
    directory = os.fsencode(directory_in_str)

    # iterate through script_data files
    for file in os.listdir(directory):
        # opens and reads all lines to a file
        filename = os.fsdecode(file)
        fr = open(directory_in_str + filename)
        lines = fr.readlines()
        fr.close()
        script_num = lines[0].strip()  # get script_num
        # iterate over scripts and searches for matching script
        for i in range(1, len(scripts)):
            if script_num == scripts[i]["script_num"]:  # script_num matches
                counter = 4
                # change all part lines in the file
                for part in scripts[i]["parts"]:
                    # generate a new part line to write in the file
                    line = str(counter - 3) + ". " + \
                        str(part["start"]) + ", " + str(part["end"])
                    for j in range(len(part["actors"])):
                        line += ", " + \
                            str(part["actors"][j]) + "-" + \
                            str(part["positions"][j])
                    line += "\n"
                    lines[counter] = line  # change part line
                    counter += 1
                fw = open(directory_in_str + filename, "wt")
                fw.writelines(lines)
                fw.close()


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

# GET route for script and blocking info
@app.route('/script/<int:script_id>')
def script(script_id):
    load_scripts()
    for i in range(1, len(scripts)):
        if int(scripts[i]["script_num"]) == script_id:
            return jsonify([scripts[i]["script_text"], scripts[i]["parts"], scripts[0]])
    abort(404)


# POST route for replacing script blocking on server
# Note: For the purposes of this assignment, we are using POST to replace an entire script.
# Other systems might use different http verbs like PUT or PATCH to replace only part
# of the script.
@app.route('/script', methods=['POST'])
def addBlocking():
    # content = request.get_json()
    # script_num = content["scriptNum"]
    # new_parts = content["scriptBlocks"][1]

    script_num = request.json["scriptNum"]
    new_parts = request.json["scriptBlocks"][1]

    # load_scripts()

    for i in range(1, len(scripts)):  # iterate over scripts and search for matching script
        if scripts[i]["script_num"] == script_num:  # script number matches
            parts = scripts[i]["parts"]
            for j in range(len(new_parts)):  # iterater over new_parts and parts
                actor_pos_lst = new_parts[j]["actors"]
                # create and fill in new_actors and new_parts
                new_actors = []
                new_pos = []
                for actor_pos in actor_pos_lst:
                    new_actors.append(actor_pos[0])
                    new_pos.append(actor_pos[1])
                # assign new_actors and new_pos into parts
                parts[j]["actors"] = new_actors
                parts[j]["positions"] = new_pos
    write_scripts()
    return jsonify(request.json)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=os.environ.get('PORT', 8848))
