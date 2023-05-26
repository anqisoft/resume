import json
from enum import Enum

from fastapi import FastAPI, Response
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
                ''')

	response.headers["Content-Type"] = "text/html"

	return html_content


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
