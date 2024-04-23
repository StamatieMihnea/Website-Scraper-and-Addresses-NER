from openai import OpenAI


class LLMService:
    def __init__(self):
        self._client = OpenAI(
            api_key='your-key-here',
        )

    def address_ner(self, text):
        message = [
            {"role": "system", "content":
                """You are a highly reliable and deterministic assistant specialized in pattern recognition and data extraction. Your task is to parse and extract address information from provided text inputs.

        The specific data to be extracted is: country, region, city, postcode, road, and road_numbers.
        The expected output format is:
        {
          "country": null or "detected/inferred value",
          "region": null or "detected/inferred value",
          "city": null or "detected/inferred value",
          "postcode": null or "detected/inferred value",
          "road": null or "detected/inferred value",
          "road_numbers": null or "detected/inferred value"
        }
        Complete the empty fields based on the provided ones. Infer hierarchically higher fields whenever possible based on the detected information. For example, if a city is detected, infer the country it belongs to.  For exemple, if "London" is mentioned, you should infer "United Kingdom" as the country.

        Remember to maintain this format consistently, ensuring your responses are deterministic based on the input provided.
        
"""},
            {"role": "user", "content": "\"\"\"" + text + "\"\"\""}
        ]
        try:
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=0,
                seed=14
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(e)

    def order_links(self, links):
        message = [
            {"role": "system", "content":
                """You are a highly reliable and deterministic assistant. Rank the provided urls by the probability of finding the company location on them. The desired information consist of: country, region, city, postcode, road, and road_numbers. Pages with a relative low probability will be excluded from the list, only if a page have a big probability.
                You will exclude urls that point to direct file downloads (like PDFs or images).
                You will exclude urls that seems to point to a product page.
                The list should not be empty.
                 The expected output format is:
                 [
                  "first url",
                  "second url",
                  ...
                 ]
                 
                 Remember to maintain this format consistently, ensuring your responses are deterministic based on the input provided.
            """},
            {"role": "user", "content": "\"\"\"" + links + "\"\"\""}
        ]
        try:
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=0,
                seed=14
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(e)
