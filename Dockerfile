FROM ubuntu

RUN apt-get update && apt-get install -y python python-pip git
RUN pip install pandas pyinstaller
RUN echo "hiddenimports = ['pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.tslibs.nattype', 'pandas._libs.skiplist']" > /usr/local/lib/python2.7/dist-packages/PyInstaller/hooks/hook-pandas.py
RUN git clone https://github.com/Blexie/Accounts-Code-Generation
