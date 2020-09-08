# Deployment
Our website is deployed [here](https://chenka51-linkexi1-theatre.herokuapp.com/actor.html).

# docker

To start:

`docker build -t a1-301 .`

`docker run -d --name a1-301-container -p 80:80 a1-301:latest`

`docker start a1-301-container`

To stop/remove container:

`docker stop a1-301-container`

`docker rm a1-301-container`

# heroku

`heroku login`

`heroku create --app <app-server-name>`

`heroku container:login`

`heroku container:push web --app <app-server-name>`

`heroku container:release web --app <app-server-name>`

`heroku open --app <app-server-name>`

<!-- # Write your documentation below -->

# Objective Statement

The objective of our theatre blocking app is to improve the efficiency during the planning stage and rehearsals of a performance, by allowing directors to conveniently modify and access the blocking for all parts of the scripts. It also allows actors to intuitively view the blockings for their own parts.


# Personas
### Leonardo (actor who plays Hamlet in *Hamlet*)
#### Bio
Leonado has been in the theatre industry for 2 years and was recently invited to play the role of Hamlet in one of Shakespeare's most famous plays. However, he finds it difficult to memorize Hamlet's role on stage due to the large number of soliliques in the play.

Leonado wonders if there is a way to better visualize the movement of his role as he is going through his script.

#### Goal
- Gain a better understanding of Hamlet's stage position

#### Frustration
- Large number of soliliques in *Hamlet* which requires a lot of memorization of movements on stage

### Julia (movement director of *Hamlet*)
#### Bio
Julia is the lead movement director of the play *Hamlet*. She is responsible for arranging all actors' movements on stage. She finds the current way of assigning movements and choreographies during rehearsal inefficient and time consuming. 

Julia would like her actors to know their position on stage prior to rehearsals to achieve maximum productivity. 
#### Goals
- Increase efficiency in rehearsals
- Assign movements and choreographies to actors before rehearsals

#### Fustration
- Movements are currently being taught on stage, which is taking up a lot of time during rehearsals

### Christopher (stage director of *Hamlet*)

#### Bio
Christopher is a senior stage director with a great reputation in the industry. He is currently a stage director of Shakespeare's legendary tragedy *Hamlet*. He wants to ensure that every aspect of the play works as expected. However, it is hard to ensure that every actor is at the correct position in large scenes where many actors are involved.

Christopher wants to be more familiar with every charactor's position at a particular line in a scene.

#### Goal
- Ensure the correctness of each actor's movement on stage

#### Frustration
- Hard to keep track of every actor's movement in a large scene involving many actors


# User Stories
As a theatre actor, I want to be able to search my scripts based on the script ID and my character name so that I am able to see only the parts I am responsible for.

- Actors are able to search their parts of a certain script by providing a script ID and a character ID.

As a theatre actor, I want to be able to view my movement on stage for my parts in the play, so that I can be more familiar with the character I am playing.

- Actors are able to view all blockings for their parts in a script, regardless of whether the actor has a line to say.

As a theatre actor, I want to be able to view my movement on stage along with the lines so that I know where should I be on stage at a specific line. 

- The blockings for actors are displayed in the following format: 
Character: line [position]

As a director, I want to be able to search any script based on the script ID so that I can view all parts of a script. 

- Directors are able to search their parts of a certain script by providing a script ID.

As a director, I want to be able to import a new script blocking file into the database so that other directors and actors can have access to it. 

- Directors are able to load a new script with blocking
- A unique blocking ID must be assigned

As a director, I want to be able to assign actors' positions and movements before rehearsals, so actors can know their movements on stage before coming to rehearsals. 

- Directors are able to assign a blocking to each actor at each line for all parts of the script.

As a director, I want to be able to modify the blockings I assigned, so that I can adjust an actor's blocking immediately when needed. 

- Directors are able to modify a blocking to each actor at each line for all parts of the script

As a director, I want to be able to view all actor's blocking in a specific script, so that I can get a better understanding of the entire visual on stage. 

- Directors are able to view all blockings of each actor.

As a director, I want to be able to view actors' blocking along with the lines, so that I can ensure all actors are at the right place at the right time.

- The blockings for directors are displayed in the following format: 
Character: line 
Character A:[position] 
Character B: [position]

# JSON
We designed out JSON serialization in a way that minimizes redundancy. 

## GET JSON serialization

#### Our GET JSON serialization is consisted of 3 layers:

- First layer:
    - the script text
    - an object that maps each actor number to the corresponding character name, according to the csv file

- Second layer:
     - an array of objects corresponding to each part of the script 
    
- Third layer:
    - a ```"start"``` key that maps to the starting char index
    - an ```"end"``` key that maps to the ending char index
    - an ```"actors"``` key that maps to the array of actors in this part
    - an ```"positions"``` key that maps to an array of the corresponding position for each actor in this part. For example, the position of the first actor in the ```"actors"``` array is the first element in the ```"positions"``` array


In the JSON example provided in the starter code, we noticed that a separate JSON array is sent for each part in the same script. This method causes redundant data such as the script text to be sent when the script has more than one part.

We designed our JSON serialization the way above so that only one JSON array is sent for each script. It prevents redundant data to be sent to the front end and increases efficiency while transmitting data.
    
## POST JSON Serialization
#### Our POST JSON serialization consists of layers

- First layer:
    - a ```"scriptNum"``` key that maps to the script number
    - a ```"scriptBlocks"``` key that maps to an array which consists of information about the script

- Second layer:
    - the script text
    - an array of objects corresponding to each part of the script

- Third layer: 
    - a ```"start"``` key that maps to the starting char index
    - an ```"end"``` key that maps to the ending char index
    - an ```"actors"``` key that maps to a nested array of ```[actor, position]``` pairs

In the starter code, ```getBlockingDetailsOnScreen()``` returns a JavaScript array where text is split into different parts of the script. This method is a bit different from how the ```addBlockToScreen()``` method is implemented as it takes the complete script text and slices it into the corresponding parts inside the method.

Since we constructed our back-end "database" according to ```addBlockToScreen()``` is implemented, we decided to concatenate text strings together before sending it to the back end. This reduces the workload at the back end as a part of the data is already formatted.
