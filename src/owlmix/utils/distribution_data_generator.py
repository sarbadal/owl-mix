import numpy as np
 
class CategoryDistributionGenerator:
    def __init__(self, categories: list):
        self.categories = categories
 
    def generate(self, n_samples=1000, sigma=1.0):
        """
        Generate category list where frequency follows normal distribution 
        centered on the most frequent category.
        """
 
        n_categories = len(self.categories)
 
        # Step 1: positions (centered)
        x = np.linspace(-2, 2, n_categories)
 
        # Step 2: normal distribution PDF
        probs = np.exp(-0.5 * (x / sigma) ** 2)
 
        # Step 3: normalize probabilities
        probs = probs / probs.sum()
 
        # Step 4: convert to counts
        counts = (probs * n_samples).astype(int)
 
        # Fix rounding issue
        diff = n_samples - counts.sum()
        counts[np.argmax(counts)] += diff
 
        # Step 5: expand into list
        result = []
        for category, count in zip(self.categories, counts):
            result.extend([category] * count)
 
        # Step 6: shuffle (important!)
        np.random.shuffle(result)
 
        return result