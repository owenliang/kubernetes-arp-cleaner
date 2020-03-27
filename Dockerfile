FROM python:3.7

WORKDIR /root
COPY *.py requirements.txt ./
RUN pip3 install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD /usr/local/bin/python3 -u /root/arp_cleaner.py