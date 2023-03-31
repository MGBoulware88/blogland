# import the function to create a db instance
from flask_app.config.mysqlconnection import connectToMySQL, DB
# import datetime to convert our datetime to Month Day, Year format
from datetime import datetime
# import user model
from flask_app.models import user

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.body = data['body']
        self.author = data['user_id'] #this is the FK from users table
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def convert_dates(dict):
        # using if statements so this can be called whenever w/o worry of key errors
        # convert created_at date to month day, year
        if dict['created_at']:
            created_date = datetime.strptime(str(dict['created_at']),'%Y-%m-%d %H:%M:%S')
            dict['created_at'] = created_date.strftime('%B %d, %Y')
        # convert updated_at date to month day, year
        if dict['updated_at']:
            created_date = datetime.strptime(str(dict['updated_at']),'%Y-%m-%d %H:%M:%S')
            dict['updated_at'] = created_date.strftime('%B %d, %Y')
        return dict

    #call this method to retrieve all posts
    @classmethod
    def get_all_posts(cls):
        # list to hold posts for query results / user search
        all_posts = []
        # get all posts from db, update date formatting, append to list, then return list
        query = "SELECT * FROM posts;"
        results = connectToMySQL(DB).query_db(query)
        for post in results:
            formatted_post = Post.convert_dates(post)
            all_posts.append(cls(formatted_post))
        return all_posts
    
    #call this method to retrieve all posts w/ author
    @classmethod
    def get_all_posts_and_authors(cls):
        # list to hold posts for query results / user search
        all_posts = []
        # get all posts from db, update date formatting, append to list, then return list
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL(DB).query_db(query)
        if results:
            for row in results:
                formatted_post = Post.convert_dates(row)
                this_post = cls(formatted_post)
                author_data = {
                    **row,
                    'id':row['users.id'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at']
                }
                this_author = user.User(author_data)
                print(f"this author is {this_author.first_name}")
                this_post.author = this_author
                print(f"this post's author is {this_author.first_name}")
                all_posts.append(this_post)
            return all_posts
        return False
    
    #call this method to retrieve specific posts
    @classmethod
    def get_search_results(cls):
        # list to hold posts for query results / user search
        search_results = []
        # get all posts from db, update date formatting, append to list, then return list
        query = "SELECT * FROM posts;"
        results = connectToMySQL(DB).query_db(query)
        for post in results:
            formatted_post = Post.convert_dates(post)
            search_results.append(cls(formatted_post))
        return search_results
    
    #call this method to retrieve one specific post
    @classmethod
    def get_post_by_id(cls, data):
        # post_list used to convert the list of dicts into a list
        post_list = []
        # get the post from db by id, update date formatting, append to list, then return list
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        data = {'id' : id}
        results = connectToMySQL(DB).query_db(query, data)
        for post in results:
            formatted_post = Post.convert_dates(post)
            post_list.append(cls(formatted_post))
        return post_list
    
    #create a new post
    @classmethod
    def create_new_post(cls, data):
        query = "INSERT INTO posts (title, body, user_id) VALUES (%(title)s, %(body)s, %(author)s);"
        return connectToMySQL(DB).query_db(query, data)
    
    # edit a post if author
    @classmethod
    def edit_post_by_id(cls, data):
        query="UPDATE posts SET title=%(title)s, body=%(body)s, updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL(DB).query_db(query, data)
    
    # delete a post if author
    @classmethod
    def delete_post_by_id(cls, id):
        data = {
            'id':id
        }
        query="DELETE FROM posts WHERE id=%(id)s"
        return connectToMySQL(DB).query_db(query, data)
        