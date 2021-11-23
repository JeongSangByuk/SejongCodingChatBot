class FindAnswer:

    keyword = list()    # 개체명 'B_LV1'
    extra_keyword = list()  # 개체명 'O'

    def __init__(self, db):
        self.db = db

    # 답변 검색
    def search(self, intent_name, ner_tags, predicts):
        answer = None

        self.keyword.clear()
        self.extra_keyword.clear()

        # 의도명과 개체명으로 답변 검색
        sql = "select * from chatbot_train_data_new"

        # 의도명만 있는 경우
        if intent_name is not None and ner_tags is None:

            where = " where (intent='{}' )".format(intent_name)

            for i in range(len(predicts)):
                self.extra_keyword.append(predicts[i][0])

            where += " and (keyword like '"

            for i in range(len(self.extra_keyword)):
                where += "%{}%".format(self.extra_keyword[i])
            where += "')"

            sql = sql + where
            answer = self.db.select_row(sql)  # 관련된 답변 전부 가져오기

            if answer is None:
                self.keyword.append("again")
                where += " and (keyword like '%again%')"
                sql = sql + where

                answer = self.db.select_row(sql)  # 관련된 답변 전부 가져오기

        # 의도명, 개체명 둘 다 있는 경우
        elif (intent_name is not None) and (ner_tags is not None):

            where = " where (intent='%s') " % intent_name

            if len(ner_tags) > 0:
                where += "and ("
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'

            # predicts 있는 경우
            if predicts is not None:

                for i in range(len(predicts)):  # predicts 길이에 따라

                    if predicts[i][1] == 'B_LV1':
                        self.keyword.append(predicts[i][0])  # keyword 리스트에 넣어주기
                    else:
                        self.extra_keyword.append(predicts[i][0])  # 나중에 다시 사용하기 위해 extra_keyword에 넣기

            where += " and (keyword like '"

            for i in range(len(self.keyword)):
                where += "%{}%".format(self.keyword[i])
            where += "')"
            sql = sql + where

            answer = self.db.select_row(sql)  # 관련된 답변 전부 가져오기

            if len(answer) > 1:
                sql_new = sql[:-2]  # )' 없애기

                for i in range(len(self.extra_keyword)):
                    sql_new += "%{}%".format(self.extra_keyword[i])

                sql_new += "')"
                answer = self.db.select_row(sql_new)

            if not answer:
                answer = self.db.select_row(sql)

        if answer:
            answer_result = answer[0]['answer']

        count = answer[0]['count']
        count = count + 1
        row_id = answer[0]['id']
        sql_count = "update chatbot_train_data_new set count = {} where (id = {})".format(count, row_id)
        self.db.execute(sql_count)

        return answer_result

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts:

            # 변환해야 하는 태그가 있는 경우 추가
            if tag == 'B_LV1':
                answer = answer.replace(tag, word)

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer