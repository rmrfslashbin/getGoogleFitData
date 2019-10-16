#!/usr/bin/env node

var fs = require('fs');
var obj = JSON.parse(fs.readFileSync('heart-bpm.json', 'utf8'));

let i;
let points = [];

for (i of obj.point) {
    points.push({
        x: i.startTimeNanos / 1000000,
        y: i.value[0].fpVal
    })
}

fs.writeFile('./data.json', JSON.stringify(points), err => {
    if (err) {
        console.log('Error writing file', err)
    } else {
        console.log('Successfully wrote file')
    }
})
