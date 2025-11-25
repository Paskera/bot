from bot.database.session import SessionLocal
from bot.database.models import User

def get_users(db, vk_id, test_id):
    users = db.query(User).filter((User.vk_id == vk_id) & (User.test_id == test_id)).all()
    

    return users

def create_user(db, vk_id, vk_session, test_id=None):
    user = User(
        vk_id=vk_id,
        name=get_name(vk_session, vk_id),
        test_id=test_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_name(vk_session, user_id):
    return vk_session.method('users.get', {'user_id': user_id})[0]['first_name'] + ' ' + \
    vk_session.method('users.get', {'user_id': user_id})[0]['last_name']
    
def get_stats(db):
    users_with_tests = db.query(User).filter(User.test_id != None ).order_by(User.id).all()
    result = []
    for user in users_with_tests:
        result.append(f"{user.id}. {user.name} | vk.com/id{user.vk_id}")
    return '\n'.join(result)