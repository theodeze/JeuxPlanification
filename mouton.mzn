% sheep count
int: N;
int: array_size = N*2+1; 
int: max_steps;

var 1..max_steps: total_steps;

% actual state at each step
% 1 : white
% 0 : empty
% 2 : black
array[1..max_steps, 1..array_size] of var 0..2: states;
% one position to another
% 1 : source
% 2 : destination
array[1..max_steps, 1..2] of var 0..array_size: transfered;

% Initialization
constraint forall(m in 1..N)(states[1, m] = 1); % white sheeps
constraint forall(m in (array_size-N+1)..array_size)(states[1, m] = 2); % black sheeps

% Constraints
constraint forall(s in 2..max_steps)(
  % black sheeps
  (
    % move from an non-empty case to an empty one
    states[s-1, transfered[s, 1]] == 1
    /\
    states[s, transfered[s, 1]] == 0
    /\
    states[s-1, transfered[s, 2]] == 0
    /\
    states[s, transfered[s, 2]] == 1
    /\
    (
      % 1 move
      ((transfered[s, 2] - transfered[s, 1]) == 1)
      \/
      % 2 moves
      (
        states[s, transfered[s, 2]-1] != 0
        /\
        (transfered[s, 2] - transfered[s, 1]) == 2
      )
    )
  )
  
  \/
  % white sheeps
  (
    % move from an non-empty case to an empty one
    states[s-1, transfered[s, 1]] == 2
    /\
    states[s, transfered[s, 1]] == 0
    /\
    states[s-1, transfered[s, 2]] == 0
    /\
    states[s, transfered[s, 2]] == 2
    /\
    (
      % 1 move
      ((transfered[s, 1] - transfered[s, 2]) == 1)
      \/
      % 2 moves
      (
        states[s, transfered[s, 2]+1] != 0
        /\
        (transfered[s, 1] - transfered[s, 2]) == 2
      )
    )   
  )
  
);

constraint forall(s in 2..max_steps)(
  forall(v in 1..array_size)(

    (
      v == transfered[s, 1] 
      /\
      states[s, v] == states[s-1, transfered[s, 2]]
    )

    \/

    (
      v == transfered[s, 2] 
      /\
      states[s, v] == states[s-1, transfered[s, 1]]
    )

    \/

    (
      v != transfered[s, 1] /\ v != transfered[s, 2] /\ states[s, v] == states[s-1, v]
    )
    
   )
);


% Final state
constraint exists(s in 2..max_steps)(
  forall(m in 1..N)(states[s, m] = 2)
  /\
  forall(m in (array_size-N+1)..array_size)(states[s, m] = 1)
  /\
  total_steps = s
  \/ 
  total_steps == max_steps
);

solve satisfy;