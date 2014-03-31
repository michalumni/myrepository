from django.shortcuts import render
from django.http import HttpResponse
from ce.models import Supplier, Review
from django.template import RequestContext, loader, Context
from django.http import Http404
from reviewform import ReviewForm
from django.utils import timezone

def index(request):
    return HttpResponse(" <!DOCTYPE html><html lang=\"en\">   <title>Choose Energy</title><a href=\"/reviews/\">Reviews</a></html>")

# Create your views here.
def reviews(request):
    supplier_list = Supplier.objects.all()
    template = loader.get_template('ce/reviews.html')
    context = RequestContext(request, {
        'supplier_list': supplier_list,
    })
    return HttpResponse(template.render(context))

def slug(request, slug):
    try:
        supplier = Supplier.objects.get(supplierSlug=slug)
    except Supplier.DoesNotExist:
        raise Http404

    mySupplier = Supplier.objects.get(supplierSlug=slug)
    myReviews = Review.objects.filter(supplier=mySupplier, published=True).order_by('-timeSubmitted')   

    template = loader.get_template('ce/slug.html')
    context = RequestContext(request, {
        'review_list': myReviews, 'supplier_list' : mySupplier,
    })
    return HttpResponse(template.render(context))

    
def write(request, slug):
    mySupplier = Supplier.objects.get(supplierSlug=slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            myReview = Review(supplier=mySupplier, timeSubmitted=timezone.now(), rating=form.data['choice_field'],
                              authorName=form.data['authorName'], reviewContent=form.data['reviewContent'],
                              published = False)
            myReview.save()
            template = loader.get_template('ce/thanks.html')
            context = RequestContext(request, { 'supplier':mySupplier
                })
            return HttpResponse(template.render(context))


        else:
            #form = ReviewForm()
            template = loader.get_template('ce/write.html')
            context = RequestContext(request, { 'form':form, 'supplier':mySupplier
        })
            return HttpResponse(template.render(context))           
    else:
        form = ReviewForm()
        template = loader.get_template('ce/write.html')
        context = RequestContext(request, { 'form':form, 'supplier':mySupplier
    })
    return HttpResponse(template.render(context))



