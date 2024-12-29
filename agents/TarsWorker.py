

import abc
from agents.TarsAgentType import TarsAgentType
from agents.TarsBase import TarsBase
from tasks.TaskBase import TaskBase


class TarsWorker(TarsBase, abc.ABC):

    default_max_retry_times = 2
    default_worker_name = 'TarsWorker'
    default_worker_role = 'You are a helpful assistant.'

    def __init__(self, name: str=default_worker_name, role: str=default_worker_role, llm_config=None, max_retry_times=default_max_retry_times):
        super().__init__(role, name, llm_config, max_retry_times, TarsAgentType.Worker)

    @abc.abstractmethod
    def answer(self, task: TaskBase):
        pass

    def build_task(self,):
        pass
    

