# world.py - single class in tot/* which is dependent on the prolog file.
# It is expected that a specific world-file be created for each prolog file.
# This world-file is specific to nani.pl



rooms = ['kitchen','cellar','office','hall','dining_room']
counter = 0


# examine reward, win, backtrack, n=iterations
def evaluate(prolog_thread, iterations):                          
    print(f"!!! world.evaluate: prolog_thread = {prolog_thread} iterations={iterations}")
    global counter
    print(f"world.evaluate: counter = {counter} reward = {thought['reward']}")
   
    # rooms_visited
    for room in rooms:
        if thought['response'] == 'go(' + room + ')':
            thought['rooms_visited'].append(room)
            thought['parent_room'] = thought['current_room']
            thought['current_room'] = room

    # backtrack?
    counter+=1
    if counter == 5:
        prolog_thread.query('go({parent_room})')
        thought['current_room'] = thought['parent_room']
    else:
        iterations+=1

    # reward
    if thought['reward'] == 0:
        if prolog_thread.query('here(office)'):
            thought['reward'] = 1
            counter = 0

    if thought['reward'] == 1:
        if prolog_thread.query('have(flashlight)'):
            thought['reward'] = 2
            counter = 0

    if thought['reward'] == 2:
        if prolog_thread.query('here(cellar)'):
            thought['reward'] = 3
            counter = 0

    if thought['reward'] == 3:
        if prolog_thread.query('have(nani)'):
            thought['reward'] = 4
            thought['reply'] = 'WIN'
            print("\nhave(nani) is True => WIN !!!!!\n")

    print(f"world.evaluate: reward={thought['reward']} counter={counter}")
    print(f"world.evaluate: iterations = {iterations}")
    return iterations


# specific to nani.pl
initial_prompt = '''
    Act as a Prolog expert. ONLY reply with single prolog predicate - no
    explanation!!!  
    The Prolog knowledge base consists of facts and rules.
    names beginning with small letters are 'atoms'
    single capital letters such as P or X are variables and represent
    possible atom values.
    You can respond to prompts by questions or actions (explained below)

    Here are some translations to English for these unchanging Prolog facts.
    These translations are given by example but can apply to other arguments
    found inside the parentheses:
    (1) room1(kitchen) means kitchen is a room.
    (2) door2(kitchen, office) means kitchen is connected to office and
    vice-versa, so it is possible to go from one room to the other.
    (3) can_carry(flashlight) means flashlight can be removed from objects.

    Here are some translations to English for these changeable Prolog facts.
    These translations are given by example but can apply to other arguments
    found inside the parentheses:
    (1) here1(kitchen) means you are in the kitchen. 
    (2) have1(flashlight) means you have removed the flashlight from some
    object and now 'have' it in your possession.
    (3) location2(flashlight,desk) means the flashlight is contained in the
    object desk. If can_carry(flashlight) then the flashlight can be removed
    from the desk. If not can_carry(flashlight) then flashlight cannot be
    removed.

    Actions are responses to prompts which may change the state of the
    problem, and possibly earn a point reward.
    Possible actions are:
    (1) go(R) - try to go to room R where R reprersents a room name atom
    (1) remove(X,T) - try to remove an object X (flashlight or nani) from
    an object T, where T reprersents an object for which location2(X,T) is
    true. (see below for the meaning of the question location2(X,T))

    Questions can be asked in Prolog by substituting a capital letter
    variable (or two) for any atom (or pair of atoms) in any fact or rule.
    Special questions are:
    (1) Let R b a variable representing any room. Responding to a prompt by
    where_amI1(R) will give a reply from Prolog the room name (atom) you 
    are presently in.
    (2) Let X be a variable representing any object for which can_carry(X)
    is true. Responding to a prompt by have(X) will give a reply from Prolog
    the names (atoms) of the objects you are carrying, or false if you are
    carrying no objects.
    (3) Let R be the name of some room which you are not in, i.e
    where_am_I1(R) returns false.
    can_go(R) will return a reply of true if the room R is connected to your
    present room by a door, and return false otherwise.
    If can_go(R) returns true then you can successfully respond to a prompt
    with the action 'go(R)'
    (4) Let X be a variable representing any object, and let T be a variable
    representing any object. Then the question location2(X,T) returns true
    if X is contained in the object T, and false otherwise. If
    location2(X,T) is true, and can_carry(X) is true, then the action
    remove(X,T) can be performed with the result that the state will change
    from have(X) false to have(X) true, and a point reward will be earned.

    The goal is to remove the nani object from the washing_machine,
    which is in the cellar. However to go to the cellar requires
    have(flashlight) true, where location2(flashlight,desk) is true.

    have(nani) true is equivalent to earning four points - you begin with 
    zero points and you sart in the kitchen.

    Please respond to each prompt with a Prolog action or question - return
    the response as a string of valid Prolog syntax. Recall that all valid
    Prolog syntax ends with a period '.'

    The first subgoal is to go to the room containing the flashlight- office.

    Here is the Prolog knowledge base:
% nani.pl
% Facts *******************************************
% Initial facts describing the world of 'Nani search' 
% These clauses are dynamic so can be modified by assert and retract
:- dynamic location/2.
:- dynamic here/1.
:- dynamic have/1.

% dynamic STATE
% locations - location(X,Y) => X is in Y
% NOTE: findall/3 returns all solutions - findall([T,P], location(T,P), S).
% returns all pairs below
% NOTE: findall/3 returns all solutions - findall(T, location(T,office), S).
% returns [computer,desk]
location(computer, office).
location(desk, office).   
location(flashlight, desk).    %retractable
location(breadbox, kitchen).
location(bread, breadbox).
location(washing_machine, cellar).
location(nani, washing_machine).   %retractable

% present location of self
here(kitchen).

% have - items taken from Place or removed from Thing - initially none - false



% static STATE
% rooms
room(office).
room(kitchen).
room(dining_room).
room(hall).
room(cellar).

% room connections - doors
door(office,hall).
door(hall,dining_room).
door(dining_room,kitchen).
door(kitchen,cellar).
door(kitchen,office).

% can_carry
can_carry(flashlight).
can_carry(bread).
can_carry(nani).




% Rules *******************************************
% self-orientation
where_am_I(P) :-
  here(P).
where_am_i(P) :-
  here(P).


% connection rules
connect(X,Y):- door(X,Y).
connect(X,Y):- door(Y,X).


% action rules **********************************
% go
% NOTE:
% max(X,Y,Z) :-
% (  X =< Y -> 
%        Z = Y
%    ;  
%        Z = X  
% ).
can_go(Place) :-
  (Place = cellar ->
      here(P),
      connect(P,Place),
      have(flashlight)
  ;
      here(P),
      connect(P,Place)
  ).


go(Place) :-
  can_go(Place),
  retract(here(_)),
  asserta(here(Place)),
  write('now you are in '), write(Place), nl.


% remove Thing from Thing
can_remove(X, Thing) :-
  here(Place),
  location(Thing, Place),
  location(X, Thing),
  can_carry(X).

remove(X, Thing) :-
  can_remove(X, Thing),
  retract(location(X,Thing)), 
  asserta(have(X)),
  (X = nani ->
    write('Nani taken - congratulations - you win!!!!!!')
  ;
    write(X), write(' taken from ' ), write(Thing), nl
  ).

        '''
