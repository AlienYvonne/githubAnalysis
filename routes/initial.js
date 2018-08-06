var express = require('express');
var router = express.Router();

/* GET the statistics for this repo. */

router.post('/', function(req, res, next) {
  repo = req.body.repos;

  // 空白输入
  if (repo == '') {
    res.render('index', {
      title: 'Provide a report for a picked github repo...'
    });
    return;
  }

  // 输入仓库不存在

  const fs = require('fs');
  timeStampStart = './public/data/' + repo + '/timeStampStart'; // 查找有无下载开始的时间戳
  state = '';

  fs.open(timeStampStart, 'r', (err, fd) => {
    // 当前没有该仓库的数据，需要下载
    if (err) {
      console.log(timeStampStart);
      if (err.code == 'ENOENT') {
        start = '2008-01-01';
        end = new Date().toISOString().slice(0, 10);
        state += 'We are going to download the data...';
        res.render('initial', {
          title: state
        });
        fetchData(repo, start, end);
        return;
      }
      throw err;
    }
    // 服务器中的该仓库数据的timeStamp小于当前系统时间，需要更新数据
    timeStampEnd = './public/data/' + repo + '/timeStampEnd';

    fs.open(timeStampEnd, 'r', (err, fd) => {
      if (err.code == 'ENOENT') {

        state += 'Downloading the data. Please wait for a minute...';
        res.render('initial', {
          title: state
        });

        return;
      }

      fs.readFile(timeStampEnd, (err, data) => {
        start = data.toString().slice(0, 10);
        end = new Date().toISOString().slice(0, 10);

        flag = compareDate(start, end);
        // flag: Ture start < end
        if(flag){
          state = "We are going to update the data..."
          res.render('initial', {
            title: state
          });
          fetchData(repo,start,end);
        }
        // start >= end
        else {
          // 生成绘图所需要的数据
          //doReport(repo);
          fetchData(repo,start,end);
          res.render('report',{title:repo});
        }
      });

    });




    // 一切准备就绪，开始加载report
  });


});
function doReport(repo){
  spawnSync = require('child_process').spawnSync;
  py = spawnSync('python', ["./public/py/analyze.py", repo]);
  console.log(py.stderr.toString());
  console.log(py.stdout.toString());

  /*
  py.stdout.on('data', function(data) {
    console.log(data.toString());
  });
  py.stderr.on('data', (data) => {
    console.log(data.toString());
  });
  py.on('exit', (code) => {
    console.log("Process quit with code:" + code);
  });
  */

}
// a<b True a>=b false
function compareDate(a, b) {
  aYear = parseInt(a.slice(0, 4));
  bYear = parseInt(b.slice(0, 4));
  aMonth = parseInt(a.slice(5, 7));
  bMonth = parseInt(b.slice(5, 7));
  if (aYear > bYear) {
    return false;
  } else if (aYear < bYear) {
    return true;
  } else if (aMonth >= bMonth) {
    return false;
  } else {
    return true;
  }
}

function fetchData(repo, start, end) {
  console.log(start, end);
  spawn = require('child_process').spawn;
  //py = spawn('python',["./public/py/compute_input.py"]);
  py = spawn('python', ["./public/py/initial.py", repo, start, end]);
  /*
  py.stdout.on('data', function(data) {
    console.log(data.toString());
  });
  py.stderr.on('data', (data) => {
    console.log(data.toString());
  });
  /*
  py.on('exit', (code) => {
    console.log("Process quit with code:" + code);
  });*/
}

module.exports = router;
