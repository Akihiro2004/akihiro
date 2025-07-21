import requests
import json
import os
import re
from typing import Any, List, Dict, Union

def _make_gemini_request(prompt: str) -> str:
    api_key = "AIzaSyDH_7WxwGq7_UmIEoDpX9IVwKCFCLxTN9k"
    if not api_key:
        raise ValueError("Please tell Darrien there is a problem with my AI")
    
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        result = response.json()
        return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except (KeyError, IndexError, ValueError) as e:
        raise Exception(f"Error processing API response: {str(e)}")

def isContext(variable, prompt):    
    full_prompt = f"Evaluate if the variable '{variable}' satisfies the condition: {prompt}. Return only 'True' or 'False' as a string."
    payload = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    api_key = "AIzaSyDH_7WxwGq7_UmIEoDpX9IVwKCFCLxTN9k"
    if not api_key:
        raise ValueError("Please tell Darrien there is a problem with my AI")
    
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
            headers=headers,
            data=json.dumps(payload)
        )
        
        response.raise_for_status()
        result = response.json()
        
        response_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        
        if response_text == "True":
            return True
        elif response_text == "False":
            return False
        else:
            raise ValueError(f"Please tell Darrien there is a problem with my AI: {response_text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except (KeyError, IndexError, ValueError) as e:
        raise Exception(f"Error processing API response: {str(e)}")

def summarizeText(text: str, max_length: int = 100) -> str:
    if max_length < 1:
        raise ValueError("max_length must be at least 1")
    
    prompt = f"Summarize the following text to approximately {max_length} words. Ensure the summary is concise, retains key points, and is grammatically correct:\n\n{text}. Do not add additional text or explanations, just return the summary."
    return _make_gemini_request(prompt)

def translateText(text: str, target_language: str) -> str:
    prompt = f"Translate the following text to {target_language}. Ensure the translation is accurate and natural:\n\n{text}. Make sure to only print the result of the translation without any additional text."
    return _make_gemini_request(prompt)

def extractEntities(data: Any) -> List[Dict[str, str]]:
    if isinstance(data, (list, dict)):
        input_text = json.dumps(data)
    else:
        input_text = str(data)
    
    prompt = f"Extract named entities (people, places, organizations, etc.) from the following text. Return a valid JSON list of objects with 'entity' and 'type' fields only, e.g., '[{{\"entity\": \"John Doe\", \"type\": \"Person\"}}]'. Do not include any additional text or explanations:\n\n{input_text}"
    response = _make_gemini_request(prompt)
    
    try:
        entities = json.loads(response)
        if not isinstance(entities, list):
            raise ValueError("API response is not a list")
        return entities
    except json.JSONDecodeError:
        json_match = re.search(r'(\[\s*\{.*?\}\s*(?:,\s*\{.*?\}\s*)*\])', response, re.DOTALL)
        if json_match:
            try:
                entities = json.loads(json_match.group(1))
                if not isinstance(entities, list):
                    raise ValueError("Extracted content is not a list")
                return entities
            except json.JSONDecodeError:
                raise Exception("Failed to parse API response as JSON after extraction attempt")
        raise Exception("Failed to parse API response as JSON")