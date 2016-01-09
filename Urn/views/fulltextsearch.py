import json
from django.http import HttpResponse
from django.db import connection
from Urn.common.formatters import format_products
from Urn.common.utils import build_json
from Urn.models import Products


def fts_products(request):
    if request.method == 'GET' and request.GET.get('filter', None) is not None:
        search_query = request.GET["filter"]
        product_guids = fts_raw_query(search_query)
        returnable = {
            'products': format_products(Products.objects.filter(product_guid__in=product_guids), json=False)
        }

        return HttpResponse(build_json(returnable))


def convert_cursor_result_dict(cursor):
    return [
        row[0] for row in cursor.fetchall()
        ]


def fts_raw_query(query):
    search_query = '''
    WITH q AS
    (
      SELECT plainto_tsquery('{0}') AS query
    ),
    ranked AS
    (
      SELECT product_guid,
             ts_rank_cd(tsv,query) AS RANK
      FROM products p, sku s,
           q
      WHERE q.query @@ tsv and p.sku_id = s.sku_id
      ORDER BY RANK DESC
      LIMIT 10
    )
    SELECT CAST(product_guid AS varchar)
    FROM ranked,
         q
    ORDER BY ranked DESC;
    '''.format(query)

    cursor = connection.cursor()
    cursor.execute(search_query)

    return convert_cursor_result_dict(cursor)
