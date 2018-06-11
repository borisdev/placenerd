/*
 *  -180    0     180
 *    c0 -- c1 -- c2   90
 *    |  A  |  B  |
 *    c3 -- c4 -- c5    0
 *    |  C  |  D  |
 *    c6 -- c7 -- c8  -90
 *
 */

var c0 = new jsts.geom.Coordinate(-180,90),
    c1 = new jsts.geom.Coordinate(0,90),
    c2 = new jsts.geom.Coordinate(180,90),
    c3 = new jsts.geom.Coordinate(-180,0),
    c4 = new jsts.geom.Coordinate(0,0),
    c5 = new jsts.geom.Coordinate(180,0),
    c6 = new jsts.geom.Coordinate(-180,-90),
    c7 = new jsts.geom.Coordinate(0,-90),
    c8 = new jsts.geom.Coordinate(180,-90),
    A = util.geomFactory.createPolygon(util.geomFactory.createLinearRing([c0,c1,c4,c3,c0])),
    B = util.geomFactory.createPolygon(util.geomFactory.createLinearRing([c1,c2,c5,c4,c1])),
    C = util.geomFactory.createPolygon(util.geomFactory.createLinearRing([c3,c4,c7,c6,c3])),
    D = util.geomFactory.createPolygon(util.geomFactory.createLinearRing([c4,c5,c8,c7,c4]));
    
console.info(A.toString());
console.info(B.toString());
console.info(C.toString());
console.info(D.toString());


var world = util.rect(-175,-85, 350, 170);
xrange = _.range(-170,180,10);
yrange = _.range(-80,90,10);
_.each(yrange, function(y) {
	var line = util.geomFactory.createLineString([new jsts.geom.Coordinate(-280, y), new jsts.geom.Coordinate(280, y)]);
	world = world.difference(line.buffer(1));
})
_.each(xrange, function(x) {
	var line = util.geomFactory.createLineString([new jsts.geom.Coordinate(x, -290), new jsts.geom.Coordinate(x, 290)]);
	world = world.difference(line.buffer(1));
})

_.each(world.geometries, function(g){ console.info(g.toString()) });

