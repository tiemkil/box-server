from flask import Flask, render_template, request, redirect
import Node.helper


app = Flask(__name__)

@app.route("/")
def readnode():
    '''
    首页
    :return:
    '''
    return render_template("index.html")

@app.route('/node', methods=['GET', 'POST'])
def get_node():
    '''
    获取node在线信息并返回
    :return:
    '''
    if request.method == 'POST':
        nodeid = request.form["nodeid"]
        node_info = Node.helper.get_nodeinfo(nodeid)
        return render_template('Node_info.html', node_info=node_info)

@app.route('/podlog', methods=['GET', 'POST'])
def get_podlog():
    if request.method == 'POST':
        nodeid = request.form["nodeid_for_log"]
        podlog = Node.helper.get_podlog(nodeid)
        print(podlog)
        return render_template('log_info.html', podlog=podlog)

if __name__ == '__main__':
    app.run(port=5000, debug=True)


