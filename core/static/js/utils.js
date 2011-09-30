function makeSegments(min, max, numSegments) {
    var segmentSize = (max - min) / numSegments;
    var segmentMin = min;
    var segments = Array();

    for (i = 1; i <= numSegments; i++) {
        var segmentMax = segmentMin + segmentSize;
        segments.push([segmentMin, segmentMax]);
        segmentMin = segmentMax;

    }
    return segments;
}

