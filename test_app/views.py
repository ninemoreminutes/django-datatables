
# Django-Datatables
import datatables

# Django-Datatables Tests
from models import *

class FortuneCookieTable(datatables.Datatable):

    text = datatables.Column(label='Your Fortune')

    class Meta:
        model = FortuneCookie

def index(request):
    fct = FortuneCookieTable(request.GET)
    
    