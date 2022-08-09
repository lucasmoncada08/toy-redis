# Encoding functionality from regular text to RESP format
class RESPEncoder:
    def encode(self, text: str) -> bytes:

        text_split = text.split(' ')

        if len(text_split) == 0 or text_split[0] == "":
            return b"+Invalid\r\n"

        if len(text_split) == 1:
            return f"+{text}\r\n".encode()

        # if the input had multiple seperate words (commands)
        encoded_str = f"*{len(text_split)}\r\n"
        for txt in text_split:
            encoded_str += self.encode_bulk_string(txt)
        return encoded_str.encode()

    def encode_bulk_string(self, text: str) -> str:
        return f"${len(text)}\r\n{text}\r\n"

