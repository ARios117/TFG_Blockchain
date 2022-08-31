from django.shortcuts import render
from django.views import generic
from .models import Block, Member
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):

    context_dict = {}

    if(request.user.username is not ""):
        blocks_recieved = Block.objects.filter(
            receiver = Member.objects.get(username = request.user.username)
            ).order_by('-date')[:5]

        context_dict['blocks_recieved'] = blocks_recieved

    return render(request, 'index.html', context_dict)

def block_create_confirm(request):
    return render(request, 'blockchain/block_create_confirm.html')

class BlockCreate(LoginRequiredMixin, CreateView):
    model = Block
    fields = ['receiver','text']
    exclude = ['emiter']

    def form_valid(self, form):
        user = self.request.user
        form.instance.emiter = Member.objects.get(username = user.username)

        if form.is_valid():
            # process the data in form.cleaned_data as required

            block = Block(
                emiter=Member.objects.get(username = user.username),
                receiver=form.cleaned_data['receiver'],
                text=form.cleaned_data['text'],
            )
            block.save()

        return HttpResponseRedirect(reverse('block_create_confirm'))

def show_block(request, slug):

    context_dict = {}

    try:
        block = Block.objects.get(slug=slug)
        print(block)

        context_dict['b'] = block

    except Block.DoesNotExist:

        context_dict['b'] = None

    return render(request, 'blockchain/block_detail.html', context_dict)
