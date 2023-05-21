from locust import HttpUser, TaskSet, task, between

 

class WordpressUserBehavior(TaskSet):

    def on_start(self):

        """Login to WordPress site upon starting the user behavior"""

        self.login()

 

    def login(self):

        """Login to WordPress"""

        response = self.client.get("/wp-login.php")

        csrftoken = response.cookies.get('wordpress_test_cookie')

 

        self.client.post("/wp-login.php",

            {"log": "admin", "pwd": "password", "wp-submit": "Log In", "testcookie": "1"},

            headers={"Referer": "/wp-login.php", "Cookie": "wordpress_test_cookie=" + csrftoken}

        )

 

    @task

    def view_homepage(self):

        """View the homepage"""

        self.client.get("/")

 

    @task

    def view_post(self):

        """View a random post"""

        post_id = self.locust.posts.pop()  # Assuming you have a list of post IDs

        self.client.get(f"/?p={post_id}")

 

class WordpressUser(HttpUser):

    tasks = [WordpressUserBehavior]

    wait_time = between(3, 5)  # Wait between 3 to 5 seconds between tasks

 

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.posts = []  # List of post IDs

 

    def on_start(self):

        """Fetch a list of post IDs before starting the user"""

        response = self.client.get("/index.php?rest_route=/wp/v2/posts")

        json_response = response.json()

        self.posts = [post['id'] for post in json_response]
