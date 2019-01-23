from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import *
import django.utils.timezone as timezone

from django.http import HttpResponse
import json
import urllib
import time
from datetime import datetime


# Create your views here.

def getpjlist(p):
    mlist = project.objects.all()
    nl = [m.name for m in mlist]
    nl.insert(0, p)
    return nl


def getdirtree(pjname):
    if pjname == "":
        return []
    d1 = directorytree.objects.filter(level=1, project=project.objects.get(name=pjname))
    d1_list = []
    for d in d1:
        tempdict = {}
        tempdict["name"] = d.name
        d2_list = []
        d2 = directorytree.objects.filter(parent=d.id)

        for d2_ in d2:
            # d3_list = []
            d3 = directorytree.objects.filter(parent=d2_.id)

            # d3_list.append()
            alist = []
            for d3_ in d3:
                tt = "-1"
                if testcase.objects.filter(belong=d3_.id):
                    tt = testcase.objects.get(belong=d3_.id).id
                alist.append({"value": d3_.name, "testcaseid": tt})

            d2_list.append({"name": d2_.name, "value": alist})

        tempdict["value"] = d2_list
        d1_list.append(tempdict)

    return d1_list
    # return HttpResponse(json.dumps(d1_list))


def my_view(request):
    print(request.user)
    if not request.user.is_authenticated():
        return True
    else:
        return False


def getpjname(request):
    p = request.COOKIES.get("project")
    if p:
        return urllib.request.unquote(p)
    return ""


def index(request):
    if (my_view(request)):
        return render(request, 'login.html', {"ts": " "})

    return render(request, 'index_my.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "dirlist": getdirtree(getpjname(request)),
                   "mydir": [{"path": "/", "name": "首页"}]})


def variable_detail(request, vid):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    if vid:
        print(vid)
        print("-" * 100)
        v = variable.objects.get(id=vid)
        variabledict = {"id": v.id, "name": v.name, "desc": v.desc, "type": v.type, "value": v.value, "mark": v.mark}
        return render(request, 'variable_detail_my.html',
                      {"projectlist": getpjlist(getpjname(request)),
                       "variabledatail": variabledict,
                       "dirlist": getdirtree(getpjname(request)),
                       "mydir": [{"path": "/", "name": "首页"},
                                 {"path": "/variable_detail/" + str(vid), "name": "新建变量"}]})

    its = itstatement.objects.all()

    # itslist= []
    # for it in its:
    #     apidict = {"id": it.id, "name": it.name,  "protocol_type": it.protocol_type,
    #            "request_type": it.request_type, "path": it.path, "responsible": it.responsible, "status": it.status}
    #
    #     itslist.append(apidict)

    return render(request, 'variable_detail_my.html',
                  {"projectlist": getpjlist(getpjname(request))})


