from django.forms import widgets
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings




class RelatedFieldWidgetSingle(widgets.Select):
    """ Inherits from widgets.Select """

    def __init__(self, related_model, related_url=None, *args, **kw):
        super(RelatedFieldWidgetSingle, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = '%s:%s_add' % info

        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetSingle, self).render(name, value, *args, **kwargs)]
        output.append('<a href="%s?_to_field=id&_popup=1" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append('<img src="%sadmin/img/icon-addlink.svg" width="20" height="20" alt="%s"/></a>' % (settings.STATIC_URL, 'Add Another'))
        return mark_safe(''.join(output))
      

class RelatedFieldWidgetMultiple(widgets.SelectMultiple):
    """ Inherits from widgets.SelectMultiple """

    def __init__(self, related_model, related_url=None, *args, **kw):
        super(RelatedFieldWidgetMultiple, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = '%s:%s_add' % info

        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetMultiple, self).render(name, value, *args, **kwargs)]
        output.append('<a href="%s?_to_field=id&_popup=1" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append('<img src="%sadmin/img/icon-addlink.svg" width="20" height="20" alt="%s"/></a>' % (settings.STATIC_URL, 'Add Another'))
        return mark_safe(''.join(output))