# thought = initial thought, then dynamic
thought = {
    'current_room': 'kitchen',
    'parent_room': 'kitchen',
    'rooms_visited': ['kitchen'],
    'objects_removed': [],
    'reward': 0,
    'win': 4,
    'task': initial_prompt,
    'response':'',  # from llm
    'reply':''      # from prolog knowledge base
}


# tasks - len(tasks)=6
tasks = [
   initial_prompt,

   '''
   ONLY reply with single prolog predicate - no explanation!!!  
   From this list of prolog predicates:
   go(kitchen).
   go(cellar).
   location(flashlight,desk).
   remove(flashlight,desk). 
   location(nani,maching_machine).
   remove(nani,washing_machine). 
   these are not physical actions - only virtual actions which you can do:
   return prolog predicate in order to find the flashlight
   return ONLY the prolog predicate!!
   ''',

   '''
   ONLY reply with single prolog predicate - no explanation!!!  
   From this list of prolog predicates:
   go(kitchen).
   go(cellar).
   location(flashlight,desk).
   remove(flashlight,desk). 
   location(nani,maching_machine).
   remove(nani,washing_machine). 
   these are not physical actions - only virtual actions which you can do:
   return prolog predicate in order to remove the flashlight from the desk
   return ONLY the prolog predicate!!
   ''',

   '''
   ONLY reply with single prolog predicate - no explanation!!!  
   From this list of prolog predicates:
   go(kitchen).
   go(cellar).
   location(flashlight,desk).
   remove(flashlight,desk). 
   location(nani,maching_machine).
   remove(nani,washing_machine). 
   these are not physical actions - only virtual actions which you can do:
   return prolog predicate to go kitchen
   return ONLY the prolog predicate!!
   ''',

   '''
   ONLY reply with single prolog predicate - no explanation!!!  
   From this list of prolog predicates:
   go(cellar).
   go(kitchen).
   location(flashlight,desk).
   remove(flashlight,desk). 
   location(nani,maching_machine).
   remove(nani,washing_machine). 
   these are not physical actions - only virtual actions which you can do:
   return the prolog predicate to go cellar
   return ONLY the prolog predicate!!
   ''',

   '''
   ONLY reply with single prolog predicate - no explanation!!!  
   From this list of prolog predicates:
   go(cellar).
   go(kitchen).
   location(flashlight,desk).
   remove(flashlight,desk). 
   location(nani,maching_machine).
   remove(nani,washing_machine). 
   these are not physical actions - only virtual actions which you can do:
   return the prolog predicate to locate nani
   return ONLY the prolog predicate!!
   ''',

   '''
   ONLY reply with single prolog predicate - no explanation!!!  
   From this list of prolog predicates:
   go(kitchen).
   go(cellar).
   location(flashlight,desk).
   remove(flashlight,desk). 
   location(nani,maching_machine).
   remove(nani,washing_machine). 
   these are not physical actions - only virtual actions which you can do:
   return prolog predicate in order to remove the nani from the washing_machine
   return ONLY the prolog predicate!!
   '''

]
   
