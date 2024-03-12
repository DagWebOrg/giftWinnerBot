from aiogram.fsm.state import State, StatesGroup

class PostState(StatesGroup):
    search_for_new_posts = State()
    deleting_a_post = State()
    delete_post_id_entry = State()
    repost_posts = State()