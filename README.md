2023年春季学期 零基础学编程期末作业 基于flask的论坛开发

主要代码来自flask的帮助文档

主要修改如下：

1.对大部分函数添加了注释

2.新增了对于敏感词的检索功能，系统会在用户在发帖和更改帖子内容的时候，检索主题和内容中的敏感词并替换

3.新增了在用户注册时，对密码的格式要求：至少6位，同时包含数字和字母

可考虑的修改如下：

1.对于前端部分的美化

2.登录之后，只建立了一个按照最新时间的排序索引，可以考虑搜索功能，或者更多的索引方式

3.博客可以分成诸多板块，即对帖子增加新的属性（分类），可以按照类别，将帖子放在不同的板块中

4.对于别人的帖子，除了浏览之外，应该还增加评论功能

存在的一些问题：

1.现在的帖子是直接显示在基础界面中的，并不存在点击这个事情，因此也就不存在点击量，因而没有办法根据点击量建立索引

2.同样的，因为帖子本身并不存在独立页面，评论功能的添加也需要进行一些考虑，毕竟将评论以及帖子内容全都直接显示在一个界面上显然是不合理的

简单来说，上述问题的问题核心在于，帖子本身并没有一个独立的界面，只需要单独写一个独立的界面就可以解决问题，但工作量不像目前做的这些这么小

3.对于前端界面的美化，不是很想单独设计一个UI，复杂而优秀的前端界面可能需要几百行甚至上千行代码实现