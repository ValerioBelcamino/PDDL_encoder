(define (problem blocks-problem)
  (:domain blocks-world)
  (:requirements :strips :typing)
  (:objects
    blockA blockB blockC - block
    table - table
  )
  (:init
    (clear blockA)
    (clear blockB)
    (clear blockC)
    (on blockA table)
    (on blockB table)
    (on blockC table)
    (handempty)
  )
  (:goal
    (and
      (on blockA blockB)
      (on blockB blockC)
      (on blockC table)
    )
  )
)