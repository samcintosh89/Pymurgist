from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL
import sys
import design
import urllib2
import json
import time

class getPostsThread(QThread):
    def __init__(self, subreddits):
        QThread.__init__(self)
        self.subreddits = subreddits

    def __del__(self):
        self.wait()

    def _get_top_post(self, subreddit):
        url = "https://www.reddit.com/r/{}.json?limit=1".format(subreddit)
        headers = {'User-Agent': 'nikolak@outlook.com tutorial code'}
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        data = json.load(response)
        top_post = data['data']['children'][0]['data']
        return "'{title}' by {author} in {subreddit}".format(**top_post)

    def run(self):
        for subreddit in self.subreddits:
            top_post = self._get_top_post(subreddit)
            self.emit(SIGNAL('add_post(QString)'), top_post)
            self.sleep(2)

class ThreadingTutorial(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.btn_start.clicked.connect(self.start_getting_top_posts)

    def start_getting_top_posts(self):
        subreddit_list = str(self.edit_subreddits.text()).split(',')
        if subreddit_list == ['']: 
            QtGui.QMessageBox.critical(self, "No subreddits",
                                       "You didn't enter any subreddits.",
                                       QtGui.QMessageBox.Ok)
            return
        self.progress_bar.setMaximum(len(subreddit_list))
        self.progress_bar.setValue(0)
        self.get_thread = getPostsThread(subreddit_list)
        self.connect(self.get_thread, SIGNAL("add_post(QString)"), self.add_post)
        self.connect(self.get_thread, SIGNAL("finished()"), self.done)
        self.get_thread.start()
        self.btn_stop.setEnabled(True)
        self.btn_stop.clicked.connect(self.get_thread.terminate)
        self.btn_start.setEnabled(False)

    def add_post(self, post_text):
        self.list_submissions.addItem(post_text)
        self.progress_bar.setValue(self.progress_bar.value()+1)

    def done(self):
        self.btn_stop.setEnabled(False)
        self.btn_start.setEnabled(True)
        self.progress_bar.setValue(0)
        QtGui.QMessageBox.information(self, "Done!", "Done fetching posts!")



def main():
    app = QtGui.QApplication(sys.argv)
    form = ThreadingTutorial()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()