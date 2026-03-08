from flask import Flask, render_template, request
import pickle
import numpy as np

# Load pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index3.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num-ratings'].values),
                           rating=list(popular_df['avg_ratings'].values),
                           total_books=len(popular_df)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend1.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('book_name', '').strip()
    data = None
    error_message = None
    
    # Check if user entered something
    if not user_input:
        error_message = "Please enter a book name."
        return render_template('recommend1.html', error_message=error_message)
    
    try:
        # Search for the book in the pt index
        if user_input not in pt.index:
            error_message = f"Sorry, '{user_input}' not found in our database. Try another book name."
            return render_template('recommend1.html', error_message=error_message)
        
        # Get the index of the book
        index = np.where(pt.index == user_input)[0][0]
        
        # Get similar books
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]
        
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        
        return render_template('recommend.html', data=data)
    
    except Exception as e:
        print(f"Error: {e}")
        error_message = f"An error occurred. Please try another book name."
        return render_template('recommend1.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)