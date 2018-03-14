const pupp = require('puppeteer');
(async () => {
  const browser = await pupp.launch({executablePath:'E:/lab/chrome/chrome-win32/chrome',headless:false});
  const page = await browser.newPage();
var dict=["1-19-00","1-19-05","1-19-10","1-60-03","2-19-04","2-19-09","2-60-02","3-19-03","3-19-08","3-60-01","1-19-01","1-19-06","1-19-11","2-19-00","2-19-05","2-19-10","2-60-03","3-19-04","3-19-09","3-60-02","1-19-02","1-19-07","1-60-00","2-19-01","2-19-06","2-19-11","3-19-00","3-19-05","3-19-10","3-60-03","1-19-03","1-19-08","1-60-01","2-19-02","2-19-07","2-60-00","3-19-01","3-19-06","3-19-11","1-19-04","1-19-09","1-60-02","2-19-03","2-19-08","2-60-01","3-19-02","3-19-07","3-60-00"];
	
  for(var k in dict){
     var url = "localhost:8888/"+dict[k]+".html";
     var path1 = dict[k] + ".png";	  
     await page.goto(url);
     await page.screenshot({path:path1,fullPage:true,width:800 });
  }
  await browser.close();
})();
