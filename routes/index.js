var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

/*
router.get('/',function callName(req,res){
  res.send("en");
  console.log("I am index.js");
  const spawn = require('child_process').spawn;//.spawn;
  var py = spawn('python',["./compute_input.py"]);

  data = [1,2,3,4,5,6],
  dataString = '';
  console.log("I want to run python.");

  py.stdout.on('data',function(data){
    console.log("I am the function.");
    dataString += data.toString();
    console.log(dataString);
  });
  //res.render('index', { title: 'Express' });
});
*/

module.exports = router;
