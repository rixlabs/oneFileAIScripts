import os
import sys
from langchain import PromptTemplate, LLMChain 
from langchain.chat_models import ChatOpenAI    

source_file_path = "source_file.txt"

# Pass a text file containing the text to analyse to the function
def analyse_sentiment(source_file):

    # OpenAI API KEY Check
    if not os.environ.get("OPENAI_API_KEY"):
        raise "OPENAI_API_KEY not set"

    # Main prompt
    prompt_sentiment_template = """
    Analyze the sentiment of the following hotel review: ##start {text} ##end
    as result provide a json with 3 attributes: General sentiment as generalSentiment, key factor of sentiment as keyFactors array, a score from 1 to 10 where 1 is extremely negative and 10 is extremely positive as score. don't add any text to the result section only the pure result
    """

    PROMPT_SENTIMENT = PromptTemplate(template=prompt_sentiment_template, input_variables=["text"]) 

    # The 0.5 temperature is to contain the randomness
    llm = ChatOpenAI(temperature=0.5) 
    sentiment_chain = LLMChain(llm=llm, prompt=PROMPT_SENTIMENT,verbose=True)   
    to_analyse = source_file.read()

    return sentiment_chain.run(to_analyse)  

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py source_file.txt")
        sys.exit(1)
    
    source_file_path = sys.argv[1]

    try:
        source_file = open(source_file_path, "r")
        # The output is a json file containing the general sentiment, the key factor of the scoring and a score from 0 to 10 (0 ultra negative to 10 ultra positive)
        print(analyse_sentiment(source_file))   
    except FileNotFoundError:
        print(f"Error: File '{source_file_path}' not found.")