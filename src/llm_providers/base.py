from abc import ABC, abstractmethod
from typing import Dict

class LLMProvider(ABC):
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    async def generate(self, prompt: str,tone_rules: list[str]) -> str:
        """
        Generate a kid-friendly response with tone level and guardrails.
        """
        # ✅ Apply guardrails
        if any(word in prompt.lower() for word in ["violence", "drugs", "adult"]):
            return "Hmm, that’s not something I can talk about. Can you ask me something fun instead? 😊"

    async def kid_friendly_guide(self, country: str, tone_rules: list[str]) -> str:
        prompt = f"""
            ## Role 🎭
            You are an **experienced educational content developer** who creates engaging, age-appropriate cultural guides for children.

            ## Task 🎯
            Craft a **lively and informative cultural guide** about **{country}**, designed to captivate young learners and foster cultural appreciation.

            ## Instructions 📝
            Your guide must include:
            1. **Festivals** 🎉 – Overview of major festivals in {country}, highlighting 1–2 that children would find fun or relatable.  
            2. **Food** 🍲 – Describe popular and delicious foods that kids in {country} commonly enjoy.  
            3. **Cartoons/TV Shows** 📺 – Share examples of shows loved by children in {country}.  
            4. **Folktale** 📖 – Provide a short and child-friendly summary of a traditional folktale from {country}.  

            ## Constraints ⏳
            - Word count: **180–220 words**  
            - Use **child-friendly, simple, and engaging** language  
            - Add **appropriate emojis** throughout  
            - Respect **cultural authenticity**  

            ## Style & Tone Rules 🌈
            - Fun, friendly, and educational  
            - Clear and accessible for kids  
            - Balanced mix of storytelling and information  
            - Follow these extra tone rules: {', '.join(tone_rules)}  

            ## Output Format 📦
            - A single, **continuous narrative guide** (not bullet points)  
            - Use **paragraphs with emojis sprinkled in**  
            - Around **200 words total**  
        """
        return await self.generate(prompt)


    async def compare_cultures(self, my_culture: str, target: str, tone_rules: list[str]) -> str:
        prompt = f"""
            ## Role 🎭
            You are an **expert in cross-cultural communication and children’s education**.

            ## Task 🎯
            Explain **similarities and differences** between **{my_culture}** and **{target}**.

            ## Instructions 📝
            - Use **two bullet lists** with these titles:  
            - **Same ✅**  
            - **Different 🌍**  
            - Write in **simple, child-friendly language** with a **friendly and clear tone**.  
            - Add **relevant emojis** to make it fun and easy to understand.  
            - Highlight **shared values** and **unique traditions, foods, clothes, or celebrations**.  
            - Follow these tone rules: {', '.join(tone_rules)}  

            ## Constraints ⏳
            - Total length: **around 120 words**  
            - Keep it **clear, friendly, accessible, and engaging for kids**.  

            ## Output Format 📦
            - Two bullet lists: **Same ✅** and **Different 🌍**  

            ---

            ## Few-Shot Examples ✨

            **Example 1 (India 🇮🇳 vs. Japan 🇯🇵):**  
            **Same ✅**  
            - People love colorful festivals 🎉  
            - Families enjoy sharing meals together 🍲  
            - Both respect teachers and elders 🙏  

            **Different 🌍**  
            - In India, many people eat with their hands, while in Japan chopsticks are used 🥢  
            - Indian festivals are often loud and bright, while Japanese festivals can be calmer with lanterns 🏮  
            - Clothes differ: saris and kurtas in India, kimonos in Japan 👘  

            ---

            **Example 2 ({my_culture} 🇨🇷 vs. {target} 🌍):**  
            *(Your answer goes here in the same format)*  
        """
        return await self.generate(prompt)

