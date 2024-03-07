from anthropic import Anthropic
import os


class AnthropicModel:
    

    def __init__(self, model_name, toolSet):
        self.model_name = model_name
        self.toolSet = toolSet
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


    def build_agent(self):
        initial_prompt = "you a good person"
        tools_description = self.agent([self.toolSet.toolreader()])
        self.prompt = f"{initial_prompt}\n\n{tools_description}"


    def agent(self, tools):
        tools_list = '\n'.join(tools)
        return (
            "In this environment you have access to a set of tools you can use to answer the user's question.\n"
            "\n"
            "You may call them like this:\n"
            "<function_calls>\n"
            "<invoke>\n"
            "<tool_name>$TOOL_NAME</tool_name>\n"
            "<parameters>\n"
            "<$PARAMETER_NAME>$PARAMETER_VALUE</$PARAMETER_NAME>\n"
            "...\n"
            "</parameters>\n"
            "</invoke>\n"
            "</function_calls>\n"
            "\n"
            "Here are the tools available:\n"
            "<tools>\n"
            f"{tools_list}\n"
            "</tools>"
        )


    def wordboxprocess(self,message):
        messages = [{"role": "user", "content": message}]
        system_response = self.client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                messages=messages,
                system=self.prompt,
                stop_sequences=["\n\nHuman:", "\n\nAssistant", "</function_calls>"]
            ).content[0].text

             
        output = self.toolSet.execute(resultC=system_response)

        final_output = self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            messages=[messages[0], {"role": "assistant", "content": output}],
            system=self.prompt,
        ).content[0].text

        return final_output




