from tools.ToolBase import ToolBase


class APITool(ToolBase):

    def __init__(self, tool_name: str, tool_description: str, tool_type: str, api: str, headers: dict, params_definition:dict) -> None:
        self.api = api
        self.headers = headers
        self.params_definition = params_definition
        super().__init__(tool_name, tool_description, tool_type)

    def post(self, params, is_json_response):
        raise NotImplementedError("API Tool post method is not implemented yet.")

    def get(self, ):
        raise NotImplementedError("API Tool get method is not implemented yet.")

