from django.shortcuts import render, get_object_or_404
from .models import Reference
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# class ReferenceListView(LoginRequiredMixin, ListView):
#     context_object_name = 'references'
#     paginate_by = 3
#     template_name = 'jurnal/share/list.html'

#     def get_queryset(self):
#         return Reference.objects.all()

@login_required
def reference_list(request):
    object_list = Reference.objects.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')

    try:
        references = paginator.page(page)
    except PageNotAnInteger:
        references = paginator.page(1)
    except EmptyPage:
        references = paginator.page(paginator.num_pages)
    return render(request,'jurnal/share/list.html',
                            {'references':references,'page':page})

# class ReferenceDetailView(LoginRequiredMixin, FormView):
#     template_name = 'jurnal/share/detail.html'

#     def get_initial(self):
#         pk = self.kwargs.get('pk')
#         slug = self.kwargs.get('slug')
#         self.reference = get_object_or_404(Reference, pk=pk, slug=slug)

#         reference_tags_ids = self.reference.tags.values_list('id', flat=True)
#         return super().get_initial()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reference'] = self.reference
#         return context

def reference_detail(request, year, month, day, reference):
    reference = get_object_or_404(Reference, slug=reference,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                'jurnal/share/detail.html',
                {'reference' : reference,})

class ReferenceCreateView(CreateView):
    model = Reference
    fields = ['title', 'slug', 'description', 'author', 'link']

class ReferenceUpdateView(CreateView):
    model = Reference
    fields = ['title', 'slug', 'description', 'author', 'link']

class ReferenceDeleteView(DeleteView):
    model = Reference
    success_url = reverse_lazy('jurnal:reference_list')
