from django.shortcuts import render, get_object_or_404, redirect
from .models import DevTool
from .forms import DevToolForm

# Create your views here.
def tool_list(request):
    tools = DevTool.objects.all().order_by('-id')
    return render(request, 'tools/list.html', {'tools':tools})

def tool_detail(request, pk):
    tool = get_object_or_404(DevTool, pk=pk)
    related_ideas = tool.ideas.all()
    return render (request, 'tools/detail.html', {'tool': tool, 'related_ideas': related_ideas})

def tool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            tool = form.save()
            return redirect('tool_detail',pk = tool.pk)
    else:
            form = DevToolForm()
    return render(request,'tools/form.html',{'form': form, 'action': '등록'})

def tool_update(request,pk):
    tool = get_object_or_404(DevTool, pk=pk)
    if request.method =='POST':
        form = DevToolForm(request.POST, instance=tool)
        if form.is_valid():
            tool = form.save()
            return redirect('tool_detail', pk=tool.pk)
        else:
            form = DevToolForm(instance=tool)
    return render(request, 'tools/form.html', {'form': form, 'action': '수정', 'tool': tool})

def tool_delete(request, pk):
    if request.method == 'POST':
        tool = get_object_or_404(DevTool, pk=pk)
        tool.delete()
    return redirect('tool_list')