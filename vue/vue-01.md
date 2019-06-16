## 1.入门

### 1.1 数据绑定

1. 入口
   
   el为挂靠的入口， 在渲染模板中绑定到名称
``` js
<div id='app'> </div>

var app =  new Vue({
    el:document.getElementById('app) // or #app
})
```

2. vue

    在vue文件中实现代码逻辑，名字双向绑定到渲染模板
    
    data段中以字典形式返回数据

    created为初始化回调

    mounted为运行时回调

    beforeDsetoryed为销毁前回调

    在methods中实现方法

``` js

<div class="hello"></div>

export default {
  name: 'HelloWorld',

  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
    }
  },
  created () {
    console.log(this.name + 'created')
  },
  mounted () {
    console.log(this.name + 'mounted')
  },
  beforeDestroy () {
  },
  methods: {
  }
}
</script>
```

3. 插值,指令与事件

   - {{}}  双向绑定到值
   - v-html 将返回值值解释为纯文本，不进行html转义
   - v-pre 不对{{}}指定值进行编译
   - {{|}} 管道符，可执行过滤操作，可以连续串联
   - v-if 执行布尔运算
   - v-bind (v-bind:? 或 :? ) 动态更新标签属性
   - v-on (v-on:? 或 @?)绑定监视，可进行交互，如执行回调 click\dbclick\keyup\mousemove 等

``` js
  <div class="hello">
    <h1 v-if="show_time">{{ msg }}</h1>
    <h2>{{book}}</h2>
    <h3>date:{{date|formatDate}}</h3>
    <h3 v-html="link">superlink:</h3>
    <span v-pre>{{不会被编译}}}</span>
    <h2 v-if="show_time">Essential Links</h2>
    <div>
      {{number/10}}
      {{ok?'ok':'cancel'}}
      {{text.split(',').reverse().join(',')}}
    </div>
    <div id="test_link">
      <a v-bind:href="test_href">百度搜索</a>
      <img v-bind:src="test_img">
      <button v-on:click="handleClose">点击隐藏</button>
    </div>
  </div>

<script>
const padDate = function (value) {
  return value < 10 ? '0' + value : value
}

export default {
  name: 'HelloWorld',

  filters: {
    formatDate: function () {
      let date = new Date()
      let year = date.getFullYear()
      let month = padDate(date.getMonth() + 1)
      let day = padDate(date.getHours())
      let hours = padDate(date.getHours())
      let minutes = padDate(date.getMinutes())
      let seconds = padDate(date.getSeconds())

      return year + '-' + month + '-' + day + ' ' + hours + ':' +
        minutes + ':' + seconds
    }
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      book: 'science book',
      date: new Date(),
      link: '<a href="#">这是一个连接</a>',
      number: 100,
      ok: false,
      text: '123,456,789',
      show_time: false,
      test_href: 'https://www.baidu.com',
      test_img: 'https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/logo_white_fe6da1ec.png',
    }
  },
  created () {
    this.msg = 'nothing shit happens '
    console.log(this.name + 'created')
  },
  mounted () {
    console.log(this.name + 'mounted')
    let _this = this
    this.timer = setInterval(function () {
      _this.date = new Date()
    }, 1000)
  },
  beforeDestroy () {
    if (this.timer) {
      clearInterval(this.timer)
    }
  },
  methods: {
    handleClose: function () {
      this.show_time = !this.show_time
    }
  }
}
</script> 
```

4 .其他

- var似乎不再使用，用let 或 const 代替
- let _this = this
- filters
- 解决webstorm 格式化不符合 Eslint, 

    settings>editor>codestyle>html>other>do not indent children berod : script style
- 调试

    webstorm下run后修改代码可实时更新，不需要手动中断重启

### 1.2 计算属性
``` js
  methods: {},
  computed: {
    reverseText: function () {
      return this.text.split(',').reverse().join(',')
    }
  },
    text2: {
      get: function () {
        return ''
      },
      set: function (value) {
        console.log(value)
      }
    }

```

- 计算属性写在computed中
- 计算属性可以实现get和set函数
- computed与 methods 的区别

    computed有缓存，不一定更新，大数据量时建议使用， methods 每次调用都会 执行 


### 1.2 v-bind

- 对象语法
  ``` js
    <div :class="{'active':isActive}" />
  ```
    为真时渲染为class='active' ,为假时渲染为空

- 加载多个属性 
  ``` js
    <div class="static"  :class="{'active':isActive,'err':isErr}" />
  ```
    都为真时渲染为class='static active err'


- 数组语法
   ``` js
    <div :class="[activeCl, errCl]" />
    <div :class="[isActive:activeCl:'', errCl]" />
    <div :class="[{'active':isActive}, errCl]" />
  ```
    同时渲染，可使用三元表达式计算，可嵌套对象语法，可使用计算属性
