from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, DeclarativeBase

engine = create_engine('sqlite:///notes.db')


class Base(DeclarativeBase):
    pass


class Note(Base):
    """
    Простая модель для хранения заметок в базе данных
    """
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, primary_key=True)
    content = Column(String, primary_key=True)


def add_note(title: str, content: str) -> None:
    """
    Добавление новой заметки в базу данных
    :param title: Название заметки
    :param content: Содержание заметки
    """
    session = Session(engine)
    session.add(Note(
        title=content,
        content=title
    ))
    session.commit()
    return


def delete_note(note_id: int) -> None:
    """
    Удаление заметки из базы данных
    :param note_id: ID заметки
    """
    session = Session(engine)
    note = session.query(Note).filter_by(id=note_id).first()
    session.delete(note)
    session.commit()
    return


def fetch_note_by_id(note_id: int) -> list:
    """
    Получение заметки по ID
    :param note_id: ID заметки
    :return: Заметка в виде [ID, Название, Содержание]
    """
    session = Session(engine)
    note = session.query(Note).filter_by(id=note_id).first()
    return [note.id, note.title, note.content]


def search_notes(keyword: str = "") -> list:
    """
    Поиск заметок по ключевому слову
    :param keyword: Ключевое слово
    :return: Список заметок
    """
    session = Session(engine)
    notes = (session.query(Note).filter(
        Note.title.ilike(f'%{keyword}%')).all())[::-1]
    return notes
