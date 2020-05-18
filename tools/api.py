import uuid
import os
import logging

from requests import Session, Request, Response
from requests.adapters import Retry, HTTPAdapter
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


class ChatStats:
    URL = 'https://api.chat-stats.ru/v1'

    def __init__(self, url: str = None):
        self.url = url or os.getenv('CHAT_STATS_URL') or self.URL
        self.session = self.make_session()

    @staticmethod
    def make_session(retries=3,
                     backoff_factor=2,
                     status_forcelist=(500, 502, 504)
                     ):
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        session = Session()
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def __make_request(self,
                       request_type: str,
                       url: str,
                       params: dict = None,
                       payload: dict = None,
                       ) -> Response:

        request_params = {
            'url': url,
            'json': payload,
            'params': params,
            'method': request_type.upper()
        }
        rid = str(uuid.uuid4())
        request_params.update({
            'headers': {
                'X-REQUEST-ID': rid
            }
        })

        req = Request(**request_params)
        prepared_request = self.session.prepare_request(req)

        response = Response()
        try:
            response = self.session.send(
                prepared_request,
                timeout=5,
            )
            logger.debug(
                'Sent request to %s. Response code: %s, response text: %s' %
                (prepared_request.url, response.status_code, response.text)
            )
        except RequestException as e:
            logger.exception(e, extra={
                'request_id': rid,
                'url': prepared_request.url
            })
            response.status_code = 500
        return response

    def get_bots(self, creator_id):
        return self.__make_request(
            request_type='GET',
            url=self.url + '/bots',
            params={'creator_id': creator_id}
        )

    def get_new_token(self, creator_id, username):
        return self.__make_request(
            request_type='POST',
            url=self.url + '/token/new',
            payload={
                'creator_id': creator_id,
                'username': username,
            }
        )

    def revoke_token(self, creator_id, token):
        return self.__make_request(
            request_type='POST',
            url=self.url + '/token/revoke',
            payload={
                'creator_id': creator_id,
                'token': token,
            }
        )

    def eventsByUsers(self, from_dt, token):
        return self.__make_request(
            request_type='POST',
            url=self.url + '/stats/eventsByUsers',
            params={
                'token': token,
                'from_dt': from_dt,
            }
        )

    def sex_distribution(self, from_dt, token):
        return self.__make_request(
            request_type='POST',
            url=self.url + '/stats/sex',
            params={
                'token': token,
                'from_dt': from_dt,
            }
        )

    def top_events(self, from_dt, token):
        return self.__make_request(
            request_type='POST',
            url=self.url + '/stats/topEvents',
            params={
                'token': token,
                'from_dt': from_dt,
            }
        )

    def new_users(self, from_dt, token):
        return self.__make_request(
            request_type='POST',
            url=self.url + '/stats/newUsers',
            params={
                'token': token,
                'from_dt': from_dt,
            }
        )

    def sessions(self, from_dt, token):
        return self.__make_request(
            request_type='POST',
            url=self.url + '/stats/sessions',
            params={
                'token': token,
                'from_dt': from_dt,
            }
        )


chat_stats = ChatStats()

__all__ = ['chat_stats']
