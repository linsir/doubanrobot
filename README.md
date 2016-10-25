# doubanrobot

A simple robot for douban.com

    .
    ├── doubanrobot.py  --by requests.
    ├── douban_urllib.py	-- by urllib/urllib2
    └── README.md

**Notice:** douban_urllib.py will never be updated.

## Usage

``` python
import doubanrobot

email = 'username@email.com'
password = 'password'

app = doubanrobot.DoubanRobot(email, password)

titile, content = app.get_joke()
print titile, content
if titile and content:
    print app.new_topic("cd", titile, content)

app.talk_status('hahahah, just for a test')
app.send_mail(63666378, 'Hallo, linsir.')
app.sofa("CentOS",['aaaa', 'bbbb', 'cccc'])
```