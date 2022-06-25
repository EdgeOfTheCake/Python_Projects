#%%
import matplotlib.pyplot as plt
import pandas as pd


class Visualizer:
    def __init__(self, scrape_results):
        self.scrape_results = scrape_results

    def create__and_print_dataframe(self):
            return pd.DataFrame(self.scrape_results)

    def visualize_products(self):
            df = self.create__and_print_dataframe()
            print(df)

            df = df.set_index('Shop')
            df['Price'] = pd.to_numeric(df['Price'])

            ax = df['Price'].plot(kind="bar", title="Price comparison in different webshops", figsize=(8, 5), legend=True, fontsize=12, color='lightblue')
            
            ax.set_xlabel("Shops", fontsize=12)
            ax.set_ylabel("Price (USD)", fontsize=12)
            ax.tick_params(axis='x', rotation=0)
            for index, value in enumerate(df['Price']):
                plt.text(index, value, str(value), ha="center", va="bottom")
            plt.show()