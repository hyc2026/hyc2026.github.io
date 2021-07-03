# AJAX

```
https://www.cnblogs.com/yuanchenqi/articles/5997456.html
```

## JSON

JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式。JSON是用字符串来表示Javascript对象；前端接受到json字符串，就可以通过JSON.parse()等方法解析成json对象(即js对象)直接使用了。

JSON字符串内的值：

- 数字  （整数或浮点数）
- 字符串 （在双引号中）
- 逻辑值 （true 或 false）
- 数组   （在方括号中）
- 对象   （在花括号中，引号用双引）
- null  

undefined,NaN,{'name':'yuan'}等都不在json对象的范畴。

```javascript
var person = {"name":"alex",
              "sex":"men",
              "teacher":{
                 "name":"tiechui",
                  "sex":"half_men",
              },
              "bobby":['basketball','running'],

               "getName":function() {return 80;}
              };
alert(person.name);
alert(person.getName());
alert(person.teacher.name);
alert(person.bobby[0]);
```

### python与json对象的对应

```
python         -->        json
dict                      object
list,tuple                array
str,unicode               string
int,long,float            number
True                      true
False                     false
None                      null
```

### .parse()和.stringify()

```
parse() 用于从一个json字符串中解析出json对象,如
var str = '{"name":"yuan","age":"23"}'
结果：JSON.parse(str)     ------>  Object  {age: "23",name: "yuan"}

stringify()用于从一个json对象解析成json字符串，如
var c= {a:1,b:2} 
结果：  JSON.stringify(c)     ------>      '{"a":1,"b":2}'

注意1：单引号写在{}外，每个属性名都必须用双引号，否则会抛出异常。
注意2:
a={name:"yuan"};   //ok
b={'name':'yuan'}; //ok
c={"name":"yuan"}; //ok
alert(a.name);  //ok
alert(a[name]); //undefined
alert(a['name']) //ok
```

### django向js发送数据

```
def login(request):
    obj={'name':"alex111"}
    return render(request,'index.html',{"objs":json.dumps(obj)})
#----------------------------------
 <script>
     var temp={{ objs|safe }}
     alert(temp.name);
     alert(temp['name'])
 </script>
```

## AJAX概述

AJAX（Asynchronous Javascript And XML）翻译成中文就是“异步Javascript和XML”。即使用Javascript语言与服务器进行异步交互，传输的数据为XML（当然，传输的数据不只是XML）。

- 同步交互：客户端发出一个请求后，需要等待服务器响应结束后，才能发出第二个请求；
- 异步交互：客户端发出一个请求后，无需等待服务器响应结束，就可以发出第二个请求。

AJAX除了**异步**的特点外，还有一个就是：浏览器页面**局部刷新**；（这一特点给用户的感受是在不知不觉中完成请求和响应过程）

优点：

- AJAX使用Javascript技术向服务器发送异步请求；
- AJAX无须刷新整个页面；
- 因为服务器响应内容不再是整个页面，而是页面中的局部，所以AJAX性能高；

缺点：

- AJAX并不适合所有场景，很多时候还是要使用同步交互；
- AJAX虽然提高了用户体验，但无形中向服务器发送的请求次数增多了，导致服务器压力增大；
- 因为AJAX是在浏览器中使用Javascript技术完成的，所以还需要处理浏览器兼容性问题；

## AJAX技术

### 四步操作：

- 创建核心对象；
- 使用核心对象打开与服务器的连接；
- 发送请求
- 注册监听，**监听服务器响应。**

### XMLHTTPRequest

- open(请求方式, URL, 是否异步)
- send(请求体)
- onreadystatechange，指定监听函数，它会在xmlHttp对象的状态发生变化时被调用
- readyState，当前xmlHttp对象的状态，其中4状态表示服务器响应结束
- status：服务器响应的状态码，只有服务器响应结束时才有这个东东，200表示响应成功；
- responseText：获取服务器的响应体

## 基于JavaScript的AJAX实现

### 第一步：创建XMLHttpRequest对象

```javascript
function createXMLHttpRequest() {
    var xmlHttp;
    // 适用于大多数浏览器，以及IE7和IE更高版本
    try{
        xmlHttp = new XMLHttpRequest();
    } catch (e) {
        // 适用于IE6
        try {
            xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            // 适用于IE5.5，以及IE更早版本
            try{
                xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e){}
        }
    }            
    return xmlHttp;
}
```

