struct Message {
    1: string text,
    2: string filename,
    3: binary data
}

service ChatService {
    void sendMessage(1: Message message),
    list<Message> getMessages()
}
