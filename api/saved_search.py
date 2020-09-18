from datetime import datetime, timedelta
from uuid import uuid4

from api.base import Base
from api.filters import *
import inspect
import logging


class SavedSearch(Base):
    def get_url(self):
        return self.urls.get('saved_searches')
    
    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)
        self.__daily_email_enabled = kwargs.get('__daily_email_enabled', False)
        self.filter = kwargs.get('filter', DateRangeFilter(field_name='acquired', lt=datetime.now(), gt=datetime.now() - timedelta(days=1)))
        self.item_types = kwargs.get('item_types', ['PSScene3Band'])
        self.name = kwargs.get('name') if kwargs.get('name') else  str(uuid4()) #string ^.{1,64}$
        self._id = None
        self._data = {}
    
    
    @property
    def data(self):
        if not self._data:
            if inspect.isclass(self.filter):
                self.filter = self.filter()
            self._data =  {
                            "__daily_email_enabled": self.__daily_email_enabled,
                            "filter": self.filter.to_dict(),
                            "item_types":self.item_types,
                            "name": self.name
                            }
            print(self._data)
            return self._data
        else:
            return self._data
    
    def create(self):
        response = self.post()
        self.is_created = response.status_code == 201
        logging.warning(response)
        logging.warning(response.text)
        return response.json() if self.is_created else response.text
    
    def update(self, search_id=None, **kwargs):
        self.data.update(kwargs)
        response = self.put(url=self.get_url() + f'/{search_id}')
        self.is_updated = response.status_code == 200
        logging.warning(response)
        logging.warning(response.text)
        return response.json() if self.is_updated else response.text
    
    def delete(self, search_id=None):
        response = self.delete_by_id(url=self.get_url() + f'/{search_id}')
        self.is_deleted = response.status_code == 204
        logging.warning(response)
        logging.warning(response.text)
        return response
    
    def get(self, search_id=None):
        response = self.get_by_id(url=self.get_url() + f'/{search_id}')
        self.is_got = response.status_code == 200
        logging.warning(response)
        logging.warning(response.text)
        return response.json() if self.is_got else response.text
        
        
        