### 第二步：调用open()方法打开与服务器的连接

open(method, url, async)：

- method：请求方式，通常为GET或POST；
- url：请求的服务器地址，例如：/ajaxdemo1/AServlet，若为GET请求，还可以在URL后追加参数；
- async：这个参数可以不给，默认值为true，表示异步请求；

```javascript
var xmlHttp = createXMLHttpRequest();
xmlHttp.open("GET", "/ajax_get/", true);
```

### 第三步：发送请求

```javascript
xmlhttp.send("name=alex") # 请求体的内容 POST
xmlhttp.send(null)        # GET
```

### 第四步：接收服务器响应

当请求发送出去后，服务器端Servlet就开始执行了，但服务器端的响应还没有接收到。接下来我们来接收服务器的响应。

XMLHttpRequest对象有一个onreadystatechange事件，它会在XMLHttpRequest对象的状态发生变化时被调用。下面介绍一下XMLHttpRequest对象的5种状态：

- 0：初始化未完成状态，只是创建了XMLHttpRequest对象，还未调用open()方法；
- 1：请求已开始，open()方法已调用，但还没调用send()方法；
- 2：请求发送完成状态，send()方法已调用；
- 3：开始读取服务器响应；
- 4：读取服务器响应结束。 

onreadystatechange事件会在状态为1、2、3、4时引发。

下面代码会被执行**四次**！对应XMLHttpRequest的四种状态！

```javascript
xmlHttp.onreadystatechange = function() {
    alert('hello');
};
```

获取服务器响应内容

```javascript
xmlHttp.onreadystatechange = function() {
	if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
		alert(xmlHttp.responseText);    
	}
};
```

**发送POST请求**

+ 需要设置请求头：xmlHttp.setRequestHeader(“Content-Type”, “application/x-www-form-urlencoded”)；注意 :form表单会默认这个键值对;不设定，Web服务器会忽略请求体的内容。

+ 在发送时可以指定请求体了：xmlHttp.send(“username=yuan&password=123”)

### 完整代码

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>注册</h1>
    <form action="" method="post">
        用户名：<input id="username" type="text" name="username" onblur="send()"/><span id="error"></span><br/>
        密　码：<input type="text" name="password"/><br/>
        <input type="submit" value="注册"/>
    </form>
</body>
<script type="text/javascript">
        function createXMLHttpRequest() {
            try {
                return new XMLHttpRequest();
            } catch (e) {
                try {
                    return new ActiveXObject("Msxml2.XMLHTTP");
                } catch (e) {
                    return new ActiveXObject("Microsoft.XMLHTTP");
                }
            }
        }

        function send() {
            var xmlHttp = createXMLHttpRequest();
            xmlHttp.onreadystatechange = function() {
                if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    if(xmlHttp.responseText == "true") {
                        document.getElementById("error").innerText = "用户名已被注册！";
                        document.getElementById("error").textContent = "用户名已被注册！";
                    } else {
                        document.getElementById("error").innerText = "";
                        document.getElementById("error").textContent = "";
                    }
                }
            };
            xmlHttp.open("POST", "/ajax_check/", true, "json");
            xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            var username = document.getElementById("username").value;
            xmlHttp.send("username=" + username);
        }
</script>
</html>
```

```python
from django.views.decorators.csrf import csrf_exempt

def login(request):
    print('hello ajax')
    return render(request,'index.html')
    # return HttpResponse('helloyuanhao')

@csrf_exempt
def ajax_check(request):
    print('ok')

    username=request.POST.get('username',None)
    if username=='yuan':
        return HttpResponse('true')
    return HttpResponse('false')
```

需要增加两个url： 一个调用login()进入页面，另一个为"/ajax_post/"绑定ajax_check()

```python
urlpatterns = [    path('ajax_check/', views.ajax_check),    path('login/', views.login),]
```

## 基于jQuery的AJAX实现

### 快捷API

```
<1>$.get(url, [data], [callback], [type])
<2>$.post(url, [data], [callback], [type])  //type: text|html|json|script
    //请求参数应该尽量放在data参数中，因为可以自动编码，手动拼接url要注意编码问题
    function testWithDataAndCallback() {
        $.get('/user/list', {type: 1}, function (data, callbacktype, jqXHR) {
            console.log(data);//将json字符串解析成json对象
        }); 回调参数的值是后端HTTPResponse返回的内容
    } jqXHR是XMLHttpRequest对象

