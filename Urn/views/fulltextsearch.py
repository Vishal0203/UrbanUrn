from django.http import HttpResponse
from django.db import connection
from Urn.common.utils import build_json


def fts_products(request):
    if request.method == 'GET' and request.GET.get('filter', None) is not None:
        search_query = request.GET["filter"]
        return HttpResponse(build_json(fts_raw_query(search_query)))


def convert_cursor_result_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
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
             s.sku_guid as sku_guid,
             p.name,
             p.description,
             ts_rank_cd(tsv,query) AS RANK
      FROM products p, sku s,
           q
      WHERE q.query @@ tsv and p.sku_id = s.sku_id
      ORDER BY RANK DESC
      LIMIT 10
    )
    SELECT CAST(product_guid AS varchar),
           CAST(sku_guid AS varchar),
           ts_headline(name, q.query) as name,
           ts_headline(description, q.query) as description
    FROM ranked,
         q
    ORDER BY ranked DESC;
    '''.format(query)

    cursor = connection.cursor()
    cursor.execute(search_query)

    return convert_cursor_result_dict(cursor)