def variable_new(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    if request.method == "POST":
        print("-" * 100)
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        type = request.POST.get("type")
        value = request.POST.get("value")
        mark = request.POST.get("mark")

        v = variable()
        v.type = type
        v.value = value
        v.mark = mark
        v.name = name
        v.desc = desc
        v.project = project.objects.get(name=getpjname(request))
        v.creator = request.user
        v.responsible = request.user
        v.timestamp = timezone.now()
        v.save()

        variabledict = {"id": v.id, "name": name, "desc": desc, "type": type, "value": value, "mark": mark}

        return render(request, 'variable_detail_my.html',
                      {"projectlist": getpjlist(getpjname(request)),
                       "variabledatail": variabledict,
                       "dirlist": getdirtree(getpjname(request)),
                       "mydir": [{"path": "/", "name": "首页"}, {"path": "/variable", "name": "资源配置"}]})

    pname = getpjname(request)
    p = project.objects.get(name=pname)
    v = itstatement.objects.filter(project=p)
    vlist = []
    for i in v:
        vdict = {}
        vdict["index"] = i.id
        vdict["name"] = i.name
        vdict["path"] = i.path
        vdict["request_type"] = i.request_type
        vdict["status"] = i.status
        vdict["responsible"] = i.responsible
        vdict["timestamp"] = i.timestamp
        vdict["expectres"] = i.expectres
        vdict["requestparam"] = i.requestparam
        vlist.append(vdict)

    return render(request, 'variable_new_my.html',
                  {"projectlist": getpjlist(getpjname(request)), "apilist": vlist,
                   "dirlist": getdirtree(getpjname(request)),
                   "mydir": [{"path": "/", "name": "首页"}, {"path": "/variable_new", "name": "新建变量"}]})


def variable_update(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    if request.method == "POST":
        print("-" * 100)
        id = request.POST.get("id")
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        type = request.POST.get("type")
        value = request.POST.get("value")
        mark = request.POST.get("mark")

        v = variable.objects.get(id=id)
        v.type = type
        v.value = value
        v.mark = mark
        v.name = name
        v.desc = desc
        # v.project = project.objects.get(name= getpjname(request)
        # v.creator = request.user
        # v.responsible = request.user
        v.timestamp = timezone.now()
        v.save()

        variabledict = {"id": v.id, "name": name, "desc": desc, "type": type, "value": value, "mark": mark}
        print("-" * 90)
        print(variabledict)
        print("-" * 90)
        return render(request, 'variable_detail_my.html',
                      {"projectlist": getpjlist(getpjname(request)),
                       "variabledatail": variabledict,
                       "dirlist": getdirtree(getpjname(request))})

    return render(request, 'variable_new_my.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "dirlist": getdirtree(getpjname(request))})


def base_addstep(request, tid):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})

    pname = getpjname(request)
    p = project.objects.get(name=pname)
    v = itstatement.objects.filter(project=p)
    vlist = []
    for i in v:
        vdict = {}
        vdict["index"] = i.id
        vdict["name"] = i.name
        vdict["path"] = i.path
        vdict["request_type"] = i.request_type
        vdict["status"] = i.status
        vdict["responsible"] = i.responsible
        vdict["timestamp"] = i.timestamp
        vdict["expectres"] = i.expectres
        vdict["requestparam"] = i.requestparam
        vlist.append(vdict)

    if tid == "-1":
        return render(request, 'base_addstep_my.html',
                      {"projectlist": getpjlist(getpjname(request)),
                       "dirlist": getdirtree(getpjname(request)),
                       "apilist": vlist, "tid": tid,
                       "tlist": [], "mydir": [{"path": "/", "name": "首页"}, {"path": " ", "name": "当前测试没有绑定目录"}]})

    tlist = []
    tcstep = testcasestep.objects.filter(tc=testcase.objects.get(id=tid))

    for t in tcstep:
        tempdict = {}
        tempdict["index"] = t.id
        tempdict["name"] = t.name
        # its = itstatement.objects.get(id=t.it.id)
        tempdict["apiname"] = t.it.name
        tempdict["request_type"] = t.it.request_type
        tempdict["requestparam"] = t.it.requestparam
        tempdict["expectres"] = t.it.expectres
        tempdict["path"] = t.it.path
        tlist.append(tempdict)

    # 得到当前的目录信息
    tc1 = testcase.objects.get(id=tid)

    alist = []

    dt = tc1.belong
    parent1 = dt.parent
    name1 = dt.name

    while parent1 > 0:
        print("-" * 100)
        print(parent1)
        dt = directorytree.objects.get(id=parent1)
        alist.insert(0, {"path": " ", "name": dt.name})
        parent1 = dt.parent

    alist.append({"path": "/base_addstep/" + str(tid), "name": name1})
    alist.insert(0, {"path": "/", "name": "首页"})

    return render(request, 'base_addstep_my.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "dirlist": getdirtree(getpjname(request)),
                   "apilist": vlist,
                   "tid": tid, "tlist": tlist, "mydir": alist})


