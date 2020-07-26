# importing packages
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime as dt
import os
import pandas as pd

# defining the format for timestamp
timestamp_format = "%Y-%m-%d %H:%M"

# reading the data through pandas
politics = pd.read_csv('final_text_sentiment.csv', sep = '|')

# function to extract month-year
def tweet_date(ts):
    result = dt.datetime.strptime(ts, timestamp_format)
    result = dt.datetime(result.year, result.month, 1)
    return result

# converting the text to all lower strings
politics['clean_tweet'] = politics['clean_tweet'].str.lower()

# getting a date column
politics['date'] = politics['date'].apply(tweet_date)

# function to filter based on text
def filter_tweets(filter_text=''):
    df = politics[politics['clean_tweet'].str.contains(str.lower(filter_text))]
    return df 

# creating plots

# line chart
def tweets_by_date(in_df):

    unq_class = in_df.sentiment_class.unique()
    list_of_dict = []
    for j in range(0, len(unq_class)):
        df = in_df.loc[in_df['sentiment_class'] == unq_class[j]]
        df = df.reset_index(drop=True)
        group_date = df.groupby('date')['date'].count()
        date_l = group_date.index.tolist()
        val_l = group_date.tolist()
        list_of_dict.append({
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": unq_class[j],
                    "x": date_l,
                    "y": val_l
                })
        
    return {
        "data": list_of_dict,
        "layout": {
            "title": "# Tweets over Time",
            "showlegend": True
        }
    }


# donut chart
def tweets_class(in_df):
    
    unq_class = in_df.sentiment_class.unique()
    labels = []
    vals = []
    for j in range(0, len(unq_class)):
        df = in_df.loc[in_df['sentiment_class'] == unq_class[j]]
        len_df = len(df.index)
        labels.append(unq_class[j])
        vals.append(len_df)

    return {
        "data": [
            {
                "type": "pie",
                "labels": labels,
                "values": vals,
                "hole": 0.6
            }
        ],
        "layout": {
            "title": "Overall Sentiment"
        }
    }

# initializing the application
app = dash.Dash()

# for heroku deployment
server = app.server

# don't understand this one bit, but apparently it's needed
server.secret_key = os.environ.get("SECRET_KEY", "secret")

# title of the application
app.title = "Social Media Analysis for Political Organisation"

# layout of the application
app.css.append_css({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
})

app.css.append_css({
    "external_url": 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.scripts.append_script({
    "external_url": "https://code.jquery.com/jquery-3.2.1.min.js"
})

app.scripts.append_script({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
})

# defining the layout now
app.layout = html.Div([
    # row: title
    html.Div([
        html.Div([
            html.H1("Social Media Analysis for Political Organisations", className="text-center")
        ], className="col-md-12")
    ], className="row"),

    # including some markdown text
    html.Div([
        html.Div([
                dcc.Markdown('''

                ''')
        ], className="col-md-12")
    ], className="row"),

    # box for filtering tweets
    html.Div([
        html.Div([
            html.P([
                html.B("Filter the tweets:  "),
                dcc.Input(
                    placeholder="Try 'Modi'",
                    id="tweet-filter",
                    value="")
            ]),
        ], className="col-md-12"),
        ], className="row"),
    
    # row: line chart + donut chart
    html.Div([
        html.Div([
            dcc.Graph(id="tweet-by-date")
        ], className="col-md-8"),
        html.Div([
            dcc.Graph(id="tweet-class")
        ], className="col-md-4")
    ], className="row"),
    
    # Row: Footer
    html.Div([
        html.Div([
            html.H1("Made by Avnish,Shrayans,Ananya,Bhavya", className="text-center")
        ], className="col-md-12"),
             
    ], className="row",
        style={
            "textAlign": "center",
            "color": "Gray"
        })
], className="container-fluid")

# defining the interaction callbacks

@app.callback(
    Output('tweet-by-date', 'figure'),
    [
        Input('tweet-filter', 'value'),
    ]
)
def filter_tweet_year(filter_text):
    return tweets_by_date(filter_tweets(filter_text))


@app.callback(
    Output('tweet-class', 'figure'),
    [
        Input('tweet-filter', 'value')
    ]
)
def filter_tweet_class(filter_text):
    return tweets_class(filter_tweets(filter_text))

# running the app
if __name__ == "__main__":
    app.run_server(debug=True)
