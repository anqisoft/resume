import json
import os
from enum import Enum

from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

app = FastAPI()

HTML_TEMPLATE = '''
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no,viewport-fit=cover,minimal-ui">
        <title>{}</title>
        <link rel="icon" href="favicon.ico" />
        <style>
            en, zh_cn, zh_tw{{display:inline;}}
            button{{cursor:pointer;}}
            html[lang='en'] zh_cn, html[lang='en'] zh_tw, html[lang='en'] button[onclick="setLang('en')"]{{display:none;}}
            html[lang='zh_cn'] en, html[lang='zh_cn'] zh_tw, html[lang='zh_cn'] button[onclick="setLang('zh_cn')"]{{display:none;}}
            html[lang='zh_tw'] en, html[lang='zh_tw'] zh_cn, html[lang='zh_tw'] button[onclick="setLang('zh_tw')"]{{display:none;}}
            
            html[lang='en'] button[onclick="setLang('zh_cn')"] en, html[lang='en'] button[onclick="setLang('zh_tw')"] en,
            html[lang='zh_cn'] button[onclick="setLang('en')"] zh_cn, html[lang='zh_cn'] button[onclick="setLang('zh_tw')"] zh_cn,
            html[lang='zh_tw'] button[onclick="setLang('en')"] zh_tw, html[lang='zh_tw'] button[onclick="setLang('zh_cn')"] zh_tw
            {{display:none;}}
            
            html[lang='en'] button[onclick="setLang('zh_cn')"] zh_cn, html[lang='en'] button[onclick="setLang('zh_tw')"] zh_tw{{display:inline;}}
            html[lang='zh_cn'] button[onclick="setLang('en')"] en, html[lang='zh_cn'] button[onclick="setLang('zh_tw')"] zh_tw{{display:inline;}}
            html[lang='zh_tw'] button[onclick="setLang('en')"] en, html[lang='zh_tw'] button[onclick="setLang('zh_cn')"] zh_cn{{display:inline;}}
        </style>
    </head>
    <body>
        {}
        <br /><br />
        <en>If you want to change the language, please click the button.</en>
        <zh_cn>如果您想切换语言，请点击下一行相应按钮。</zh_cn>
        <zh_tw>如果您想切換語言，請點擊下一行相應按鈕。</zh_tw>
        <br />
        <button type="button" onclick="setLang('en')"><en>En</en><zh_cn>Chinese</zh_cn><zh_tw>Traditional</zh_tw></button>
        <button type="button" onclick="setLang('zh_cn')"><en>英语</en><zh_cn>简体</zh_cn><zh_tw>繁体</zh_tw></button>
        <button type="button" onclick="setLang('zh_tw')"><en>英語</en><zh_cn>簡體</zh_cn><zh_tw>繁體</zh_tw></button>
        <script>
            document.getElementsByTagName('html')[0].setAttribute('lang', localStorage.getItem('lang') || 'en' );
            function setLang(lang){{localStorage.setItem('lang', lang); window.location.reload();}}
            
            function updateBookHtml() {{
                // const response = await fetch('/books/', {{method: 'GET'}});
                // console.log('response', response);
                // // document.getElementById('books').innerHTML = JSON.stringify(response.text);
                // document.getElementById('books').innerHTML = response.text;
                fetch('/books/')
                .then(response => {{
			      if (!response.ok) {{
			        throw new Error('Failed to update book');
			      }} else {{
			        return response.text();
			      }}
			      // document.getElementById('books').innerHTML = JSON.stringify(response.text());
			      // document.getElementById('books').innerHTML = response.text();
			    }})
                // .then(data => {{
                //     console.log('data', data);
			    //   document.getElementById('books').innerHTML = data; // JSON.stringify(data);
			    // }})
                .then(data => {{
                   console.log('data', data);
			       // document.getElementById('books').innerHTML = JSON.parse(data.substr(1, data.length - 2)); // JSON.stringify(data);
			       document.getElementById('books').innerHTML = JSON.parse(data); // JSON.stringify(data);
			    }})
			    ;
            }}
            
            function addBook(target) {{
                const bookId = target.getAttribute('data-book-id');
                // 用post方式调用/add_book接口，传入bookId
                fetch('/add_book/' + bookId, {{method: 'POST'}})
                .then(response => {{
			      if (!response.ok) {{
			        throw new Error('Failed to update book');
			      }}
			      updateBookHtml();
			    }})
			    .catch(error => {{
			      console.error(error);
			      // 处理错误
			    }});
            }}
            
            function likeBook(target) {{
                const bookId = target.getAttribute('data-book-id');
                // 调用/like_book接口，传入bookId
                fetch('/like_book/' + bookId, {{method: 'PUT'}})
                .then(response => {{
			      if (!response.ok) {{
			        throw new Error('Failed to update book');
			      }}
			      updateBookHtml();
			    }})
			    .catch(error => {{
			      console.error(error);
			      // 处理错误
			    }});
            }}
            
            function unlikeBook(target) {{
                const bookId = target.getAttribute('data-book-id');
                // 调用/unlike_book接口，传入bookId
                fetch('/unlike_book/' + bookId, {{method: 'PATCH'}})
                .then(response => {{
			      if (!response.ok) {{
			        throw new Error('Failed to update book');
			      }}
			      updateBookHtml();
			    }})
			    .catch(error => {{
			      console.error(error);
			      // 处理错误
			    }});
            }}
            
            function removeBook(target) {{
                const bookId = target.getAttribute('data-book-id');
                // 调用/remove_book接口，传入bookId
                fetch('/remove_book/' + bookId, {{method: 'DELETE'}})
                .then(response => {{
			      if (!response.ok) {{
			        throw new Error('Failed to update book');
			      }}
			      updateBookHtml();
			    }})
			    .catch(error => {{
			      console.error(error);
			      // 处理错误
			    }});
            }}
        </script>
    </body>
</html>
'''


