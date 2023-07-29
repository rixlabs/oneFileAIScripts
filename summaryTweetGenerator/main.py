import os
import sys
import arxiv_search 
from langchain import PromptTemplate, LLMChain 
from langchain.chat_models import ChatOpenAI    

source_file_path = "source_file.txt"

def generate_tweet(source_file):
    # OpenAI API KEY Check
    if not os.environ.get("OPENAI_API_KEY"):
        raise "OPENAI_API_KEY not set"

    # Main prompt
    prompt_tweet_template = """
    You are a AI technology blogger who write regular tweets for shortly summarizing new papers on Arxiv about language
    model topics. You write summary for tweets based on text with content of Title, Abstract, URL: ##start {text} ##end
    Your write a 50-word quick summary including key information from the Title and Abstract, then, attach the URL after summary.
    Summary: 
    """

    PROMPT_TWEET = PromptTemplate(template=prompt_tweet_template, input_variables=["text"]) 
    llm = ChatOpenAI(temperature=0.5) 

    tweet_chain = LLMChain(llm=llm, prompt=PROMPT_TWEET,verbose=True)  

    # format the text to help the model identify the different sections and to specify a URL manually
    #to_summarise = f"Title: Meta and Microsoft Introduce the Next Generation of Llama, Abstract:  {source_file.read()} , URL: https://about.fb.com/news/2023/07/llama-2/" 

    # BONUS: you can comment line 28 and uncomment line 31 to use the ARXIS api as a source. Youi still need to pass a dummy file(or change the guard at line 37)
    to_summarise = arxiv_search.arxiv_search()

    return tweet_chain.run(to_summarise)  


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py source_file.txt")
        sys.exit(1)
    
    source_file_path = sys.argv[1]

    try:
        source_file = open(source_file_path, "r")
        # The output is a json file containing the general sentiment, the key factor of the scoring and a score from 0 to 10 (0 ultra negative to 10 ultra positive)
        tweet_text = generate_tweet(source_file)

        print("\n--- Tweet body ---\n")
        print(tweet_text)   
        print("\n--- End of Tweet body ---\n")
        
    except FileNotFoundError:
        print(f"Error: File '{source_file_path}' not found.")