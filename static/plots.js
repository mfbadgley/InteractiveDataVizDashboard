


// grab the element by ID you want to append to.
var select = document.getElementById("selDataset"); 
var options ="/names";
//get the data from the endpoint, in json form..
Plotly.d3.json(options, function(error, response){
    //store respone in a variable
      var results = response;
      //log the response in the console for debugging
      console.log(results);

 //add first item to list of dropdown to be "select", forcing a selection of actual data item
  d3.select("#selDataset").append("option").attr("value", "Select").text("Select")
  // Loop through results/response
      for (var i = 0; i < results.length; i++) {
      
      // append an option element vith attribute value equal to the result, and text equal to the result
          var gifDiv = d3.select("#selDataset").append("option")
          .attr("value", results[i]).text(results[i]);
        }
    });

//grab the selected item from the dropdown
function getData(dataset){
    //clear variable
    var x =""
    //initialize x as the value selected by user
    var x = document.getElementById("selDataset").value;
    //if user selects, 'select', throw error
    if (x === "Select"){
        window.alert("Please choose valid entry");
    }
    //otherwise console log user selection 
    else
    console.log(x);
   //and if it is not 'Select' 
    if (x!="Select"){
        //initialize variable as desired endpoint, plus user selection
        var newdata=`/metadata/${x}`;
        //go out and access the endpoint
        Plotly.d3.json(newdata, function(error, response){
            //store respone in a variable
              var results = response;
              //log the response in the console for debugging
              console.log(results);
       
            //access the data from the results, which is a dictionary..
            d3.select("#table").html(null);//clear the previous data
            d3.select("#table").append("p").text("AGE: " + results.AGE);
            d3.select("#table").append("p").text("BBTYPE: " + results.BBTYPE);
            d3.select("#table").append("p").text("ETHNICITY: " + results.ETHNICITY);
            d3.select("#table").append("p").text("GENDER: " + results.GENDER);
            d3.select("#table").append("p").text("LOCATION: " + results.LOCATION);

            function buildPlot() {
        
                /* data route */
                var url = `/samples/${x}`;//user input goes here

                Plotly.d3.json(url, function (error, response) {//return the json
                    
                    console.log("response:", response);
                   
                    var data = response[0].sample_values;//data comes in as an array of arrays, so we access the first array, .sample_values;
                    console.log("data:", data);
                    var labels = response[0].otu_ids;//access the sample labels(otu_ids) 
                    console.log("labels:", labels)
            
                    var trace1 = {
                    labels: labels.slice(0,10),//take the first 10
                       values: data.slice(0,10),
                       type: 'pie',
                      
                       };
                    
                       var layout = {
                        margin: {t:0, l:0}
                       };

                     var chartData = [trace1];
                   
        
                Plotly.newPlot("pie", chartData, layout);
            });
        }
        
        buildPlot();

    }); 

    var wfreq=`/wfreq/${x}`;
        //go out and access the endpoint
        Plotly.d3.json(wfreq, function(error, response){
            //store respone in a variable
              var results = response;
              //log the response in the console for debugging
              console.log("wfreq:", results);

    // Enter a speed between 0 and 180
    var level = results;

    // Trig to calc meter point
    var degrees = 180 - level*21,
     radius = .5;
    var radians = degrees * Math.PI / 180;
    var x = radius * Math.cos(radians);
    var y = radius * Math.sin(radians);

    // Path: may have to change to create a better triangle
    var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
     pathX = String(x),
     space = ' ',
     pathY = String(y),
     pathEnd = ' Z';
    var path = mainPath.concat(pathX,space,pathY,pathEnd);

    var data = [{ type: 'scatter',
   x: [0], y:[0],
    marker: {size: 5, color:'850000'},
    showlegend: false,
    name: 'Freq',
    text: level,
    hoverinfo: 'text+name'},
  { values: [50/9,50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50/9, 50],
  rotation: 90,
  text: ['8-9','7-8','6-7', '5-6', '4-5', '3-4', '2-3',
            '1-2', '0-1', ''],
  textinfo: 'text',
  textposition:'inside',
  marker: {colors:['rgba(14, 127, 0, .5)', 'rgba(110, 154, 22, .5)',
                         'rgba(170, 202, 42, .5)', 'rgba(202, 209, 95, .5)',
                         'rgba(210, 206, 145, .5)', 'rgba(232, 226, 202, .5)',
                         'rgba(255, 255, 255, 0)']},
  labels: ['8-9','7-8','6-7','5-6', '4-5', '3-4', '2-3', '1-2', '0-1', ''],
  hoverinfo: 'label',
  hole: .5,
  type: 'pie',
  showlegend: false
}];

var layout = {
  shapes:[{
      type: 'path',
      path: path,
      fillcolor: '850000',
      line: {
        color: '850000'
      }
    }],
  //title: 'Wash Frequency',
    
  height: 500,
  width: 500,
  margin: {t:0},
  xaxis: {zeroline:false, showticklabels:false,
             showgrid: false, range: [-1, 1]},
  yaxis: {zeroline:false, showticklabels:false,
             showgrid: false, range: [-1, 1]}
};

Plotly.newPlot('gauge', data, layout);
              
          })
        };

    }