from datetime import datetime
from .models import Gist

def search_gists(db_connection, **kwargs):

    cursor = db_connection.execute('SELECT * FROM gists')

    # Return everything if no filters specified
    if not kwargs:
        return [Gist(gist) for gist in cursor]

    # Process any filtering constraints passed in kwargs
    DATE_ATTRS = ['created_at', 'updated_at']
    gists = []

    for row in cursor:
        gist = Gist(row)
        for field, search_value in kwargs.items():
            field_value = getattr(gist, field)
            if field in DATE_ATTRS:
                field_value = datetime.strptime(field_value, '%Y-%m-%dT%H:%M:%SZ')
            if field_value != search_value:
                break
            gists.append(gist)

    return gists