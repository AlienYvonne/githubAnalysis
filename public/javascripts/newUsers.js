
function drawChartForNewUsers(folder,title){

  var file = folder + "/" + title + ".json";
  $.getJSON(file,function(allData){
    var maxData = 0;
    console.log("all:", allData);

    for (var i = 2008; i < 2019; i++){
      var year = String(i);
      var data = allData[year]["everyUsers"];
      maxData = maxData > d3.max(data) ? maxData : d3.max(data);
    }
    console.log("max:",maxData);

    for (var i = 2008; i < 2019; i++){
      year = String(i);
      console.log("year:",year);
      var data = allData[year]
      var everyUsersData = allData[year]["everyUsers"];
      var newUsersData = allData[year]["newUsers"];
      console.log("everyUsers:",everyUsersData);

      var notNullFlag = false;
      for (j = 0, length = everyUsersData.length; j < length; j ++ ){
        if (everyUsersData[j] !=0){
          notNullFlag = true;
          break;
        }
      }
      if( !notNullFlag){
        continue;
      }

      var svgWidth = 300, svgHeight = 200;
      var margin = {top:30, right:30, bottom:50, left:50};
      var width = svgWidth - margin.left - margin.right;
      var height = svgHeight - margin.top - margin.bottom;

      console.log('#'+title)
      //d3.select('#' + title + "Svg")
      //  .remove();
      var svg = d3.select("body")//d3.select('#'+title)
          .append("svg")
          .attr("id", title + "Svg")
          .attr("width",svgWidth)
          .attr("height", svgHeight);

      var g = svg.append("g")
              .attr("width", width)
              .attr("height", height)
              .attr("transform","translate("+margin.left+","+margin.top+")");
      var x = d3.scaleLinear()
              .rangeRound([0,width]);
              //.padding(0.1);

      var y = d3.scaleLinear()
              .rangeRound([height,0]);

      x.domain([0,12]);
      y.domain([0,maxData]);

      var rectPadding = width / 24;

      g.append("g")
        .attr("transform", "translate(0,"+height+")")
        .call(d3.axisBottom(x));

      g.append("g")
        .call(d3.axisLeft(y).ticks(maxData))
        .append("text")
        .attr("fill","#000")
        .attr("transform","rotate(-90)")
        .attr("y",6)
        .attr("dy","0.71em")
        .attr("text-anchor","end")
        .text("Number");

      g.selectAll(".bar")
        .data(everyUsersData)
        .enter()
        .append("rect")
        .attr("fill","#00868B")
        .attr("class","bar")
        .attr("x",function(d,i){
          return x(i) + rectPadding/2*3;
        })
        .attr("y",function(d){
          return y(Number(d));
        })
        .attr("width", rectPadding)
        .attr("height",function(d){
          return height-y(Number(d));
        });

        g.selectAll("#newUsersBar")
          .data(newUsersData)
          .enter()
          .append("rect")
          .attr("fill","#98F5FF")
          .attr("x",function(d,i){
            return x(i) + rectPadding/2*3;
          })
          .attr("y",function(d,i){
            return y(Number(everyUsersData[i]));
          })
          .attr("width", rectPadding)
          .attr("height",function(d,i){
            return height-y(Number(d));
          });


     svg.data([title])
      .append("text")
      .attr("class","text")
      .attr("transform","translate("+(margin.left) + "," + (svgHeight-5) + ")")
      .text(function(d){
        if(d == "newUsers"){
          return year　+ "-New devoloper for every month";
        }
        if(d == "everyUsers"){
          return year + "-devolopers for every month";
        }
        if(d == "analysisUsers"){
          return year + "-代码提交者分析";
        }
      });


    }

    // 增加图例
    svg = d3.select("body")
            .append("svg")
            .attr("width",400)
            .attr("height",100);
    svg.append("rect")
        .attr("x",10)
        .attr("y",10)
        .attr("width",30)
        .attr("height",10)
        .attr("class","rect")
        .attr("fill","#98F5FF");

    svg.append("text")
        .attr("x",50)
        .attr("y",20)
        .text(folder + "-当月新增代码提交者");

  });

}

//drawChart("JSON","newUsers");
//drawChart("JSON","everyUsers");
drawChartForNewUsers("javascript","analysisUsers")
