(define (domain blocks-world)
  (:requirements :strips :typing)
  (:types block table - object)
  (:predicates 
    (on ?x - block ?y - object)
    (clear ?x - object)
    (handempty)
  )
  
  (:action pickup
    :parameters (?x - block)
    :precondition (and (clear ?x) (on ?x table) (handempty))
    :effect (and (not (on ?x table)) (not (clear ?x)) (not (handempty)))
  )

  (:action putdown
    :parameters (?x - block)
    :precondition (and (holding ?x))
    :effect (and (not (holding ?x)) (clear ?x) (handempty) (on ?x table))
  )

  (:action stack
    :parameters (?x - block ?y - block)
    :precondition (and (holding ?x) (clear ?y))
    :effect (and (not (holding ?x)) (not (clear ?y)) (clear ?x) (handempty) (on ?x ?y))
  )

  (:action unstack
    :parameters (?x - block ?y - block)
    :precondition (and (on ?x ?y) (clear ?x) (handempty))
    :effect (and (holding ?x) (clear ?y) (not (clear ?x)) (not (handempty)) (not (on ?x ?y)))
  )
)