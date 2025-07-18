(define (domain x0)
  (:requirements :strips :typing)
  (:types x1 x2 - object)
  (:predicates 
    (x3 ?x4 - x1 ?x5 - object)
    (x6 ?x4 - object)
    (x7)
  )
  
  (:action x8
    :parameters (?x4 - x1)
    :precondition (and (x6 ?x4) (x3 ?x4 x2) (x7))
    :effect (and (not (x3 ?x4 x2)) (not (x6 ?x4)) (not (x7)))
  )

  (:action x9
    :parameters (?x4 - x1)
    :precondition (and (x10 ?x4))
    :effect (and (not (x10 ?x4)) (x6 ?x4) (x7) (x3 ?x4 x2))
  )

  (:action x11
    :parameters (?x4 - x1 ?x5 - x1)
    :precondition (and (x10 ?x4) (x6 ?x5))
    :effect (and (not (x10 ?x4)) (not (x6 ?x5)) (x6 ?x4) (x7) (x3 ?x4 ?x5))
  )

  (:action x12
    :parameters (?x4 - x1 ?x5 - x1)
    :precondition (and (x3 ?x4 ?x5) (x6 ?x4) (x7))
    :effect (and (x10 ?x4) (x6 ?x5) (not (x6 ?x4)) (not (x7)) (not (x3 ?x4 ?x5)))
  )
)