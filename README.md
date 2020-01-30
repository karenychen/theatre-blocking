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

The objective of our theatre blocking app is to improve the efficiency during the planning stage and rehearsals of a performance, by allowing directors to conveniently modify and access the blocking for all parts of the scripts。 It also allows actors to intuitively view the blockings for their own parts.

# Personas

### Leonardo (actor who plays Hamlet in _Hamlet_)

#### Bio

Leonado has been in the theatre industry for 2 years and was recently invited to play the role of Hamlet in one of Shakespeare's most famous plays. However, he finds it difficult to memorize Hamlet's role on stage due to the large number of soliliques in the play.
Leonado wonders if there is a way to better visualize the movement of his role as he is going through his script.

#### Goal

- Gain a better understanding of Hamlet's stage position

#### Frustration

- Large number of soliliques in _Hamlet_ which requires a lot of memorization of movements on stage

### Julia (movement director of _Hamlet_)

#### Bio

Julia is the lead movement director of the play _Hamlet_. She is responsible for arranging all actors' movements on stage. She finds the current way of assigning movements and choreographies during rehearsal inefficient and time consuming.

Julia would like her actors to know their position on stage prior to rehearsals to achieve maximum productivity.

#### Goals

- Increase efficiency and flexibility in theatre production
- Assign movements and choreographies to actors before rehearsals

#### Fustration

- Movements are currently being taught on stage, which is taking up a lot of time during rehearsals

### Christopher (stage director of _Hamlet_)

#### Bio

Christopher is a senior stage director with a great reputation in the industry. He is currently a stage director of Shakespeare's legendary tragedy _Hamlet_. He wants to ensure that every aspect of the play works as expected. However, it is hard to ensure that every actor is at the correct position in large scenes where many actors are involved.

Christopher wants to be more familiar with every charactor's position at a particular line in a scene.

#### Goal

- Ensure the correctness of each actor's movement on stage

#### Frustration

- Hard to keep track of every actor's movement in a large scene involving many actors

# User Stories

### Leonardo

As a theatre actor, I want to be able to view my movement on stage for all my parts in the play, so that I can be more familiar with the character I am playing.

### Julia

As a movement director, I want to be able to assign actors' positions and movements before rehearsals, so that rehearsals can be more efficient and less time consuming.

### Christopher

As a stage director, I want be able to keep track of all actors' position on stage, so that I can ensure the play runs smoothly.

# Acceptance Criteria

- An actor is able to view all blockings for their parts on stage, regardless of whether the actor has a line to say.
- An actor is able to see their parts of a particular script with blockings with a username and the script ID.
- Blockings for actors are printed in the format:

  <center>Character: line [position]</center>

- A director is able to assign, modify and view blockings for every actor for all parts of the script.
- Blockings viewed by directors are:

  <center> Character: line <br> Character A:[modifiable position] <br> Character B: [modifiable position] 
  </center>

- A director is able to load a new script with blocking and assign a script ID to the new script.
