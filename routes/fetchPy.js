var express = require('express');
var router = express.Router();

router.get('/',callName);
function callName(req,res){
  var spawn = require('child_process').spawn,
  py = spawn('python',["./javascripts/compute_input.py"]),
  data = [1,2,3,4,5,6],
  dataString = '';

  py.stdin.write(JSON.stringify(data));
  py.stdin.end();

  py.stdout.on('data',function(data){
    console.log(data);
    dataString += data.toString();
    res.send(data.toString())
  });
}
module.exports = router;
/*
py.stdout.on('end',function(){
  console.log('Sum of numbers=',dataString);
});*/
