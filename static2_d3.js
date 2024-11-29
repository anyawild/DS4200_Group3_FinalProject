//Define data
let data = [
  {industry: 'Cement', emission: 156181.053},
  {industry: 'Coal', emission: 1741908.6660000002},
  {industry: 'Flaring', emission: 54122.888},
  {industry: 'Gas', emission: 924634.226},
  {industry: 'Land Use Change', emission: 873080.804},
  {industry: 'Oil', emission: 1606441.2540000002},
  {industry: 'Other', emission: 38867.2}
];

let 
  width = 600,
  height = 500;

let margin = {
  top:30,
  bottom: 130,
  left: 120,
  right:30
}

// Make a canvas for the picture
let svg = d3.select('#static2')
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .style('background', 'var(--col1)')

// Define the scale
let yScale = d3.scaleLinear() // for the continous data
              .domain([0,1800000]) //the data
              .range([height - margin.bottom, margin.top])

let xScale = d3.scaleBand()
              .domain(data.map(d => d.industry))
              .range([margin.left, width - margin.right])
              .padding(0.25);

// Draw the axis
let yAxis = svg.append('g')
            .call(d3.axisLeft().scale(yScale))
            .attr('transform', `translate(${margin.left},0)`)
            .attr('color', 'var(--col2)')
            .selectAll('text')
            .style('fill', 'var(--col2)')
            .attr("transform", "scale(1.3)");

let xAxis  = svg.append('g')
            .call(d3.axisBottom().scale(xScale))
            .attr('transform', `translate(0,${height-margin.bottom})`)
            .attr('color', 'var(--col2)')
            .selectAll("text")  
            .style("text-anchor", "end")
            .style('fill', 'var(--col2)')
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-65) scale(1.3)");

//Draw the labels
svg.append('text')
  .attr('x', width/2)
  .attr('y', height - 50)
  .text('Industry')
  .style('text-anchor', 'middle')
  .style('fill', 'var(--col2)')

svg.append('text')
  .attr('x', 0 - height/2)
  .attr('y', 25)
  .text('Sum of Emissions')
  .attr('transform', 'rotate(-90)')
  .style('fill', 'var(--col2)')

//Draw the bars
bar = svg.selectAll('rect')
      .data(data)
      .enter()
      .append('rect')
      .attr('x', d => xScale(d.industry))
      .attr('y', d => yScale(d.emission))
      .attr('width', xScale.bandwidth())
      .attr('height', d => height - margin.bottom - yScale(d.emission))
      .attr('fill', 'var(--col2)'
)

