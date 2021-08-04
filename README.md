# Tourist walk algorithm
A deterministic walk over an environment. 

The objective of the tourist is to explore the environment. The tourist has a memory of the last _mu_ visited places.
Starting from an initial position, it goes to the next position according to some rule. 
The rule can be the maximum or the minimum difference between positions.

The traversal stops when the tourist gets trapped in a cycle or when got stuck in a point because there are no other places to go.
