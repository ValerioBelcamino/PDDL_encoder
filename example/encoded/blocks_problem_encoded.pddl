(define (problem x15)
  (:domain x0)
  (:requirements :x1 :x2)
  (:objects
    x16 x17 x18 - x3
    x4 - x4
  )
  (:init
    (x8 x16)
    (x8 x17)
    (x8 x18)
    (x5 x16 x4)
    (x5 x17 x4)
    (x5 x18 x4)
    (x9)
  )
  (:goal
    (and
      (x5 x16 x17)
      (x5 x17 x18)
      (x5 x18 x4)
    )
  )
)