def api_detail_respone(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    return render(request, 'api_detail_respone.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "dirlist": getdirtree(getpjname(request))})


def api_detail_request(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    return render(request, 'api_detail_my.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "dirlist": getdirtree(getpjname(request))})


def api_new(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    if request.method == "POST":
        name = request.POST.get("name")
        protocol_type = request.POST.get("protocol_type")
        request_type = request.POST.get("request_type")
        path = request.POST.get("path")
        desc = request.POST.get("desc")
        fzr = request.POST.get("fzr")
        expectres = request.POST.get("expectres")
        requestparam = request.POST.get("requestparam")

        its = itstatement()
        its.desc = desc
        its.name = name
        its.timestamp = timezone.now()
        its.path = path
        its.protocol_type = protocol_type
        its.request_type = request_type
        its.responsible = User.objects.get(username=fzr)
        its.project = project.objects.get(name=getpjname(request))
        its.status = "未开始"
        its.creator = request.user
        its.expectres = expectres
        its.requestparam = requestparam
        its.save()

        apidict = {"id": its.id, "name": its.name, "desc": its.desc, "protocol_type": its.protocol_type,
                   "request_type": its.request_type, "path": its.path, "responsible": its.responsible,
                   "status": its.status, "expectres": its.expectres}

        return render(request, 'api_detail_my.html',
                      {"projectlist": getpjlist(getpjname(request)),
                       "apidatail": apidict,
                       "dirlist": getdirtree(getpjname(request)),
                       "mydir": [{"path": "/", "name": "首页"}, {"path": "/api_new", "name": "创建接口"}]})

    al = User.objects.all()
    responsible_list = [a.username for a in al]
    return render(request, 'api_new_my.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "responsible_list": responsible_list,
                   "dirlist": getdirtree(getpjname(request)),
                   "mydir": [{"path": "/", "name": "首页"}, {"path": "/api_new", "name": "创建接口"}]})


def api_update(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        protocol_type = request.POST.get("protocol_type")
        request_type = request.POST.get("request_type")
        path = request.POST.get("path")
        desc = request.POST.get("desc")
        # responsible = request.POST.get("responsible")
        status = request.POST.get("status")
        expectres = request.POST.get("expectres")
        # requestparam = request.POST.get("requestparam")

        its = itstatement.objects.get(id=id)
        its.desc = desc
        its.name = name
        # its.timestamp = timezone.now()
        its.path = path
        its.protocol_type = protocol_type
        its.request_type = request_type
        # its.responsible = User.objects.get(username=responsible)
        # its.project = project.objects.get(name= getpjname(request)
        its.status = status
        # its.creator = request.user
        its.expectres = expectres
        # its.requestparam = requestparam
        its.save()

        apidict = {"id": its.id, "name": its.name, "desc": its.desc, "protocol_type": its.protocol_type,
                   "request_type": its.request_type, "path": its.path, "responsible": its.responsible,
                   "status": its.status, "expectres": its.expectres}

        return render(request, 'api_detail_my.html',
                      {"projectlist": getpjlist(getpjname(request)),
                       "apidatail": apidict,
                       "dirlist": getdirtree(getpjname(request))})


def ctrl(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    pname = getpjname(request)
    p = project.objects.get(name=pname)

    v = variable.objects.filter(project=p)
    vlist = []
    for i in v:
        vdict = {}
        vdict["index"] = i.id
        vdict["name"] = i.name
        vdict["type"] = i.type
        vdict["mark"] = i.mark
        vdict["pname"] = pname
        vdict["creator"] = i.creator
        vdict["timestamp"] = i.timestamp
        vlist.append(vdict)

    return render(request, 'variable_my.html',
                  {"projectlist": getpjlist(getpjname(request)), "vlist": vlist,
                   "dirlist": getdirtree(getpjname(request)),
                   "mydir": [{"path": "/", "name": "首页"}, {"path": "/variable", "name": "资源配置"}]})


def deal_result(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})
    return render(request, 'deal_result.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "dirlist": getdirtree(getpjname(request))})


def api_ctrl(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})

    pname = getpjname(request)
    p = project.objects.get(name=pname)

    v = itstatement.objects.filter(project=p)
    vlist = []
    for i in v:
        vdict = {}
        vdict["index"] = i.id
        vdict["name"] = i.name
        vdict["path"] = i.path
        vdict["request_type"] = i.request_type
        vdict["status"] = i.status
        vdict["responsible"] = i.responsible
        vdict["timestamp"] = i.timestamp
        vlist.append(vdict)

    return render(request, 'api_ctrl_my.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "itstatementlist": vlist,
                   "dirlist": getdirtree(getpjname(request)),
                   "mydir": [{"path": "/", "name": "首页"}, {"path": "/api_ctrl", "name": "接口管理"}]})


def api_detail(request, aid):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})

    h = itheader.objects.filter(it=itstatement.objects.get(id=aid), header_type=0)
    alist = []
    for x in h:
        adict = {}
        adict["id"] = x.id
        adict["name"] = x.name
        adict["value"] = x.value
        adict["desc"] = x.desc
        alist.append(adict)

    h = itbody.objects.filter(it=itstatement.objects.get(id=aid), body_type=0)
    blist = []
    for x in h:
        adict = {}
        adict["id"] = x.id
        adict["name"] = x.name
        adict["value"] = x.value
        adict["desc"] = x.desc
        adict["type"] = x.type
        blist.append(adict)

    h = itheader.objects.filter(it=itstatement.objects.get(id=aid), header_type=1)
    clist = []
    for x in h:
        adict = {}
        adict["id"] = x.id
        adict["name"] = x.name
        adict["value"] = x.value
        adict["desc"] = x.desc
        clist.append(adict)

    h = itbody.objects.filter(it=itstatement.objects.get(id=aid), body_type=1)
    dlist = []
    for x in h:
        adict = {}
        adict["id"] = x.id
        adict["name"] = x.name
        adict["value"] = x.value
        adict["desc"] = x.desc
        adict["type"] = x.type
        dlist.append(adict)

    if aid:
        v = itstatement.objects.get(id=aid)
        apidict = {"id": v.id, "name": v.name, "desc": v.desc, "protocol_type": v.protocol_type,
                   "request_type": v.request_type, "path": v.path, "responsible": v.responsible, "status": v.status,
                   "expectres": v.expectres}

        return render(request, 'api_detail_my.html',
                      {"projectlist": getpjlist(getpjname(request)),
                       "apidatail": apidict,
                       "dirlist": getdirtree(getpjname(request)), "aid": aid,
                       "req_header": alist, "req_body": blist,
                       "res_header": clist,
                       "res_body": dlist,
                       "mydir": [{"path": "/", "name": "首页"}, {"path": "/api_detail/" + str(aid), "name": "接口详情"}]})

    return render(request, 'api_detail_my.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "dirlist": getdirtree(getpjname(request)), "aid": aid,
                   "req_header": alist, "req_body": blist, "res_header": clist, "res_body": dlist})


def login_(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not len(str(username)) or not len(str(password)):
            return render(request, 'login.html', {"ts": "请填写账号，密码"})

        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                login(request, user)

                if request.COOKIES.get("project"):
                    return render(request, 'index_my.html',
                                  {"projectlist": getpjlist(getpjname(request)),
                                   "dirlist": getdirtree(getpjname(request))})
                else:
                    return render(request, 'index_my.html',
                                  {"projectlist": [],
                                   "dirlist": []})


            else:
                print("The password is valid, but the account has been disabled!")
                return render(request, 'login.html',
                              {"ts": "The password is valid, but the account has been disabled!"})
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
            return render(request, 'login.html', {"ts": "The username and password were incorrect."})

    return render(request, 'login.html', {"ts": " "})


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_ = request.POST.get("password_")
        email = request.POST.get("email")

        if not len(str(username)) or not len(str(password)):
            return render(request, 'signup.html', {"ts": "请填写账号，密码"})

        if not password == password_:
            return render(request, 'signup.html', {"ts": "两次密码不等"})

        if User.objects.filter(username=username):
            return render(request, 'signup.html', {"ts": "账户已存在，请登录"})

        user = User.objects.create_user(username, email, password)
        user.save()

        return render(request, 'signup.html', {"ts": "注册成功请登录"})

    return render(request, 'signup.html', {"ts": " "})


def logout_view(request):
    # if my_view(request):
    #     return render(request, 'login.html', {"ts": " "})
    logout(request)
    return render(request, 'login.html', {"ts": " "})
    # Redirect to a success page.


def new_project(request):
    if request.user.is_authenticated():
        p = project()
        p.name = request.POST.get("name")
        p.desc = request.POST.get("desc")
        p.user = request.user

        p.save()

        return HttpResponse("success")
    else:
        return HttpResponse("error")


def apitest_post(request):
    if request.method == "POST":
        return HttpResponse(json.dumps({'methed': 'POST', "a": 213}))


def apitest_get(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({"a": 213}))


def getLevel3(request):
    if request.method == "POST":
        # 拿到当前项目下面的所有路径，拿到 对于的testcase
        dt = directorytree.objects.filter(level=3, project=project.objects.get(
            name=getpjname(request)))
        llist = []
        for d in dt:
            t = testcase.objects.filter(belong=d)
            if t:
                llist.append({"name": d.name, "id": t[0].id})
        # llist = [{"name": d.name, "id": d.id} for d in dt if testcase.objects.filter(belong=d)]

        return HttpResponse(json.dumps(llist))


def getparentlevel(request):
    if request.method == "POST":
        level = request.POST.get("level")

        level = int(level) - 1

        if level < 1:
            return HttpResponse(
                json.dumps([{"name": getpjname(request), "id": -1}]))

        dt = directorytree.objects.filter(level=level, project=project.objects.get(
            name=getpjname(request)))
        llist = [{"name": d.name, "id": d.id} for d in dt if not testcase.objects.filter(belong=d)]
        # print("-" * 100)
        # print(llist)
        # print("-" * 100)

        return HttpResponse(json.dumps(llist))


def newylj(request):
    # "level": level, "name": name, "key": key, "parent": parent
    if request.method == "POST":
        level = request.POST.get("level")
        name = request.POST.get("name")

        print("-" * 100)
        print(name)
        print("-" * 100)

        # key = request.POST.get("key")
        parent = request.POST.get("parent")

        d = directorytree()
        d.name = name
        d.level = level
        d.project = project.objects.get(name=getpjname(request))
        d.parent = parent
        d.key = "none"
        d.save()

        return HttpResponse("成功")


def newtestcase(request):
    if request.method == "POST":
        name = request.POST.get("name")
        tree = request.POST.get("tree")
        tags = request.POST.get("tags")

        responsible_id = request.POST.get("responsible")

        if testcase.objects.filter(belong=tree):
            t = testcase.objects.get(belong=tree)
        else:
            t = testcase()

        t.name = name
        t.belong = directorytree.objects.get(id=tree)
        t.tags = tags
        t.status = "no start"
        t.author = request.user
        t.timestamp = timezone.now()
        t.responsible = User.objects.get(id=responsible_id)
        t.save()

        return HttpResponse("成功")


def responsible_list(request):
    al = User.objects.all()
    responsible_list = [{"name": a.username, "id": a.id} for a in al]
    return HttpResponse(json.dumps(responsible_list))


def addtestcasestep(request):
    if request.method == "POST":
        tid = request.POST.get("tid")
        if tid == "-1":
            return HttpResponse("地址没有绑定测试，请在新建测试绑定")
        stepname = request.POST.get("stepname")
        aid = request.POST.get("aid")

        t = testcasestep()
        t.name = stepname
        t.tc = testcase.objects.get(id=int(tid))
        t.index = 100
        t.it = itstatement.objects.get(id=aid)

        t.save()

        return HttpResponse("成功")


def new_its_req_header(request):
    if request.method == "POST":
        name = request.POST.get("name")
        value = request.POST.get("value")
        desc = request.POST.get("desc")
        type_ = request.POST.get("type")
        aid = request.POST.get("aid")
        headertype = request.POST.get("headertype")
        # req_body_format = request.POST.get("req_body_format")
        # req_body_type =  request.POST.get("req_body_type")

        h = itheader()
        h.name = name
        h.desc = desc
        h.value = value
        h.type = type_
        h.it = itstatement.objects.get(id=aid)
        # h.req_body_format = req_body_format
        # h.body_type = req_body_type
        h.header_type = headertype
        h.save()

        return HttpResponse("成功")


def new_its_req_body(request):
    if request.method == "POST":
        name = request.POST.get("name")
        value = request.POST.get("value")
        desc = request.POST.get("desc")
        type_ = request.POST.get("type")
        aid = request.POST.get("aid")
        # headertype = request.POST.get("headertype")
        req_body_format = request.POST.get("req_body_format")
        req_body_type = request.POST.get("req_body_type")

        h = itbody()
        h.name = name
        h.desc = desc
        h.value = value
        h.type = type_
        h.it = itstatement.objects.get(id=aid)
        h.body_format = req_body_format
        h.body_type = req_body_type
        h.upload_file = "none"
        # h.header_type = headertype
        h.save()

        return HttpResponse("成功")


def new_its_res_header(request):
    if request.method == "POST":
        name = request.POST.get("name")
        value = request.POST.get("value")
        desc = request.POST.get("desc")
        # type_ = request.POST.get("type")
        aid = request.POST.get("aid")
        headertype = request.POST.get("headertype")
        # req_body_format = request.POST.get("req_body_format")
        # req_body_type =  request.POST.get("req_body_type")

        h = itheader()
        h.name = name
        h.desc = desc
        h.value = value
        # h.type = type_
        h.it = itstatement.objects.get(id=aid)
        # h.req_body_format = req_body_format
        # h.body_type = req_body_type
        h.header_type = headertype
        h.save()

        return HttpResponse("成功")


def new_its_res_body(request):
    if request.method == "POST":
        name = request.POST.get("name")
        value = request.POST.get("value")
        desc = request.POST.get("desc")
        type_ = request.POST.get("type")
        aid = request.POST.get("aid")
        # headertype = request.POST.get("headertype")
        req_body_format = request.POST.get("req_body_format")
        req_body_type = request.POST.get("req_body_type")

        h = itbody()
        h.name = name
        h.desc = desc
        h.value = value
        h.type = type_
        h.it = itstatement.objects.get(id=aid)
        h.body_format = req_body_format
        h.body_type = req_body_type
        h.upload_file = "none"
        # h.header_type = headertype
        h.save()

        return HttpResponse("成功")


def run_testsuit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        tid = request.POST.get("tid")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        passednum = request.POST.get("passednum")
        skippednum = request.POST.get("skippednum")
        failednum = request.POST.get("failednum")

        start_time = start_time[4:-18]
        start_time = datetime.strptime(start_time, "%b %d %Y %H:%M:%S")
        print("-" * 100)
        print(start_time)

        end_time = end_time[4:-18]
        end_time = datetime.strptime(end_time, "%b %d %Y %H:%M:%S")

        ts = testsuite()
        ts.name = name
        ts.start_time = start_time
        ts.end_time = end_time
        ts.runner = request.user
        ts.rerun = 0
        ts.testcase = testcase.objects.get(id=tid)
        ts.passednum = passednum
        ts.failednum = failednum
        ts.skippednum = skippednum
        ts.save()

        return HttpResponse(ts.id)


def showtestsuit(request, sid):
    if (my_view(request)):
        return render(request, 'login.html', {"ts": " "})

    ts = testsuite.objects.get(id=sid)

    return render(request, 'show_testsuit_my.html',
                  {"projectlist": getpjlist(getpjname(request)),
                   "dirlist": getdirtree(getpjname(request)),
                   "mydir": [{"path": "/", "name": "首页"}],
                   "testsuitlist": {"name": ts.name, "runner": ts.runner, "start_time": ts.start_time,
                                    "end_time": ts.end_time, "time": ts.end_time - ts.start_time,
                                    "totle": ts.passednum + ts.skippednum + ts.failednum,
                                    "passednum": ts.passednum, "skippednum": ts.skippednum,
                                    "failednum": ts.failednum, "precent": ts.passednum / (
                       ts.passednum + ts.skippednum + ts.failednum + 0.001) * 100}})


def updateStatus(request):
    if my_view(request):
        return render(request, 'login.html', {"ts": " "})

    if request.method == "POST":
        sid = request.POST.get("sid")
        status = request.POST.get("status")

        mit = testcasestep.objects.get(id=sid).it
        mit.status = status
        mit.save()

        return HttpResponse("成功")
