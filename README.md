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

## Topics_Up function

This function help you to save time of manually posting a comment in order to **up** your **topic**. You can deploy this code on your `server`, such as `Linux VPS`

This function fecth all of your topics in your `douban group` homepage. The url of this page looks like this 

```
	https://www.douban.com/group/people/your_douban_id/publish
```

The variable `douban_id` should be filled in. You can find it in the above url or your douban homepage. 

Some people use charactor as their `douban_id`, however I just test the interge type `douban_id `, which is also the original format.


`topics_list` is a list of the interger part of your topics url 

```
	https://www.douban.com/group/topic/topic_id/
```

You can manually modify it, the example already given in the `code comment`.

In the end, `content` list contains all of your possible `comments`.

## Tips

You can also combine this script with Linux `crontab` to automaticlly up your topics in specific time. For example:

```
	0 8-24/4 * * * /usr/bin/python /root/doubanrobot.py
```

## Todo List

- [ ] Delete Comment
- [ ] Picture Example
