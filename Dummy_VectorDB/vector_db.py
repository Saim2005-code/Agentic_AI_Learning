
def search_knowledge_base(query:str) -> str:
    
    mock_qdrant = { "quantum computing": "quantum translation uses quantum entanglement to transfer quantum information between two locations" ,
    "operating system": "In POSIX, the fork() system call creates a new process by duplicating the calling process " ,
    "company policy" : "Employeees are granted 20 days of paid time off per year." 
    }

    for key,context in mock_qdrant.items():
        if key in query.lower():
            return f"Retrieved Context: {context}"

        return "No relevant document was found in the knowledge base."
