import pandas as pd
import numpy as np

# Load existing dataset
file_path = r'synthetic_dataset.csv'

try:
    df = pd.read_csv(file_path)
    print("Original data loaded successfully!")
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Function to generate synthetic data
def generate_synthetic_data(df, n_samples=500):
    synthetic_data = []

    for _ in range(n_samples):
        # Randomly select values based on existing data distributions
        timestamp = pd.Timestamp.now()  # You can modify this to create realistic timestamps
        name = f"Synthetic_{np.random.randint(1000)}"  # Generate a synthetic name
        gender = np.random.choice(df['Gender'].dropna().unique())  # Sample gender
        section = np.random.choice(df['Section'].dropna().unique())  # Sample section
        age = np.random.randint(17, 25)  # Assuming age range from 17 to 25
        
        collision_types = np.random.choice(
            ['Body to Ground', 'Ball to body Impact', 'Head to Body collisions', 'None'], 
            size=np.random.randint(1, 4), replace=False
        )
        collision_types_str = ';'.join(collision_types)
        
        injuries = np.random.choice(
            ['Knee Injury', 'Head Injury', 'Ligament Tear', 'Dislocation of joint', 'None'], 
            size=np.random.randint(1, 3), replace=False
        )
        injuries_str = ';'.join(injuries)

        symptoms = np.random.choice(
            ['Swelling', 'Pain', 'Bruising', 'Weakness', 'None'], 
            size=np.random.randint(1, 4), replace=False
        )
        symptoms_str = ';'.join(symptoms)

        knee_injury_overtime = np.random.choice(['Yes', 'No'])
        knee_injury_instant = np.random.choice(['Yes', 'No'])
        
        synthetic_data.append([
            timestamp, name, gender, section, age,
            collision_types_str, injuries_str,
            symptoms_str, knee_injury_overtime,
            knee_injury_instant
        ])
    
    # Create a DataFrame from synthetic data
    columns = [
        "Timestamp", "Name", "Gender", "Section", "Age",
        "Have you experienced these collision during any sports activity?",
        "What kind of injuries have you experienced during game?",
        "Symptoms experienced by player after injury?",
        "Did you experience knee injury overtime?",
        "Did you experience knee injury at one instant of the game?"
    ]
    
    synthetic_df = pd.DataFrame(synthetic_data, columns=columns)
    return synthetic_df

# Generate synthetic data
synthetic_df = generate_synthetic_data(df)

# Combine original and synthetic datasets if needed
combined_df = pd.concat([df, synthetic_df], ignore_index=True)

# Save the combined dataset to an Excel file
output_file_path = r'C:\Users\User\Desktop\project 1\synthetic_dataset.xlsx'
combined_df.to_excel(output_file_path, index=False)
print(f"Combined dataset saved successfully to {output_file_path}")
