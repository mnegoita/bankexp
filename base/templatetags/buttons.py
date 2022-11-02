from django import template
from django.urls import reverse

register = template.Library()

template_path = 'base/buttons/'





def get_view_name(instance, action):
    """
    Function to get the name of a specific when using the same pattern in forming
    the name of the views.
    Used for views like: add, edit, delete, list, etc
    """

    assert action in ('add', 'edit', 'delete', 'import', 'export', 'clone', 'list')
    view_name = "{}:{}_{}".format(
        instance._meta.app_label, instance._meta.model_name, action
    )
    
    return view_name


# List View URL template tag ##########################
# Used in breadcrumb

@register.simple_tag
def list_view_url(instance):
    
    view_name = get_view_name(instance, 'list')    
    url = '{}'.format(reverse(view_name))

    return url


# Add Button ##########################################

@register.inclusion_tag(template_path + 'add.html')
def add_button(app_name, obj_name):

    add_url = reverse(f"{app_name}:{obj_name}_add")

    return {
        'url': add_url,
    }


# Import Button ########################################

@register.inclusion_tag(template_path + 'import.html')
def import_button(instance):
    
    view_name = get_view_name(instance, 'import')   
    url = '{}'.format(reverse(view_name))
    return {'url': url}


# Export Button #########################################

@register.inclusion_tag(template_path + 'export.html')
def export_button(instance):
    
    view_name = get_view_name(instance, 'export')    
    url = '{}'.format(reverse(view_name))
    return {'url': url}


# Edit Button ############################################

@register.inclusion_tag(template_path + 'edit.html')
def edit_button(instance):
    
    view_name = get_view_name(instance, 'edit')
    url = reverse(view_name, kwargs={'pk': instance.pk})    

    return {'url': url}


# Delete Button #############################################

@register.inclusion_tag(template_path + 'delete.html')
def delete_button(instance):
    
    view_name = get_view_name(instance, 'delete')    
    url = reverse(view_name, kwargs={'pk': instance.pk})
    return {'url': url}


# Clone Button ################################################

def prepare_cloned_fields(instance):

    params = {}
    for field_name in getattr(instance, 'clone_fields', []):
        field = instance._meta.get_field(field_name)
        field_value = field.value_from_object(instance)

        # Swap out False with URL-friendly value
        if field_value is False:
            field_value = ''

        # Omit empty values
        if field_value not in (None, ''):
            params[field_name] = field_value

    # Concatenate parameters into a URL query string
    param_string = '&'.join(
        ['{}={}'.format(k, v) for k, v in params.items()]
    )

    return param_string


@register.inclusion_tag(template_path + 'clone.html')
def clone_button(instance):
    view_name = get_view_name(instance, 'add')

    # Populate cloned field values
    param_string = prepare_cloned_fields(instance)
    if param_string:
        url = '{}?{}'.format(reverse(view_name), param_string) 

    return {
        'url': url,
    }


# Add Expense Record From Chequing Transaction Button #################

@register.inclusion_tag(template_path + 'expense_record_add_from_here.html')
def add_exp_rec_from_chq_tr_button(obj):
    """
    Button to add an expense record from the detail page
    of a chequing transaction
    """
    
    url = f"/expenserecords/add/?chq_tr={obj}"
    return {'url': url}


# Add Expense Record From Credit Card Transaction Button #################

@register.inclusion_tag(template_path + 'expense_record_add_from_here.html')
def add_exp_rec_from_cc_tr_button(obj):
    """
    Button to add an expense record from the detail page
    of a credit card transaction
    """
    
    url = f"/expenserecords/add/?cc_tr={obj}"
    return {'url': url}

# Add a tag to multiple transactions from here

@register.inclusion_tag(template_path + 'tag_multiple_assign_from_here.html')
def tag_multiple_assign_from_here():
    """
    Button to add an expense record from the detail page
    of a credit card transaction
    """
    
    url = f"/tags/tag-multiple-assign/"
    return {'url': url}

# Remove a tag from multiple transactions from here

@register.inclusion_tag(template_path + 'tag_multiple_remove_from_here.html')
def tag_multiple_remove_from_here():
    """
    Button to add an expense record from the detail page
    of a credit card transaction
    """
    
    url = f"/tags/tag-multiple-remove/"
    return {'url': url}

