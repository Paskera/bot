import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bot.config import settings
from bot.tests.tests import tests
from bot.database.session import create_tables, SessionLocal
from bot.database.models import User
from bot.database.crud import get_or_create_user, get_stats

user_states: dict[int, dict[int, int]] = {} # {user_id: {'test_id': test_id, 'que_id': que_id}}

def main():
    create_tables()

    # auth
    try:
        vk_session = vk_api.VkApi(token=settings.VK_BOT_TOKEN)
        longpoll = VkLongPoll(vk_session)
        vk = vk_session.get_api()
        print("Бот подключен")
    except Exception as error:
        print(f"Error with the connection BOT\n {error}")
        return
    
    print("Бот запущен")

    keyboard = VkKeyboard()
    keyboard.add_button('Начать тест', VkKeyboardColor.NEGATIVE)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:
            db = SessionLocal()

            try:
                # get ref
                message_info = vk.messages.getById(message_ids=[event.message_id], extended=1)
                ref_value = message_info['items'][0].get('ref')
                ref_source_value = message_info['items'][0].get('ref_source')

                handle_message(db, event, vk_session, ref_value)
            except Exception as e:
                print(f"Ошибка обработки сообщения: {e}")
            # ? 
            finally: 
                db.close

def handle_message(db, event, vk_session, ref_value):
    id = event.user_id
    msg = event.text.lower()
    # peer_id = event.peer_id

    if msg == '' or msg == 'начать':
        keyboard = VkKeyboard()
        keyboard.add_button('Начать тест', VkKeyboardColor.POSITIVE)
        send_msg(vk_session, id, 'Перейдите по qr code, чтобы начать тест', keyboard)

    # Get stats users
    elif msg == 'список':
        stats_users = get_stats(db)
        send_msg(vk_session, id, stats_users)

    # Start test
    elif msg == 'начать тест':
        keyboard = VkKeyboard()
        keyboard.add_button('Начать тест', VkKeyboardColor.POSITIVE)
        if not ref_value:
            send_msg(vk_session, id, 'Перейдите по qr code, чтобы начать тест', keyboard)
            return 0
        send_msg(vk_session, id, 'Подпишитесь на Студенческие отряды Республики Крым \nВК https://vk.com/rso_crimea \nТГ https://t.me/krorso', keyboard)
        test_id = int(ref_value[4])
        user = get_or_create_user(db, id, vk_session, test_id)

        test_completed = False
        if test_id == 1 and user.test1:
            test_completed = True
        elif test_id == 2 and user.test2:
            test_completed = True
        elif test_id == 3 and user.test3:
            test_completed = True
        
        if test_completed:
            send_msg(vk_session, id, 'Вы уже прошли этот тест!')
            return 0

        send_test(vk_session, id, int(ref_value[4]), 1)
        return 0 

    # During test
    elif id in user_states:
        send_msg(vk_session, id, f"{tests[user_states[id]['test_id']][user_states[id]['que_id']][1]}")
        # добавить билет
        if user_states[id]['que_id'] == 5:
            test_id = user_states[id]['test_id']
            user = get_or_create_user(db, id, vk_session, test_id)
            if user:
                # Обновляем существующую запись
                if test_id == 1:
                    user.test1 = True
                elif test_id == 2:
                    user.test2 = True
                elif test_id == 3:
                    user.test3 = True
                db.commit()

            user_states.pop(id)
            return 0
        user_states[id]['que_id'] += 1
        send_test(vk_session, id, user_states[id]['test_id'], user_states[id]['que_id'])

def send_msg(vk_session, id, text, keyboard=None):
    if keyboard is None:
        vk_session.method('messages.send',
                            {'user_id': id, 'message': text, 'random_id': 0, })
    else:
        vk_session.method('messages.send',
                            {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard.get_keyboard()})

# Need it?    


# # Need it?
# def send_attachment(id, url, text=None):
#     vk_session.method('messages.send', {'user_id': id, 'message': text, 'attachment': url, 'random_id': 0})


def send_test(vk_session, id, test_id, que_id):
    user_states[id] = {'test_id': test_id, 'que_id': que_id}
    send_msg(vk_session, id, f"{tests[test_id][que_id][0]}")


if __name__ == '__main__':
    main()
    