def read_contact_info():
	global PHONE_INFO_TEL_HTML
	global EMAIL

	with open('static/contactInfo.json', 'r', encoding='utf-8') as f:
		CONTACT_INFO = json.load(f)

		email = CONTACT_INFO["email"]
		EMAIL = HTML_TEMPLATE.format("AnQi's Email", f'<a href="mailto:{email}" target="_blank">{email}</a>')

		PHONE_INFO = CONTACT_INFO['phones']

		PHONE_INFO_TEL = []
		for item in PHONE_INFO:
			phone = item['phone']

			name = item['name']
			name_en = name['en']
			name_chinese = name['chinese']
			name_traditional = name['traditional']

			kind = item['kind']
			kind_en = kind['en']
			kind_chinese = kind['zh_cn']
			kind_traditional = kind['zh_tw']

			PHONE_INFO_TEL.append(
				f'{phone}: <a href="tel:{phone}"><en>{name_en}({kind_en})</en><zh_cn>{name_chinese}（{kind_chinese}）</zh_cn><zh_tw>{name_traditional}（{kind_traditional}）</zh_tw></a>')

		PHONE_INFO_TEL_HTML = HTML_TEMPLATE.format("AnQi's Phone", '<br>'.join(PHONE_INFO_TEL))


read_contact_info()

