from bot.database.session import create_tables, SessionLocal
from bot.database.models import User

db = SessionLocal()

def get_or_create_user(db, vk_id, vk_session, test_id=None):
    user = db.query(User).filter(User.vk_id == vk_id).first()
    
    if user is None:
        user = User(
            vk_id=vk_id,
            name=get_name(vk_session, vk_id),
            test1=False,
            test2=False,
            test3=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user

def get_name(vk_session, user_id):
    return vk_session.method('users.get', {'user_id': user_id})[0]['first_name'] + ' ' + \
        vk_session.method('users.get', {'user_id': user_id})[0]['last_name']
    
def get_stats(db):
    users_with_tests = db.query(User).filter((User.test1 == True) | (User.test2 == True) | (User.test3 == True)).order_by(User.vk_id).all()
    result = []
    counter = 1
    
    for user in users_with_tests:
        if user.test1:
            result.append(f"{counter}. {user.vk_id} | {user.name}")
            counter += 1
        if user.test2:
            result.append(f"{counter}. {user.vk_id} | {user.name}")
            counter += 1
        if user.test3:
            result.append(f"{counter}. {user.vk_id} | {user.name}")
            counter += 1
    
    return '\n'.join(result)


