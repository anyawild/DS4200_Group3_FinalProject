let data = [
  { industry: 'Cement', emission: 156181.053 },
  { industry: 'Coal', emission: 1741908.666 },
  { industry: 'Flaring', emission: 54122.888 },
  { industry: 'Gas', emission: 924634.226 },
  { industry: 'Land Use Change', emission: 873080.804 },
  { industry: 'Oil', emission: 1606441.254 },
  { industry: 'Other', emission: 38867.2 }
];

// Function to create the graph
function createGraph() {
  let container = document.getElementById('svg-container');

  let width = container.clientWidth;
  let height = 500;
  let margin = { top: 80, bottom: 175, left: 200, right: 50 };

  // clear contents
  let svg = d3.select('#static3');
  svg.selectAll('*').remove();

  svg
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)
    .style('background', 'white');

  // Define scales
  let yScale = d3.scaleLinear()
    .domain([0, 1800000]) // the data range
    .range([height - margin.bottom, margin.top]);

  let xScale = d3.scaleBand()
    .domain(data.map(d => d.industry))
    .range([margin.left, width - margin.right])
    .padding(0.25);

  // Draw axes
  svg.append('g')
    .call(d3.axisLeft(yScale))
    .attr('transform', `translate(${margin.left}, 0)`)
    .attr('color', 'black')
    .selectAll('text')
    .style('font-family', 'monospace')
    .style('fill', 'black')
    .attr('transform', 'scale(1.8)');

  svg.append('g')
    .call(d3.axisBottom(xScale))
    .attr('transform', `translate(0, ${height - margin.bottom})`)
    .attr('color', 'black')
    .selectAll('text')
    .style('font-family', 'monospace')
    .style('text-anchor', 'end')
    .style('fill', 'black')
    .attr('dx', '-.8em')
    .attr('dy', '.15em')
    .attr('transform', 'rotate(-50) scale(1.8)');

  //Draw the labels
  svg.append('text')
    .attr('x', width/2 - 50)
    .attr('y', height - 60)
    .text('Industry')
    .style('font-weight', 'bold')
    .style('text-anchor', 'middle')
    .style('fill', 'black')

  svg.append('text')
    .attr('x', 0 - height/1.75)
    .attr('y', 50)
    .text('Sum of Emissions')
    .style('font-weight', 'bold')
    .attr('transform', 'rotate(-90)')
    .style('fill', 'black')

  svg.append('text')
    .attr('x', width/2)
    .attr('y', 50)
    .text('Sum of Emissions')
    .style('font-weight', 'bold')
    .style('text-anchor', 'middle')
    .style('fill', 'black')
  
  // Draw bars
  let colorScale = d3.scaleOrdinal(d3.schemeTableau10)
    .domain([0, d3.max(data, d => d.emission)]);

  svg.selectAll('rect')
    .data(data)
    .enter()
    .append('rect')
    .attr('x', d => xScale(d.industry))
    .attr('y', d => yScale(d.emission))
    .attr('width', xScale.bandwidth())
    .attr('height', d => height - margin.bottom - yScale(d.emission))
    .attr('fill', d => colorScale(d.emission));
}

createGraph();
window.addEventListener('resize', createGraph);