@app.get('/', response_class=HTMLResponse)
def get_html(response: Response):
	# 遍历books目录下的所有文件，以及BOOKS列表，获取当前所有书籍的点赞数，合并为表格html。不在books目录的书籍，点赞数为0，且下方允许添加。
	# 读取books目录下的所有文件，按文件名排序
	books = sorted(os.listdir('books'))
	# 读取books文件内容，获取点赞数（json结构）
	books_info = []
	for book in books:
		with open(f'books/{book}', 'r', encoding='utf-8') as f:
			books_info.append(json.load(f))

	html_content = HTML_TEMPLATE.format("AnQi's resume Demo(python3.9 + FastAPI + REST API)", '''
                <en>Resume:</en><zh_cn>简历：</zh_cn><zh_tw>簡歷：</zh_tw>
                <en>
	                <a href="en/" target="_blank">English</a>
	                <a href="zh_cn/" target="_blank">Chinese</a>
	                <a href="zh_tw/" target="_blank">Traditional</a>
                </en>
                <zh_cn>
	                <a href="en/" target="_blank">英语</a>
	                <a href="zh_cn/" target="_blank">简体</a>
	                <a href="zh_tw/" target="_blank">繁體</a>
                </zh_cn>
                <zh_tw>
	                <a href="en/" target="_blank">英語</a>
	                <a href="zh_cn/" target="_blank">簡體</a>
	                <a href="zh_tw/" target="_blank">繁體</a>
                </zh_tw><br/><br/>
                
				/users/{{user_id}}&nbsp;
				<en>Users(Enligsh Only):</en><zh_cn>用户（仅显示英文名）：</zh_cn><zh_tw>用戶（僅顯示英文名）：</zh_tw>
                <en>
	                <a href="/users/0" target="_blank">0: AnQi</a>
	                <a href="/users/1" target="_blank">1: erioruan</a>
	                <a href="/users/2" target="_blank">2: Damien Polegato</a>
                </en>
                <zh_cn>
	                <a href="/users/0" target="_blank">0：安启（吴启萍）</a>
	                <a href="/users/1" target="_blank">1：保密1</a>
	                <a href="/users/2" target="_blank">2：保密2</a>
                </zh_cn>
                <zh_tw>
	                <a href="/users/0" target="_blank">0：安啟（吳啟萍）</a>
	                <a href="/users/1" target="_blank">1：保密1</a>
	                <a href="/users/2" target="_blank">2：保密2</a>
                </zh_tw><br/><br/>
                
                /name/{{name_kind_id}}&nbsp;
                <en>Name:</en><zh_cn>名字：</zh_cn><zh_tw>名字：</zh_tw>
                <en>
	                <a href="/name/0" target="_blank">0: English</a>
	                <a href="/name/1" target="_blank">1: Chinese</a>
	                <a href="/name/2" target="_blank">2: Traditional</a>
	                <a href="/name/3" target="_blank">3: Buddhist</a>
                </en>
                <zh_cn>
	                <a href="/name/0" target="_blank">0：英文名</a>
	                <a href="/name/1" target="_blank">1：中文名</a>
	                <a href="/name/2" target="_blank">2：繁體中文名</a>
	                <a href="/name/3" target="_blank">3：佛教法名</a>
                </zh_cn>
                <zh_tw>
	                <a href="/name/0" target="_blank">0：英文名</a>
	                <a href="/name/1" target="_blank">1：中文名</a>
	                <a href="/name/2" target="_blank">2：繁體中文名</a>
	                <a href="/name/3" target="_blank">3：佛教法名</a>
                </zh_tw><br/><br/>
                
                /name2/{{name_kind_name}}&nbsp;
                <en>Name2:</en><zh_cn>名字2：</zh_cn><zh_tw>名字2：</zh_tw>
                <en>
	                <a href="/name2/english" target="_blank">0: English</a>
	                <a href="/name2/chinese" target="_blank">1: Chinese</a>
	                <a href="/name2/traditional" target="_blank">2: Traditional</a>
	                <a href="/name2/buddhist" target="_blank">3: Buddhist</a>
                </en>
                <zh_cn>
	                <a href="/name2/english" target="_blank">0：英文名</a>
	                <a href="/name2/chinese" target="_blank">1：中文名</a>
	                <a href="/name2/traditional" target="_blank">2：繁體中文名</a>
	                <a href="/name2/buddhist" target="_blank">3：佛教法名</a>
                </zh_cn>
                <zh_tw>
	                <a href="/name2/english" target="_blank">0：英文名</a>
	                <a href="/name2/chinese" target="_blank">1：中文名</a>
	                <a href="/name2/traditional" target="_blank">2：繁體中文名</a>
	                <a href="/name2/buddhist" target="_blank">3：佛教法名</a>
                </zh_tw><br/><br/>
                
                /phone &nbsp;
                <a href="/phone" target="_blank"><en>Phone</en><zh_cn>电话</zh_cn><zh_tw>電話</zh_tw></a>
                <br/><br/>
                
                /email &nbsp;
                <a href="/email" target="_blank"><en>Email</en><zh_cn>邮箱</zh_cn><zh_tw>郵箱</zh_tw></a>
                <br/><br/>
                '''
                + f'<div id="books">{get_books_html()}</div>')

	response.headers["Content-Type"] = "text/html"

	return html_content


