from datetime import datetime
from .models import Gist


def search_gists(db_connection, **kwargs):

    PARSED_DATE_CRITERION = {
        'created_at__lt': {
            'name': 'datetime(created_at)',
            'operator': '<'
            },
        'created_at__lte': {
            'name': 'datetime(created_at)',
            'operator': '<='
            },
        'created_at__gt': {
            'name': 'datetime(created_at)',
            'operator': '>'
            },
        'created_at__gte': {
            'name': 'datetime(created_at)',
            'operator': '>='
            },
        'created_at': {
            'name': 'datetime(created_at)',
            'operator': '=='
            },
        'updated_at__lt': {
            'name': 'datetime(updated_at)',
            'operator': '<'
            },
        'updated_at__lte': {
            'name': 'datetime(updated_at)',
            'operator': '<='
            },
        'updated_at__gt': {
            'name': 'datetime(updated_at)',
            'operator': '>'
            },
        'updated_at__gte': {
            'name': 'datetime(updated_at)',
            'operator': '>='
            },
        'updated_at': {
            'name': 'datetime(updated_at)',
            'operator': '=='
            }
        }

    query = 'SELECT * FROM gists WHERE '

    params = {}

    # Process any filtering constraints passed via kwargs
    count = 0
    for criterion, search_value in kwargs.items():
        count += 1
        if criterion in PARSED_DATE_CRITERION.keys():
            parsed_criterion = PARSED_DATE_CRITERION[criterion]
        else:
            parsed_criterion = {
                'name': criterion,
                'operator': '=='
                }

        search_value_tag = 'search_value_{i}'.format(i=count)
        query += '{criterion_name} {operator} :{search_value_tag} AND '.format(
            criterion_name=parsed_criterion['name'],
            operator=parsed_criterion['operator'],
            search_value_tag=search_value_tag
            )

        params.update({search_value_tag: search_value})

    # Clean up hanging bits from query construction
    query = query.rstrip('WHERE ').rstrip('AND ')

    # Run the query and return a list of Gist objects
    cursor = db_connection.execute(query, params)
    return [Gist(gist) for gist in cursor]