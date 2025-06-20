# import enum
# import logging
#
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#
# class Role(enum.StrEnum):
#     STUDENT = enum.auto()
#     TEACHER = enum.auto()
#
# class User:
#     def __init__(self, name: str, email: str, role: Role) -> None:
#         self.name = name
#         self.email = email
#         self.role = role
#
#     def send_notification(self, notification, output_method="print"):
#         formatted_message = notification.format()
#         match output_method:
#             case "print":
#                 print(f"Notification for {self.name} ({self.role}):\n{formatted_message}")
#             case "log":
#                 logging.info(f"Notification for {self.name} ({self.role}):\n{formatted_message}")
#             case _:
#                 raise ValueError(f"Unknown output method: {output_method}")
#
# class Notification:
#     def __init__(self, subject: str, message: str, attachment: str = "") -> None:
#         self.subject = subject
#         self.message = message
#         self.attachment = attachment
#
#     def format(self) -> str:
#         formatted_message = f"Subject: {self.subject}\nMessage: {self.message}"
#         if self.attachment:
#             formatted_message += f"\nAttachment: {self.attachment}"
#         return formatted_message
#
# class StudentNotification(Notification):
#     def format(self) -> str:
#         base_message = super().format()
#         return f"{base_message}\nSent via Student Portal"
#
# class TeacherNotification(Notification):
#     def format(self) -> str:
#         base_message = super().format()
#         return f"{base_message}\nTeacher's Desk Notification"
#
# def main():
#     student = User(name="noname", email="noname@email.com", role=Role.STUDENT)
#     teacher = User(name="Zahar cramble cookie", email="example@example.com", role=Role.TEACHER)
#
#     student_notification = StudentNotification(
#         subject="Python",
#         message="Don't forget to submit your homework before Thursday!",
#         attachment="homework.py"
#     )
#     teacher_notification = TeacherNotification(
#         subject="Meeting;Python",
#         message="Python Course."
#     )
#
#     print("Sending notifications...")
#     student.send_notification(student_notification, output_method="print")
#     teacher.send_notification(teacher_notification, output_method="print")
#
# if __name__ == "__main__":
#     main()
# from re import search
#
# import requests
#
#
# BASE_URL = "https://jsonplaceholder.typicode.com"
#
#
# class Post:
#
#     def __init__(self, id: int, title: str, body: str):
#
#         self.id = id
#
#         self.title = title
#
#         self.body = body
#
# class User:
#
#     def __init__(self, id: int, name: str):
#
#         self.id = id
#
#         self.name = name
#
#         self.posts: list[Post] = []
#
#     def add_post(self, post: Post):
#         self.posts.append(post)
#
#     def average_title_length(self, post) -> float:
#         if not self.posts:
#             return 0.0
#         total_length = sum(len(post.title) for s in self.posts)
#         return total_length / len(self.posts)
#
#     def average_body_length(self) -> float:
#         if not self.posts:
#             return 0.0
#         total_length = sum(len(post.body) for post in self.posts)
#         return total_length / len(self.posts)
#
# class BlogAnalytics:
#
#     def __init__(self):
#         self.users: list[User] = []
#
#     def fetch_data(self):
#         response = requests.get(f"{BASE_URL}/users")
#         user_date = response.json()
#
#         for user in user_date:
#             user = User(id=user_date['id'], name=user_date['name'])
#             self.users.append(user)
#
#         for user in self.users:
#             posts_response = requests.get(f"{BASE_URL}/posts?userId={user.id}")
#             posts_date = posts_response.json()
#             for post_data in posts_date:
#                 post = Post(
#                     id=post_data['id'],
#                     title=post_data['title'],
#                     body=post_data['body']
#                 )
#                 user.add_post(post)
#
#     def user_with_longest_average_body(self) -> User:
#         return max(self.users, key=lambda user: user.average_body_length(), default=None)
#
#     def users_with_many_long_titles(self) -> list[User]:
#         result = []
#         for user in self.users:
#             long_titles = [post for post in user.posts if len(post.title) > 40]
#             if len(long_titles) > 5:
#                 result.append(user)
#             return result
#
#
#
# """
#
# TASK 2: Comment Moderation System
#
# you're building a simple backend moderation system for post comments
#
# - fetch all comments from https://jsonplaceholder.typicode.com/comments
#
# - create a class `Comment` to store comment data
#
# - build a class `CommentModerator` with methods to:
#
#     - identify comments containing suspicious content (e.g., includes words like "buy", "free", "offer", or repeated exclamation marks)
#
#     - group flagged comments by postId
#
#     - provide a summary report: number of flagged comments per post, and a global list of the top 5 most spammy emails (authors of flagged comments)
#
# - the system should support exporting flagged comments to a local JSON file called `flagged_comments.json`
#
# - handle HTTP errors gracefully and skip any malformed data entries
#
# """
# import json
#
#
# BASE_URL = "https://jsonplaceholder.typicode.com"
#
# class Comment:
#
#     def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
#
#         self.id = id
#
#         self.post_id = post_id
#
#         self.name = name
#
#         self.email = email
#
#         self.body = body
#
# class CommentModerator:
#
#     def __init__(self):
#
#         self.comments: list[Comment] = []
#
#         self.flagged_comments: list[Comment] = []
#
#     def fetch_comments(self):
#         try:
#             response = requests.get(f"{BASE_URL}/comments")
#             response.raise_for_status()
#             comments_data = response.json()
#             for comment_data in comments_data:
#                 try:
#                     comment = Comment(
#                         id=comment_data['id'],
#                         post_id=comment_data['PostId'],
#                         name=comment_data['name'],
#                         email=comment_data['email'],
#                         body=comment_data['body']
#                     )
#                     self.comments.append(comment)
#                 except KeyError:
#                     continue
#         except requests.RequestException as e:
#             print(f"Error fetching comments: {e}")
#
#     def flag_suspicious_comments(self):
#         suspicious_keywords = ["buy", "free", "offer"]
#         for comment in self.comments:
#             body_lower = comment.body.lower()
#             suspicious_word = any(word in body_lower for word in suspicious_keywords)
#             exclamations = "!!!" in body_lower
#             if suspicious_word or exclamations:
#                 self.flagged_comments.append(comment)
#
#     def group_by_post(self) -> dict[int, list[Comment]]:
#         grouped = {}
#         for comment in self.flagged_comments:
#             if comment.post_id not in grouped:
#                 grouped[comment.post_id] = []
#             grouped[comment.post_id].append(comment)
#         return grouped
#
#     def top_spammy_emails(self, n: int = 5) -> list[str]:
#         email_counts = {}
#         for comment in self.flagged_comments:
#             email_counts[comment.email] = email_counts.get(comment.email, 0) + 1
#         sorted_emails = sorted(email_counts.items(), key=lambda x: x[1], reverse=True)
#         return [email for email, _ in sorted_emails[:n]]
#
#     def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
#         flagged_data = [
#             {
#                 "id": comment.id,
#                 "post_id": comment.post_id,
#                 "name": comment.name,
#                 "email": comment.email,
#                 "body": comment.body
#             }
#             for comment in self.flagged_comments
#         ]
#         with open(filename, 'w') as f:
#             json.dump(flagged_data, f, indent=4)
import aiohttp
import asyncio


