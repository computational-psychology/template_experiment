background { color rgb <0.27, 0.27,0.27>}

#declare lens=camera{perspective location <0, 16,-50>  look_at <0,0,0>  angle 12};
camera{lens}

light_source{<20, 10, 7>  color rgb <1.00, 1.00, 1.00> area_light 6*x, 6*y, 12, 12}

union{
box{<-2.900000, -1.000000, 1.160000>, <-2.320000, -0.710000, 1.740000> pigment{ color rgb <1.670000, 1.670000, 1.670000> }}// a08 
box{<-2.900000, -1.000000, 1.740000>, <-2.320000, -0.710000, 2.320000> pigment{ color rgb <1.050000, 1.050000, 1.050000> }}// a09 
box{<-2.900000, -1.000000, -2.320000>, <-2.320000, -0.710000, -1.740000> pigment{ color rgb <0.060000, 0.060000, 0.060000> }}// a02 
box{<-2.900000, -1.000000, -1.740000>, <-2.320000, -0.710000, -1.160000> pigment{ color rgb <1.290000, 1.290000, 1.290000> }}// a03 
box{<-2.900000, -1.000000, -2.900000>, <-2.320000, -0.710000, -2.320000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// a01 
box{<-2.900000, -1.000000, 0.000000>, <-2.320000, -0.710000, 0.580000> pigment{ color rgb <0.820000, 0.820000, 0.820000> }}// a06 
box{<-2.900000, -1.000000, 0.580000>, <-2.320000, -0.710000, 1.160000> pigment{ color rgb <2.220000, 2.220000, 2.220000> }}// a07 
box{<-2.900000, -1.000000, -1.160000>, <-2.320000, -0.710000, -0.580000> pigment{ color rgb <0.060000, 0.060000, 0.060000> }}// a04 
box{<-2.900000, -1.000000, -0.580000>, <-2.320000, -0.710000, 0.000000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// a05 
box{<1.740000, -1.000000, -2.320000>, <2.320000, -0.710000, -1.740000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// i02 
box{<1.740000, -1.000000, -1.740000>, <2.320000, -0.710000, -1.160000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// i03 
box{<1.740000, -1.000000, -2.900000>, <2.320000, -0.710000, -2.320000> pigment{ color rgb <0.060000, 0.060000, 0.060000> }}// i01 
box{<1.740000, -1.000000, 0.000000>, <2.320000, -0.710000, 0.580000> pigment{ color rgb <2.220000, 2.220000, 2.220000> }}// i06 
box{<1.740000, -1.000000, 0.580000>, <2.320000, -0.710000, 1.160000> pigment{ color rgb <0.060000, 0.060000, 0.060000> }}// i07 
box{<1.740000, -1.000000, -1.160000>, <2.320000, -0.710000, -0.580000> pigment{ color rgb <1.670000, 1.670000, 1.670000> }}// i04 
box{<1.740000, -1.000000, -0.580000>, <2.320000, -0.710000, 0.000000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// i05 
box{<1.740000, -1.000000, 1.160000>, <2.320000, -0.710000, 1.740000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// i08 
box{<1.740000, -1.000000, 1.740000>, <2.320000, -0.710000, 2.320000> pigment{ color rgb <1.050000, 1.050000, 1.050000> }}// i09 
box{<-0.580000, -1.000000, 2.320000>, <0.000000, -0.710000, 2.900000> pigment{ color rgb <1.050000, 1.050000, 1.050000> }}// e10 
box{<0.580000, -1.000000, 1.160000>, <1.160000, -0.710000, 1.740000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// g08 
box{<0.580000, -1.000000, 1.740000>, <1.160000, -0.710000, 2.320000> pigment{ color rgb <1.050000, 1.050000, 1.050000> }}// g09 
box{<0.580000, -1.000000, -1.160000>, <1.160000, -0.710000, -0.580000> pigment{ color rgb <0.630000, 0.630000, 0.630000> }}// g04 
box{<0.580000, -1.000000, -0.580000>, <1.160000, -0.710000, 0.000000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// g05 
box{<0.580000, -1.000000, 0.000000>, <1.160000, -0.710000, 0.580000> pigment{ color rgb <0.630000, 0.630000, 0.630000> }}// g06 
box{<0.580000, -1.000000, 0.580000>, <1.160000, -0.710000, 1.160000> pigment{ color rgb <1.290000, 1.290000, 1.290000> }}// g07 
box{<0.580000, -1.000000, -2.900000>, <1.160000, -0.710000, -2.320000> pigment{ color rgb <1.050000, 1.050000, 1.050000> }}// g01 
box{<0.580000, -1.000000, -2.320000>, <1.160000, -0.710000, -1.740000> pigment{ color rgb <0.820000, 0.820000, 0.820000> }}// g02 
box{<0.580000, -1.000000, -1.740000>, <1.160000, -0.710000, -1.160000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// g03 
box{<-1.160000, -1.000000, -1.160000>, <-0.580000, -0.710000, -0.580000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// d04 
box{<-0.580000, -1.000000, 1.160000>, <0.000000, -0.710000, 1.740000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// e08 
box{<-0.580000, -1.000000, 1.740000>, <0.000000, -0.710000, 2.320000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// e09 
box{<-0.580000, -1.000000, 0.000000>, <0.000000, -0.710000, 0.580000> pigment{ color rgb <1.670000, 1.670000, 1.670000> }}// e06 
box{<-0.580000, -1.000000, 0.580000>, <0.000000, -0.710000, 1.160000> pigment{ color rgb <1.050000, 1.050000, 1.050000> }}// e07 
box{<-0.580000, -1.000000, -1.160000>, <0.000000, -0.710000, -0.580000> pigment{ color rgb <1.670000, 1.670000, 1.670000> }}// e04 
box{<-0.580000, -1.000000, -0.580000>, <0.000000, -0.710000, 0.000000> pigment{ color rgb <0.820000, 0.820000, 0.820000> }}// e05 
box{<-0.580000, -1.000000, -2.320000>, <0.000000, -0.710000, -1.740000> pigment{ color rgb <2.220000, 2.220000, 2.220000> }}// e02 
box{<-0.580000, -1.000000, -1.740000>, <0.000000, -0.710000, -1.160000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// e03 
box{<-0.580000, -1.000000, -2.900000>, <0.000000, -0.710000, -2.320000> pigment{ color rgb <0.310000, 0.310000, 0.310000> }}// e01 
box{<-1.740000, -1.000000, 1.160000>, <-1.160000, -0.710000, 1.740000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// c08 
box{<-1.740000, -1.000000, 1.740000>, <-1.160000, -0.710000, 2.320000> pigment{ color rgb <1.950000, 1.950000, 1.950000> }}// c09 
box{<-1.740000, -1.000000, -2.900000>, <-1.160000, -0.710000, -2.320000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// c01 
box{<-1.740000, -1.000000, -2.320000>, <-1.160000, -0.710000, -1.740000> pigment{ color rgb <2.220000, 2.220000, 2.220000> }}// c02 
box{<-1.740000, -1.000000, -1.740000>, <-1.160000, -0.710000, -1.160000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// c03 
box{<-1.740000, -1.000000, -1.160000>, <-1.160000, -0.710000, -0.580000> pigment{ color rgb <0.820000, 0.820000, 0.820000> }}// c04 
box{<-1.740000, -1.000000, -0.580000>, <-1.160000, -0.710000, 0.000000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// c05 
box{<-1.740000, -1.000000, 0.000000>, <-1.160000, -0.710000, 0.580000> pigment{ color rgb <1.950000, 1.950000, 1.950000> }}// c06 
box{<-1.740000, -1.000000, 0.580000>, <-1.160000, -0.710000, 1.160000> pigment{ color rgb <1.290000, 1.290000, 1.290000> }}// c07 
box{<2.320000, -1.000000, 1.740000>, <2.900000, -0.710000, 2.320000> pigment{ color rgb <1.670000, 1.670000, 1.670000> }}// j09 
box{<2.320000, -1.000000, 1.160000>, <2.900000, -0.710000, 1.740000> pigment{ color rgb <1.290000, 1.290000, 1.290000> }}// j08 
box{<2.320000, -1.000000, -2.900000>, <2.900000, -0.710000, -2.320000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// j01 
box{<2.320000, -1.000000, -1.740000>, <2.900000, -0.710000, -1.160000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// j03 
box{<2.320000, -1.000000, -2.320000>, <2.900000, -0.710000, -1.740000> pigment{ color rgb <1.670000, 1.670000, 1.670000> }}// j02 
box{<2.320000, -1.000000, -0.580000>, <2.900000, -0.710000, 0.000000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// j05 
box{<2.320000, -1.000000, -1.160000>, <2.900000, -0.710000, -0.580000> pigment{ color rgb <0.310000, 0.310000, 0.310000> }}// j04 
box{<2.320000, -1.000000, 0.580000>, <2.900000, -0.710000, 1.160000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// j07 
box{<2.320000, -1.000000, 0.000000>, <2.900000, -0.710000, 0.580000> pigment{ color rgb <0.630000, 0.630000, 0.630000> }}// j06 
box{<1.160000, -1.000000, 1.740000>, <1.740000, -0.710000, 2.320000> pigment{ color rgb <2.220000, 2.220000, 2.220000> }}// h09 
box{<1.160000, -1.000000, 1.160000>, <1.740000, -0.710000, 1.740000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// h08 
box{<1.160000, -1.000000, -1.740000>, <1.740000, -0.710000, -1.160000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// h03 
box{<1.160000, -1.000000, -2.320000>, <1.740000, -0.710000, -1.740000> pigment{ color rgb <1.290000, 1.290000, 1.290000> }}// h02 
box{<1.160000, -1.000000, -2.900000>, <1.740000, -0.710000, -2.320000> pigment{ color rgb <2.220000, 2.220000, 2.220000> }}// h01 
box{<1.160000, -1.000000, 0.580000>, <1.740000, -0.710000, 1.160000> pigment{ color rgb <0.820000, 0.820000, 0.820000> }}// h07 
box{<1.160000, -1.000000, 0.000000>, <1.740000, -0.710000, 0.580000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// h06 
box{<1.160000, -1.000000, -0.580000>, <1.740000, -0.710000, 0.000000> pigment{ color rgb <0.630000, 0.630000, 0.630000> }}// h05 
box{<1.160000, -1.000000, -1.160000>, <1.740000, -0.710000, -0.580000> pigment{ color rgb <0.310000, 0.310000, 0.310000> }}// h04 
box{<0.000000, -1.000000, -0.580000>, <0.580000, -0.710000, 0.000000> pigment{ color rgb <1.050000, 1.050000, 1.050000> }}// f05 
box{<0.000000, -1.000000, -1.160000>, <0.580000, -0.710000, -0.580000> pigment{ color rgb <0.310000, 0.310000, 0.310000> }}// f04 
box{<0.000000, -1.000000, 0.580000>, <0.580000, -0.710000, 1.160000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// f07 
box{<0.000000, -1.000000, 0.000000>, <0.580000, -0.710000, 0.580000> pigment{ color rgb <0.060000, 0.060000, 0.060000> }}// f06 
box{<0.000000, -1.000000, -2.900000>, <0.580000, -0.710000, -2.320000> pigment{ color rgb <0.820000, 0.820000, 0.820000> }}// f01 
box{<0.000000, -1.000000, -1.740000>, <0.580000, -0.710000, -1.160000> pigment{ color rgb <1.670000, 1.670000, 1.670000> }}// f03 
box{<0.000000, -1.000000, -2.320000>, <0.580000, -0.710000, -1.740000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// f02 
box{<0.000000, -1.000000, 1.740000>, <0.580000, -0.710000, 2.320000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// f09 
box{<0.000000, -1.000000, 1.160000>, <0.580000, -0.710000, 1.740000> pigment{ color rgb <1.950000, 1.950000, 1.950000> }}// f08 
box{<2.320000, -1.000000, 2.320000>, <2.900000, -0.710000, 2.900000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// j10 
box{<-1.160000, -1.000000, 0.580000>, <-0.580000, -0.710000, 1.160000> pigment{ color rgb <0.310000, 0.310000, 0.310000> }}// d07 
box{<-1.160000, -1.000000, 0.000000>, <-0.580000, -0.710000, 0.580000> pigment{ color rgb <0.060000, 0.060000, 0.060000> }}// d06 
box{<-1.160000, -1.000000, -0.580000>, <-0.580000, -0.710000, 0.000000> pigment{ color rgb <1.950000, 1.950000, 1.950000> }}// d05 
box{<-1.740000, -1.000000, 2.320000>, <-1.160000, -0.710000, 2.900000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// c10 
box{<-1.160000, -1.000000, -1.740000>, <-0.580000, -0.710000, -1.160000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// d03 
box{<-1.160000, -1.000000, -2.320000>, <-0.580000, -0.710000, -1.740000> pigment{ color rgb <0.460000, 0.460000, 0.460000> }}// d02 
box{<-1.160000, -1.000000, -2.900000>, <-0.580000, -0.710000, -2.320000> pigment{ color rgb <1.290000, 1.290000, 1.290000> }}// d01 
box{<1.160000, -1.000000, 2.320000>, <1.740000, -0.710000, 2.900000> pigment{ color rgb <0.060000, 0.060000, 0.060000> }}// h10 
box{<-1.160000, -1.000000, 1.740000>, <-0.580000, -0.710000, 2.320000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// d09 
box{<-1.160000, -1.000000, 1.160000>, <-0.580000, -0.710000, 1.740000> pigment{ color rgb <0.630000, 0.630000, 0.630000> }}// d08 
box{<-2.320000, -1.000000, -2.900000>, <-1.740000, -0.710000, -2.320000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// b01 
box{<-2.320000, -1.000000, -1.740000>, <-1.740000, -0.710000, -1.160000> pigment{ color rgb <1.670000, 1.670000, 1.670000> }}// b03 
box{<-2.320000, -1.000000, -2.320000>, <-1.740000, -0.710000, -1.740000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// b02 
box{<-2.320000, -1.000000, -0.580000>, <-1.740000, -0.710000, 0.000000> pigment{ color rgb <2.220000, 2.220000, 2.220000> }}// b05 
box{<-2.320000, -1.000000, -1.160000>, <-1.740000, -0.710000, -0.580000> pigment{ color rgb <1.290000, 1.290000, 1.290000> }}// b04 
box{<-2.320000, -1.000000, 0.580000>, <-1.740000, -0.710000, 1.160000> pigment{ color rgb <0.060000, 0.060000, 0.060000> }}// b07 
box{<-2.320000, -1.000000, 0.000000>, <-1.740000, -0.710000, 0.580000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// b06 
box{<-2.320000, -1.000000, 1.740000>, <-1.740000, -0.710000, 2.320000> pigment{ color rgb <0.190000, 0.190000, 0.190000> }}// b09 
box{<-2.320000, -1.000000, 1.160000>, <-1.740000, -0.710000, 1.740000> pigment{ color rgb <0.820000, 0.820000, 0.820000> }}// b08 
box{<0.000000, -1.000000, 2.320000>, <0.580000, -0.710000, 2.900000> pigment{ color rgb <1.500000, 1.500000, 1.500000> }}// f10 
box{<-1.160000, -1.000000, 2.320000>, <-0.580000, -0.710000, 2.900000> pigment{ color rgb <1.290000, 1.290000, 1.290000> }}// d10 
box{<-2.320000, -1.000000, 2.320000>, <-1.740000, -0.710000, 2.900000> pigment{ color rgb <0.820000, 0.820000, 0.820000> }}// b10 
box{<-2.900000, -1.000000, 2.320000>, <-2.320000, -0.710000, 2.900000> pigment{ color rgb <2.220000, 2.220000, 2.220000> }}// a10 
box{<1.740000, -1.000000, 2.320000>, <2.320000, -0.710000, 2.900000> pigment{ color rgb <0.110000, 0.110000, 0.110000> }}// i10 
box{<0.580000, -1.000000, 2.320000>, <1.160000, -0.710000, 2.900000> pigment{ color rgb <1.950000, 1.950000, 1.950000> }}// g10 
rotate y * 45}

#declare tex =  pigment{ wood color_map { [0 rgb <.5,.5,.5>][1 rgb <.3,.3,.3>] } turbulence .5  scale <1, 1, 20>*.01 }
polygon{4, <-5, 0, 4> <5, 0, 4> <5, 0, -7.5> <-5, 0, -7.5>
pigment{tex} scale <2, 2, 2> translate<1, -1, 0>}

