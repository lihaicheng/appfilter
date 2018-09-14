#使用


##运行
在文件appfilter.py中修改 `AppFilter("/Users/tangchris/Desktop/inputdirs","/Users/tangchris/Desktop/outputdirs")`,其中
第一个参数包含所有apk的文件夹，第二个参数为筛选出来的apk所存放的文件夹 

##配置及其他
1. 最大线程数：在`appfilter.py`中修改 `MAX_THREAD = 5` 这里表示支持最大的线程数量
2. 删除Apktool生成的中间文件：在`DELETE_TEMP_FOLDER` 表示是否删除由Apktool生成的中间文件
3. 请下载 apktool.jar（https://ibotpeaches.github.io/Apktool/install/） 并重命名为 `apktool.jar` 放在 `org.appfilter`文件夹下。 如需更改位置请修改 `singleapkparse.py::SingleAPKParse::def def parse(self)` (Line 60)中的命令

##编译
python 3.6

