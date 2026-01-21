import os
import json
from typing import Optional, Tuple
from src.models import Extension

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class RiskAssessor:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        self.model = "gpt-4"

        if self.groq_api_key and OpenAI:
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.groq_api_key
            )
            # Updated to current supported model
            self.model = "llama-3.3-70b-versatile" 
        elif self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key)

    def assess(self, extension: Extension) -> Tuple[str, str]:
        if not self.client:
           return "UNKNOWN", "LLM Analysis skipped (No API Key or OpenAI lib)."

        prompt = self._build_prompt(extension)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Security Analyst. You assess browser extensions for security risks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            content = response.choices[0].message.content
            
            # Expecting something like:
            # Risk: High
            # Reason: ...
            
            # Or try to parse JSON if we asked for it. 
            # flexible parsing:
            lines = content.strip().split('\n')
            score = "UNKNOWN"
            reason = content
            
            for line in lines:
                if line.lower().startswith("risk:"):
                    score = line.split(":", 1)[1].strip()
                if line.lower().startswith("reason:"):
                     # This might just capture the first line of reason
                     pass
                     
            return score, reason
            
        except Exception as e:
            return "UNKNOWN", f"Error during LLM analysis: {e}"

    def _build_prompt(self, extension: Extension) -> str:
        # Construct a detailed summary
        return f"""
Analyze the risk of the following browser extension:

Name: {extension.name}
ID: {extension.id}
Version: {extension.version}
Author: {extension.author}
Description: {extension.description}
Permissions: {', '.join(extension.permissions)}
CSP: {extension.csp}
Extension Age (Days): {extension.age_days or 'Unknown'}
Extracted URLs: {', '.join(extension.extracted_urls[:10])} ... ({len(extension.extracted_urls)} total)
Extracted IPs: {', '.join(extension.extracted_ips[:10])} ... ({len(extension.extracted_ips)} total)

Determine the Risk Level (Low, Medium, High, Critical) and provide a justification.
Format your response exactly as follows:
Risk: <Level>
Reason: <Short justification summary>
"""