BOOKS = [
	{
		'id': 0,
	    'url': 'https://book.douban.com/subject/26298694/',
	    'name': {'en': 'An Introduction to General Systems Thinking', 'zh_cn': '系统化思维导论', 'zh_tw': '系統化思維導論'},
	    'author': {'en': 'Gerald M.Weinberg', 'zh_cn': '（美）杰拉尔德·温伯格', 'zh_tw': '（美）傑拉爾德·溫伯格'}
	 },
	{
		'id': 1,
	    'url': 'https://book.douban.com/subject/26664522/',
	    'name': {'en': 'The Non-Designer\'s Design Book', 'zh_cn': '写给大家看的设计书', 'zh_tw': '寫給大家看的設計書'},
	    'author': {'en': 'Robin Wiliams', 'zh_cn': '（美）罗宾·威廉姆斯', 'zh_tw': '（美）羅賓·威廉姆斯'}
	 },
	{
		'id': 2,
	    'url': 'https://book.douban.com/subject/1193565/',
	    'name': {'en': 'The Art of Word', 'zh_cn': 'Word排版艺术', 'zh_tw': 'Word排版藝術'},
	    'author': {'en': 'Jie Hou', 'zh_cn': '侯捷', 'zh_tw': '侯捷'},
	 },
]
# 转BOOKS为JSON，赋值给BOOKS_JSON
BOOKS_JSON = json.dumps(BOOKS, ensure_ascii=False)

@app.get('/en/', response_class=HTMLResponse)
def get_en():
	return FileResponse('static/en.htm', media_type="text/html; charset=utf-8")


@app.get('/zh_cn/', response_class=HTMLResponse)
def get_en():
	return FileResponse('static/zh_cn.htm', media_type="text/html; charset=utf-8")


@app.get('/zh_tw/', response_class=HTMLResponse)
def get_en():
	return FileResponse('static/zh_tw.htm', media_type="text/html; charset=utf-8")


users = [{'id': 0, 'name': 'AnQi'}, {'id': 1, 'name': 'ezioruan'}, {'id': 2, 'name': 'Damien Polegato'}, ]


@app.get('/users/{user_id}')
def get_user(user_id: int):
	return next((user['name'] for user in users if user['id'] == user_id), None)


class NameKind(Enum):
	English = 0
	Chinese = 1
	Traditional = 2
	Buddhist = 3


names = {NameKind.English: 'AnQi',  # 英文
         NameKind.Chinese: '吴启萍',  # 简体
         NameKind.Traditional: '吳啟萍',  # 繁体姓名
         NameKind.Buddhist: 'AnQi/安启/安啟/安啓',  # 佛教法名安启，同时提供英文、简体中文、繁体中文，以/分隔
         }


# get_names的本机测试网址
# http://127.0.0.1:8000/names/0
# http://127.0.0.1:8000/names/1
# http://127.0.0.1:8000/names/2
# http://127.0.0.1:8000/names/3

@app.get('/name/{name_kind_id}')
def get_name(name_kind_id: int):
	return names.get(NameKind(name_kind_id), None)


@app.get('/name2/{name_kind_name}')
def get_name2(name_kind_name: str):
	get_name_kind = lambda name: next((kind for kind in NameKind if kind.name.lower() == name.lower()), None)
	name_kind_name = get_name_kind(name_kind_name)

	return names.get(name_kind_name, None)


@app.get('/phone/', response_class=HTMLResponse)
def get_phone(response: Response):
	response.headers["Content-Type"] = "text/html"
	return PHONE_INFO_TEL_HTML


@app.get('/email/', response_class=HTMLResponse)
def get_phone(response: Response):
	response.headers["Content-Type"] = "text/html"
	return EMAIL


