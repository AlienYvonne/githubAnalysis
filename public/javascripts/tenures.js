//绘制开发者贡献时长分布图
function drawChartTenure(anchor, data){
  var svgWidth = 1000, svgHeight = 400;
  var margin = {top:30, right:30, bottom:50, left:50};
  var width = svgWidth - margin.left - margin.right;
  var height = svgHeight - margin.top - margin.bottom;
  var len = data.length;
  var maxData = d3.max(data);
  console.log(len);
  var svg = d3.select("body")
      .append("svg")
      .attr("id", "tenuresSvg")
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

  x.domain([0,len]);
  y.domain([0,maxData]);

  var rectPadding = width / len;

  g.append("g")
    .attr("transform", "translate(0,"+height+")")
    .call(d3.axisBottom(x)
            .tickValues([]));

  g.append("g")
    .call(d3.axisLeft(y).ticks(maxData))
    .append("text")
    .attr("fill","#000")
    .attr("transform","rotate(-90)")
    .attr("y",6)
    .attr("dy","0.71em")
    .attr("text-anchor","end")
    .text("Number");
  var color = d3.scaleOrdinal(["#F9DBBD","#FCA17D","#DA627D","#9A348E"
                              ,"#F7F6C5","#B2EDC5","#7C7287","#88A2AA",
                              "#E2856E","#E3D081"]);

  g.selectAll(".bar")
    .data(data)
    .enter()
    .append("rect")
    .attr("fill",function(d,i){
      month = (anchor + i) % 12;
      if(month == 0){
        month = 12;
      }
      year = ((anchor + i) - month ) / 12 + 2008;
      return color(year - 2008);
    })
    .attr("class","bar")
    .attr("x",function(d,i){
      return x(i) + rectPadding/2;
    })
    .attr("y",function(d){
      return y(Number(d));
    })
    .attr("width", rectPadding)
    .attr("height",function(d){
      return height-y(Number(d));
    });

    firstMonth = anchor % 12;
    if(firstMonth == 0){
      firstMonth = 12;
    }
    firstYear = parseInt((anchor - firstMonth ) / 12 + 2008);

    lastMonth = (anchor + len - 1) % 12;
    if(lastMonth == 0){
      lastMonth = 12;
    }
    lastYear = parseInt((anchor + len - lastMonth) / 12 + 2008);

    years = new Array(lastYear-firstYear + 1);

    if(firstYear == lastYear){
      years[0] = lastMonth - firstMonth + 1;
    }
    else {
      years[0] = 12 - firstMonth + 1;
      for (i = firstYear+1; i < lastYear; i++){
        years[i-firstYear] = 12;
      }
      years[lastYear-firstYear] = lastMonth;
    }
    console.log(years);

    g.selectAll("#years")
     .data(years)
     .enter()
     .append("text")
     .attr("class","text")
     .attr("transform",function(d,i){
       prelen = 0;
       for (tmp = 0; tmp < i; tmp ++){
         prelen += years[tmp];
       }
       console.log(prelen);
       console.log(d);

       console.log("translate("+ (prelen*rectPadding + (rectPadding*d)/2) + "," + (svgHeight-10)  + ")");
       return "translate("+ (prelen*rectPadding + (rectPadding*d)/2) + "," + (svgHeight-50)  + ")";
     })
     .text(function(d,i){

       return firstYear + i;
     });

     svg.append("text")
      .attr("class","text")
      .attr("font-size","30px")
      .attr("transform","translate("+(width/2-50) + "," + 50 + ")")
      .text(function(d){
        return "每月存活开发者"
      });

}
function drawTenure(folder){
  var file = folder + "/" +"tenures.json";
  console.log(file);
  $.getJSON(file,function(data){
    var array = new Array(300);
    array.fill(0,0,300);
    for (var user in data){
      start = data[user]["start"]
      startYear = eval(start.slice(0,4));
      startMonth = eval(start.slice(5,7));
      startDay = eval(start.slice(8,10));
      startIndex = (startYear-2008) * 12 + startMonth;

      end = data[user]["end"]
      endYear = eval(end.slice(0,4));
      endMonth = eval(end.slice(5,7));
      endDay = eval(end.slice(8,10));
      endIndex = (endYear - 2008) * 12 + endMonth;
      while(startIndex <= endIndex){
        array[startIndex] += 1;
        startIndex += 1;
      }

    }
    for (start = 0; start < array.length; start++){
      if(array[start] != 0){
        break;
      }
    }

    for (end = array.length-1; end >= 0; end--){
      if(array[end] != 0){
        break;
      }
    }

    array = array.slice(start,end);

    drawChartTenure(start,array);

  })
}

drawTenure("JSON")
