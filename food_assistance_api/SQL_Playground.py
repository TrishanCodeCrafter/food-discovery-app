from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///food_assistance.db")

with engine.connect() as conn:
    # result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    # print("Tables in DB:")
    # for row in result:
    #     print(row[0])
        
    
        
    result = conn.execute(text("SELECT * FROM agencies LIMIT 0"))
    print("\nColumns\n")
    for row in result.keys():
        print(row,  end = "  |  ")  # Print each row, add \n for readability
     

    # Example: show data from a specific table
    result = conn.execute(text("SELECT * FROM agencies WHERE agency_id = '15567-MOMK-01' LIMIT 5;"))
    print("\nSample Data:\n")
    for row in result:
        print(row,  "\n")  # Print each row, add \n for readability
        
        
    result = conn.execute(text("SELECT * FROM agencies;"))
    print("\nSample Data:\n")
    for row in result:
        print(row,  "\n")     
        
    