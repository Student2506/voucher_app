import logging

from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render
from dotenv import load_dotenv

from .converter import generate_pdf
from .models import ContrAgent

load_dotenv()

logger = logging.getLogger()


def index(request):
    logger.debug(f'{settings.SERVER}, {settings.DATABASE}, {settings.USER}, '
                 f'{settings.PASS}')
    tableCA = ContrAgent(
        settings.SERVER, settings.DATABASE, settings.USER, settings.PASS
    )
    companies = tableCA.session.query(
        tableCA.client
    ).order_by(tableCA.client.sName).all()
    paginator = Paginator(companies, settings.COMPANIES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'index.html', {'page': page})


def voucher_index(request, company):
    tableCA = ContrAgent(
        settings.SERVER, settings.DATABASE, settings.USER, settings.PASS
    )
    company = (
        tableCA.session.query(tableCA.client).filter_by(lID=company).first()
    )
    if not company:
        return HttpResponseNotFound('Not found')
    return render(request, 'company_view.html', {'company': company})


def codes_index(request, voucher):
    tableCA = ContrAgent(
        settings.SERVER, settings.DATABASE, settings.USER, settings.PASS
    )
    orders = (
        tableCA.session
        .query(tableCA.client_order_item)
        .filter_by(lID=voucher).first()
    )
    vouchers = orders.tblvouchertype.tblstock_collection
    for voucher in vouchers:
        generate_pdf(voucher.Stock_strBarcode, qr_code=True)

    return render(
        request,
        'vouchers.html',
        {'first': vouchers[0], 'last': vouchers[-1]}
    )
