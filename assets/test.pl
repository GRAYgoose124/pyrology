man(socrates).
man(plato).
man(aristotle).
woman(adele).
woman(bertha).
woman(catherine).
friends(raju, mahesh).
singer(sonu).

parent(adele, bertha).
parent(adele, catherine).
parent(socrates, bertha).
parent(socrates, catherine).
parent(plato, aristotle).
parent(bertha, aristotle).

odd_number(5).


mortal(X) :- animal(X); fungi(X); plant(X).

human(X) :- man(X); woman(X).
mammal(X) :- human(X).
animal(X) :- mammal(X).



child(X, Y) :- parent(Y, X).
grandchild(X, Y) :- parent(Y, Z), parent(Z, X).
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

son(X, Y) :- child(X, Y), man(X).
daughter(X, Y) :- child(X, Y), woman(X).

father(X, Y) :- parent(X, Y), man(X).
mother(X, Y) :- parent(X, Y), woman(X).




siblings(X, Y) :- parent(X, Z), parent(Y, Z), X \= Y.