def get_books_html():
	# 遍历books目录下的所有文件，以及BOOKS列表，获取当前所有书籍的点赞数，合并为表格html。不在books目录的书籍，点赞数为0，且下方允许添加。
	# 读取books目录下的所有文件，按文件名排序
	books = sorted(os.listdir('books'))
	# 读取books文件内容，获取点赞数（json结构）
	books_info = []
	for book in books:
		with open(f'books/{book}', 'r', encoding='utf-8') as f:
			books_info.append(json.load(f))

	# print('books_info.length', len(books_info))

	# 转换为html
	books_html_list = []
	for book_info in books_info:
		# 读取书籍信息
		book_id = book_info['id']

		book_name = book_info['name']
		book_name_en = book_name['en']
		book_name_chinese = book_name['zh_cn']
		book_name_traditional = book_name['zh_tw']

		book_author = book_info['author']
		book_author_en = book_author['en']
		book_author_chinese = book_author['zh_cn']
		book_author_traditional = book_author['zh_tw']

		book_url = book_info['url']

		book_like = book_info['like']

		# 生成html
		books_html_list.append(
			f'<tr>'
			f'<td><a href="{book_url}" target="_blank"><en>{book_name_en}</en><zh_cn>{book_name_chinese}</zh_cn><zh_tw>{book_name_traditional}</zh_tw></a></td>'
			f'<td><en>{book_author_en}</en><zh_cn>{book_author_chinese}</zh_cn><zh_tw>{book_author_traditional}</zh_tw></td>'
			f'<td style="text-align:right;">{book_like}</td>'
			f'<td style="text-align:center;">'
			f'<button type="button" onclick="likeBook(this)" data-book-id="{book_id}"><en>Like</en><zh_cn>喜欢</zh_cn><zh_tw>喜歡</zh_tw></button>'
			f'&nbsp;&nbsp;<button type="button" onclick="unlikeBook(this)" data-book-id="{book_id}"><en>Unlike</en><zh_cn>不喜欢</zh_cn><zh_tw>不喜歡</zh_tw></button>'
			f'</td>'
			f'<td style="text-align:center;"><button type="button" onclick="removeBook(this)" data-book-id="{book_id}"><en>Remove</en><zh_cn>移除</zh_cn><zh_tw>移除</zh_tw></button></td>'
			f'</tr>')

	# print('books_html.length', len(books_html), books_html[0])

	# 如果books_html为空，则转为""；否则，转为html
	if not books_html_list:
		print('not books_html')
		books_html = ""
	else:
		books_html = ''.join(books_html_list)

		books_html = f'<br /><br /><en>AnQi\'s Books</en><zh_cn>安启书架</zh_cn><zh_tw>安啟書架</zh_tw><br />' \
		f'<table border="1" width="100%"><tr>' \
		f'<th><en>Name</en><zh_cn>书名</zh_cn><zh_tw>書名</zh_tw></th>' \
		f'<th><en>Author</en><zh_cn>作者</zh_cn><zh_tw>作者</zh_tw></th>' \
		f'<th><en>Like Count</en><zh_cn>点赞数</zh_cn><zh_tw>點贊數</zh_tw></th>' \
		f'<th><en>Like/Unlike</en><zh_cn>点赞/取消</zh_cn><zh_tw>點贊/取消</zh_tw></th>' \
		f'<th><en>Remove</en><zh_cn>移除</zh_cn><zh_tw>移除</zh_tw></th>' \
		f'</tr>{books_html}</table>'
		# f'</tr>' + "".join(books_html) + f'</table>'
	# print('books_html:', books_html)

	# 结合books列表与BOOKS，生成未点赞的书籍html
	EXISTS_BOOKS_ID = [book['id'] for book in books_info]
	ALL_BOOKS_ID = [book['id'] for book in BOOKS] # BOOKS.keys() # AttributeError: 'list' object has no attribute 'keys'
	NOT_EXISTS_BOOKS_ID = list(set(ALL_BOOKS_ID).difference(set(EXISTS_BOOKS_ID)))
	NOT_EXISTS_BOOKS_ID = sorted(NOT_EXISTS_BOOKS_ID)

	NOT_EXISTS_BOOKS_HTML = []
	for book_id in NOT_EXISTS_BOOKS_ID:
		book = BOOKS[book_id]

		book_name = book['name']
		book_name_en = book_name['en']
		book_name_chinese = book_name['zh_cn']
		book_name_traditional = book_name['zh_tw']

		book_author = book['author']
		book_author_en = book_author['en']
		book_author_chinese = book_author['zh_cn']
		book_author_traditional = book_author['zh_tw']

		# book_url = book['url']

		NOT_EXISTS_BOOKS_HTML.append(
			f'<en>Name: </en><zh_cn>书名：</zh_cn><zh_tw>書名：</zh_tw>' \
			f'<en>{book_name_en}</en><zh_cn>{book_name_chinese}</zh_cn><zh_tw>{book_name_traditional}</zh_tw><br/>' \
			f'<en>Author: </en><zh_cn>作者：</zh_cn><zh_tw>作者：</zh_tw>' \
			f'<en>{book_author_en}</en><zh_cn>{book_author_chinese}</zh_cn><zh_tw>{book_author_traditional}</zh_tw><br/>' \
			f'<button type="button" onclick="addBook(this)" data-book-id="{book_id}"><en>Add</en><zh_cn>添加</zh_cn><zh_tw>添加</zh_tw></button>')

	# 如果NOT_EXISTS_BOOKS_HTML为空，则转为""；否则，转为html
	if not NOT_EXISTS_BOOKS_HTML:
		NOT_EXISTS_BOOKS_HTML = ""
	else:
		NOT_EXISTS_BOOKS_HTML = f"<br /><br /><en>Add New Books</en><zh_cn>添加新书</zh_cn><zh_tw>添加新書</zh_tw><br />" \
		                        f"{'<br /><br />'.join(NOT_EXISTS_BOOKS_HTML)}"

	return f'{books_html}{NOT_EXISTS_BOOKS_HTML}'
