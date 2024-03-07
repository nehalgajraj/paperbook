import re
from tools.box.calculator import Calculator


TOOLS = [
    # Assuming the TOOLS list is already filled with tool metadata
    {
        "id": "do_pairewise_arithmetic", 
        "function": Calculator.do_pairwise_arithmetic, 
        "metadata": Calculator.function_metadata
    },
    # Add more tools as needed
]

# Static mapping of agents to tools.
agent_tools_mapping = {
        "agent_k": ["do_pairewise_arithmetic"],
        # Add other agent mappings here
    }

class Tool:

    def __init__(self, agent_uid):
        global agent_tools_mapping, TOOLS
        self.agent_tools_mapping = agent_tools_mapping 
        self.tools = TOOLS
        self.agent_uid = agent_uid
        self.accessible_tools_ids = self.agent_tools_mapping.get(agent_uid, [])
        self.available_functions = {tool["id"]: tool["function"] for tool in self.tools}


    def get_functions(self):
        """Returns a list of functions available to the agent."""
        return [tool["function"] for tool in self.tools if tool["id"] in self.accessible_tools_ids]
    
    def get_metadata(self):
        """Returns metadata for all tools available to the agent."""
        return [tool["metadata"] for tool in TOOLS if tool["id"] in self.accessible_tools_ids]
    
    def toolreader(self):

        tool_metadata = self.get_metadata()
        tool_metadata = tool_metadata[0]
        
        name = tool_metadata["function"]["name"]
        description = tool_metadata["function"]["description"]
        parameters = tool_metadata["function"]["parameters"]["properties"]


        constructed_prompt = (
            "<tool_description>\n"
            f"<tool_name>{name}</tool_name>\n"
            "<description>\n"
            f"{description}\n"
            "</description>\n"
            "<parameters>\n"
            + "\n".join(
            f"<parameter>\n<name>{parameter}</name>\n<type>{parameters[parameter]['type']}</type>\n<description>{parameters[parameter]['description']}</description>\n</parameter>"
            for parameter in parameters)
            + "\n</parameters>\n"
            "</tool_description>"
        )
        return constructed_prompt
    


    @staticmethod
    def extract_between_tags(tag: str, string: str, strip: bool = False) -> list[str]:
        ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
        if strip:
            ext_list = [e.strip() for e in ext_list]
        return ext_list
    

    def execute(self,resultC ):
        # Assuming you've already got the function(s) from get_functions
        functions = self.get_functions()
        if not functions:
            print("No accessible functions for this agent.")
            return

        # Directly using the first available function for simplicity.
        # In a real-world scenario, you'd have a more sophisticated way to select the correct function.
        function = functions[0]
        
        # Assuming the metadata structure you provided
        tool_metadata = self.get_metadata()
        if not tool_metadata:
            print("No metadata available for this tool.")
            return
        tool_metadata = tool_metadata[0]  # Get the first item if there are multiple.

        function_metadata = tool_metadata['function']  # Accessing 'function' directly based on your structure
        parameters_metadata = function_metadata['parameters']['properties']

        parameter_values = {}
        for parameter_name in parameters_metadata:
            try:
                parameter_value = self.extract_between_tags(parameter_name, resultC, strip=True)[0]  # Using strip=True based on your method signature
                parameter_type = parameters_metadata[parameter_name]["type"]
                if parameter_type == "number":
                    parameter_value = float(parameter_value)
                elif parameter_type == "string":  # Ensure correct type handling
                    parameter_value = str(parameter_value)
                # Extend type handling as necessary
                parameter_values[parameter_name] = parameter_value
            except IndexError:
                print(f"Missing value for parameter: {parameter_name}")
                return

        # Execute the function with the parameter values
        result = function(**parameter_values)

        f_results = [{
            'tool_name': tool_metadata['function']['name'],
            'tool_result': result,
        }]

        constructed_prompt = (
            "<function_results>\n"
            + '\n'.join(
                f"<result>\n<tool_name>{res['tool_name']}</tool_name>\n<stdout>\n{res['tool_result']}\n</stdout>\n</result>" 
                for res in f_results
            ) + "\n</function_results>"
        )
        
        p_a_m =  resultC + "</function_calls>" + constructed_prompt   

        return p_a_m


