(define (problem ZTRAVEL-28-42)
(:domain zeno-travel)
(:objects
	plane1 - aircraft
	plane2 - aircraft
	plane3 - aircraft
	plane4 - aircraft
	plane5 - aircraft
	plane6 - aircraft
	plane7 - aircraft
	plane8 - aircraft
	plane9 - aircraft
	plane10 - aircraft
	plane11 - aircraft
	plane12 - aircraft
	plane13 - aircraft
	plane14 - aircraft
	plane15 - aircraft
	plane16 - aircraft
	plane17 - aircraft
	plane18 - aircraft
	plane19 - aircraft
	plane20 - aircraft
	plane21 - aircraft
	plane22 - aircraft
	plane23 - aircraft
	plane24 - aircraft
	plane25 - aircraft
	plane26 - aircraft
	plane27 - aircraft
	plane28 - aircraft
	person1 - person
	person2 - person
	person3 - person
	person4 - person
	person5 - person
	person6 - person
	person7 - person
	person8 - person
	person9 - person
	person10 - person
	person11 - person
	person12 - person
	person13 - person
	person14 - person
	person15 - person
	person16 - person
	person17 - person
	person18 - person
	person19 - person
	person20 - person
	person21 - person
	person22 - person
	person23 - person
	person24 - person
	person25 - person
	person26 - person
	person27 - person
	person28 - person
	person29 - person
	person30 - person
	person31 - person
	person32 - person
	person33 - person
	person34 - person
	person35 - person
	person36 - person
	person37 - person
	person38 - person
	person39 - person
	person40 - person
	person41 - person
	person42 - person
	city0 - city
	city1 - city
	city2 - city
	city3 - city
	city4 - city
	city5 - city
	city6 - city
	city7 - city
	city8 - city
	city9 - city
	city10 - city
	city11 - city
	city12 - city
	city13 - city
	city14 - city
	city15 - city
	city16 - city
	city17 - city
	city18 - city
	city19 - city
	city20 - city
	city21 - city
	city22 - city
	city23 - city
	city24 - city
	city25 - city
	city26 - city
	city27 - city
	city28 - city
	city29 - city
	city30 - city
	city31 - city
	city32 - city
	city33 - city
	city34 - city
	city35 - city
	city36 - city
	city37 - city
	city38 - city
	city39 - city
	city40 - city
	city41 - city
	city42 - city
	city43 - city
	city44 - city
	city45 - city
	city46 - city
	city47 - city
	city48 - city
	city49 - city
	city50 - city
	city51 - city
	city52 - city
	city53 - city
	city54 - city
	city55 - city
	city56 - city
	city57 - city
	city58 - city
	city59 - city
	city60 - city
	city61 - city
	city62 - city
	city63 - city
	city64 - city
	city65 - city
	city66 - city
	city67 - city
	city68 - city
	city69 - city
	city70 - city
	city71 - city
	city72 - city
	city73 - city
	city74 - city
	city75 - city
	city76 - city
	city77 - city
	city78 - city
	city79 - city
	city80 - city
	city81 - city
	city82 - city
	city83 - city
	city84 - city
	city85 - city
	city86 - city
	city87 - city
	city88 - city
	city89 - city
	city90 - city
	city91 - city
	city92 - city
	city93 - city
	city94 - city
	city95 - city
	city96 - city
	city97 - city
	city98 - city
	city99 - city
	city100 - city
	city101 - city
	city102 - city
	city103 - city
	city104 - city
	city105 - city
	city106 - city
	city107 - city
	city108 - city
	city109 - city
	city110 - city
	city111 - city
	city112 - city
	city113 - city
	fl0 - flevel
	fl1 - flevel
	fl2 - flevel
	fl3 - flevel
	fl4 - flevel
	fl5 - flevel
	fl6 - flevel
	)
(:init
	(at plane1 city88)
	(fuel-level plane1 fl0)
	(at plane2 city76)
	(fuel-level plane2 fl0)
	(at plane3 city101)
	(fuel-level plane3 fl0)
	(at plane4 city60)
	(fuel-level plane4 fl0)
	(at plane5 city11)
	(fuel-level plane5 fl0)
	(at plane6 city1)
	(fuel-level plane6 fl0)
	(at plane7 city23)
	(fuel-level plane7 fl0)
	(at plane8 city103)
	(fuel-level plane8 fl0)
	(at plane9 city57)
	(fuel-level plane9 fl0)
	(at plane10 city12)
	(fuel-level plane10 fl0)
	(at plane11 city30)
	(fuel-level plane11 fl0)
	(at plane12 city104)
	(fuel-level plane12 fl0)
	(at plane13 city110)
	(fuel-level plane13 fl0)
	(at plane14 city26)
	(fuel-level plane14 fl0)
	(at plane15 city62)
	(fuel-level plane15 fl0)
	(at plane16 city4)
	(fuel-level plane16 fl0)
	(at plane17 city61)
	(fuel-level plane17 fl0)
	(at plane18 city84)
	(fuel-level plane18 fl0)
	(at plane19 city63)
	(fuel-level plane19 fl0)
	(at plane20 city22)
	(fuel-level plane20 fl0)
	(at plane21 city75)
	(fuel-level plane21 fl0)
	(at plane22 city32)
	(fuel-level plane22 fl0)
	(at plane23 city51)
	(fuel-level plane23 fl0)
	(at plane24 city84)
	(fuel-level plane24 fl0)
	(at plane25 city90)
	(fuel-level plane25 fl0)
	(at plane26 city32)
	(fuel-level plane26 fl0)
	(at plane27 city105)
	(fuel-level plane27 fl0)
	(at plane28 city35)
	(fuel-level plane28 fl0)
	(at person1 city57)
	(at person2 city59)
	(at person3 city74)
	(at person4 city66)
	(at person5 city19)
	(at person6 city71)
	(at person7 city100)
	(at person8 city34)
	(at person9 city14)
	(at person10 city93)
	(at person11 city18)
	(at person12 city27)
	(at person13 city91)
	(at person14 city91)
	(at person15 city86)
	(at person16 city33)
	(at person17 city13)
	(at person18 city28)
	(at person19 city98)
	(at person20 city96)
	(at person21 city56)
	(at person22 city86)
	(at person23 city10)
	(at person24 city78)
	(at person25 city105)
	(at person26 city44)
	(at person27 city25)
	(at person28 city66)
	(at person29 city67)
	(at person30 city43)
	(at person31 city7)
	(at person32 city18)
	(at person33 city21)
	(at person34 city89)
	(at person35 city62)
	(at person36 city73)
	(at person37 city81)
	(at person38 city70)
	(at person39 city76)
	(at person40 city113)
	(at person41 city46)
	(at person42 city8)
	(next fl0 fl1)
	(next fl1 fl2)
	(next fl2 fl3)
	(next fl3 fl4)
	(next fl4 fl5)
	(next fl5 fl6)
)
(:goal (and
	(at plane1 city66)
	(at plane7 city40)
	(at plane13 city67)
	(at plane14 city12)
	(at plane15 city90)
	(at plane17 city50)
	(at plane19 city35)
	(at plane20 city68)
	(at plane22 city8)
	(at plane24 city109)
	(at plane25 city5)
	(at person1 city69)
	(at person2 city8)
	(at person4 city72)
	(at person5 city27)
	(at person6 city41)
	(at person7 city60)
	(at person8 city73)
	(at person9 city89)
	(at person10 city102)
	(at person11 city46)
	(at person12 city105)
	(at person13 city66)
	(at person14 city18)
	(at person15 city38)
	(at person16 city109)
	(at person17 city96)
	(at person19 city31)
	(at person20 city10)
	(at person21 city28)
	(at person23 city33)
	(at person24 city11)
	(at person25 city97)
	(at person26 city17)
	(at person27 city30)
	(at person28 city58)
	(at person29 city43)
	(at person30 city26)
	(at person31 city82)
	(at person32 city55)
	(at person33 city65)
	(at person34 city30)
	(at person35 city21)
	(at person36 city66)
	(at person37 city91)
	(at person38 city44)
	(at person39 city112)
	(at person40 city42)
	(at person41 city49)
	(at person42 city68)
	))

)
