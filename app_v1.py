import json
from enum import Enum

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

app = FastAPI()
# app.default_response_class = HTMLResponse
# app.encoding = "utf-8"

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
        <script>
            document.getElementsByTagName('html')[0].setAttribute('lang', localStorage.getItem('lang') || 'en' );
            function setLang(lang){{localStorage.setItem('lang', lang); window.location.reload();}}
        </script>
        <br /><br />
        <en>If you want to change the language, please click the button.</en>
        <zh_cn>如果您想切换语言，请点击下一行相应按钮。</zh_cn>
        <zh_tw>如果您想切換語言，請點擊下一行相應按鈕。</zh_tw>
        <br />
        <button type="button" onclick="setLang('en')"><en>En</en><zh_cn>Chinese</zh_cn><zh_tw>Traditional</zh_tw></button>
        <button type="button" onclick="setLang('zh_cn')"><en>英语</en><zh_cn>简体</zh_cn><zh_tw>繁体</zh_tw></button>
        <button type="button" onclick="setLang('zh_tw')"><en>英語</en><zh_cn>簡體</zh_cn><zh_tw>繁體</zh_tw></button>
    </body>
</html>
'''


def read_contact_info():
	global PHONE_INFO_TEL_HTML
	global EMAIL
	# 启动时预读static/contactInfo.json，于后续的API调用中直接返回
	with open('static/contactInfo.json', 'r', encoding='utf-8') as f:
		CONTACT_INFO = json.load(f)

		email = CONTACT_INFO["email"]
		EMAIL = HTML_TEMPLATE.format("AnQi's Email", f'<a href="mailto:{email}" target="_blank">{email}</a>')

		PHONE_INFO = CONTACT_INFO['phones']
		# 进一步将这个数组转成多条tel:xxxxx的格式，嵌套到a标签中，最终合并成一个html字符串，方便前端直接使用
		PHONE_INFO_TEL = []
		for item in PHONE_INFO:
			'''
			"phone": "137*****404",
			"name": {
				"en": "AnQi",
				"chinese": "吴启萍",
				"traditional": "吳啟萍"
			},
			"kind": {
				"en": "feature phone",
				"zh_cn": "功能手机",
				"zh_tw": "功能手機"
			}
			'''
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
		# 以”AnQi's Phone“和'<br>'.join(PHONE_INFO_TEL)分别填充HTML_TEMPLATE中的两个{}，生成PHONE_INFO_TEL_HTML
		PHONE_INFO_TEL_HTML = HTML_TEMPLATE.format("AnQi's Phone", '<br>'.join(
			PHONE_INFO_TEL))  # 优化上一句，直接使用f-string  # PHONE_INFO_TEL_HTML = HTML_TEMPLATE.replace('%', "AnQi's Phone").replace('%', f'<br>{'<br>'.join(PHONE_INFO_TEL)}')


read_contact_info()

''' v0.1 Normal json: {'Hello': 'World'}
@app.get('/')
def read_root():
    return {'Hello': 'World'}
'''

''' v0.2 HTML: <html><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no,viewport-fit=cover,minimal-ui"><title>AnQi's resume Demo(python3.9 + FastAPI + REST API)</title><link rel="icon" href="favicon.ico" /></head><body><a href="en/" target="_blank">English</a><a href="zh_cn/" target="_blank">简体中文</a><a href="zh_tw/" target="_blank">繁體中文</a></body></html>
'''


@app.get('/', response_class=HTMLResponse)
def get_html(response: Response):
	# html_content = '''
	#     <html>
	#         <head>
	#             <meta charset="utf-8" />
	#             <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no,viewport-fit=cover,minimal-ui">
	#             <title>AnQi's resume Demo(python3.9 + FastAPI + REST API)</title>
	#             <link rel="icon" href="favicon.ico" />
	#         </head>
	#         <body>
	#             Resume:
	#             <a href="en/" target="_blank">English</a>
	#             <a href="zh_cn/" target="_blank">简体中文</a>
	#             <a href="zh_tw/" target="_blank">繁體中文</a>
	#         </body>
	#     </html>
	#     '''
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
                </zh_tw>
                ''')

	# html_content = '<html><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no,viewport-fit=cover,minimal-ui"><title>AnQi\'s resume Demo(python3.9 + FastAPI + REST API)</title><link rel="icon" href="favicon.ico" /></head><body><a href="en/" target="_blank">English</a>&nbsp;&nbsp;<a href="zh_cn/" target="_blank">简体中文</a>&nbsp;&nbsp;<a href="zh_tw/" target="_blank">繁體中文</a></body></html>'
	response.headers["Content-Type"] = "text/html"

	# response.headers["charset"] = "utf-8"
	# response.body = html_content
	# 转换编码html_content，解决中文乱码问题
	# return html_content.encode('utf-8')

	return html_content


'''
@app.get('/en/', response_class=HTMLResponse)
def get_en(response: Response):
    return get_html_content('./en.htm', response)

