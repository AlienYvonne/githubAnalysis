var express = require('express');
var router = express.Router();

/* GET the statistics for this repo. */

router.post('/', function(req, res, next) {
  repo = req.body.repos;

  // 空白输入
  if(repo == ''){
    res.render('index', { title: 'Provide a report for a picked github repo...' });
    return ;
  }

  // 输入仓库不存在

  const fs = require('fs');
  timeStamp = 'data/' + repo + '/timeStamp';
  state = '';
  fs.open('timeStamp','r',(err,fd) => {
    // 当前没有该仓库的数据，需要下载
    if(err){
      console.log(timeStamp);
      if(err.code == 'ENOENT'){
        start = '2008-01-01';
        end = new Date();
        state += 'We are going to download the data...';
        res.render('initial',{title:state});
        fetchData(repo,start,end);
        return ;
      }
      throw err;
    }
    // 服务器中的该仓库数据的timeStamp小于当前系统时间，需要更新数据
    start = fd;
    end = new Date();

    // 一切准备就绪，开始加载report

  })

});
function fetchData(repo,start,end){
  console.log('Start the initial.py...');
  spawn = require('child_process').spawn;
  py = spawn('python',["./public/py/compute_input.py"]);
  //py = spawn('python',["./public/py/initial.py",repo,start,end]);
  py.stdout.on('data',function(data){
    console.log(data.toString());
  });

}
module.exports = router;
