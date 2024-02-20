import re


class ParseCSV:
    def __call__(self, df):
        df["ip_stance"] = df.generated_text.map(
            lambda x: self.get_category(x, "israel-palestine stance:.+\n"))
        df["ur_stance"] = df.generated_text.map(
            lambda x: self.get_category(x, "russia-ukraine stance:.+\n"))
        
        df["ip_score"] = df.generated_text.map(
            lambda x: self.get_score(x, 0))
        df["ru_score"] = df.generated_text.map(
            lambda x: self.get_score(x, 1))
        
        df["ip_reason"] = df.generated_text.map(
            lambda x: self.get_reason(x, 0))
        df["ru_reason"] = df.generated_text.map(
            lambda x: self.get_reason(x, 1))
        
        return df
        
    def get_reason(self, text, id):
        pattern = "(?<=reason:).+"
        matches = [match for match in re.finditer(pattern, text)]
        
        if matches is None:
            return None
        
        return text[matches[id].start() : matches[id].end()].strip()
    
    def get_category(self, text, pattern):
        match = re.search(pattern, text)
        
        if match is None:
            return None
        
        return text[match.start():match.end()].split()[-1].lower()
    
    def get_score(self, text, id):
        pattern = "score:.+\n"
        matches = [match for match in re.finditer(pattern, text)]
        
        if matches is None:
            return None
        
        try:
            return float(text[matches[id].start() : matches[id].end()].split()[-1])
        except Exception:
            return None