# Django
from django.template.response import TemplateResponse

# Django-DataTables
import datatables

# Django-FortuneCookie
from fortunecookie.models import *

class FortuneCookieTable(datatables.DataTable):

    #pk = datatables.CheckboxColumn()
    fortune = datatables.Column(label='Your Fortune', sort_field='fortune_lower')
    fortune_lower = datatables.Column(label='Lower Fortune', bVisible=False)
    lucky_numbers = datatables.Column(display_field='lucky_numbers_display', sClass='okie')
    chinese_word = datatables.Column(label='Chinese Word', sort_field='chinese_word.english_word', sClass='okie')

    def get_queryset(self):
        qs = self.base_queryset()
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
        #fnInitComplete = 'function(oSettings, json) { alert("Init Complete!"); }'

@datatables.datatable(FortuneCookieTable, name='fct')
def index(request):
    qs = request.fct.get_queryset()
    request.fct.update_queryset(qs)
    return TemplateResponse(request, 'index.html', {'table': request.fct})
