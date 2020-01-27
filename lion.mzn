%problème de traversée de rivière avec buffles et lions


% include "globals.mzn"; 
int: num_animaux  = 3;
int: max_trav = 10; %nombre max de traversées
int: max_num_trav = 2; % nombre maximum d'animaux par traversée (min=1)
int: A = 1; % rive A
int: B = 2; % rive B


% Où sont les buffles
array[1..max_trav, 1..num_animaux] of var A..B: buffles;

% Où sont les lions
array[1..max_trav, 1..num_animaux] of var A..B: lions;


% Où est le radeau
array[1..max_trav] of var A..B: radeau;

% Nombre min de traversées
var 1..max_trav: total_trav;

%les animaux transférés (sur le radeau)
array[1..max_trav] of var set of 1..num_animaux: transfereB;
array[1..max_trav] of var set of 1..num_animaux: transfereL;



%solve minimize total_trav;
solve:: 
       int_search(
         [buffles[i,j] | i in 1..max_trav, j in 1..num_animaux] ++ 
          [lions[i,j] | i in 1..max_trav, j in 1..num_animaux] ++ 
        radeau ++
        [total_trav],
        occurrence, 
        indomain_min, 
                complete) 
     minimize total_trav ;

constraint

   % initialisation 
   forall(i in 1..num_animaux) (
      buffles[1,i] = A
   )
   /\
   forall(i in 1..num_animaux) (
      lions[1,i] = A
   )
   /\
   radeau[1] = A
   /\
   transfereB[1] = 1..num_animaux
   /\
   transfereL[1] = 1..num_animaux
 ;
  
  
 constraint %pas plus de lions que de buffles sur chaque rive 
   forall(t in 2..max_trav) (
   forall(place in A..B)(
   sum(a in 1..num_animaux where not(a in transfereB[t]))(bool2int(buffles[t,a]=place)) >= sum(a in 1..num_animaux where not(a in transfereL[t]))(bool2int(lions[t,a]=place))
   )
   )
   ;
   
 constraint %gestion des transferts 
 
       forall(t in 2..max_trav) (
       (card(transfereB[t]) +  card(transfereL[t])) <= 2 /\ (card(transfereB[t]) + card(transfereL[t])) >=1
       /\
       exists(place in A..B) (      
       radeau[t-1] = place
       /\ 
       radeau[t] != radeau[t-1]
       /\
       forall(i in 1..num_animaux) (
          ((i in transfereB[t]) <-> (
                                     buffles[t-1,i] = place /\
                                     buffles[t-1,i] != buffles[t,i]
                                 ))
          /\
          (not(i in transfereB[t]) <-> buffles[t-1,i] = buffles[t,i])
       )
      /\
      forall(i in 1..num_animaux) (
          ((i in transfereL[t]) <-> (
                                     lions[t-1,i] = place /\
                                     lions[t-1,i] != lions[t,i]
                                 ))
          /\
          (not(i in transfereL[t]) <-> lions[t-1,i] = lions[t,i])
       )
     )

   )
;

constraint % la fin
   exists(t in 2..max_trav) (
      forall(i in 1..num_animaux) (
          buffles[t, i] = B /\ lions[t,i]=B
      )
      /\
      radeau[t] = B
      /\
      total_trav = t

   )
   
;


output
[
   "total_trav: " ++ show(total_trav)
]
++
[
  if p = 1 /\ t <= fix(total_trav) then "\n" else " " endif ++
    if t <= fix(total_trav) then
       "B: " ++ show(buffles[t,p]) ++ " L:" ++ show(lions[t,p]) ++
       if p = num_animaux 
            then " R: " ++ show(radeau[t]) ++ " Trans: B : " ++ show(transfereB[t]) ++" L:" ++ show(transfereL[t])
       else "" endif
    else "" endif
  | t in 1..max_trav, p in 1..num_animaux
]
;
