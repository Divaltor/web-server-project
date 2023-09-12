import django_filters
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.mixins import DestroyModelMixin

from server.models import Item, Category, User
from server.serializers import ItemSerializer, CategorySerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        field_classes = {'email': forms.EmailField}

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})



class LoginView(DjangoLoginView):
    authentication_form = LoginForm
    redirect_authenticated_user = True


class ItemFilterSet(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        to_field_name='id',
    )

    class Meta:
        model = Item
        fields = ['category']


class ItemViewSet(viewsets.ReadOnlyModelViewSet, DestroyModelMixin):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = ItemFilterSet
    search_fields = ['sku', 'name', 'description']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['sku', 'name', 'description', 'buy_price', 'sell_price', 'quantity', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'maxlength': 50}),
            'description': forms.Textarea(attrs={'maxlength': 2000}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 1024 * 1024 * 15:
            raise forms.ValidationError("Image file too large ( > 15mb )")

        if image and image.name.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
            raise forms.ValidationError("Image file type not supported. Only jpg, jpeg and png are supported.")

        return image

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if len(category) > 1:
            raise forms.ValidationError("You can select only one category.")
        return category


@login_required
def items_page(request):
    return render(request, 'items.html')


class ItemUpdateView(UpdateView, LoginRequiredMixin):
    model = Item
    form_class = ItemForm
    template_name = 'item_form.html'
    success_url = reverse_lazy('items')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


@login_required
def item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = ItemForm()
    return render(request, 'item_form.html', {'form': form, 'categories': Category.objects.all()})


@login_required
def main_page(request):
    return redirect('items')