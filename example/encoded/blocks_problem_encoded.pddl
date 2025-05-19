(define (problem u9)
  (:domain u0)
  (:requirements :strips :typing)
  (:objects
    d0 a1 x2 - d1
    a2 - a2
  )
  (:init
    (h6 d0)
    (h6 a1)
    (h6 x2)
    (x3 d0 a2)
    (x3 a1 a2)
    (x3 x2 a2)
    (e7)
  )
  (:goal
    (and
      (x3 d0 a1)
      (x3 a1 x2)
      (x3 x2 a2)
    )
  )
)