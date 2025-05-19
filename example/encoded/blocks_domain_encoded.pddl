(define (domain x0)
  (:requirements :x1 :x2)
  (:types x3 x4 - object)
  (:predicates 
    (x5 ?x6 - x3 ?x7 - object)
    (x8 ?x6 - object)
    (x9)
  )
  
  (:action x10
    :parameters (?x6 - x3)
    :precondition (and (x8 ?x6) (x5 ?x6 x4) (x9))
    :effect (and (not (x5 ?x6 x4)) (not (x8 ?x6)) (not (x9)))
  )

  (:action x11
    :parameters (?x6 - x3)
    :precondition (and (x12 ?x6))
    :effect (and (not (x12 ?x6)) (x8 ?x6) (x9) (x5 ?x6 x4))
  )

  (:action x13
    :parameters (?x6 - x3 ?x7 - x3)
    :precondition (and (x12 ?x6) (x8 ?x7))
    :effect (and (not (x12 ?x6)) (not (x8 ?x7)) (x8 ?x6) (x9) (x5 ?x6 ?x7))
  )

  (:action x14
    :parameters (?x6 - x3 ?x7 - x3)
    :precondition (and (x5 ?x6 ?x7) (x8 ?x6) (x9))
    :effect (and (x12 ?x6) (x8 ?x7) (not (x8 ?x6)) (not (x9)) (not (x5 ?x6 ?x7)))
  )
)