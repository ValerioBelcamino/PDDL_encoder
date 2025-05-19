(define (domain u0)
  (:requirements :strips :typing)
  (:types d1 a2 - object)
  (:predicates 
    (x3 ?i4 - d1 ?h5 - object)
    (h6 ?i4 - object)
    (e7)
  )
  
  (:action x8
    :parameters (?i4 - d1)
    :precondition (and (h6 ?i4) (x3 ?i4 a2) (e7))
    :effect (and (not (x3 ?i4 a2)) (not (h6 ?i4)) (not (e7)))
  )

  (:action d9
    :parameters (?i4 - d1)
    :precondition (and (v0 ?i4))
    :effect (and (not (v0 ?i4)) (h6 ?i4) (e7) (x3 ?i4 a2))
  )

  (:action x1
    :parameters (?i4 - d1 ?h5 - d1)
    :precondition (and (v0 ?i4) (h6 ?h5))
    :effect (and (not (v0 ?i4)) (not (h6 ?h5)) (h6 ?i4) (e7) (x3 ?i4 ?h5))
  )

  (:action r2
    :parameters (?i4 - d1 ?h5 - d1)
    :precondition (and (x3 ?i4 ?h5) (h6 ?i4) (e7))
    :effect (and (v0 ?i4) (h6 ?h5) (not (h6 ?i4)) (not (e7)) (not (x3 ?i4 ?h5)))
  )
)