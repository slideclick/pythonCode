# -*- coding:utf-8 -*-   
#中文注释   
#dosomething.py  
#每种语言都有类似的dosomething工程 至少我用过的c++ nodejs delphi objectivec我知道有

import sys

'''        别被这些红字吓住 这些都是注释 去掉全部注释 剩下的代码是50行 
           这可以知乎首发 别处没有的 不是copypaste来的 嘿嘿
           
           程序复杂了 下面的class A 

           1.可以放到一个文件中 例如 filea.py
             用 from filea import A  导入A

           2.可以放到一个目录中 例如 modulea
             用 from modulea import A  导入A
             modulea目录必须要有__init__.py 
             class A 代码可以放在里面
             modulea目录就是新的python库 你自己的
             嘿嘿 

           3.你如果有共享精神同时觉得自己的东西还不错
             愿意把自己的class A（自己的python库）和别人分享
             这有一篇 告诉你如何打包上传到pypi.python.org/pypi
             http://liluo.org/blog/2012/08/how-to-create-python-egg/
             以后别人就可以pip install modulea 安装你的库了
             （巴菲特不会干这事 你愿意把赚钱的绝招告诉别人吗？这些人都是赚钱偷着乐 ）

             到这步 你就是个真上路的python coder了
             吼吼
'''
class A:
 
    s1 = 333 #公共属性 
    __age = 0 #私有属性 __开头

    def __init__(self,age): #构造器 专有函数 __开头 __结尾
        self.__age=age
        return

    def __del__(self): #析够 专有函数 __开头 __结尾
        print 'destroyed'
        return #函数体没内容则必须有return 否则可有可无

    #private
    def __doSomething(self, s): #私有成员函数 __开头 无__结尾
        print self.__age #类内部访问私有属性 外部不可访问
        return            
    #public
    def doSomething(self, s): #公共成员函数
        self.__doSomething(s) #类内部访问私有成员函数 外部不可访问   
        print s

class AA(A):    #AA继承自A python如果是写后台程序 继承用的少 直接库中类的实例化多
                #delphi－objpascal xcode－objc这种写客户端设计UI控件的  
                #要有很多编码在标准UI组件的继承类上或者通过接口定制 
                #90%的工作在这块不为过
                #python少继承多直接实例化多
                #（这是python程序容易读 除了强制排版外的另一个原因） 
                #原因很简单
                #覆盖一个例如numpy的成员函数的难度要比改一个按钮的行为 难度大很多
                #或者说几乎不可能 因为这些函数多c/c++写的 你的python方法慢10倍
                #有些人好奇这个 确实以前没人搞明白 我把原因说清了 嘿嘿
                #如果说继承的主要目的是为了覆盖父类的成员函数也不为过
                #所以说python初学者从可视化编程开始不明智 
                #这个要涉及继承和接口 事件函数 回调 还无法集中主要矛盾和本质

    def doSomething(self, s): #公共成员函数 覆盖父类A的同名公共成员函数
        print '==='   
        print s
        print '==='
 
def doSomething(v):
    vv=v+1;
    return vv

def main():
 
    a=A(111) #对象a对类A实例化
    a.doSomething('222')  #调用对象的公共成员函数
    print a.s1 #访问对象的公共属性
    del a #授权垃圾回收销毁对象 python会自己处理必要时刻销毁（对象没引用了）
          #但是你后面的代码已经不能访问对象a了 你如果不写 del a 
          #python会在程序执行完统一销毁
          #java垃圾回收一样不是c＋＋那种即时销毁 这个是android跑多了卡顿的重要原因之一

    aa=AA(111) #对象aa对类AA实例化
    aa.doSomething('222') 
    del aa  

    print doSomething(444) #函数调用函数 同时被调用函数有返回值

'''
这写东西也行 如果只是这有内容 退化为命令行顺序执行
这个是过程式编程 上面class A那堆是面向对象编程
python和javascript是多范式语言 就是可以多种编程风格 

java是更加彻底的面向对象编程 不是函数型 过程式 编程语言
所以最简单的python helloworld是 print "helloworld" java要写一堆东西

c＋＋也是多范式语言 除了面向对象 也支持过程式 但它还一个有名的是范型式编程 很强大 

python支持面向对象 过程式 命令式 函数型 等多种编程风格
初学者 用面向对象 过程式 命令式（这50行代码都涉及了）够用了 可满足全部工作需求
以后熟悉了可以试探少许函数式编程风格（优点：适合并发开发 找bug容易 程序可以热更新 代码短）
python写函数式程序相对有些丑陋 也比较繁琐（相对erlang这种彻底的函数型语言） 参考用
guido（python发明人）解释过python主要不是一种函数型编程语言
（需要穿墙 搞it要先会穿墙 不会或者懒不愿意学 建议改行 
google英文技术资料的搜索／大数据引擎处理能力是百度的10倍＋）
http://python-history.blogspot.com/2009/04/origins-of-pythons-functional-features.html

'''
print '------------------------'

if __name__ == '__main__':
    main()