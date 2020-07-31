from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# creating database file and connecting
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


# Describing our table
class Table(Base):
    __tablename__ = 'task'  # this method creates a table using task as it's name

    id = Column(Integer, primary_key=True)  # creating id column
    task = Column(String, default='default_value')  # creating the tasks column
    deadline = Column(Date, default=datetime.today())  # creating the deadline column using datetime.today to end it.

    def __repr__(self):
        return self.task


# Creating a table on the database

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class TodoList:
    # this method is used to navigate through the application
    def ui_method(self):
        print("\n1) Today's tasks\n2) Add task\n0) Exit")
        inp = input(">")
        self.process_method(inp)
    # this process access the other methods that check the tasks and insert them into the database
    def process_method(self, inp):
        if inp == "1":
            print("Today:")
            self.check_task()
        elif inp == "2":
            self.add_task()
        elif inp == "0":
            print("Bye!")
            pass
        else:
            print("Wrong input")
    # User is told to enter a task and using add and commit, add the method to the database
    def add_task(self):
        print("Enter task")
        task_insert = Table(task=input())
        session.add(task_insert)
        session.commit()
        print("The task has been added!")
        self.ui_method()
    # If the query result of the query is "empty" print Nothing to do!, else, it will print each instance recorded.
    def check_task(self):
        if not session.query(Table).all():
            print("Nothing to do!")
        else:
            for instance in session.query(Table):
                print(f"{instance.id}. {instance.task}")
        self.ui_method()


todo_list = TodoList()

todo_list.ui_method()
