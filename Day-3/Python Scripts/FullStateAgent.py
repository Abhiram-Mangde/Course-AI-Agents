class StatefulAgent:
    def __init__(self):
        self.session = ChatSession()
        self.compressed_memory = ""
    
    def add_memory(self, text):
        store_memory(text)

    def get_context(self, query):
        retrieved = recall(query)
        return [
            {"role": "system", "content": f"Memory: {retrieved}"},
            {"role": "system", "content": f"Conversation summary: {self.compressed_memory}"}
        ] + self.session.get() + [{"role": "user", "content": query}]

    def answer(self, query):
        self.add_memory(query)

        # compress if too long
        if len(self.session.get()) > 10:
            self.compressed_memory = compress_history(self.session.get())
            self.session = ChatSession()  # reset session but keep summary

        messages = self.get_context(query)

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        ).choices[0].message.content
        
        self.session.add("assistant", response)
        return response
