from src.decision_engine import answer
from src.retriever import retrieve
from src.database import SessionLocal
from src.models import Memory


user_id = "test@gmail.com"

# Step 1: Reset user memory (optional but recommended for testing)
def reset_memory(user_id):
    db = SessionLocal()
    db.query(Memory).filter(Memory.user_id == user_id).delete()
    db.commit()
    db.close()


# Step 2: Store test data (same as webpage input)
def setup_user(user_id):
    data = """
    My name is Harsh. I am 23 years old and I live in Hyderabad. 
    I work at TCS as a system engineer. I previously completed my B.Tech in Computer Science. 
    I enjoy playing badminton and I like chess. I also love coding and solving problems. 
    I am currently learning artificial intelligence and machine learning. 

    I often travel during holidays and last year I visited Goa with my friends. 
    I also visited Bangalore for a tech conference. 

    My favorite food is biryani and I also like pizza and ice cream. 
    I usually wake up early and prefer working in the morning. 
    I sometimes work late at night when I have deadlines. 

    I have an exam scheduled on December 10th. 
    I use Python and Java for coding. I am interested in backend development. 

    I have a younger brother and my parents live in my hometown. 
    I like watching movies on weekends and listening to music while coding.
    """
    
    answer(data, user_id)


# Step 3: Debug memory (to verify data is stored)
def print_memory(user_id):
    db = SessionLocal()
    mems = db.query(Memory).filter(Memory.user_id == user_id).all()

    print(f"\n📦 Stored Memories ({len(mems)}):\n")
    for m in mems:
        print(f"- {m.text}")

    db.close()


# Step 4: Test queries
queries = [
    # Basic
    "What is my name",
    "How old am I",
    "Where do I live",
    "Where do I work",
    "What is my job",

    # Variations / synonyms
    "What is my profession",
    "What do I do for a living",
    "Where am I based",

    # Preferences
    "What do I like",
    "What are my hobbies",
    "What do I enjoy",
    "What food do I prefer",

    # Interests / skills
    "What am I interested in",
    "What do I use for coding",
    "Which technologies do I use",

    # Education (NEW)
    "Where did I study",
    "What did I study",

    # Travel
    "Where did I travel last year",
    "Where else did I travel",
    "Did I visit Bangalore",

    # Behavior
    "Do I wake up early",
    "Do I work at night",

    # Multi-intent
    "Where do I work and what do I like",
    "What do I do and where do I live",

    # Broad
    "Tell me about me",
    "What do you know about me",

    # Edge cases
    "What is my salary",
    "Do I have a car",
    "Do I have siblings",
    "Who is in my family",

    # Yes/No style
    "Do I like pizza",
    "Do I travel often",

    # Confusion test
    "Where do my parents live",
]


def run_tests():
    print("\n--- TEST RESULTS ---\n")

    for i, q in enumerate(queries, 1):
        print(f"\n{i:02d}. Q: {q}")

        # 🔍 Show retrieval debug
        results = retrieve(user_id, q)
        print("   🔎 Top Matches:")
        for score, text in results:
            print(f"      {round(score, 3)} → {text}")

        # 🤖 Final answer
        res = answer(q, user_id)
        print(f"   💬 A: {res}")
        print("-" * 60)


# MAIN EXECUTION
if __name__ == "__main__":
    print("\n Running Memory System Test...\n")

    reset_memory(user_id)      # optional (clean slate)
    setup_user(user_id)        # store data
    print_memory(user_id)      # verify storage
    run_tests()                # run queries