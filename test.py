import unittest
from vectorDatabase import *
from functionsCompletions import *
from telegramBot import *

chatId = 1

class ChatbotTests(unittest.TestCase):

    def testReturnList(self):
        userFirstInput = "Crea una lista de la compra con pan y huevo"
        milvusVectorDatabase.insertData(f"Usuario: {userFirstInput}", INFO_FLAG, 1, chatId)

        userQuery = "Dime la lista de la compra"
        listDataLastMessages = milvusVectorDatabase.getLastMessages(chatId)
        memorySentences = milvusVectorDatabase.searchInformation(userQuery, chatId, listDataLastMessages[1])
        responseChatbot = completion(listDataLastMessages[0], memorySentences).lower()
        self.assertTrue("pan" in responseChatbot and "huevo" in responseChatbot)

        messageChatbot =  "Repite lo siguiente: Esto es una prueba"
        milvusVectorDatabase.insertData("prueba1", NOT_INFO_FLAG, 2, chatId)
        milvusVectorDatabase.insertData("prueba2", NOT_INFO_FLAG, 3, chatId)
        milvusVectorDatabase.insertData("prueba3", NOT_INFO_FLAG, 4, chatId)
        milvusVectorDatabase.insertData(messageChatbot, NOT_INFO_FLAG, 5, chatId)
        milvusVectorDatabase.insertData(messageChatbot, NOT_INFO_FLAG, 5, chatId)
        connectionMilvus = milvusVectorDatabase.getConnection()
        messages = connectionMilvus.query(
                expr = f"chatId == {chatId}", 
                output_fields = ["id", "text", "date"],
                consistency_level="Strong"
            )
        sortedMessages = sorted(messages, key=lambda k: k['date'])[-1:]
         
        self.assertEqual( sortedMessages[0]['text'], messageChatbot)
        idMessageSent = sortedMessages[0]['id']
        milvusVectorDatabase.deleteListIds([idMessageSent])
        messages = connectionMilvus.query(
                expr = f"text == '{messageChatbot}'", 
                output_fields = ["id", "text"],
                consistency_level="Strong"
            )
        self.assertEqual(len(messages), 0)

        self.assertFalse(milvusVectorDatabase.isNewUser(chatId))
        milvusVectorDatabase.deleteUserMessages(chatId)
        self.assertTrue(milvusVectorDatabase.isNewUser(chatId))    

if __name__ == '__main__':
    unittest.main()