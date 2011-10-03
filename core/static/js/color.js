var Color = Class.extend({
    init: function(red, green, blue, opacity) {
        this.red = red;
        this.green = green;
        this.blue = blue;
        this.opacity = opacity;
    },
    paddedHex: function(i, numDigits) {
        iHex = i.toString(16);
        while (iHex.length < numDigits) {
            iHex = "0" + iHex;
        }
        return iHex;
    },
    toRgb:  function() {
        return 'rgb(' + this.red + ',' + this.green + ',' + this.blue + ')'; 
    },
   toRgba: function() {
        return 'rgba(' + this.red + ',' + this.green + ',' + this.blue +
               ',' + this.opacity + ')'; 
    },
    toHex: function() {
        return '#' + paddedHex(this.red, 2) + paddedHex(this.green, 2) + paddedHex(this.blue, 2);
    },
    clone: function() {
        return new Color(this.red, this.green, this.blue, this.opacity);
    }
});
