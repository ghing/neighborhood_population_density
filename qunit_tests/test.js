function compareSegmentArrays(ary1, ary2) {
    if (ary1.length == ary2.length) {
        for (i = 0; i < ary1.length; i++) {
            if (ary1[i][0] != ary2[i][0] || ary1[i][1] != ary2[i][1]) {
                return false;
            }
        }
        return true;
    }
    else {
        return false;
    }
}

test('Test makeSegments() with 1 segment', function() {
    segments = makeSegments(0, 1, 1);
    ok(compareSegmentArrays(segments, [[0, 1]]));
});

test('Test makeSegments() with 2 segment', function() {
    segments = makeSegments(0, 2, 2);
    ok(compareSegmentArrays(segments, [[0, 1], [1, 2]]));
});

test('Test makeSegments() with 3 segment', function() {
    segments = makeSegments(0, 3, 3);
    ok(compareSegmentArrays(segments, [[0, 1], [1, 2], [2, 3]]));
});
