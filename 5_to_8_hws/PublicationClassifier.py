from re import split as sp


class PublicationClassifier:
    keywords = {
        'news': { 'news', 'headline', 'report', 'reporter', 'journal', 'journalist',
        'breaking', 'update', 'live', 'coverage', 'announcement',
        'exclusive', 'interview', 'media', 'daily', 'broadcast', 'channel',
        'editorial', 'alert', 'developing', 'latest',
        'newspaper', 'press', 'article', 'source', 'coverage',
        'trending', 'event', 'public', 'statement', 'reveal', 'expose',
        'anchor', 'bulletin', 'issue', 'publication', 'column'},

        'privatead': {'ad', 'advertisement', 'advertising', 'promo', 'promotion',
        'sell', 'buy', 'discount', 'offer', 'deal', 'bargain', 'shop', 'shopping',
        'save', 'clearance', 'exclusive', 'coupon', 'hurry', 'subscribe', 'pricing',
        'available', 'gift', 'investment', 'purchase'},
   
        'weatherforecast': {'weather', 'forecast', 'temperature', 'rain', 'rainy', 'snow', 'snowfall',
        'cloudy', 'sunny', 'storm', 'stormy', 'wind', 'windy', 'humidity',
        'climate', 'hot', 'cold', 'freezing', 'thunder', 'lightning',
        'degrees', 'conditions', 'precipitation', 'heatwave', 'chilly', 'warm',
        'tornado', 'hail', 'fog', 'drizzle', 'meteorologist'}
    }
 
    @staticmethod
    def classify(text):
        words = set(sp(r'[!,.? :;]', text.lower()))
        match_counts = {category: len(words & kw_set) for category, kw_set in PublicationClassifier.keywords.items()}
        best_match = max(match_counts, key=match_counts.get)
        return best_match
