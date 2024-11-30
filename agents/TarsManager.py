

from agents.TarsBase import TarsBase


class TarsManager(TarsBase):

    default_max_retry_times = 2
    default_manager_name = 'TarsManager'
    default_manager_role = 'You are a manager of Tars worker agents.'

    

    def __init__(self, name: str=default_manager_name, role: str=default_manager_role, llm_config=None, max_retry_times=default_max_retry_times):
        super().__init__(role, name, llm_config, max_retry_times)

