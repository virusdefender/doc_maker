doc_maker
=========
一个基于Django的简单的生成api文档的工具。

 1. 输入url后自动获取和格式化数据。因为有了数据和url，以后返回值发生变化的时候，可以自动化的更新示例数据。
 2. 树形分类，默认全部折叠显示。
 3. 暂时只支持提交和获取json数据
 4. 初次使用请将doc_maker/settings.py里面的`API_BASE_URL`修改为实际地址，然后运行maker_main/view.py里面的create_data()创建根目录
