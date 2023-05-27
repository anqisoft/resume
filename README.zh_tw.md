這是一個小demo，相關演示網址：http://resume_of_anqi.sonya.cc/。本Demo使用Python 3.9和FastAPI以REST API搭建。當前已實現了GET/POST/PUT/DELETE/PATCH操作。<br/>
FastAPI自動生成了相關文檔：http://resume_of_anqi.sonya.cc/docs/<br/>
在您清理localStorage物件前，您的流覽器將保留上次您所設置的語言（預設英語），以便您重新打開流覽器後快速切換到您最後一次所設置的語言。
<br/><br/>
您可以通過pip來安裝所需庫及uvicorn（本地運行所需）：<br/>
```
pip install -r requirements.txt
pip install uvicorn
```
您需要創建books目錄，並且授予讀寫許可權：<br/>
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
然後運行：<br/>
```
uvicorn app:app --reload
```
