import os
import pandas as pd
import matplotlib.pyplot as plt

class SmartFanAIAgent:
    def __init__(self, data_file="atomberg_sov_results.csv"):
        self.data_file = data_file
        self.required_cols = ["Brand", "SoV (%)", "Avg Sentiment"]
        self.load_data()

    def load_data(self):
        
        if os.path.exists(self.data_file):
            self.df = pd.read_csv(self.data_file)
            print(f"Loaded data from {self.data_file}")
        else:
            print("Data file not found. Using default data.")
            self.df = pd.DataFrame({
                "Brand": ["Atomberg", "Havells", "Crompton", "Orient", "Usha"],
                "Mentions": [45, 30, 20, 15, 10],
                "Avg Sentiment": [0.35, 0.10, -0.20, 0.05, -0.10]
            })
        
        if "SoV (%)" not in self.df.columns:
            self.df["SoV (%)"] = (self.df["Mentions"] / self.df["Mentions"].sum()) * 100
       
        missing = [c for c in self.required_cols if c not in self.df.columns]
        if missing:
            raise ValueError(f"Missing columns in data: {missing}")
       
        self.df["SoV (%)"] = pd.to_numeric(self.df["SoV (%)"], errors="coerce")
        self.df["Avg Sentiment"] = pd.to_numeric(self.df["Avg Sentiment"], errors="coerce")

    def plot_sov(self):
        plt.figure(figsize=(8,5))
        plt.bar(self.df["Brand"], self.df["SoV (%)"])
        plt.title("Share of Voice (SoV) - Smart Fan Search", fontsize=14)
        plt.xlabel("Brand")
        plt.ylabel("SoV (%)")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.show()

    def plot_sentiment(self):
        plt.figure(figsize=(8,5))
        plt.bar(self.df["Brand"], self.df["Avg Sentiment"])
        plt.title("Average Sentiment by Brand", fontsize=14)
        plt.xlabel("Brand")
        plt.ylabel("Sentiment Score (-1 = Negative, +1 = Positive)")
        plt.axhline(0)
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.show()

    def brand_info(self, brand_name):
        brand_data = self.df[self.df["Brand"].str.lower() == brand_name.lower()]
        if brand_data.empty:
            return f"No data found for brand '{brand_name}'."
        brand_data = brand_data.iloc[0]
        return (f"Brand: {brand_data['Brand']}\n"
                f"Share of Voice: {brand_data['SoV (%)']:.2f}%\n"
                f"Average Sentiment: {brand_data['Avg Sentiment']:.2f}")

    def run(self):
        print("Welcome to the Smart Fan AI Agent!")
        print("You can ask about brand performance or command plots.")
        print("Examples:")
        print("- brand info Atomberg")
        print("- show sov chart")
        print("- show sentiment chart")
        print("- exit")
        while True:
            user_input = input("\nEnter command: ").strip().lower()
            if user_input == "exit":
                print("Exiting Smart Fan AI Agent. Goodbye!")
                break
            elif user_input.startswith("brand info"):
                _, _, brand = user_input.partition("brand info")
                brand = brand.strip()
                if brand:
                    print(self.brand_info(brand))
                else:
                    print("Please specify a brand name after 'brand info'.")
            elif user_input == "show sov chart":
                self.plot_sov()
            elif user_input == "show sentiment chart":
                self.plot_sentiment()
            else:
                print("Unknown command. Please try again.")

if __name__ == "__main__":
    agent = SmartFanAIAgent()
    agent.run()

