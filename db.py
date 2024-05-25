from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from sqlalchemy import create_engine, ForeignKey, select, text


class Base(DeclarativeBase):
    pass


class Question(Base):
    __tablename__ = "question"

    data_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(unique=True)
    votes: Mapped[int]
    answers: Mapped[int]
    views: Mapped[int]
    time: Mapped[str]

    content: Mapped["Content"] = relationship(back_populates="question")

    def __repr__(self) -> str:
        return f"Question(question_id={self.question_id}, votes={self.votes}, answers={self.answers}, views={self.views}, time={self.time})"


class Content(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id = mapped_column(ForeignKey("question.question_id"))
    title: Mapped[str]
    content: Mapped[str]
    top_answer: Mapped[str] = mapped_column(nullable=True)
    top_answer_votes: Mapped[int] = mapped_column(nullable=True)

    question: Mapped["Question"] = relationship(back_populates="content")

    def __repr__(self) -> str:
        return f"Content(\nquestion_id={self.question_id},\ntitle={self.title},\ncontent={self.content},\ntop_answer={self.top_answer})"


engine = create_engine("sqlite:///questions.db")

Base.metadata.create_all(engine)


def get_question_ids():
    with Session(engine) as session:
        questions = session.scalars(select(Question))
        return [question.question_id for question in questions]


def drop_table(table_name: str):
    """Drop a table from the database."""
    with Session(engine) as session:
        session.execute(text(f"DROP TABLE {table_name}"))
        session.commit()


def question_exists(question_id: int):
    with Session(engine) as session:
        return (
            session.scalar(select(Question).where(Question.question_id == question_id))
            is not None
        )


def content_exists(question_id: int):
    with Session(engine) as session:
        return (
            session.scalar(select(Content).where(Content.question_id == question_id))
            is not None
        )


def add_question(question: Question):
    with Session(engine) as session:
        session.add(question)
        session.commit()


def add_content(content: Content):
    with Session(engine) as session:
        session.add(content)
        session.commit()


def remove_question(question_id: int):
    with Session(engine) as session:
        question = session.scalar(
            select(Question).where(Question.question_id == question_id)
        )
        session.delete(question)
        session.commit()


def get_data(id: int = 1) -> list:
    with Session(engine) as session:
        question = session.get(Question, id)
        if question is None:
            return None

        content = question.content
        if content is None:
            return None

        return [
            question.question_id,
            question.votes,
            question.answers,
            question.views,
            question.time,
            content.title,
            content.content,
            content.top_answer,
            content.top_answer_votes,
        ]


if __name__ == "__main__":
    drop_table("content")
    # print(get_data())
