(define (problem x13)
  (:domain x0)
  (:requirements :strips :typing)
  (:objects
    x14 x15 x16 - x1
    x2 - x2
  )
  (:init
    (x6 x14)
    (x6 x15)
    (x6 x16)
    (x3 x14 x2)
    (x3 x15 x2)
    (x3 x16 x2)
    (x7)
  )
  (:goal
    (and
      (x3 x14 x15)
      (x3 x15 x16)
      (x3 x16 x2)
    )
  )
)