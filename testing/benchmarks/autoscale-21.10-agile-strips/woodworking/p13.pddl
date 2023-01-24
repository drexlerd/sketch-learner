; woodworking task with 99 parts and 200% wood
; Machines:
;   2 highspeed-saw
;   2 glazer
;   2 grinder
;   2 immersion-varnisher
;   2 planer
;   2 saw
;   2 spray-varnisher

(define (problem wood-prob)
  (:domain woodworking)
  (:objects
    highspeed-saw0 highspeed-saw1 - highspeed-saw
    glazer0 glazer1 - glazer
    grinder0 grinder1 - grinder
    immersion-varnisher0 immersion-varnisher1 - immersion-varnisher
    planer0 planer1 - planer
    saw0 saw1 - saw
    spray-varnisher0 spray-varnisher1 - spray-varnisher
    mauve white red blue green black - acolour
    teak mahogany pine beech walnut cherry oak - awood
    p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 p17 p18 p19 p20 p21 p22 p23 p24 p25 p26 p27 p28 p29 p30 p31 p32 p33 p34 p35 p36 p37 p38 p39 p40 p41 p42 p43 p44 p45 p46 p47 p48 p49 p50 p51 p52 p53 p54 p55 p56 p57 p58 p59 p60 p61 p62 p63 p64 p65 p66 p67 p68 p69 p70 p71 p72 p73 p74 p75 p76 p77 p78 p79 p80 p81 p82 p83 p84 p85 p86 p87 p88 p89 p90 p91 p92 p93 p94 p95 p96 p97 p98 - part
    b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 b24 b25 b26 b27 b28 b29 b30 b31 b32 b33 b34 b35 b36 b37 b38 - board
    s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 - aboardsize
  )
  (:init
    (grind-treatment-change varnished colourfragments)
    (grind-treatment-change glazed untreated)
    (grind-treatment-change untreated untreated)
    (grind-treatment-change colourfragments untreated)
    (is-smooth smooth)
    (is-smooth verysmooth)
    (= (total-cost) 0)
    (boardsize-successor s0 s1)
    (boardsize-successor s1 s2)
    (boardsize-successor s2 s3)
    (boardsize-successor s3 s4)
    (boardsize-successor s4 s5)
    (boardsize-successor s5 s6)
    (boardsize-successor s6 s7)
    (boardsize-successor s7 s8)
    (boardsize-successor s8 s9)
    (boardsize-successor s9 s10)
    (boardsize-successor s10 s11)
    (empty highspeed-saw0)
    (empty highspeed-saw1)
    (has-colour glazer0 black)
    (has-colour glazer0 natural)
    (has-colour glazer0 white)
    (has-colour glazer0 mauve)
    (has-colour glazer0 blue)
    (has-colour glazer0 red)
    (has-colour glazer0 green)
    (has-colour glazer1 black)
    (has-colour glazer1 natural)
    (has-colour glazer1 white)
    (has-colour glazer1 mauve)
    (has-colour glazer1 blue)
    (has-colour glazer1 red)
    (has-colour glazer1 green)
    (has-colour immersion-varnisher0 green)
    (has-colour immersion-varnisher0 black)
    (has-colour immersion-varnisher0 natural)
    (has-colour immersion-varnisher0 mauve)
    (has-colour immersion-varnisher0 red)
    (has-colour immersion-varnisher0 blue)
    (has-colour immersion-varnisher0 white)
    (has-colour immersion-varnisher1 green)
    (has-colour immersion-varnisher1 black)
    (has-colour immersion-varnisher1 natural)
    (has-colour immersion-varnisher1 mauve)
    (has-colour immersion-varnisher1 red)
    (has-colour immersion-varnisher1 blue)
    (has-colour immersion-varnisher1 white)
    (has-colour spray-varnisher0 green)
    (has-colour spray-varnisher0 black)
    (has-colour spray-varnisher0 natural)
    (has-colour spray-varnisher0 mauve)
    (has-colour spray-varnisher0 red)
    (has-colour spray-varnisher0 blue)
    (has-colour spray-varnisher0 white)
    (has-colour spray-varnisher1 green)
    (has-colour spray-varnisher1 black)
    (has-colour spray-varnisher1 natural)
    (has-colour spray-varnisher1 mauve)
    (has-colour spray-varnisher1 red)
    (has-colour spray-varnisher1 blue)
    (has-colour spray-varnisher1 white)
    (available p0)
    (treatment p0 glazed)
    (surface-condition p0 rough)
    (wood p0 cherry)
    (colour p0 blue)
    (goalsize p0 medium)
    (= (spray-varnish-cost p0) 10)
    (= (glaze-cost p0) 15)
    (= (grind-cost p0) 30)
    (= (plane-cost p0) 20)
    (unused p1)
    (goalsize p1 small)
    (= (spray-varnish-cost p1) 5)
    (= (glaze-cost p1) 10)
    (= (grind-cost p1) 15)
    (= (plane-cost p1) 10)
    (unused p2)
    (goalsize p2 small)
    (= (spray-varnish-cost p2) 5)
    (= (glaze-cost p2) 10)
    (= (grind-cost p2) 15)
    (= (plane-cost p2) 10)
    (unused p3)
    (goalsize p3 medium)
    (= (spray-varnish-cost p3) 10)
    (= (glaze-cost p3) 15)
    (= (grind-cost p3) 30)
    (= (plane-cost p3) 20)
    (unused p4)
    (goalsize p4 small)
    (= (spray-varnish-cost p4) 5)
    (= (glaze-cost p4) 10)
    (= (grind-cost p4) 15)
    (= (plane-cost p4) 10)
    (unused p5)
    (goalsize p5 large)
    (= (spray-varnish-cost p5) 15)
    (= (glaze-cost p5) 20)
    (= (grind-cost p5) 45)
    (= (plane-cost p5) 30)
    (unused p6)
    (goalsize p6 medium)
    (= (spray-varnish-cost p6) 10)
    (= (glaze-cost p6) 15)
    (= (grind-cost p6) 30)
    (= (plane-cost p6) 20)
    (unused p7)
    (goalsize p7 large)
    (= (spray-varnish-cost p7) 15)
    (= (glaze-cost p7) 20)
    (= (grind-cost p7) 45)
    (= (plane-cost p7) 30)
    (available p8)
    (treatment p8 colourfragments)
    (surface-condition p8 smooth)
    (wood p8 oak)
    (colour p8 white)
    (goalsize p8 large)
    (= (spray-varnish-cost p8) 15)
    (= (glaze-cost p8) 20)
    (= (grind-cost p8) 45)
    (= (plane-cost p8) 30)
    (unused p9)
    (goalsize p9 medium)
    (= (spray-varnish-cost p9) 10)
    (= (glaze-cost p9) 15)
    (= (grind-cost p9) 30)
    (= (plane-cost p9) 20)
    (unused p10)
    (goalsize p10 medium)
    (= (spray-varnish-cost p10) 10)
    (= (glaze-cost p10) 15)
    (= (grind-cost p10) 30)
    (= (plane-cost p10) 20)
    (unused p11)
    (goalsize p11 small)
    (= (spray-varnish-cost p11) 5)
    (= (glaze-cost p11) 10)
    (= (grind-cost p11) 15)
    (= (plane-cost p11) 10)
    (available p12)
    (treatment p12 colourfragments)
    (surface-condition p12 rough)
    (wood p12 beech)
    (colour p12 blue)
    (goalsize p12 large)
    (= (spray-varnish-cost p12) 15)
    (= (glaze-cost p12) 20)
    (= (grind-cost p12) 45)
    (= (plane-cost p12) 30)
    (available p13)
    (treatment p13 glazed)
    (surface-condition p13 smooth)
    (wood p13 oak)
    (colour p13 white)
    (goalsize p13 medium)
    (= (spray-varnish-cost p13) 10)
    (= (glaze-cost p13) 15)
    (= (grind-cost p13) 30)
    (= (plane-cost p13) 20)
    (unused p14)
    (goalsize p14 small)
    (= (spray-varnish-cost p14) 5)
    (= (glaze-cost p14) 10)
    (= (grind-cost p14) 15)
    (= (plane-cost p14) 10)
    (unused p15)
    (goalsize p15 small)
    (= (spray-varnish-cost p15) 5)
    (= (glaze-cost p15) 10)
    (= (grind-cost p15) 15)
    (= (plane-cost p15) 10)
    (unused p16)
    (goalsize p16 large)
    (= (spray-varnish-cost p16) 15)
    (= (glaze-cost p16) 20)
    (= (grind-cost p16) 45)
    (= (plane-cost p16) 30)
    (available p17)
    (treatment p17 glazed)
    (surface-condition p17 verysmooth)
    (wood p17 oak)
    (colour p17 mauve)
    (goalsize p17 large)
    (= (spray-varnish-cost p17) 15)
    (= (glaze-cost p17) 20)
    (= (grind-cost p17) 45)
    (= (plane-cost p17) 30)
    (available p18)
    (treatment p18 colourfragments)
    (surface-condition p18 smooth)
    (wood p18 walnut)
    (colour p18 red)
    (goalsize p18 medium)
    (= (spray-varnish-cost p18) 10)
    (= (glaze-cost p18) 15)
    (= (grind-cost p18) 30)
    (= (plane-cost p18) 20)
    (unused p19)
    (goalsize p19 large)
    (= (spray-varnish-cost p19) 15)
    (= (glaze-cost p19) 20)
    (= (grind-cost p19) 45)
    (= (plane-cost p19) 30)
    (available p20)
    (treatment p20 glazed)
    (surface-condition p20 rough)
    (wood p20 oak)
    (colour p20 black)
    (goalsize p20 medium)
    (= (spray-varnish-cost p20) 10)
    (= (glaze-cost p20) 15)
    (= (grind-cost p20) 30)
    (= (plane-cost p20) 20)
    (unused p21)
    (goalsize p21 medium)
    (= (spray-varnish-cost p21) 10)
    (= (glaze-cost p21) 15)
    (= (grind-cost p21) 30)
    (= (plane-cost p21) 20)
    (unused p22)
    (goalsize p22 large)
    (= (spray-varnish-cost p22) 15)
    (= (glaze-cost p22) 20)
    (= (grind-cost p22) 45)
    (= (plane-cost p22) 30)
    (unused p23)
    (goalsize p23 medium)
    (= (spray-varnish-cost p23) 10)
    (= (glaze-cost p23) 15)
    (= (grind-cost p23) 30)
    (= (plane-cost p23) 20)
    (unused p24)
    (goalsize p24 large)
    (= (spray-varnish-cost p24) 15)
    (= (glaze-cost p24) 20)
    (= (grind-cost p24) 45)
    (= (plane-cost p24) 30)
    (available p25)
    (treatment p25 glazed)
    (surface-condition p25 rough)
    (wood p25 beech)
    (colour p25 black)
    (goalsize p25 small)
    (= (spray-varnish-cost p25) 5)
    (= (glaze-cost p25) 10)
    (= (grind-cost p25) 15)
    (= (plane-cost p25) 10)
    (available p26)
    (treatment p26 colourfragments)
    (surface-condition p26 smooth)
    (wood p26 cherry)
    (colour p26 blue)
    (goalsize p26 small)
    (= (spray-varnish-cost p26) 5)
    (= (glaze-cost p26) 10)
    (= (grind-cost p26) 15)
    (= (plane-cost p26) 10)
    (unused p27)
    (goalsize p27 large)
    (= (spray-varnish-cost p27) 15)
    (= (glaze-cost p27) 20)
    (= (grind-cost p27) 45)
    (= (plane-cost p27) 30)
    (unused p28)
    (goalsize p28 medium)
    (= (spray-varnish-cost p28) 10)
    (= (glaze-cost p28) 15)
    (= (grind-cost p28) 30)
    (= (plane-cost p28) 20)
    (unused p29)
    (goalsize p29 medium)
    (= (spray-varnish-cost p29) 10)
    (= (glaze-cost p29) 15)
    (= (grind-cost p29) 30)
    (= (plane-cost p29) 20)
    (unused p30)
    (goalsize p30 large)
    (= (spray-varnish-cost p30) 15)
    (= (glaze-cost p30) 20)
    (= (grind-cost p30) 45)
    (= (plane-cost p30) 30)
    (unused p31)
    (goalsize p31 medium)
    (= (spray-varnish-cost p31) 10)
    (= (glaze-cost p31) 15)
    (= (grind-cost p31) 30)
    (= (plane-cost p31) 20)
    (unused p32)
    (goalsize p32 large)
    (= (spray-varnish-cost p32) 15)
    (= (glaze-cost p32) 20)
    (= (grind-cost p32) 45)
    (= (plane-cost p32) 30)
    (available p33)
    (treatment p33 glazed)
    (surface-condition p33 rough)
    (wood p33 oak)
    (colour p33 natural)
    (goalsize p33 medium)
    (= (spray-varnish-cost p33) 10)
    (= (glaze-cost p33) 15)
    (= (grind-cost p33) 30)
    (= (plane-cost p33) 20)
    (available p34)
    (treatment p34 varnished)
    (surface-condition p34 verysmooth)
    (wood p34 cherry)
    (colour p34 black)
    (goalsize p34 medium)
    (= (spray-varnish-cost p34) 10)
    (= (glaze-cost p34) 15)
    (= (grind-cost p34) 30)
    (= (plane-cost p34) 20)
    (available p35)
    (treatment p35 varnished)
    (surface-condition p35 smooth)
    (wood p35 cherry)
    (colour p35 mauve)
    (goalsize p35 large)
    (= (spray-varnish-cost p35) 15)
    (= (glaze-cost p35) 20)
    (= (grind-cost p35) 45)
    (= (plane-cost p35) 30)
    (available p36)
    (treatment p36 glazed)
    (surface-condition p36 smooth)
    (wood p36 mahogany)
    (colour p36 natural)
    (goalsize p36 large)
    (= (spray-varnish-cost p36) 15)
    (= (glaze-cost p36) 20)
    (= (grind-cost p36) 45)
    (= (plane-cost p36) 30)
    (available p37)
    (treatment p37 glazed)
    (surface-condition p37 verysmooth)
    (wood p37 mahogany)
    (colour p37 black)
    (goalsize p37 large)
    (= (spray-varnish-cost p37) 15)
    (= (glaze-cost p37) 20)
    (= (grind-cost p37) 45)
    (= (plane-cost p37) 30)
    (unused p38)
    (goalsize p38 medium)
    (= (spray-varnish-cost p38) 10)
    (= (glaze-cost p38) 15)
    (= (grind-cost p38) 30)
    (= (plane-cost p38) 20)
    (unused p39)
    (goalsize p39 medium)
    (= (spray-varnish-cost p39) 10)
    (= (glaze-cost p39) 15)
    (= (grind-cost p39) 30)
    (= (plane-cost p39) 20)
    (unused p40)
    (goalsize p40 large)
    (= (spray-varnish-cost p40) 15)
    (= (glaze-cost p40) 20)
    (= (grind-cost p40) 45)
    (= (plane-cost p40) 30)
    (unused p41)
    (goalsize p41 large)
    (= (spray-varnish-cost p41) 15)
    (= (glaze-cost p41) 20)
    (= (grind-cost p41) 45)
    (= (plane-cost p41) 30)
    (unused p42)
    (goalsize p42 large)
    (= (spray-varnish-cost p42) 15)
    (= (glaze-cost p42) 20)
    (= (grind-cost p42) 45)
    (= (plane-cost p42) 30)
    (unused p43)
    (goalsize p43 large)
    (= (spray-varnish-cost p43) 15)
    (= (glaze-cost p43) 20)
    (= (grind-cost p43) 45)
    (= (plane-cost p43) 30)
    (unused p44)
    (goalsize p44 medium)
    (= (spray-varnish-cost p44) 10)
    (= (glaze-cost p44) 15)
    (= (grind-cost p44) 30)
    (= (plane-cost p44) 20)
    (unused p45)
    (goalsize p45 small)
    (= (spray-varnish-cost p45) 5)
    (= (glaze-cost p45) 10)
    (= (grind-cost p45) 15)
    (= (plane-cost p45) 10)
    (unused p46)
    (goalsize p46 small)
    (= (spray-varnish-cost p46) 5)
    (= (glaze-cost p46) 10)
    (= (grind-cost p46) 15)
    (= (plane-cost p46) 10)
    (unused p47)
    (goalsize p47 small)
    (= (spray-varnish-cost p47) 5)
    (= (glaze-cost p47) 10)
    (= (grind-cost p47) 15)
    (= (plane-cost p47) 10)
    (unused p48)
    (goalsize p48 medium)
    (= (spray-varnish-cost p48) 10)
    (= (glaze-cost p48) 15)
    (= (grind-cost p48) 30)
    (= (plane-cost p48) 20)
    (available p49)
    (treatment p49 glazed)
    (surface-condition p49 verysmooth)
    (wood p49 mahogany)
    (colour p49 black)
    (goalsize p49 medium)
    (= (spray-varnish-cost p49) 10)
    (= (glaze-cost p49) 15)
    (= (grind-cost p49) 30)
    (= (plane-cost p49) 20)
    (unused p50)
    (goalsize p50 small)
    (= (spray-varnish-cost p50) 5)
    (= (glaze-cost p50) 10)
    (= (grind-cost p50) 15)
    (= (plane-cost p50) 10)
    (unused p51)
    (goalsize p51 medium)
    (= (spray-varnish-cost p51) 10)
    (= (glaze-cost p51) 15)
    (= (grind-cost p51) 30)
    (= (plane-cost p51) 20)
    (unused p52)
    (goalsize p52 medium)
    (= (spray-varnish-cost p52) 10)
    (= (glaze-cost p52) 15)
    (= (grind-cost p52) 30)
    (= (plane-cost p52) 20)
    (unused p53)
    (goalsize p53 medium)
    (= (spray-varnish-cost p53) 10)
    (= (glaze-cost p53) 15)
    (= (grind-cost p53) 30)
    (= (plane-cost p53) 20)
    (unused p54)
    (goalsize p54 small)
    (= (spray-varnish-cost p54) 5)
    (= (glaze-cost p54) 10)
    (= (grind-cost p54) 15)
    (= (plane-cost p54) 10)
    (unused p55)
    (goalsize p55 large)
    (= (spray-varnish-cost p55) 15)
    (= (glaze-cost p55) 20)
    (= (grind-cost p55) 45)
    (= (plane-cost p55) 30)
    (available p56)
    (treatment p56 glazed)
    (surface-condition p56 smooth)
    (wood p56 teak)
    (colour p56 mauve)
    (goalsize p56 medium)
    (= (spray-varnish-cost p56) 10)
    (= (glaze-cost p56) 15)
    (= (grind-cost p56) 30)
    (= (plane-cost p56) 20)
    (unused p57)
    (goalsize p57 medium)
    (= (spray-varnish-cost p57) 10)
    (= (glaze-cost p57) 15)
    (= (grind-cost p57) 30)
    (= (plane-cost p57) 20)
    (unused p58)
    (goalsize p58 small)
    (= (spray-varnish-cost p58) 5)
    (= (glaze-cost p58) 10)
    (= (grind-cost p58) 15)
    (= (plane-cost p58) 10)
    (unused p59)
    (goalsize p59 small)
    (= (spray-varnish-cost p59) 5)
    (= (glaze-cost p59) 10)
    (= (grind-cost p59) 15)
    (= (plane-cost p59) 10)
    (unused p60)
    (goalsize p60 medium)
    (= (spray-varnish-cost p60) 10)
    (= (glaze-cost p60) 15)
    (= (grind-cost p60) 30)
    (= (plane-cost p60) 20)
    (unused p61)
    (goalsize p61 medium)
    (= (spray-varnish-cost p61) 10)
    (= (glaze-cost p61) 15)
    (= (grind-cost p61) 30)
    (= (plane-cost p61) 20)
    (unused p62)
    (goalsize p62 large)
    (= (spray-varnish-cost p62) 15)
    (= (glaze-cost p62) 20)
    (= (grind-cost p62) 45)
    (= (plane-cost p62) 30)
    (available p63)
    (treatment p63 colourfragments)
    (surface-condition p63 smooth)
    (wood p63 oak)
    (colour p63 green)
    (goalsize p63 small)
    (= (spray-varnish-cost p63) 5)
    (= (glaze-cost p63) 10)
    (= (grind-cost p63) 15)
    (= (plane-cost p63) 10)
    (unused p64)
    (goalsize p64 large)
    (= (spray-varnish-cost p64) 15)
    (= (glaze-cost p64) 20)
    (= (grind-cost p64) 45)
    (= (plane-cost p64) 30)
    (unused p65)
    (goalsize p65 small)
    (= (spray-varnish-cost p65) 5)
    (= (glaze-cost p65) 10)
    (= (grind-cost p65) 15)
    (= (plane-cost p65) 10)
    (unused p66)
    (goalsize p66 medium)
    (= (spray-varnish-cost p66) 10)
    (= (glaze-cost p66) 15)
    (= (grind-cost p66) 30)
    (= (plane-cost p66) 20)
    (available p67)
    (treatment p67 varnished)
    (surface-condition p67 rough)
    (wood p67 oak)
    (colour p67 blue)
    (goalsize p67 medium)
    (= (spray-varnish-cost p67) 10)
    (= (glaze-cost p67) 15)
    (= (grind-cost p67) 30)
    (= (plane-cost p67) 20)
    (unused p68)
    (goalsize p68 medium)
    (= (spray-varnish-cost p68) 10)
    (= (glaze-cost p68) 15)
    (= (grind-cost p68) 30)
    (= (plane-cost p68) 20)
    (unused p69)
    (goalsize p69 medium)
    (= (spray-varnish-cost p69) 10)
    (= (glaze-cost p69) 15)
    (= (grind-cost p69) 30)
    (= (plane-cost p69) 20)
    (unused p70)
    (goalsize p70 medium)
    (= (spray-varnish-cost p70) 10)
    (= (glaze-cost p70) 15)
    (= (grind-cost p70) 30)
    (= (plane-cost p70) 20)
    (unused p71)
    (goalsize p71 medium)
    (= (spray-varnish-cost p71) 10)
    (= (glaze-cost p71) 15)
    (= (grind-cost p71) 30)
    (= (plane-cost p71) 20)
    (unused p72)
    (goalsize p72 medium)
    (= (spray-varnish-cost p72) 10)
    (= (glaze-cost p72) 15)
    (= (grind-cost p72) 30)
    (= (plane-cost p72) 20)
    (unused p73)
    (goalsize p73 medium)
    (= (spray-varnish-cost p73) 10)
    (= (glaze-cost p73) 15)
    (= (grind-cost p73) 30)
    (= (plane-cost p73) 20)
    (unused p74)
    (goalsize p74 medium)
    (= (spray-varnish-cost p74) 10)
    (= (glaze-cost p74) 15)
    (= (grind-cost p74) 30)
    (= (plane-cost p74) 20)
    (available p75)
    (treatment p75 colourfragments)
    (surface-condition p75 rough)
    (wood p75 walnut)
    (colour p75 natural)
    (goalsize p75 large)
    (= (spray-varnish-cost p75) 15)
    (= (glaze-cost p75) 20)
    (= (grind-cost p75) 45)
    (= (plane-cost p75) 30)
    (unused p76)
    (goalsize p76 small)
    (= (spray-varnish-cost p76) 5)
    (= (glaze-cost p76) 10)
    (= (grind-cost p76) 15)
    (= (plane-cost p76) 10)
    (unused p77)
    (goalsize p77 large)
    (= (spray-varnish-cost p77) 15)
    (= (glaze-cost p77) 20)
    (= (grind-cost p77) 45)
    (= (plane-cost p77) 30)
    (unused p78)
    (goalsize p78 medium)
    (= (spray-varnish-cost p78) 10)
    (= (glaze-cost p78) 15)
    (= (grind-cost p78) 30)
    (= (plane-cost p78) 20)
    (unused p79)
    (goalsize p79 small)
    (= (spray-varnish-cost p79) 5)
    (= (glaze-cost p79) 10)
    (= (grind-cost p79) 15)
    (= (plane-cost p79) 10)
    (available p80)
    (treatment p80 glazed)
    (surface-condition p80 rough)
    (wood p80 teak)
    (colour p80 green)
    (goalsize p80 medium)
    (= (spray-varnish-cost p80) 10)
    (= (glaze-cost p80) 15)
    (= (grind-cost p80) 30)
    (= (plane-cost p80) 20)
    (unused p81)
    (goalsize p81 large)
    (= (spray-varnish-cost p81) 15)
    (= (glaze-cost p81) 20)
    (= (grind-cost p81) 45)
    (= (plane-cost p81) 30)
    (unused p82)
    (goalsize p82 large)
    (= (spray-varnish-cost p82) 15)
    (= (glaze-cost p82) 20)
    (= (grind-cost p82) 45)
    (= (plane-cost p82) 30)
    (unused p83)
    (goalsize p83 medium)
    (= (spray-varnish-cost p83) 10)
    (= (glaze-cost p83) 15)
    (= (grind-cost p83) 30)
    (= (plane-cost p83) 20)
    (unused p84)
    (goalsize p84 medium)
    (= (spray-varnish-cost p84) 10)
    (= (glaze-cost p84) 15)
    (= (grind-cost p84) 30)
    (= (plane-cost p84) 20)
    (unused p85)
    (goalsize p85 medium)
    (= (spray-varnish-cost p85) 10)
    (= (glaze-cost p85) 15)
    (= (grind-cost p85) 30)
    (= (plane-cost p85) 20)
    (available p86)
    (treatment p86 colourfragments)
    (surface-condition p86 verysmooth)
    (wood p86 teak)
    (colour p86 red)
    (goalsize p86 large)
    (= (spray-varnish-cost p86) 15)
    (= (glaze-cost p86) 20)
    (= (grind-cost p86) 45)
    (= (plane-cost p86) 30)
    (unused p87)
    (goalsize p87 large)
    (= (spray-varnish-cost p87) 15)
    (= (glaze-cost p87) 20)
    (= (grind-cost p87) 45)
    (= (plane-cost p87) 30)
    (unused p88)
    (goalsize p88 small)
    (= (spray-varnish-cost p88) 5)
    (= (glaze-cost p88) 10)
    (= (grind-cost p88) 15)
    (= (plane-cost p88) 10)
    (unused p89)
    (goalsize p89 medium)
    (= (spray-varnish-cost p89) 10)
    (= (glaze-cost p89) 15)
    (= (grind-cost p89) 30)
    (= (plane-cost p89) 20)
    (unused p90)
    (goalsize p90 large)
    (= (spray-varnish-cost p90) 15)
    (= (glaze-cost p90) 20)
    (= (grind-cost p90) 45)
    (= (plane-cost p90) 30)
    (available p91)
    (treatment p91 glazed)
    (surface-condition p91 verysmooth)
    (wood p91 cherry)
    (colour p91 green)
    (goalsize p91 medium)
    (= (spray-varnish-cost p91) 10)
    (= (glaze-cost p91) 15)
    (= (grind-cost p91) 30)
    (= (plane-cost p91) 20)
    (unused p92)
    (goalsize p92 large)
    (= (spray-varnish-cost p92) 15)
    (= (glaze-cost p92) 20)
    (= (grind-cost p92) 45)
    (= (plane-cost p92) 30)
    (unused p93)
    (goalsize p93 small)
    (= (spray-varnish-cost p93) 5)
    (= (glaze-cost p93) 10)
    (= (grind-cost p93) 15)
    (= (plane-cost p93) 10)
    (unused p94)
    (goalsize p94 medium)
    (= (spray-varnish-cost p94) 10)
    (= (glaze-cost p94) 15)
    (= (grind-cost p94) 30)
    (= (plane-cost p94) 20)
    (available p95)
    (treatment p95 glazed)
    (surface-condition p95 verysmooth)
    (wood p95 pine)
    (colour p95 blue)
    (goalsize p95 medium)
    (= (spray-varnish-cost p95) 10)
    (= (glaze-cost p95) 15)
    (= (grind-cost p95) 30)
    (= (plane-cost p95) 20)
    (unused p96)
    (goalsize p96 large)
    (= (spray-varnish-cost p96) 15)
    (= (glaze-cost p96) 20)
    (= (grind-cost p96) 45)
    (= (plane-cost p96) 30)
    (unused p97)
    (goalsize p97 medium)
    (= (spray-varnish-cost p97) 10)
    (= (glaze-cost p97) 15)
    (= (grind-cost p97) 30)
    (= (plane-cost p97) 20)
    (unused p98)
    (goalsize p98 large)
    (= (spray-varnish-cost p98) 15)
    (= (glaze-cost p98) 20)
    (= (grind-cost p98) 45)
    (= (plane-cost p98) 30)
    (boardsize b0 s8)
    (wood b0 cherry)
    (surface-condition b0 rough)
    (available b0)
    (boardsize b1 s6)
    (wood b1 cherry)
    (surface-condition b1 rough)
    (available b1)
    (boardsize b2 s7)
    (wood b2 cherry)
    (surface-condition b2 rough)
    (available b2)
    (boardsize b3 s7)
    (wood b3 cherry)
    (surface-condition b3 smooth)
    (available b3)
    (boardsize b4 s4)
    (wood b4 cherry)
    (surface-condition b4 rough)
    (available b4)
    (boardsize b5 s10)
    (wood b5 beech)
    (surface-condition b5 rough)
    (available b5)
    (boardsize b6 s10)
    (wood b6 beech)
    (surface-condition b6 rough)
    (available b6)
    (boardsize b7 s8)
    (wood b7 beech)
    (surface-condition b7 smooth)
    (available b7)
    (boardsize b8 s9)
    (wood b8 beech)
    (surface-condition b8 rough)
    (available b8)
    (boardsize b9 s8)
    (wood b9 beech)
    (surface-condition b9 smooth)
    (available b9)
    (boardsize b10 s7)
    (wood b10 beech)
    (surface-condition b10 smooth)
    (available b10)
    (boardsize b11 s10)
    (wood b11 teak)
    (surface-condition b11 rough)
    (available b11)
    (boardsize b12 s9)
    (wood b12 teak)
    (surface-condition b12 rough)
    (available b12)
    (boardsize b13 s7)
    (wood b13 teak)
    (surface-condition b13 rough)
    (available b13)
    (boardsize b14 s9)
    (wood b14 teak)
    (surface-condition b14 rough)
    (available b14)
    (boardsize b15 s9)
    (wood b15 teak)
    (surface-condition b15 rough)
    (available b15)
    (boardsize b16 s9)
    (wood b16 teak)
    (surface-condition b16 smooth)
    (available b16)
    (boardsize b17 s10)
    (wood b17 teak)
    (surface-condition b17 rough)
    (available b17)
    (boardsize b18 s9)
    (wood b18 teak)
    (surface-condition b18 rough)
    (available b18)
    (boardsize b19 s6)
    (wood b19 teak)
    (surface-condition b19 rough)
    (available b19)
    (boardsize b20 s8)
    (wood b20 oak)
    (surface-condition b20 rough)
    (available b20)
    (boardsize b21 s7)
    (wood b21 oak)
    (surface-condition b21 rough)
    (available b21)
    (boardsize b22 s8)
    (wood b22 oak)
    (surface-condition b22 smooth)
    (available b22)
    (boardsize b23 s6)
    (wood b23 oak)
    (surface-condition b23 rough)
    (available b23)
    (boardsize b24 s5)
    (wood b24 oak)
    (surface-condition b24 rough)
    (available b24)
    (boardsize b25 s10)
    (wood b25 mahogany)
    (surface-condition b25 smooth)
    (available b25)
    (boardsize b26 s7)
    (wood b26 mahogany)
    (surface-condition b26 rough)
    (available b26)
    (boardsize b27 s7)
    (wood b27 mahogany)
    (surface-condition b27 smooth)
    (available b27)
    (boardsize b28 s10)
    (wood b28 mahogany)
    (surface-condition b28 rough)
    (available b28)
    (boardsize b29 s9)
    (wood b29 mahogany)
    (surface-condition b29 smooth)
    (available b29)
    (boardsize b30 s3)
    (wood b30 mahogany)
    (surface-condition b30 rough)
    (available b30)
    (boardsize b31 s8)
    (wood b31 pine)
    (surface-condition b31 smooth)
    (available b31)
    (boardsize b32 s10)
    (wood b32 pine)
    (surface-condition b32 rough)
    (available b32)
    (boardsize b33 s10)
    (wood b33 pine)
    (surface-condition b33 rough)
    (available b33)
    (boardsize b34 s9)
    (wood b34 walnut)
    (surface-condition b34 rough)
    (available b34)
    (boardsize b35 s9)
    (wood b35 walnut)
    (surface-condition b35 rough)
    (available b35)
    (boardsize b36 s7)
    (wood b36 walnut)
    (surface-condition b36 rough)
    (available b36)
    (boardsize b37 s10)
    (wood b37 walnut)
    (surface-condition b37 rough)
    (available b37)
    (boardsize b38 s11)
    (wood b38 walnut)
    (surface-condition b38 smooth)
    (available b38)
  )
  (:goal
    (and
    (available p0)
    (wood p0 cherry)
    (surface-condition p0 smooth)
    (treatment p0 varnished)
    (available p1)
    (treatment p1 varnished)
    (colour p1 red)
    (available p2)
    (wood p2 beech)
    (treatment p2 glazed)
    (available p3)
    (wood p3 teak)
    (surface-condition p3 verysmooth)
    (treatment p3 varnished)
    (colour p3 natural)
    (available p4)
    (wood p4 oak)
    (surface-condition p4 smooth)
    (available p5)
    (wood p5 mahogany)
    (surface-condition p5 smooth)
    (treatment p5 glazed)
    (colour p5 black)
    (available p6)
    (wood p6 teak)
    (surface-condition p6 smooth)
    (available p7)
    (wood p7 teak)
    (treatment p7 varnished)
    (available p8)
    (wood p8 oak)
    (surface-condition p8 smooth)
    (colour p8 blue)
    (available p9)
    (wood p9 oak)
    (treatment p9 glazed)
    (colour p9 mauve)
    (available p10)
    (wood p10 pine)
    (treatment p10 glazed)
    (available p11)
    (surface-condition p11 smooth)
    (treatment p11 glazed)
    (available p12)
    (wood p12 beech)
    (treatment p12 glazed)
    (available p13)
    (wood p13 oak)
    (surface-condition p13 verysmooth)
    (treatment p13 glazed)
    (colour p13 blue)
    (available p14)
    (surface-condition p14 verysmooth)
    (treatment p14 glazed)
    (available p15)
    (surface-condition p15 smooth)
    (treatment p15 glazed)
    (colour p15 mauve)
    (available p16)
    (wood p16 teak)
    (surface-condition p16 verysmooth)
    (treatment p16 glazed)
    (colour p16 natural)
    (available p17)
    (surface-condition p17 verysmooth)
    (colour p17 blue)
    (available p18)
    (wood p18 walnut)
    (surface-condition p18 smooth)
    (treatment p18 glazed)
    (colour p18 white)
    (available p19)
    (wood p19 mahogany)
    (colour p19 mauve)
    (available p20)
    (wood p20 oak)
    (colour p20 natural)
    (available p21)
    (treatment p21 varnished)
    (colour p21 black)
    (available p22)
    (treatment p22 varnished)
    (colour p22 red)
    (available p23)
    (wood p23 beech)
    (surface-condition p23 smooth)
    (colour p23 red)
    (available p24)
    (treatment p24 varnished)
    (colour p24 green)
    (available p25)
    (treatment p25 varnished)
    (colour p25 white)
    (available p26)
    (surface-condition p26 smooth)
    (treatment p26 varnished)
    (available p27)
    (treatment p27 glazed)
    (colour p27 green)
    (available p28)
    (wood p28 teak)
    (surface-condition p28 smooth)
    (available p29)
    (surface-condition p29 verysmooth)
    (colour p29 red)
    (available p30)
    (wood p30 beech)
    (surface-condition p30 verysmooth)
    (colour p30 blue)
    (available p31)
    (wood p31 beech)
    (colour p31 green)
    (available p32)
    (surface-condition p32 verysmooth)
    (treatment p32 varnished)
    (colour p32 black)
    (available p33)
    (wood p33 oak)
    (surface-condition p33 verysmooth)
    (treatment p33 glazed)
    (colour p33 green)
    (available p34)
    (wood p34 cherry)
    (surface-condition p34 smooth)
    (treatment p34 glazed)
    (colour p34 mauve)
    (available p35)
    (surface-condition p35 smooth)
    (treatment p35 glazed)
    (available p36)
    (wood p36 mahogany)
    (surface-condition p36 smooth)
    (treatment p36 glazed)
    (colour p36 red)
    (available p37)
    (wood p37 mahogany)
    (surface-condition p37 verysmooth)
    (treatment p37 glazed)
    (colour p37 natural)
    (available p38)
    (surface-condition p38 verysmooth)
    (treatment p38 glazed)
    (colour p38 red)
    (available p39)
    (wood p39 cherry)
    (colour p39 natural)
    (available p40)
    (wood p40 walnut)
    (surface-condition p40 smooth)
    (available p41)
    (surface-condition p41 smooth)
    (treatment p41 glazed)
    (available p42)
    (treatment p42 glazed)
    (colour p42 green)
    (available p43)
    (wood p43 oak)
    (surface-condition p43 smooth)
    (available p44)
    (wood p44 cherry)
    (surface-condition p44 verysmooth)
    (treatment p44 varnished)
    (available p45)
    (wood p45 cherry)
    (surface-condition p45 smooth)
    (treatment p45 glazed)
    (available p46)
    (wood p46 walnut)
    (treatment p46 glazed)
    (available p47)
    (wood p47 pine)
    (colour p47 red)
    (available p48)
    (wood p48 oak)
    (surface-condition p48 verysmooth)
    (treatment p48 varnished)
    (colour p48 blue)
    (available p49)
    (wood p49 mahogany)
    (surface-condition p49 smooth)
    (available p50)
    (treatment p50 glazed)
    (colour p50 mauve)
    (available p51)
    (treatment p51 varnished)
    (colour p51 black)
    (available p52)
    (surface-condition p52 smooth)
    (colour p52 white)
    (available p53)
    (wood p53 cherry)
    (surface-condition p53 verysmooth)
    (treatment p53 glazed)
    (colour p53 black)
    (available p54)
    (wood p54 walnut)
    (surface-condition p54 smooth)
    (available p55)
    (surface-condition p55 verysmooth)
    (colour p55 black)
    (available p56)
    (surface-condition p56 verysmooth)
    (treatment p56 glazed)
    (colour p56 black)
    (available p57)
    (wood p57 walnut)
    (treatment p57 varnished)
    (colour p57 black)
    (available p58)
    (wood p58 walnut)
    (surface-condition p58 verysmooth)
    (available p59)
    (treatment p59 glazed)
    (colour p59 black)
    (available p60)
    (wood p60 teak)
    (surface-condition p60 smooth)
    (colour p60 white)
    (available p61)
    (wood p61 oak)
    (surface-condition p61 verysmooth)
    (treatment p61 glazed)
    (colour p61 white)
    (available p62)
    (wood p62 mahogany)
    (surface-condition p62 verysmooth)
    (available p63)
    (wood p63 oak)
    (treatment p63 glazed)
    (available p64)
    (wood p64 teak)
    (surface-condition p64 smooth)
    (treatment p64 glazed)
    (colour p64 green)
    (available p65)
    (surface-condition p65 verysmooth)
    (treatment p65 glazed)
    (colour p65 black)
    (available p66)
    (treatment p66 varnished)
    (colour p66 red)
    (available p67)
    (wood p67 oak)
    (treatment p67 glazed)
    (available p68)
    (wood p68 walnut)
    (treatment p68 varnished)
    (available p69)
    (wood p69 oak)
    (treatment p69 varnished)
    (available p70)
    (wood p70 cherry)
    (treatment p70 varnished)
    (available p71)
    (wood p71 oak)
    (surface-condition p71 verysmooth)
    (available p72)
    (wood p72 walnut)
    (treatment p72 glazed)
    (available p73)
    (wood p73 oak)
    (treatment p73 varnished)
    (colour p73 white)
    (available p74)
    (surface-condition p74 smooth)
    (treatment p74 glazed)
    (colour p74 mauve)
    (available p75)
    (wood p75 walnut)
    (surface-condition p75 smooth)
    (colour p75 mauve)
    (available p76)
    (wood p76 mahogany)
    (treatment p76 varnished)
    (colour p76 natural)
    (available p77)
    (surface-condition p77 smooth)
    (treatment p77 varnished)
    (available p78)
    (surface-condition p78 verysmooth)
    (treatment p78 glazed)
    (available p79)
    (surface-condition p79 verysmooth)
    (treatment p79 glazed)
    (available p80)
    (surface-condition p80 smooth)
    (colour p80 white)
    (available p81)
    (wood p81 teak)
    (treatment p81 varnished)
    (available p82)
    (wood p82 beech)
    (colour p82 natural)
    (available p83)
    (wood p83 mahogany)
    (treatment p83 varnished)
    (available p84)
    (wood p84 beech)
    (surface-condition p84 smooth)
    (available p85)
    (wood p85 teak)
    (surface-condition p85 verysmooth)
    (treatment p85 glazed)
    (available p86)
    (surface-condition p86 smooth)
    (colour p86 green)
    (available p87)
    (wood p87 beech)
    (surface-condition p87 verysmooth)
    (available p88)
    (wood p88 beech)
    (surface-condition p88 smooth)
    (available p89)
    (wood p89 walnut)
    (colour p89 blue)
    (available p90)
    (surface-condition p90 verysmooth)
    (treatment p90 varnished)
    (available p91)
    (treatment p91 varnished)
    (colour p91 natural)
    (available p92)
    (wood p92 mahogany)
    (colour p92 black)
    (available p93)
    (surface-condition p93 smooth)
    (treatment p93 varnished)
    (colour p93 white)
    (available p94)
    (surface-condition p94 smooth)
    (colour p94 white)
    (available p95)
    (treatment p95 glazed)
    (colour p95 red)
    (available p96)
    (wood p96 beech)
    (colour p96 blue)
    (available p97)
    (treatment p97 varnished)
    (colour p97 mauve)
    (available p98)
    (surface-condition p98 verysmooth)
    (treatment p98 glazed)
    )
  )
  (:metric minimize (total-cost))
)
