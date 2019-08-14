var mem = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]
var cpu = [ 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]

function getsysteminfo(){
  $.ajax({
      type:'GET',
      url:"/API/systeminfo",
      async: false,
      success:function(result){
        //console.log(result);
        if(result.code == 200){
          //console.log(result);
          $("#all_containers").html(result.all_containers);
          $("#images").html(result.images);
          $("#running_containers").html(result.running_containers);
          $("#died_containers").html(result.shutdown_containers);
          $("#died_containers_percent").attr("style","width: "+result.shutdown_containers+"%");
          $("#all_containers_percent").attr("style","width: "+result.all_containers+"%");
          $("#running_containers_percent").attr("style","width: "+result.running_containers+"%");
          $("#images_percent").attr("style","width: "+result.images+"%");
          $("#cpu").html(result.cpu+"<small> %</small>");
          $("#mem").html(result.mem+"<small> %</small>");
          $("#chall_count").html(result.chall_count);
          $("#user_count").html(result.user_count);
          $("#running_dockers").html(result.running_containers);
          showrecords(result.solverecords);
          cpu.shift();
          cpu.push(result.cpu);
          mem.shift();
          mem.push(result.mem);
          draw(cpu,mem);
        };
      },error:function(){
        //alert("网络错误");
      }
  });
  return false;
}


$(document).ready(function(){
    getsysteminfo();
    window.setInterval(function(){getsysteminfo()},30000);

});



function showrecords(solverecords){
  var html ="";
  for(var i=0;i<solverecords.length;i++){
    if(solverecords[i].status == 1){
        html += '<tr>\
                    <td><a href="#">'+solverecords[i].id+'</a></td>\
                    <td>'+solverecords[i].username+'</td>\
                    <td><span class="label label-success">success</span></td>\
                    <td>\
                      <div class="sparkbar" data-color="#00a65a" data-height="20">'+solverecords[i].challenge+'</div>\
                    </td>\
                  </tr>';
    }else{
      html += '<tr>\
                    <td><a href="#">'+solverecords[i].id+'</a></td>\
                    <td>'+solverecords[i].username+'</td>\
                    <td><span class="label label-danger">&nbsp;&nbsp;failed&nbsp;&nbsp;</span></td>\
                    <td>\
                      <div class="sparkbar" data-color="#00a65a" data-height="20">'+solverecords[i].challenge+'</div>\
                    </td>\
                  </tr>';
    }
  };
  $("#records").html(html);
};



function draw(cpu,mem){

  'use strict';

  /* ChartJS
   * -------
   * Here we will create a few charts using ChartJS
   */

  // -----------------------
  // - MONTHLY SALES CHART -
  // -----------------------

  // Get context with jQuery - using jQuery's .get() method.
  var salesChartCanvas = $('#salesChart').get(0).getContext('2d');
  // This will get the first returned node in the jQuery collection.
  var salesChart       = new Chart(salesChartCanvas);

  var salesChartData = {
    labels  : ['','','','','','','','','','','','','','',''],
    datasets: [
      {
        fillColor : "rgba(220,220,220,0.2)",
        strokeColor : "rgba(220,220,220,1)",
        pointColor : "rgba(220,220,220,1)",
        pointStrokeColor : "#fff",
        pointHighlightFill : "#fff",
        pointHighlightStroke : "rgba(220,220,220,1)",
        data                : cpu
      },
      {
        fillColor : "rgba(151,187,205,0.2)",
        strokeColor : "rgba(151,187,205,1)",
        pointColor : "rgba(151,187,205,1)",
        pointStrokeColor : "#fff",
        pointHighlightFill : "#fff",
        pointHighlightStroke : "rgba(151,187,205,1)",
        data                : mem
      }
    ]
  };

  var salesChartOptions = {
    // Boolean - If we should show the scale at all
    showScale               : true,
    // Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines      : false,
    // String - Colour of the grid lines
    scaleGridLineColor      : 'rgba(0,0,0,.05)',
    // Number - Width of the grid lines
    scaleGridLineWidth      : 1,
    // Boolean - Whether to show horizontal lines (except X axis)
    scaleShowHorizontalLines: true,
    // Boolean - Whether to show vertical lines (except Y axis)
    scaleShowVerticalLines  : true,
    // Boolean - Whether the line is curved between points
    bezierCurve             : true,
    // Number - Tension of the bezier curve between points
    bezierCurveTension      : 0.3,
    // Boolean - Whether to show a dot for each point
    pointDot                : false,
    // Number - Radius of each point dot in pixels
    pointDotRadius          : 4,
    // Number - Pixel width of point dot stroke
    pointDotStrokeWidth     : 1,
    // Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    pointHitDetectionRadius : 20,
    // Boolean - Whether to show a stroke for datasets
    datasetStroke           : true,
    // Number - Pixel width of dataset stroke
    datasetStrokeWidth      : 2,
    // Boolean - Whether to fill the dataset with a color
    datasetFill             : true,
    // String - A legend template
    legendTemplate          : '<ul class=\'<%=name.toLowerCase()%>-legend\'><% for (var i=0; i<datasets.length; i++){%><li><span style=\'background-color:<%=datasets[i].lineColor%>\'></span><%=datasets[i].label%></li><%}%></ul>',
    // Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
    maintainAspectRatio     : true,
    // Boolean - whether to make the chart responsive to window resizing
    responsive              : true
  };

  // Create the line chart
  salesChart.Line(salesChartData, salesChartOptions);

};
