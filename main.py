from graph import graph

topic = input("Topic: ").strip()

if not topic:
    print("Please enter a topic.")
else:
    result = graph.invoke({"topic": topic, "research": "", "report": ""})
    print("\n===== REPORT =====\n")
    print(result["report"])