@app.get('/zh_cn/', response_class=HTMLResponse)
def get_en(response: Response):
    return get_html_content('zh_cn.htm', response)

@app.get('/zh_tw/', response_class=HTMLResponse)
def get_en(response: Response):
    return get_html_content('zh_tw.htm', response)

def get_html_content(html_filename, response):
    # 读取zh_tw.htm文件内容，以html格式返回
    with open(html_filename, 'r', encoding='utf-8') as f:
        html_content = f.read()
        response.headers["Content-Type"] = "text/html"
        return html_content
'''


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
	# 根据用户 ID 获取用户信息的逻辑 # GPT3.5原始代码
	# return {'user_id': user_id, 'name': 'John Doe'}

	# return users[user_id] # Copilot第一次推荐

	# print(user_id, (user for user in users if user['id'] == user_id))

	# 在users里面查找id为user_id的用户，如果找到就返回这个用户，如果找不到就返回None
	# return next((user for user in users if user['id'] == user_id), None)

	# 在users里面查找id为user_id的用户，如果找到就返回这个用户的名字，如果找不到就返回None
	return next((user['name'] for user in users if user['id'] == user_id), None)


# 定义一个关于名称的枚举类，用于指定名称的类型：中文名、英文名、佛教法名
class NameKind(Enum):
	English = 0
	Chinese = 1
	Traditional = 2
	Buddhist = 3


# 定义一个字典，用于存储不同类型的名称
names = {
	NameKind.English: 'AnQi', # 英文
	NameKind.Chinese: '吴启萍',  # 简体
	NameKind.Traditional: '吳啟萍',   # 繁体姓名
	NameKind.Buddhist: 'AnQi/安启/安啟/安啓', # 佛教法名安启，同时提供英文、简体中文、繁体中文，以/分隔
}
# get_names的本机测试网址
# http://127.0.0.1:8000/names/0
# http://127.0.0.1:8000/names/1
# http://127.0.0.1:8000/names/2
# http://127.0.0.1:8000/names/3
'''
fastapi.exceptions.FastAPIError: Invalid args for response field! Hint: check that <class 'app.NameKind'> is a valid Pydantic field type. If you are using a return t
ype annotation that is not a valid Pydantic field (e.g. Union[Response, dict, None]) you can disable generating the response model from the type annotation with the 
path operation decorator parameter response_model=None. Read more: https://fastapi.tiangolo.com/tutorial/response-model/
def get_names(name_kind: NameKind):
'''


@app.get('/name/{name_kind}')
def get_name(name_kind: int):
	# 把name_kind转为NameKind。如果它在字典里面，就返回对应的名称（只返回值）；如果不在就返回None
	# return {'name_kind': name_kind, 'name': names.get(NameKind(name_kind), None)}
	return names.get(NameKind(name_kind), None)


# 被我改lambda表达式了
# def get_name_kind(name):
#     name_lower = name.lower()
#     for kind in NameKind:
#         if kind.name.lower() == name_lower:
#             return kind
#     raise ValueError("Invalid name kind")

# 定义一个路径，用于获取名称，参数是字符串english, chinese, traditional, buddhist
@app.get('/name2/{name_kind}')
def get_name2(name_kind: str):
	# 把字符串转换成枚举类型
	# name_kind = NameKind[name_kind] # TypeError: 'type' object is not subscriptable

	# print(name_kind, name_kind.capitalize()) # english English
	# print(NameKind[name_kind.capitalize()]) # TypeError: 'type' object is not subscriptable

	# name_kind = name_kind.capitalize()
	# # 把name_kind转为NameKind枚举值
	# name_kind = NameKind[name_kind].enum
	# # name_kind = NameKind[name_kind.capitalize()]

	get_name_kind = lambda name: next((kind for kind in NameKind if kind.name.lower() == name.lower()), None)
	name_kind = get_name_kind(name_kind)  # get_name_kind(name_kind.lower())

	# 如果名称类型在字典里面，就返回对应的名称，如果不在就返回None
	return names.get(name_kind, None)


'''
@app.get('/phone/')
def get_phone():
	return PHONE_INFO
'''


@app.get('/phone/', response_class=HTMLResponse)
def get_phone(response: Response):
	response.headers["Content-Type"] = "text/html"
	return PHONE_INFO_TEL_HTML

@app.get('/email/', response_class=HTMLResponse)
def get_phone(response: Response):
	response.headers["Content-Type"] = "text/html"
	return EMAIL
