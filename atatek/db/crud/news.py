from atatek.db import db, News, Coments, NewsSettings
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

def create_site_settings(page, description, logo=None, newsletter_bg=None, icon=None):
    exict_settings = NewsSettings.query.filter_by(page=page).first()
    if exict_settings:
        exict_settings.description = description
        if logo is not None:
            exict_settings.logo = logo
        if newsletter_bg is not None:
            exict_settings.newsletter_bg = newsletter_bg
        if icon is not None:
            exict_settings.newsletter_icon = icon

        db.session.commit()
        return exict_settings
    else:

        news_settings = NewsSettings(
            page=page,
            logo=logo,
            newsletter_bg=newsletter_bg,
            icon=icon,
            description=description,
        )
        db.session.add(news_settings)
        db.session.commit()
        return news_settings

def get_site_settings(page):
    settings = NewsSettings.query.filter_by(page=page).first()
    return settings