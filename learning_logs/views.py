from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry
from .forms import TopicForm,EntryForm


def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  #查询数据库获取所有Topic对象，按时间戳排序
    context = {'topics':topics}  #定义将要发送给模板的上下文。其中的context表示将要发送给模板的上下文（字典型数据，键是模板中用来访问数据的名称，值是要发送给模板的数据）
    return render(request,'learning_logs/topics.html',context)  #渲染网页。创建使用数据的网页时，除对象request和模板的路径之外，还需要context（上下文）

@login_required
def topic(request,topic_id):
    """显示单个主题及其所有条目"""
    # topic和entries被称为查询,向数据库查询特定的信息,可以先在Django shell中查询
    topic = Topic.objects.get(id=topic_id)
    #确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404

    # 根据topic查询与其相关的所有条目（外键）
    entries = topic.entry_set.order_by('-date_added')  # 减号表示降序,使得先显示最新的条目
    #查询数据库获取所有Topic对象，按时间戳排序
    context = {'topic':topic,'entries':entries}  #定义将要发送给模板的上下文。其中的context表示将要发送给模板的上下文（字典型数据，键是模板中用来访问数据的名称，值是要发送给模板的数据）
    return render(request,'learning_logs/topic.html',context)  #渲染网页。创建使用数据的网页时，除对象request和模板的路径之外，还需要context（上下文）

@login_required
def new_topic(request):
    """添加新主题"""

    if request.method != 'POST':  #未提交数据则创建一个新表单
        form  = TopicForm()  #创建一个新表单
    else:
        form = TopicForm(request.POST)  #对POST提交的数据进行处理
        if form.is_valid():  #核实用户是否填写了所有必不可少的字段，且输入符合要求
            new_topic = form.save(commit=False)  #保存表单到数据库
            new_topic.owner = request.user  #指定主题所属的用户
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form':form}  #将表单通过上下文字典发送给模板
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request, topic_id):
    '''在特定的主题中添加新条目'''

    # 从数据库根据主题的ID获取特定主题
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()  # 未提交数据，创建一个空表单
    else:
        # 根据POST提交的数据对数据进行处理
        form = EntryForm(data=request.POST)
        # 表单内容是否有效
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # 条目内容有效则创建新条目后回到主题页面
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    # GET请求或者POST请求的内容无效 则根据表单内容创建新页面
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request,entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)  #获取需要修改的条目对象以及相关的主题
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #初次请求时创建一个表单并使用当前条目填充表单：显示条目的现有信息
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))

    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)
