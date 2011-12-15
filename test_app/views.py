# Django
from django.template.response import TemplateResponse

# Django-DataTables
import datatables

# Django-FortuneCookie
from fortunecookie.models import *

class FortuneCookieTable(datatables.DataTable):

    #pk = datatables.CheckboxColumn()
    fortune = datatables.Column(label='Your Fortune', sort_field='fortune_lower')
    fortune_lower = datatables.Column(label='Lower Fortune', visible=False)
    lucky_numbers = datatables.Column(display_field='lucky_numbers_display', searchable=False)
    chinese_word = datatables.Column(label='Chinese Word', sort_field='chinese_word.english_word', searchable=False)

    def get_queryset(self):
        #qs = super(FortuneCookieTable, self).get_queryset()
        qs = FortuneCookie.objects.all()
        qs = qs.extra(select={
            'fortune_lower': 'LOWER(fortune)',
        })
        return qs

    class Meta:
        model = FortuneCookie
        bInfo = True
        bSort = True
        bPaginate = False
        sScrollY = '400px'
        aaSorting = [[2, "desc"]]


@datatables.datatable(FortuneCookieTable, name='fct')
def index(request):
    #request.fct.update_queryset()
    return TemplateResponse(request, 'index.html', {'table': request.fct})
