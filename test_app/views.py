# Django
from django.template.response import TemplateResponse

# Django-DataTables
import datatables

# Django-FortuneCookie
from fortunecookie.models import *

class FortuneCookieTable(datatables.DataTable):

    fortune = datatables.Column(label='Your Fortune', sort_field='fortune_lower')
    chinese_word = datatables.Column(label='Chinese Word', sort_field='chinese_word.english_word')

    def get_queryset(self):
        qs = super(FortuneCookieTable, self).get_queryset()
        qs.extra({'select': {
            'fortune_lower': 'LOWER(fortune)',
        }})
        return qs

    class Meta:
        model = FortuneCookie
        bInfo = True


@datatables.datatable(FortuneCookieTable, name='fct')
def index(request):
    return TemplateResponse(request, 'index.html', {'table': request.fct})
