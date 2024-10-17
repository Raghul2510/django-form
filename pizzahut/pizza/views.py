from django.shortcuts import render
from .forms import PizzaForm,MultiplepizzaForm
from .models import Pizza
from django.forms import formset_factory



# Create your views here.
def homepage(request):

    return render(request,'pizza/home.html')

def order(request):
    multiple_pizza_form = MultiplepizzaForm()
    created_pizza_pk = None
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST )
        if filled_form.is_valid():
            note = 'Thanks for ordering %s,%s,%s!'%(filled_form.cleaned_data['topping1'],
                                                    filled_form.cleaned_data['topping2'],
                                                    filled_form.cleaned_data['size'])
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
        else:
            note = 'Sorry please tryagain..'
        new_form = PizzaForm()
        return render(request,'pizza/order.html',{'note' :note,'multiple_pizza_form':multiple_pizza_form,'created_pizza_pk':created_pizza_pk})
    else:
        form = PizzaForm()
        return render(request,'pizza/order.html',{'pizzaform':form,'multiple_pizza_form':multiple_pizza_form})

def edit(request,pk):

    note = ''
    pizza =Pizza.objects.get(pk = pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        edited_form = PizzaForm(request.POST,instance=pizza)
        if edited_form.is_valid():
            edited_form.save()
            note = 'Order Edited successfully!!!'
        else:
            note = 'Sorry please try agian!'
    return render(request,'pizza/edit.html',{'pizzaform':form,'pk':pk,'note':note})

def pizzas(request):
    no_of_pizzas = 2
    if request.method =='GET':
        filled_multiple_pizza_form = MultiplepizzaForm(request.GET)
        if filled_multiple_pizza_form.is_valid():
            no_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
        print(no_of_pizzas)
    PizzaFormset =formset_factory(PizzaForm, extra= no_of_pizzas)
    formset = PizzaFormset()
    if request.method == 'POST':
        filled_formset =PizzaFormset(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                form.save()
            note = 'Order placed successfully'
        else:
            note = 'Sorry, Order not placed, please try again!'
        return render(request,'pizza/pizzas.html',{'formset': formset, 'note': note})

    return render(request,'pizza/pizzas.html',{'formset':formset})
