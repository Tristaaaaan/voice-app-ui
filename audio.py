import requests


class Audio:

    def __init__(self):
        pass

    def FI(self):
        self.url = "https://jsonplaceholder.typicode.com/todos/1"

        self.response = requests.get(self.url)

        for i in range(3):
            self.response = requests.get(self.url)

            if self.response.status_code == 200:
                return True

            return False

    def CS(self):
        self.url = "https://jsonplaceholder.typicode.com/todos/1"

        self.response = requests.get(self.url)

        for i in range(3):
            self.response = requests.get(self.url)

            if self.response.status_code == 200:
                return True

            return False

    def CT(self):
        self.url = "https://jsonplaceholder.typicode.com/todos/1"

        self.response = requests.get(self.url)

        for i in range(3):
            self.response = requests.get(self.url)

            if self.response.status_code == 200:
                return True

            return False

    def AU(self):
        self.url = "https://jsonplaceholder.typicode.com/todos/1"

        self.response = requests.get(self.url)

        for i in range(3):
            self.response = requests.get(self.url)

            if self.response.status_code == 200:
                return True

            return False

    def SO(self):

        self.url = "https://jsonplaceholder.typicode.com/todos/1"

        self.response = requests.get(self.url)

        for i in range(3):
            self.response = requests.get(self.url)

            if self.response.status_code == 200:
                return True

            return False

    def AA(self):

        self.url = "https://jsonplaceholder.typicode.com/todos/1"

        self.response = requests.get(self.url)

        for i in range(3):
            self.response = requests.get(self.url)

            if self.response.status_code == 200:
                return True

            return False
