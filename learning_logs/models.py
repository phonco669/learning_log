from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):  #继承了Model——Django中一个定义了模型基本功能的类
    """用户学习的主题"""
    text = models.CharField(max_length = 200)  #属性text是一个CharField——由字符或文本组成的数据,且告诉Django该在数据库中预留200个字符
    date_added = models.DateTimeField(auto_now_add=True)  #我们传递了实参auto_now_add=True，每当用户创建新主题时，这都让Django将这个属性自动设置成当前日期和时间
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):  #需要告诉Django，默认应使用哪个属性来显示有关主题的信息。Django调用方法__str__()来显示模型的简单表示，如果你使用的是Python 2.7，应调用方法__unicode__()，而不是__str__()，但其中的代码相同
        """返回模型的字符串表示"""
        return self.text

class Entry(models.Model):  #Entry也继承了Django基类Model
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)  #第一个属性topic是一个ForeignKey实例,每个主题创建时，都给它分配了一个键（或ID）
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:  #在Entry类中嵌套了Meta类。Meta存储用于管理模型的额外信息，在这里，它让我们能够设置一个特殊属性，让Django在需要时使用Entries来表示多个条目。如果没有这个类， Django将使用Entrys来表示多个条目
        verbose_name_plural = 'entries'
    def __str__(self):
        """返回模型的字符串表示"""
        return self.text[:50]+"..."  #由于条目包含的文本可能很长，我们让Django只显示text的前50个字符
