from sanic import Sanic
from sanic.response import json


app = Sanic(__name__)
device_list = ["94f6d61241aa"]


@app.route("/test/",methods=['GET','POST'])
async def test(request):

    device = None
    if request.method == 'POST':
        device =  request.form.get("device")
    else:
        device =  request.args.get("device")

    flag = False
    if device:
        if device in  device_list:
            flag = True
        else:
            flag = False
    else:
        flag = False

    print(device,flag)
    return json({ "flag": flag })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, auto_reload=True)