% nani.pl


% Facts *******************************************
% Initial facts describing the world of 'Nani search' 
% These clauses are dynamic so can be modified by assert and retract
:- dynamic location2/2.
:- dynamic here1/1.
:- dynamic have1/1.

% dynamic STATE
% locations - location(X,Y) => X is in Y
% NOTE: findall/3 returns all solutions - findall([T,P], location2(T,P), S).
% returns all pairs below
% NOTE: findall/3 returns all solutions - findall(T, location2(T,office), S).
% returns [computer,desk]
location2(computer, office).
location2(desk, office).   
location2(flashlight, desk).    %retractable
location2(breadbox, kitchen).
location2(bread, breadbox).
location2(washing_machine, cellar).
location2(nani, washing_machine).   %retractable

% present location of self
here1(kitchen).

% have1 - items taken from Place or removed from Thing - initially none - false



% static STATE
% rooms
room1(office).
room1(kitchen).
room1(dining_room).
room1(hall).
room1(cellar).

% room connections - doors
door2(office,hall).
door2(hall,dining_room).
door2(dining_room,kitchen).
door2(kitchen,cellar).
door2(kitchen,office).

% can_carry
can_carry(flashlight).
can_carry(nani).




% Rules *******************************************
% self-orientation
where_am_I1(P) :-
  here1(P).
where_am_i1(P) :-
  here1(P).


% connection rules
connect2(X,Y):- door2(X,Y).
connect2(X,Y):- door2(Y,X).


% action rules **********************************
% go
% NOTE:
% max(X,Y,Z) :-
% (  X =< Y -> 
%        Z = Y
%    ;  
%        Z = X  
% ).
can_go1(Place) :-
  (Place = cellar ->
      here1(P),
      connect2(P,Place),
      have1(flashlight)
  ;
      here1(P),
      connect2(P,Place)
  ).


go1(Place) :-
  can_go1(Place),
  retract(here1(_)),
  asserta(here1(Place)),
  write('now you are in '), write(Place), nl.


% take Thing from Place
can_take2(Thing, Place) :-
  here1(Place),
  can_carry(Thing),
  location2(Thing, Place).

take2(Thing, Place) :-
  can_take2(Thing, Place),
  retract(location2(Thing,Place)), 
  asserta(have1(Thing)),
  write(Thing), write(' taken from present location in '), write(Place), nl.


% remove Thing from Thing
can_remove2(X, Thing) :-
  here1(Place),
  location2(Thing, Place),
  location2(X, Thing),
  can_carry(X).

remove2(X, Thing) :-
  can_remove2(X, Thing),
  retract(location2(X,Thing)), 
  asserta(have1(X)),
  (X = nani ->
    write('Nani taken - congratulations - you win!!!!!!')
  ;
    write(X), write(' taken from ' ), write(Thing), nl
  ).

