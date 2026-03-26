import os
# Set default region to CN to ensure connectivity for the translators library in China
os.environ["translators_default_region"] = "CN"

import translators as ts
import time

class DocTranslator:
    def __init__(self, source='en', target='zh-CN', engine='bing'):
        self.source = source
        self.target = target
        self.engine = engine

    def _map_lang(self, lang, engine):
        if lang == 'zh-CN':
            return 'zh-Hans' if engine == 'bing' else 'zh'
        return lang

    def translate_texts(self, texts):
        """Translate a list of strings in batches to save time."""
        if not texts:
            return []
            
        results = [None] * len(texts)
        current_batch_indices = []
        current_batch_texts = []
        current_len = 0
        
        # Separator that shouldn't appear in text
        separator = "\n---[SEP]---\n"
        
        for i, text in enumerate(texts):
            if not text or not text.strip():
                results[i] = text
                continue
            
            # If adding this text would exceed ~4000 chars, translate the current batch
            if current_len + len(text) + len(separator) > 3500:
                translated = self._translate_batch(current_batch_texts, separator)
                for idx, t in zip(current_batch_indices, translated):
                    results[idx] = t
                current_batch_indices = []
                current_batch_texts = []
                current_len = 0
            
            current_batch_indices.append(i)
            current_batch_texts.append(text)
            current_len += len(text) + len(separator)
            
        if current_batch_texts:
            translated = self._translate_batch(current_batch_texts, separator)
            for idx, t in zip(current_batch_indices, translated):
                results[idx] = t
            
        return results

    def _translate_batch(self, batch, separator):
        if not batch:
            return []
        
        combined_text = separator.join(batch)
        translated_combined = self.translate_text(combined_text)
        
        # Split back by the separator
        translated_list = translated_combined.split(separator.strip())
        
        # Clean up and ensure we have same count (if translation messed up separator, fallback to single)
        if len(translated_list) != len(batch):
            print(f"Batch translation error (Count mismatch). Expected {len(batch)}, got {len(translated_list)}. Falling back to single translation.")
            return [self.translate_text(t) for t in batch]
            
        return [t.strip() for t in translated_list]

    def translate_text(self, text):
        if not text.strip():
            return text
        try:
            # First try with Bing which is fast
            src = self._map_lang(self.source, self.engine)
            tgt = self._map_lang(self.target, self.engine)
            return ts.translate_text(text, translator=self.engine, from_language=src, to_language=tgt)
        except Exception as e:
            print(f"Translation error with {self.engine}: {e}. Retrying with alibaba...")
            try:
                # Fallback to Alibaba
                src = self._map_lang(self.source, 'alibaba')
                tgt = self._map_lang(self.target, 'alibaba')
                return ts.translate_text(text, translator='alibaba', from_language=src, to_language=tgt)
            except Exception as e2:
                print(f"Second translation error: {e2}")
                return text

    def set_languages(self, source, target):
        self.source = source
        self.target = target