<3>$.getScript()使用 AJAX 请求，获取和运行 JavaScript:
     应用：
     function testGetScript() {
            // alert(testFun(3, 4));
            $.getScript('test.js', function () {
                alert(add(1, 6));
            });
        }

    // test.js
    function add(a,b){
       return a+b
       }  

<4>$.getJSON()
   与$.get()是一样的，只不过就是做后一个参数type必须是json数据了。一般同域操作用$.get()就可以，$.getJson 最主要是用来进行jsonp跨域操作的。
```

### 核心API

```
<1>  $.ajax的两种写法：
    $.ajax("url",{})
    $.ajax({})
    
<2>  $.ajax的基本使用
    $.ajax({
        url:"//",
        data:{a:1,b:2},
        type:"GET",
        success:function(){}
    })

<3> 回调函数
$.ajax('/user/allusers', {
    success: function (data) {
    	console.log(arguments);
    },
	error: function (jqXHR, textStatus, err) {
        // jqXHR: jQuery增强的xhr
        // textStatus: 请求完成状态
        // err: 底层通过throw抛出的异常对象，值与错误类型有关
        console.log(arguments);
    },
    complete: function (jqXHR, textStatus) {
        // jqXHR: jQuery增强的xhr
        // textStatus: 请求完成状态 success | error
        console.log('statusCode: %d, statusText: %s', jqXHR.status, jqXHR.statusText);
        console.log('textStatus: %s', textStatus);
    },
    statusCode: {
        '403': function (jqXHR, textStatus, err) {
        	console.log(arguments);  //注意：后端模拟errror方式：HttpResponse.status_code=500
        },
        '400': function () {
        }
    }
});

<1> ----------请求数据相关: data, processData, contentType, traditional--------------
data: 当前ajax请求要携带的数据，是一个json的object对象，ajax方法就会默认地把它编码成某种格式(urlencoded:?a=1&b=2)发送给服务端；此外，ajax默认以get方式发送请求。
    # function testData() {
    #   $.ajax("/test",{     //此时的data是一个json形式的对象
    #      data:{
    #        a:1,
    #        b:2
    #      }      
    #   });                   //?a=1&b=2
processData：声明当前的data数据是否进行转码或预处理，默认为true，即预处理；if为false，
    # 那么对data：{a:1,b:2}会调用json对象的toString()方法，即{a:1,b:2}.toString()
    # ,最后得到一个［object，Object］形式的结果。   
    # {"1":"111","2":"222","3":"333"}.toString();//[object Object]
    # 该属性的意义在于，当data是一个dom结构或者xml数据时，我们希望数据不要进行处理，直接发过去，
    # 就可以讲其设为true。
contentType：默认值: "application/x-www-form-urlencoded"。发送信息至服务器时内容编码类型。
    # 用来指明当前请求的数据编码格式；urlencoded:?a=1&b=2；如果想以其他方式提交数据，
    # 比如contentType:"application/json"，即向服务器发送一个json字符串： 
    #   $.ajax("/ajax_get",{
    # 
    #      data:JSON.stringify({
    #           a:22,
    #           b:33
    #       }),
    #       contentType:"application/json",
    #       type:"POST",
    #       
    #   });                          //{a: 22, b: 33}
    # 注意：contentType:"application/json"一旦设定，data必须是json字符串，不能是json对象
 traditional：一般是我们的data数据有数组时会用到 ：data:{a:22,b:33,c:["x","y"]}, 
    # traditional为false会对数据进行深层次迭代；

<2> ------------------------ 响应数据: dataType、dataFilter------------------------
dataType：预期服务器返回的数据类型,服务器端返回的数据会根据这个值解析后，传递给回调函数。
    # 默认不需要显性指定这个属性，ajax会根据服务器返回的content Type来进行转换；比如我们的服务器响应的
    # content Type为json格式，这时ajax方法就会对响应的内容进行一个json格式的转换，if转换成功，我们在
    # success的回调函数里就会得到一个json格式的对象；转换失败就会触发error这个回调函数。如果我们明确地指
    # 定目标类型，就可以使用data Type。
    # dataType的可用值：html｜xml｜json｜text｜script
    # 见下dataType实例
dataFilter: 类型：Function 给 Ajax返回的原始数据的进行预处理的函数。见下dataFilter实例

