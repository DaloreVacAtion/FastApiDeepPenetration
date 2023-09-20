import abc
import datetime
import logging
import structlog


class LoggingBased(abc.ABC):

    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(self.source_logging)

    @property
    @abc.abstractmethod
    def source_logging(self) -> str:
        raise NotImplementedError

    async def create_error_message(self, error_code: int, reason: str) -> None:
        """Создает сообщение об ошибке."""
        self._logger.error(
            self.source_logging + f' Error code ${0}, message: {1}'.format(
                error_code, reason))


class LoggingRequests(LoggingBased):
    source_logging = 'LOGGING_REQUEST:'

    async def log_request(self, request):
        """Логирование запроса от клиента."""
        self._logger.info(
            f' Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")}'
            f' Request event hook: {request.method} {request.url} - Waiting for response'
        )

    async def log_response(self, response):
        """Логирование ответа от сервера."""
        request = response.request
        self._logger.info(
            f' Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")} Response event hook:'
            f' {request.method} {request.url} - Status {response.status_code}'
        )


logger = structlog.get_logger()