class CurrencyConversionError(Exception):
    pass


class Price:
    def __init__(self, amount: float, currency: str, api_key: str = None):
        self.amount = amount
        self.currency = currency.upper()
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API-ключ обязателен для конвертации валют.")

    async def _fetch_exchange_rate(self, session, from_currency: str, to_currency: str) -> float:
        base_url = "https://www.alphavantage.co/query"
        function = "CURRENCY_EXCHANGE_RATE"
        url = f"{base_url}?function={function}&from_currency={from_currency}&to_currency={to_currency}&apikey={self.api_key}"

        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                exchange_rate = data.get("Realtime Currency Exchange Rate", {}).get("5. Exchange Rate")
                if not exchange_rate:
                    raise CurrencyConversionError(f"Не удалось получить курс для {from_currency}->{to_currency}")
                return float(exchange_rate)
        except aiohttp.ClientError as e:
            raise CurrencyConversionError(f"Ошибка сети при получении курса: {e}")
        except ValueError as e:
            raise CurrencyConversionError(f"Некорректные данные курса: {e}")

    async def _convert_to_chf(self, session, amount: float, currency: str) -> float:
        if currency == "CHF":
            return amount
        exchange_rate = await self._fetch_exchange_rate(session, currency, "CHF")
        return amount * exchange_rate

    async def _convert_from_chf(self, session, amount: float, currency: str) -> float:
        if currency == "CHF":
            return amount
        exchange_rate = await self._fetch_exchange_rate(session, "CHF", currency)
        return amount * exchange_rate

    async def _perform_operation(self, session, other, operator: str) -> 'Price':
        if not isinstance(other, Price):
            raise TypeError("Неподдерживаемый тип операнда. Должен быть объект класса Price.")

        if self.currency == other.currency:
            result_amount = self.amount + other.amount if operator == '+' else self.amount - other.amount
            return Price(result_amount, self.currency, self.api_key)

        self_in_chf = await self._convert_to_chf(session, self.amount, self.currency)
        other_in_chf = await self._convert_to_chf(session, other.amount, other.currency)
        result_in_chf = self_in_chf + other_in_chf if operator == '+' else self_in_chf - other_in_chf
        result_amount = await self._convert_from_chf(session, result_in_chf, self.currency)
        return Price(result_amount, self.currency, self.api_key)

# def __add__(self, other) -> 'Price':
#         async with aiohttp.ClientSession() as session:
#             return self._perform_operation(session, other, '+')
# def __sub__(self, other) -> 'Price':
#         async with aiohttp.ClientSession() as session:
#             return self._perform_operation(session, other, '-')
#
#     def __repr__(self):
#         return f"Price(amount={self.amount}, currency='{self.currency}')"


async def main():
    API_KEY = "YOUR_API_KEY"
    a = Price(100, "USD", api_key=API_KEY)
    b = Price(150, "UAH", api_key=API_KEY)

    c = await a.__add__(b)
    print("Сложение:", c)

    d = await a.__sub__(b)
    print("Вычитание:", d)


if __name__ == "__main__":
    asyncio.run(main())