<3> 请求类型 type：
    类型：String 默认值: "GET")。请求方式 ("POST" 或 "GET")， 默认为 "GET"。注意：其它 HTTP 请求方法，
    如 PUT 和 DELETE 也可以使用，但仅部分浏览器支持。

<4> 前置处理 beforeSend(XHR)
    类型：Function 发送请求前可修改 XMLHttpRequest 对象的函数，如添加自定义 HTTP 头。XMLHttpRequest 
    # 对象是唯一的参数。这是一个 Ajax 事件。如果返回 false 可以取消本次 ajax 请求。
    # 见下beforeSend实例
    
<5> jsonp  类型：String
    # 在一个 jsonp 请求中重写回调函数的名字。这个值用来替代在 "callback=?" 这种 GET 或 POST 请求中 URL 
    # 参数里的 "callback" 部分，比如 {jsonp:'onJsonPLoad'} 会导致将 "onJsonPLoad=?" 传给服务器。

<6> jsonpCallback  类型：String
    # 为 jsonp 请求指定一个回调函数名。这个值将用来取代 jQuery 自动生成的随机函数名。这主要用来让 jQuery 生
    # 成度独特的函数名，这样管理请求更容易，也能方便地提供回调函数和错误处理。你也可以在想让浏览器缓存 GET 请求
    # 的时候，指定这个回调函数名。
```

### JSON使用

```python
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def login(request):
    return render(request,'Ajax.html')

def ajax_get(request):
    l=['alex','little alex']
    dic={"name":"alex","pwd":123}
    #return HttpResponse(l)              # 元素直接转成字符串alexlittle alex
    #return HttpResponse(dic)            # 字典的键直接转成字符串namepwd
    return HttpResponse(json.dumps(l))
    return HttpResponse(json.dumps(dic)) # 传到前端的是json字符串,要想使用,需要JSON.parse(data)
```

```javascript
function testData() {
    $.ajax('ajax_get', {
        success: function (data) {
            console.log(data);
            console.log(typeof(data));
            //console.log(data.name);
            //JSON.parse(data);
            //console.log(data.name);
            },
        //dataType:"json",
    })
}
```

### csrf跨站请求伪造

```javascript
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});
```

## 跨域请求

### 同源策略机制

浏览器有一个很重要的概念——同源策略(Same-Origin Policy)。所谓同源是指，域名，协议，端口相同。不同源的客户端脚本(javascript、ActionScript)在没明确授权的情况下，不能读写对方的资源。

简单的来说，浏览器允许包含在页面A的脚本访问第二个页面B的数据资源，这一切是建立在A和B页面是同源的基础上。

如果Web世界没有同源策略，当你登录淘宝账号并打开另一个站点时，这个站点上的JavaScript可以跨域读取你的淘宝账号数据，这样整个Web世界就无隐私可言了。

### jsonp的js实现

JSONP是JSON with Padding的略称。可以让网页从别的域名（网站）那获取资料，即跨域读取数据。

它是一个非官方的协议，它允许在服务器端集成Script tags返回至客户端，通过javascript callback的形式实现跨域访问（这仅仅是JSONP简单的实现形式）。

```python
#---------------------------http://127.0.0.1:8001/login
def login(request):
    print('hello ajax')
    return render(request,'index.html')
#-----------------------------http://127.0.0.1:8002/get_byjsonp
def get_byjsonp(req):
    print('8002...')
    return HttpResponse('fun1("yuan")')
```

```html
<h1>发送JSONP数据</h1>
<script>
    function fun1(arg){
        alert("hello"+arg)
    }
</script>
<script src="http://127.0.0.1:8002/get_byjsonp/"></script>  //返回：<script>fun1("yuan")</script>
```

这其实就是JSONP的简单实现模式，或者说是JSONP的原型：**创建一个回调函数，然后在远程服务上调用这个函数并且将JSON 数据形式作为参数传递，完成回调**。

**将JSON数据填充进回调函数**，这应该就是JSONP的JSON+Padding的含义吧。

一般情况下，我们希望这个script标签能够动态的调用，而不是像上面因为固定在html里面所以没等页面显示就执行了，很不灵活。我们可以通过javascript动态的创建script标签，这样我们就可以灵活调用远程服务了。

```html
<button onclick="f()">submit</button>

