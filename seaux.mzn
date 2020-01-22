int: max_steps = 10;

int: N;
array[1..N] of int: storage;

% steps
array[1..max_steps, 1..N] of var 0..sum(storage): steps;
array[1..max_steps, 1..3] of var 1..N: transfered;
array[1..max_steps] of var 1..sum(storage): water;
%array[1..max_steps] of var set of 1..N: keep;

% initialization
array[1..N] of int: init;
constraint forall(n in 1..N)(steps[1, n] = init[n]);

var 1..max_steps: total_steps;

constraint forall(s in 2..max_steps)(
  transfered[s, 1] != transfered[s, 2]
  /\
  % quantity transfered
  water[s] = min(steps[s-1, transfered[s, 1]], storage[transfered[s, 2]] - steps[s-1, transfered[s, 2]])
  /\
  % water in X
  steps[s, transfered[s, 1]] = steps[s-1, transfered[s, 1]] - water[s]
  /\
  % water in Y
  steps[s, transfered[s, 2]] = steps[s-1, transfered[s, 2]] + water[s]
  /\
  % keep the previous state for the next steps
  steps[s, transfered[s, 3]] = steps[s-1, transfered[s, 3]]
);

array[1..N] of int: goal;
constraint
  exists(s in 2..max_steps) (
    forall(n in 1..N)(steps[s, n] = goal[n])
     /\
    total_steps = s
   );
  
solve minimize total_steps;