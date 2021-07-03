# jQuery

```
https://www.cnblogs.com/yuanchenqi/articls/5663118.html
https://jquery.cuishifeng.cn/
```

- jQuery是一个快速的，简洁的javaScript库，使用户能更方便地处理HTML documents、events、实现动画效果，并且方便地为网站提供AJAX交互。
- jQuery还有一个比较大的优势是，它的文档说明很全，而且各种应用也说得很详细，同时还有许多成熟的插件可供选择。

## 引用jQuery

```html
<script src="jquery-3.5.1.js"></script>
```

## jQuery对象

`jQuery`或`$`

基本方法：`$(selector).action() `

## 选择器

+ 基本选择器：`$("*")` 、 `$("#id")`、` $(".class")`、` $("element") `、`$(".class,p,div")`

+ 层级选择器：`$(".outer div")`、`$(".outer>div")`、`$(".outer+div")`、`$(".outer~div")`

+ 基本筛选器：`$("li:first")`、`$("li:eq(2)")`、`$("li:even")`、`$("li:gt(1)")`

+ 属性选择器：`$('[id="div1"]')`、`$('[alex="sb"][id]')`

+ 表单选择器：`$("[type='text']")`、`$(":text")`(只适用于input标签)、`$("input:checked")`

## 筛选器

`$("li").eq(2)`、`$("li").first()`、`$("ul li").hasclass("test")`

`$("div").children(".test")`(儿子)、`$("div").find(".test")` (后代)

`$(".test").next()`、`$(".test").nextAll()`、`$(".test").nextUntil(".test1")`

`$("div").prev()`、`$("div").prevAll()`、`$("div").prevUntil(".test1")`

`$(".test").parent()`、`$(".test").parents()`、`$(".test").parentUntil() `

`$("div").siblings()`

## 属性操作

`$("p").text()`、`$("p").html()`、`$(":checkbox").val()`

`$(".test").attr("alex")`(取属性)、`$(".test").attr("alex","sb") `(设置属性)

`$(".test").attr("checked","checked")`、`$(":checkbox").removeAttr("checked")`

`$(".test").prop("checked",true)`(prop用于固有属性，attr用于所有属性)

`$(".test").addClass("hide")`

## CSS操作

+ 样式 `css("{color:'red',backgroud:'blue'}") `

+ 位置 `offset()`、`position()`、`scrollTop()`、`scrollLeft()   `

+ 尺寸 `height()`、`width()  `

## 文档处理

+ 内部插入 `$("#c1").append("<b>hello</b>")`、`$("p").appendTo("div")`、`prepend()`、`prependTo()`

+ 外部插入 `before()`、`insertBefore()`、`after()`、`insertAfter()`、`replaceWith()`、`remove()`、`empty()`、`clone()`

## 事件

`$(document).ready(function(){})`、`$(function(){})`

`$("p").click(function(){})`

`$("p").bind("click",function(){})`

`$("ul").delegate("li","click",function(){})`

## 动画效果

都可加回调函数

`show()`、`hide()`、`toggle()`

`fadeIn()`、`fadeOut()`、`fadeToggle()`、`fadeTo()`(加透明度)

`slideDown()`、`slideUp()`、`slideToggle()`

## 扩展

`jquery.extend({})`

```javascript
$.extend({
    getmax:function(a,b) {
        return a>b?a:b;
    }
})
alert($.getmax(5,8));
```

`jquery.fn.extend({})`

放在自执行函数中，防止自己定义的变量与别人的产生冲突。

```javascript
(function() {
    $.fn.extend({
        print:function() {
            console.log($(this).html);
        }
    });
})();
$("p").print();
```

## jQuery对象和DOM对象

```javascript
obj = document.getElementById('id') /*----转为jQuery对象---->*/ $(obj)
$('obj') /*----转为DOM对象---->*/ $('obj')[0]
```