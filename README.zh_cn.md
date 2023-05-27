这是一个小demo，相关演示网址：http://resume_of_anqi.sonya.cc/。本Demo使用Python 3.9和FastAPI以REST API搭建。当前已实现了GET/POST/PUT/DELETE/PATCH操作。<br/>
FastAPI自动生成了相关文档：http://resume_of_anqi.sonya.cc/docs/<br/>
在您清理localStorage对象前，您的浏览器将保留上次您所设置的语言（默认英语），以便您重新打开浏览器后快速切换到您最后一次所设置的语言。
<br/><br/>
您可以通过pip来安装所需库及uvicorn（本地运行所需）：<br/>
```
pip install -r requirements.txt
pip install uvicorn
```
您需要创建books目录，并且授予读写权限：<br/>
Windows
```
# cd to the catalog
md books
icacls books /grant Everyone:F
```
Mac或Linux
```
# cd to the catalog
mkdir books && chmod 777 books
```
然后运行：<br/>
```
uvicorn app:app --reload
```