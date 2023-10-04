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

