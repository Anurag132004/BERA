import os
import json
from typing import Optional, Tuple
from src.models import Extension

# Try to import OpenAI - it might not be installed
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# This is my AI-powered risk assessor
# I send extension info to an LLM and it tells me if it looks risky
class RiskAssessor:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        self.model = "gpt-4"

        # I prefer Groq because it's free! If that's not available I fall back to OpenAI
        if self.groq_api_key and OpenAI:
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.groq_api_key
            )
            self.model = "llama-3.3-70b-versatile"
        elif self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key)

    def assess(self, extension: Extension) -> Tuple[str, str]:
        # If there's no API key, I can't do the assessment
        if not self.client:
            return "UNKNOWN", "LLM Analysis skipped (No API Key or OpenAI lib)."

        prompt = self._build_prompt(extension)
        
        try:
            # Ask the AI to analyze the extension
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Security Analyst. You assess browser extensions for security risks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0  # I want consistent answers, not random
            )
            content = response.choices[0].message.content
            
            # Parse the response to get the risk level
            lines = content.strip().split('\n')
            score = "UNKNOWN"
            reason = content
            
            for line in lines:
                if line.lower().startswith("risk:"):
                    score = line.split(":", 1)[1].strip()
                     
            return score, reason
            
        except Exception as e:
            return "UNKNOWN", f"Error during LLM analysis: {e}"

    def _build_prompt(self, extension: Extension) -> str:
        # I build a detailed prompt with all the info I gathered
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
