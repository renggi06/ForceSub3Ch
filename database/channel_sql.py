from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from database.sql import BASE, SESSION



class Channel(BASE):
    __tablename__ = "channels"
    __table_args__ = {'extend_existing': True}
    channel_id = Column(BigInteger, primary_key=True)
    admin_id = Column(Integer)
    caption = Column(String, nullable=True)
    buttons = Column(String, nullable=True)
    position = Column(String, nullable=True)
    sticker_id = Column(String, nullable=True)
    edit_mode = Column(String, nullable=True)
    webpage_preview = Column(Boolean)

    def __init__(self, channel_id, admin_id, caption=None, buttons=None, edit_mode=None, position=None, webpage_preview=False, sticker_id=None):
        self.channel_id = channel_id
        self.admin_id = admin_id
        self.caption = caption
        self.buttons = buttons
        self.position = position
        self.webpage_preview = webpage_preview
        self.sticker_id = sticker_id
        self.edit_mode = edit_mode

    # def __repr__(self):
    #     return "<User {} {} {} ({})>".format(self.thumbnail, self.thumbnail_status, self.video_to, self.channel_id)


Channel.__table__.create(checkfirst=True)


async def num_channels():
    try:
        return SESSION.query(Channel).count()
    finally:
        SESSION.close()


async def add_channel(channel_id, user_id):
    q = SESSION.query(Channel).get(channel_id)
    if not q:
        SESSION.add(Channel(channel_id, user_id))
        SESSION.commit()


async def remove_channel(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        SESSION.delete(q)
        SESSION.commit()


async def get_channel_info(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        info = {
            'admin_id': q.admin_id,
            'buttons': q.buttons,
            'caption': q.caption,
            'position': q.position,
            'sticker_id': q.sticker_id,
            'webpage_preview': q.webpage_preview,
            'edit_mode': q.edit_mode
        }
        SESSION.close()
        return True, info
    else:
        return False, {}  # Redundant though
