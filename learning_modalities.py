import pandas as pd

def load_data():
    while True:
    #prompt for file path until successful
        file_path = input("Data file path: ")
        try:
            df = pd.read_csv(file_path)
            #print("CSV columns:", df.columns.tolist()) //test the columns
            df['week'] = pd.to_datetime(df['week'], format="%m/%d/%Y %I:%M:%S %p")
            return df
        except Exception as e:
            print(f"Error loading file: {e}")
            continue

def list_dates(df):
    unique_dates = sorted(df['week'].dt.strftime("%m/%d/%Y").unique(), reverse=True)
    for date in unique_dates:
        print(date)

def modality_summary(df, state, date_str):
    #parse date
    try:
        date = pd.to_datetime(date_str, format="%m/%d/%Y")
    except:
        print("Invalid date format. Use MM/DD/YYYY.")
        return

    #filter by date (df['week'] is a datetime)
    filtered = df[df['week'] == date]

    #filter by state if not "all"
    if state.lower() != 'all':
        filtered = filtered[filtered['state'] == state.upper()]

    if filtered.empty:
        print("No data found for that state and date.\n")
        return

    #totals
    total_schools  = filtered['operational_schools'].sum()
    total_students = filtered['student_count'].sum()

    #group sums by modality
    school_counts  = filtered.groupby('learning_modality')['operational_schools'].sum()
    student_counts = filtered.groupby('learning_modality')['student_count'].sum()

    modalities = ["In Person", "Hybrid", "Remote"]

    print("-------------------------------")
    print(f"Date: {date.strftime('%m/%d/%Y')}")
    print(f"Description: {state.upper()}")
    print(f"{total_schools:,} schools")
    print(f"{total_students:,} students")
    print("Schools per modality:")
    for m in modalities:
        cnt   = school_counts.get(m, 0)
        pct   = cnt / total_schools * 100 if total_schools else 0
        print(f" * {cnt:,} ({pct:.1f}%) {m}")
    print("Students per modality:")
    for m in modalities:
        cnt   = student_counts.get(m, 0)
        pct   = cnt / total_students * 100 if total_students else 0
        print(f" * {cnt:,} ({pct:.1f}%) {m}")
    print("-------------------------------\n")


def analysis_by_state_over_time(df):
    while True:
        state = input("Enter state (2-letter code) or 'all': ").upper()
        modality = input("Enter modality (In Person, Hybrid, Remote): ").strip().lower()
        modality_key = None

        if modality == "in person":
            modality_key = "In Person"
        elif modality == "hybrid":
            modality_key = "Hybrid"
        elif modality == "remote":
            modality_key = "Remote"
        else:
            print("Invalid modality.")
            continue

        filtered = df.copy()
        if state != "ALL":
            filtered = filtered[filtered["state"] == state]

        #filter rows for selected modality
        modality_filtered = filtered[filtered["learning_modality"] == modality_key]

        #group by week and sum operational schools
        grouped = modality_filtered.groupby("week")["operational_schools"].sum().sort_index()
        print(f"\nTrend of {modality.title()} schools for {'all states' if state == 'ALL' else state}:")
        for date, count in grouped.items():
            print(f"{date.strftime('%m/%d/%Y')}: {count:,}")

        again = input("\nDo another modality trend analysis? (y/n): ").lower()
        if again != 'y':
            break

def main():
    print("Learning Modalities Analyzer")
    df = load_data()

    while True:
        print("\nData analysis options:\n")
        print("1. List dates")
        print("2. Learning modality by state on date")
        print("3. Learning modality by state across time")
        print("4. Exit")
        choice = input("\nEnter the number of the option (1, 2, 3, or 4): ").strip()

        if choice == '1':
            list_dates(df)
        elif choice == '2':
            while True:
                print("Enter the two digit code (CA, MO, IL, TX, etc.) for a state or 'all' for all states.")
                state = input("State (2 digit code or 'all'): ").strip()
                date  = input("Date (MM/DD/YYYY): ").strip()
                modality_summary(df, state, date)
                if input("Enter another state and date? (y/n): ").lower() != 'y':
                    break
        elif choice == '3':
            analysis_by_state_over_time(df)
        elif choice == '4':
            print("Exiting program.")
            exit()
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
