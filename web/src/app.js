// Local SCSS styles
import styles from "./styles/styles.scss";

// https://www.npmjs.com/package/d3
import * as d3 from "d3";

// https://github.com/doowb/sma
//import * as sma from "sma"

// Use Material Design typography
// https://material.io/develop/web/components/typography/
//body.addClass("mdc-typography");

async function getData() {
    let response = await fetch("data.json");
    return await response.json();
}

getData().then(data => {
    let dataset = [];
    let i;
    let minValue = 500;
    let maxValue = 0;
    let minDate = 9999999999999;
    let maxDate = 0;

    console.log(data)
    for (i of data.sma.points) {
        dataset.push({
            date: new Date(i.timestamp),
            value: i.value
        });

        if (i.value > maxValue) {
            maxValue = i.value;
        }

        if (i.value < minValue) {
            minValue = i.value;
        }

        if (i.timestamp > maxDate) {
            maxDate = i.timestamp;
        }

        if (i.timestamp < minDate) {
            minDate = i.timestamp;
        }
    }

    
    maxValue = maxValue + 10;
    minValue = minValue - 10;
    console.log(`min value: ${minValue}`);
    console.log(`max value: ${maxValue}`);
    console.log(`min date: ${new Date(minDate).toISOString()}`);
    console.log(`max date: ${new Date(maxDate).toISOString()}`);

    //https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89

    // 2. Use the margin convention practice 
    let margin = {top: 50, right: 50, bottom: 50, left: 50};
    let width = window.innerWidth - margin.left - margin.right; // Use the window's width 
    let height = window.innerHeight - margin.top - margin.bottom; // Use the window's height

    // The number of datapoints
    let n = dataset.length

    var xScale = d3.scaleTime()
        .domain([new Date(minDate), new Date(maxDate)])
        .range([0, width]);

    let yScale = d3.scaleLinear()
        .domain([minValue, maxValue])
        .range([height, 0]);


    // 7. d3's line generator
    let line = d3.line()
        //.x((d, i) => { return xScale(d.x); }) // set the x values for the line generator
        //.y((d) => { return yScale(d.y); }) // set the y values for the line generator 
        .x( d => xScale(d.date))
        .y( d => yScale(d.value))
        .curve(d3.curveMonotoneX) // apply smoothing to the line

    // 8. An array of objects of length N. Each object has key -> value pair, the key being "y" and the value is a random number
    //dataset = d3.range(n).map(function(d) { return {"y": d3.randomUniform(1)() } })
    
    // 1. Add the SVG to the page and employ #2
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // 3. Call the x axis in a group tag
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

    // 4. Call the y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

    // 9. Append the path, bind the data, and call the line generator 
    svg.append("path")
        .datum(dataset) // 10. Binds data to the line 
        .attr("class", "line") // Assign a class for styling 
        .attr("d", line); // 11. Calls the line generator 

    let focus = svg.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("line")
        .attr("class", "x-hover-line hover-line")
        .attr("y1", 0)
        .attr("y2", height);

    focus.append("line")
        .attr("class", "y-hover-line hover-line")
        .attr("x1", width)
        .attr("x2", width);

    focus.append("circle")
        .attr("r", 7.5);

    focus.append("text")
        .attr("x", 15)
        .attr("dy", ".31em");

    svg.append("rect")
        .attr("transform", `translate(${margin.left},${margin.top})`)
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height)
        .on("mouseover", () => { focus.style("display", null); })
        .on("mouseout", () => { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    let bisectDate = d3.bisector( d => d.date ).left;

    svg.append("path") // this is the black vertical line to follow mouse
        .attr("class","mouseLine")  
        .style("stroke","black")
        .style("stroke-width", "1px")
        .style("opacity", "0");

    function mousemove() {
        let x0 = xScale.invert(d3.mouse(this)[0]);
        let i = bisectDate(dataset, x0, 1);

        let d0 = dataset[i - 1];
        let d1 = dataset[i];
        let d = x0 - d0.date > d1.date - x0 ? d1 : d0;

        focus.attr("transform", `translate(${xScale(d.date)},${yScale(d.value)})`);
        focus.select("text").text( () => { 
            let dateStr = d.date.toLocaleDateString(
                navigator.language, 
                {
                    hourCycle: "h24",
                    weekday: "short",
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit"
                })
            return `${dateStr} - ${d.value} bpm`;
        });
        
        focus.select(".x-hover-line").attr("y2", height - yScale(d.value));
        focus.select(".y-hover-line").attr("x2", width + width);
    }


})