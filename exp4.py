import re

a = "go_url('http://news.tvchosun.com/site/data/html_dir/2022/07/12/2022071290160.html')"
a = "go_url('asdf')"
a = link = re.findall(r"""(?<=\(').*(?='\))""", a)
print(a)