<script>
    function addScriptTag(src){
     var script = document.createElement('script');
         script.setAttribute("type","text/javascript");
         script.src = src;
         document.body.appendChild(script);
         document.body.removeChild(script);
    }
    function fun1(arg){
        alert("hello"+arg)
    }
    function f(){
         addScriptTag("http://127.0.0.1:8002/get_byjsonp/")
    }
</script>
```

为了更加灵活，现在将你自己在客户端定义的回调函数的函数名传送给服务端，服务端则会返回以你定义的回调函数名的方法，将获取的json数据传入这个方法完成回调：

```html
<button onclick="f()">submit</button>

<script>
    function addScriptTag(src){
     var script = document.createElement('script');
         script.setAttribute("type","text/javascript");
         script.src = src;
         document.body.appendChild(script);
         document.body.removeChild(script);
    }
    function SayHi(arg){
        alert("Hello "+arg)
    }
    function f(){
         addScriptTag("http://127.0.0.1:8002/get_byjsonp/?callbacks=SayHi")
    }
</script>
```

```python
def get_byjsonp(req):
    func=req.GET.get("callbacks")
    return HttpResponse("%s('yuan')"%func)
```

### jsonp的jQuery实现

```
<script type="text/javascript">
    $.getJSON("http://127.0.0.1:8002/get_byjsonp?callback=?",function(arg){
        alert("hello"+arg)
    });
</script>
```

结果是一样的，要注意的是在url的后面必须添加一个callback参数，这样getJSON方法才会知道是用JSONP方式去访问服务，callback后面的那个问号是内部自动生成的一个回调函数名。

此外，如果说我们想指定自己的回调函数名，或者说服务上规定了固定回调函数名该怎么办呢？我们可以使用$.ajax方法来实现

```html
<script type="text/javascript" src="/static/jquery-2.2.3.js"></script>
<script type="text/javascript">
   $.ajax({
        url:"http://127.0.0.1:8002/get_byjsonp",
        dataType:"jsonp",
        jsonp: 'callbacks',
        jsonpCallback:"SayHi"
   });
    function SayHi(arg){
        alert(arg);
    }
</script>
```

```python
def get_byjsonp(req):
    callback=req.GET.get('callbacks')
    print(callback)
    return HttpResponse('%s("yuan")'%callback)
```

通过回调函数来处理：

```html
<script type="text/javascript" src="/static/jquery-2.2.3.js"></script>
<script type="text/javascript">
   $.ajax({
        url:"http://127.0.0.1:8002/get_byjsonp",
        dataType:"jsonp",   //必须有，告诉server，这次访问要的是一个jsonp的结果。
        jsonp: 'callbacks', //jQuery帮助随机生成的：callbacks="wner"
        success:function(data){
            alert(data)
        }
   });
</script>
```

```python
def get_byjsonp(req):
    callbacks=req.GET.get('callbacks')
    print(callbacks)                 #wner  
	return HttpResponse("%s('yuan')"%callbacks)
```

jsonp: 'callbacks'就是定义一个存放回调函数的键，jsonpCallback是前端定义好的回调函数方法名'SayHi'，server端接受callback键对应值后就可以在其中填充数据打包返回了; 

jsonpCallback参数可以不定义，jquery会自动定义一个随机名发过去，那前端就得用回调函数来处理对应数据了。

利用jQuery可以很方便的实现JSONP来进行跨域访问。

JSONP一定是GET请求

```html
<button onclick="f()">submit</button>

<script src="/static/jquery-1.8.2.min.js"></script>
<script type="text/javascript">
    function f(){
        $.ajax({
        url:"http://127.0.0.1:8002/get_byjsonp",
        dataType:"jsonp",
        jsonp: 'callbacks',
        success :function(data){        //传过来的数据会被转换成js对象
            console.log(data);          //Object {name: Array[2]}
            console.log(typeof data);   //object
            console.log(data.name)      //["alex", "alvin"]
        }
   });
    }
</script>
```

```python
def get_byjsonp(req):
    func=req.GET.get("callbacks")
    a=json.dumps({'name':('alex','alvin')})
    return HttpResponse("%s(%s)"%(func,a))
    # return HttpResponse("%s({'name':('alex','alvin')})"%func)
    # return HttpResponse("%s('hello')"%func)
    # return HttpResponse("%s([12,34])"%func)
    # return HttpResponse("%s(5)"%func)
```