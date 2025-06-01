from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import CashFlowRecord, Status, Type, Category, Subcategory
from .filters import CashFlowFilter
from .forms import CashFlowForm


def record_list(request):
    """
    Display a filtered and paginated list of cash flow records.
    
    Args:
        request: HttpRequest object
        
    Returns:
        HttpResponse: Rendered record list template with filtered records
        
    Context:
        filter: CashFlowFilter instance for filtering records
        records: Filtered and ordered queryset of CashFlowRecords
    """
    records = CashFlowRecord.objects.all().order_by('-date')
    record_filter = CashFlowFilter(request.GET, queryset=records)
    
    return render(request, 'cashflow/record_list.html', {
        'filter': record_filter,
        'records': record_filter.qs
    })


def add_record(request):
    """
    Handle cash flow record creation through form submission.
    
    GET: Returns empty form for new record creation
    POST: Processes form submission and creates new record
    
    Returns:
        HttpResponse: Rendered form template or redirect to record list
        
    Context:
        form: CashFlowForm instance
        statuses: All available Status objects
        types: All available Type objects
        categories: All available Category objects
        subcategories: All available Subcategory objects
    """
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = CashFlowForm()
    
    context = {
        'form': form,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all()
    }
    return render(request, 'cashflow/add_record.html', context)


def edit_record(request, pk):
    """
    Handle editing of existing cash flow records.
    
    Args:
        request: HttpRequest object
        pk: Primary key of record to edit
        
    Returns:
        HttpResponse: Rendered form template or redirect to record list
        
    Context:
        form: CashFlowForm instance pre-populated with record data
        is_edit: Boolean flag indicating edit mode
        record_id: ID of record being edited
        statuses/types/categories/subcategories: All available options
        selected_[field]_id: Currently selected IDs for dropdowns
    """
    record = get_object_or_404(CashFlowRecord, pk=pk)

    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = CashFlowForm(instance=record)

    context = {
        'form': form,
        'is_edit': True,
        'record_id': record.id,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'selected_category_id': record.category.id,
        'selected_status_id': record.status.id,
        'selected_type_id': record.type.id,
        'selected_subcategory_id': record.subcategory.id,
    }
    return render(request, 'cashflow/add_record.html', context)


@require_POST
def delete_record(request, pk):
    """
    Handle deletion of cash flow records via POST request.
    
    Args:
        request: HttpRequest object (POST only)
        pk: Primary key of record to delete
        
    Returns:
        JsonResponse: Operation result with status and message
        
    Possible Responses:
        200: Successful deletion
        404: Record not found
        500: Server error during deletion
    """
    try:
        record = CashFlowRecord.objects.get(pk=pk)
        record.delete()
        return JsonResponse({
            'status': 'success',
            'message': f'Record {pk} deleted successfully'
        })
    except CashFlowRecord.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Record {pk} not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }, status=500)


# AJAX API Endpoints
@csrf_exempt
def quick_add_status(request):
    """
    AJAX endpoint for creating new Status records.
    
    Args:
        request: HttpRequest object with POST data
        
    Returns:
        JsonResponse: New status data or error message
        
    Required POST Parameters:
        name: Name of new status
        
    Possible Responses:
        200: Success with new status data
        400: Invalid request or missing parameters
    """
    if request.method == 'POST':
        status_name = request.POST.get('name', '').strip()
        if status_name:
            status, created = Status.objects.get_or_create(name=status_name)
            return JsonResponse({
                'id': status.id, 
                'name': status.name
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def quick_add_type(request):
    """
    AJAX endpoint for creating new Type records.
    (Implementation similar to quick_add_status)
    """
    if request.method == 'POST':
        type_name = request.POST.get('name', '').strip()
        if type_name:
            type_obj, created = Type.objects.get_or_create(name=type_name)
            return JsonResponse({
                'id': type_obj.id, 
                'name': type_obj.name
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def quick_add_category(request):
    """
    AJAX endpoint for creating new Category records.
    
    Args:
        request: HttpRequest object with POST data
        
    Returns:
        JsonResponse: New category data or error message
        
    Required POST Parameters:
        name: Name of new category
        
    Possible Responses:
        200: Success with new category data
        400: Invalid request or missing parameters
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
            
        try:
            category = Category.objects.create(name=name)
            return JsonResponse({
                'id': category.id,
                'name': category.name
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def quick_add_subcategory(request):
    """
    AJAX endpoint for creating new Subcategory records.
    
    Args:
        request: HttpRequest object with POST data
        
    Returns:
        JsonResponse: New subcategory data or error message
        
    Required POST Parameters:
        category_id: ID of parent category
        name: Name of new subcategory
        
    Possible Responses:
        200: Success with new subcategory data
        400: Invalid request or missing parameters
    """
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        name = request.POST.get('name', '').strip()
        
        if not category_id:
            return JsonResponse({'error': 'Category ID is required'}, status=400)
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
            
        try:
            subcategory = Subcategory.objects.create(
                name=name,
                category_id=category_id
            )
            return JsonResponse({
                'id': subcategory.id,
                'name': subcategory.name
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_categories(request):
    """
    AJAX endpoint for fetching categories filtered by type.
    
    Args:
        request: HttpRequest object with GET parameters
        
    Returns:
        JsonResponse: List of categories in JSON format
        
    Required GET Parameters:
        type_id: ID of type to filter categories
        
    Response Format:
        [{'id': int, 'name': str}, ...]
    """
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)


def get_subcategories(request):
    """
    AJAX endpoint for fetching subcategories filtered by category.
    
    Args:
        request: HttpRequest object with GET parameters
        
    Returns:
        JsonResponse: List of subcategories in JSON format
        
    Required GET Parameters:
        category_id: ID of category to filter subcategories
        
    Response Format:
        [{'id': int, 'name': str}, ...]
    """
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)