@app.get('/books/')
def get_books():
	return get_books_html()

@app.get('/books/', response_class=HTMLResponse)
def get_books(response: Response):
	response.headers["Content-Type"] = "text/html"
	# 返回BOOKS_JSON，去掉首尾的双引号
	return BOOKS_JSON[1:-1]

# 定义POST方法，/add_book/，接收一个int型参数book_id，用于添加书籍
@app.post('/add_book/{book_id}')
def add_book(book_id: int):
	# 从BOOKS中获取book_id对应的书籍，如果不存在，则返回None
	book = next((book for book in BOOKS if book['id'] == book_id), None)
	# 如果book为None，则返回404
	if book is None:
		raise HTTPException(status_code=404, detail='Book not found')

	filename = get_book_json_file(book_id)

	# 判断books目录有没有以book_id加后缀.json的文件，如果没有则创建，如果有则忽略
	if not os.path.exists(filename):
		# 增加整数型属性like，值为0
		book['like'] = 0
		# 将book转为JSON，赋值给book_json
		book_json = json.dumps(book, ensure_ascii=False)

		# 将book_json写入books目录下以book_id加后缀.json的文件
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(book_json)

	# 如果book不为None，则返回book
	return book

# 定义PUT方法，/like_book/，接收一个int型参数book_id，用于点赞书籍（每次加1）
@app.put('/like_book/{book_id}')
def like_book(book_id: int):
	# 先调用add_book方法，如果book_id对应的书籍不存在，则会创建
	book = add_book(book_id)
	# 如果book为None，则返回404
	if book is None:
		raise HTTPException(status_code=404, detail='Book not found')

	# 从books目录下以book_id加后缀.json的文件中读取数据，like加1后写回文件
	filename = get_book_json_file(book_id)
	book = None
	# 先读取，再覆盖式写入
	with open(filename, 'r', encoding='utf-8') as f:
		book = json.load(f)

	with open(filename, 'w', encoding='utf-8') as f:
		book['like'] += 1
		book_json = json.dumps(book, ensure_ascii=False)
		f.write(book_json)

	return book

# 定义DELETE方法，/remove_book/，接收一个int型参数book_id，用于删除书籍
@app.delete('/remove_book/{book_id}')
def remove_book(book_id: int):
	# 从BOOKS中获取book_id对应的书籍，如果不存在，则返回None
	book = next((book for book in BOOKS if book['id'] == book_id), None)
	# 如果book为None，则返回404
	if book is None:
		raise HTTPException(status_code=404, detail='Book not found')

	# 从books目录下以book_id加后缀.json的文件中删除
	filename = get_book_json_file(book_id)
	if os.path.exists(filename):
		os.remove(filename)

	return book

# 定义PATCH方法，/unlike_book/，接收一个int型参数book_id，用于更新书籍
@app.patch('/unlike_book/{book_id}')
def unlike_book(book_id: int):
	# 从BOOKS中获取book_id对应的书籍，如果不存在，则返回None
	book = next((book for book in BOOKS if book['id'] == book_id), None)
	# 如果book为None，则返回404
	if book is None:
		raise HTTPException(status_code=404, detail='Book not found')

	# 从books目录下以book_id加后缀.json的文件中读取数据，like加1后写回文件
	filename = get_book_json_file(book_id)

	# 如果没有文件，则返回404
	if not os.path.exists(filename):
		raise HTTPException(status_code=404, detail='Book not found')

	# 先读取，再覆盖式写入
	with open(filename, 'r', encoding='utf-8') as f:
		book = json.load(f)
		book['like'] -= 1

	if book['like'] <= 0:
		os.remove(filename)
	else:
		with open(filename, 'w', encoding='utf-8') as f:
			book_json = json.dumps(book, ensure_ascii=False)
			f.write(book_json)

	return book


def get_book_json_file(book_id):
	filename = './books/' + str(book_id) + '.json'
	return filename