import yaml
import pandas as pd
import re


def build_example_prompt(input_label, input_value, output_label=None, output_value=None, base_prompt=None):
    input_value =  re.sub("\s+", " ", input_value)
    input_prompt = f"{base_prompt or ''}{input_label}:\n{input_value}"
    example_prompt = [
        {
            "role": "user",
            "content": input_prompt
        }
    ]

    if output_label:
        output_prompt = f"{output_label}:\n{output_value or ''}"
        example_prompt.append({
            "role": "assistant",
            "content": output_prompt
        })

    return example_prompt


def build_examples_prompt(
    strategy: str, 
    examples_df: pd.DataFrame, 
    input_data: object = None, 
    headless: bool=False, 
    limit: int=10
):    
    strategies = load_strategies()
    if strategy not in strategies:
        raise ValueError(f"Strategy {strategy} not found in {strategies.keys()}")
    
    properties = strategies[strategy]
    
    example_prompts = []
    if (examples_df is not None) and (not examples_df.empty):
      for index, row in examples_df[:limit].iterrows():
          example_prompt = build_example_prompt(
              input_value=row[properties["input_column"]], 
              input_label=properties["input_label"],
              output_value=row[properties["output_column"]],
              output_label=properties["output_label"],
              base_prompt=properties["user_prompt_examples"] if index == 0 else "",
          )
          example_prompts += example_prompt

    if headless:
        prompt = example_prompts
    else:
        prompt = [{
            "role": "system", 
            "content": properties["system_prompt"]
        }] 
        
        prompt += example_prompts
        
        if input_data is not None:
            input_prompt = build_example_prompt(
                input_value=input_data[properties["input_column"]], 
                input_label=properties["input_label"],
                output_value=input_data[properties["output_column"]] if properties["output_column"] in input_data else None,
                output_label=properties["output_label"]
            )
            previous_examples_context = "Based on the previous examples, " if example_prompts else ""
            prediction_instruction = previous_examples_context + properties["prediction_prompt"]
            input_prompt[0]["content"] = prediction_instruction + input_prompt[0]["content"]
            
            prompt += input_prompt
    
    return prompt


def build_spec_prompt(
    strategy: str, 
    path: str = './config/prompts/content/**/*.txt', 
    input_data: object = None, 
    examples_df: pd.DataFrame = None, 
    examples_limit: int = 0,
    headless: bool=False,
):
    strategies = load_strategies()
    if strategy not in strategies:
        raise ValueError(f"Strategy {strategy} not found in {strategies.keys()}")
    
    properties = strategies[strategy]
    
    prompt_dict = {}
    for prompt_file in glob.glob(path):
        key = os.path.basename(prompt_file).split('.')[0].lower()
        with open(prompt_file, "r") as f:
            prompt_dict[key] = f.read()
    
    spec = ""
    for key, value in prompt_dict.items():
        spec += f"# {key.upper()}:\n\n{value}\n\n"
    prompt = properties["user_prompt_spec"] + "\n\n" + spec
    
    spec_prompt = [{
        "role": "user",
        "content": prompt
    },
    {
        "role": "assistant",
        "content": "ok"
    }]
    
    if examples_limit > 0 and examples_df is not None:
        spec_prompt
        spec_prompt += build_examples_prompt(strategy=strategy, examples_df=examples_df, limit=examples_limit, headless=True)
            
    if headless:
        prompt = spec_prompt
    else:
        prompt = [{
            "role": "system", 
            "content": properties["system_prompt"]
        }] 
        
        prompt += spec_prompt
        
        if input_data is not None:
            input_prompt = build_example_prompt(
                input_value=input_data[properties["input_column"]], 
                input_label=properties["input_label"], 
                output_label=properties["output_label"]
            )
            prompt += [{
                "role": "user",
                "content": "Based on the API specifications and previous examples, " + properties["prediction_prompt"] + input_prompt[0]["content"]
            }]
    
    
    return prompt


def build_prompt(
    strategy: str,
    prompt_type: str = 'examples',
    input_data: object = None, 
    examples_df: pd.DataFrame = None, 
    examples_limit: int = 30,
    chat_format: bool = True
):
    if prompt_type == 'examples':
        prompt = build_examples_prompt(strategy=strategy, examples_df=examples_df, input_data=input_data, limit=examples_limit)
    elif prompt_type == 'apispec':
        prompt = build_spec_prompt(strategy=strategy, input_data=input_data, examples_df=examples_df, examples_limit=examples_limit)
    
    if not chat_format:
        raise NotImplementedError("Not implemented yet")
    
    return prompt


def load_strategies(filepath='./config/prompts/prompt_strategies.yml'):
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    return data