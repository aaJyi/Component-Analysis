import re


class Deduplicator:

    def normalize(self, text):

        text = text.upper()

        text = re.sub(r'\\s+', '', text)

        return text

    def deduplicate(self, components):

        seen = set()

        results = []

        for c in components:

            key = self.normalize(c['name'])

            if key in seen:
                continue

            seen.add(key)

            results.append(c)

        return results