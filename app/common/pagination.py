import urllib
import urlparse


class PaginatedDataView(object):
    def __init__(self, collection_type, collection, current_page_url,
                 next_page_marker=None, total_count=None, limit=None, **kwargs):
        self.total_count = total_count
        self.collection_type = collection_type
        self.collection = collection
        self.current_page_url = current_page_url
        self.next_page_marker = next_page_marker
        self.page = kwargs['page']
        self.page_size = limit
        self.total_page = self.total_count / self.page_size
        if self.total_count % self.page_size > 0:
            self.total_page += 1

    def data(self):
        return {self.collection_type: self.collection,
                'links': self._links(),
                'total_count': self.total_count
                }

    def _links(self):
        if not self.next_page_marker:
            return []
        app_url = AppUrl(self.current_page_url)
        next_url = app_url.change_query_params(marker=self.next_page_marker)
        next_link = {
            'rel': 'next',
            'href': str(next_url),
        }
        return [next_link]


class SimplePaginatedDataView(object):
    # In some cases, we can't create a PaginatedDataView because
    # we don't have a collection query object to create a view on.
    # In that case, we have to supply the URL and collection manually.

    def __init__(self, url, name, view, marker, total_count=None):
        self.url = url
        self.name = name
        self.view = view
        self.marker = marker
        self.total_count = total_count

    def data(self):
        if not self.marker:
            data = self.view.data()
            if isinstance(data, dict) and ('total_count' not in data
                                           or data['total_count'] is None):
                data['total_count'] = self.total_count
            return data

        app_url = AppUrl(self.url)
        next_url = str(app_url.change_query_params(marker=self.marker))
        next_link = {'rel': 'next',
                     'href': next_url}
        view_data = {self.name: self.view.data()[self.name],
                     'links': [next_link],
                     'marker': self.marker,
                     'total_count': self.total_count}
        return view_data


class AppUrl(object):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return self.url

    def change_query_params(self, **kwargs):
        # Seeks out the query params in a URL and changes/appends to them
        # from the kwargs given. So change_query_params(foo='bar')
        # would remove from the URL any old instance of foo=something and
        # then add &foo=bar to the URL.
        parsed_url = urlparse.urlparse(self.url)
        # Build a dictionary out of the query parameters in the URL
        query_params = dict(urlparse.parse_qsl(parsed_url.query))
        # Use kwargs to change or update any values in the query dict.
        query_params.update(kwargs)

        # Build a new query based on the updated query dict.
        new_query_params = urllib.urlencode(query_params)
        return self.__class__(
            # Force HTTPS.
            urlparse.ParseResult('https',
                                 parsed_url.netloc, parsed_url.path,
                                 parsed_url.params, new_query_params,
                                 parsed_url.fragment).geturl())
