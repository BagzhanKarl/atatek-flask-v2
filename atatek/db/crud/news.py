from atatek.db import db, News, Coments
from sqlalchemy.exc import IntegrityError

def create_news_admin(page, content, title, poster):
    new_news = News(
        title=title,
        content=content,
        poster=poster,  # Сохраняем новое имя файла
        page=page,
        views=0,
        clicks=0,
    )
    db.session.add(new_news)
    db.session.commit()
    return new_news

def get_news_all_by_page_id(page):
    news = News.query.filter_by(page=page).all()
    return news