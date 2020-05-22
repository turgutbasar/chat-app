from threading import Event


class Listener:
    def __init__(self):
        self.signal_condition = Event()
        self.message_buffer = []


class MessageBus:
    __listeners = {}  # There can be race conditions

    def attach(self, user_id):
        listener = Listener()
        self.__listeners.update({user_id: listener})
        return listener

    def detach(self, user_id):
        self.__listeners.pop(user_id)

    def notify(self, message):
        user_id = str(message['user_id'])
        for listener in [v for k, v in self.__listeners.items() if k != user_id]:
            listener.message_buffer.append(message)
            listener.signal_condition.set()

